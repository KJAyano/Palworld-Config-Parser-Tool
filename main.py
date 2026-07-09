import os
import platform
import re
import shutil
import sys
from pathlib import Path

VERSION = "v0.7.3"

ALPHA_DASH_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")
VALID_CROSSPLAY_PLATFORMS = {"Steam", "Xbox", "PS5", "Mac"}


def validate_numeric(value):
    try:
        return int(value) >= 0
    except ValueError:
        return False


def validate_floating(value):
    try:
        float(value)
    except ValueError:
        return False
    decimal_point_index = value.find(".")
    if decimal_point_index == -1:
        return False
    return decimal_point_index < len(value) - 1


def validate_true_false(value):
    return value == "True" or value == "False"


def validate_string(value):
    return True


def validate_alpha_dash(value):
    return ALPHA_DASH_PATTERN.fullmatch(value) is not None


def validate_crossplay_platforms(value):
    value = value.strip("() ")
    if value == "":
        return True
    platforms = value.split(",")
    for single_platform in platforms:
        single_platform = single_platform.strip()
        if single_platform != "" and single_platform not in VALID_CROSSPLAY_PLATFORMS:
            return False
    return True


VALIDATION_RULES = {
    "Numeric": validate_numeric,
    "Floating": validate_floating,
    "TrueFalse": validate_true_false,
    "String": validate_string,
    "AlphaDash": validate_alpha_dash,
    "CrossplayPlatforms": validate_crossplay_platforms,
}

ENV_VARS = {
    "Difficulty": "DIFFICULTY",
    "DayTimeSpeedRate": "DAY_TIME_SPEED_RATE",
    "NightTimeSpeedRate": "NIGHT_TIME_SPEED_RATE",
    "ExpRate": "EXP_RATE",
    "PalCaptureRate": "PAL_CAPTURE_RATE",
    "PalSpawnNumRate": "PAL_SPAWN_NUM_RATE",
    "PalDamageRateAttack": "PAL_DAMAGE_RATE_ATTACK",
    "PalDamageRateDefense": "PAL_DAMAGE_RATE_DEFENSE",
    "PlayerDamageRateAttack": "PLAYER_DAMAGE_RATE_ATTACK",
    "PlayerDamageRateDefense": "PLAYER_DAMAGE_RATE_DEFENSE",
    "PlayerStomachDecreaceRate": "PLAYER_STOMACH_DECREACE_RATE",
    "PlayerStaminaDecreaceRate": "PLAYER_STAMINA_DECREACE_RATE",
    "PlayerAutoHPRegeneRate": "PLAYER_AUTO_HP_REGENE_RATE",
    "PlayerAutoHpRegeneRateInSleep": "PLAYER_AUTO_HP_REGENE_RATE_IN_SLEEP",
    "PalStomachDecreaceRate": "PAL_STOMACH_DECREACE_RATE",
    "PalStaminaDecreaceRate": "PAL_STAMINA_DECREACE_RATE",
    "PalAutoHPRegeneRate": "PAL_AUTO_HP_REGENE_RATE",
    "PalAutoHpRegeneRateInSleep": "PAL_AUTO_HP_REGENE_RATE_IN_SLEEP",
    "BuildObjectDamageRate": "BUILD_OBJECT_DAMAGE_RATE",
    "BuildObjectDeteriorationDamageRate": "BUILD_OBJECT_DETERIORATION_DAMAGE_RATE",
    "CollectionDropRate": "COLLECTION_DROP_RATE",
    "CollectionObjectHpRate": "COLLECTION_OBJECT_HP_RATE",
    "CollectionObjectRespawnSpeedRate": "COLLECTION_OBJECT_RESPAWN_SPEED_RATE",
    "EnemyDropItemRate": "ENEMY_DROP_ITEM_RATE",
    "DeathPenalty": "DEATH_PENALTY",
    "bEnablePlayerToPlayerDamage": "ENABLE_PLAYER_TO_PLAYER_DAMAGE",
    "bEnableFriendlyFire": "ENABLE_FRIENDLY_FIRE",
    "bEnableInvaderEnemy": "ENABLE_ENEMY",
    "bActiveUNKO": "ACTIVE_UNKO",
    "bEnableAimAssistPad": "ENABLE_AIM_ASSIST_PAD",
    "bEnableAimAssistKeyboard": "ENABLE_AIM_ASSIST_KEYBOARD",
    "DropItemMaxNum": "DROP_ITEM_MAX_NUM",
    "DropItemMaxNum_UNKO": "DROP_ITEM_MAX_NUM_UNKO",
    "BaseCampMaxNum": "BASE_CAMP_MAX_NUM",
    "BaseCampWorkerMaxNum": "BASE_CAMP_WORKER_MAX_NUM",
    "DropItemAliveMaxHours": "DROP_ITEM_ALIVE_MAX_HOURS",
    "bAutoResetGuildNoOnlinePlayers": "AUTO_RESET_GUILD_NO_ONLINE_PLAYERS",
    "AutoResetGuildTimeNoOnlinePlayers": "AUTO_RESET_GUILD_TIME_NO_ONLINE_PLAYERS",
    "GuildPlayerMaxNum": "GUILD_PLAYER_MAX_NUM",
    "BaseCampMaxNumInGuild": "BASE_CAMP_MAX_NUM_IN_GUILD",
    "PalEggDefaultHatchingTime": "PAL_EGG_DEFAULT_HATCHING_TIME",
    "WorkSpeedRate": "WORK_SPEED_RATE",
    "bIsMultiplay": "IS_MULTIPLAY",
    "bIsPvP": "IS_PVP",
    "bCanPickupOtherGuildDeathPenaltyDrop": "CAN_PICKUP_OTHER_GUILD_DEATH_PENALTY_DROP",
    "bEnableNonLoginPenalty": "ENABLE_NON_LOGIN_PENALTY",
    "bEnableFastTravel": "ENABLE_FAST_TRAVEL",
    "bIsStartLocationSelectByMap": "IS_START_LOCATION_SELECT_BY_MAP",
    "bExistPlayerAfterLogout": "EXIST_PLAYER_AFTER_LOGOUT",
    "bEnableDefenseOtherGuildPlayer": "ENABLE_DEFENSE_OTHER_GUILD_PLAYER",
    "CoopPlayerMaxNum": "COOP_PLAYER_MAX_NUM",
    "ServerPlayerMaxNum": "MAX_PLAYERS",
    "ServerName": "SERVER_NAME",
    "ServerDescription": "SERVER_DESCRIPTION",
    "ServerPassword": "SERVER_PASSWORD",
    "AdminPassword": "ADMIN_PASSWORD",
    "PublicPort": "SERVER_PORT",
    "RCONPort": "RCON_PORT",
    "RCONEnabled": "RCON_ENABLE",
    "bUseAuth": "USE_AUTH",
    "BanListURL": "BAN_LIST_URL",
    "Region": "SERVER_REGION",
    "bShowPlayerList": "SHOW_PLAYER_LIST",
    "RESTAPIEnabled": "REST_API_ENABLED",
    "RESTAPIPort": "REST_API_PORT",
    "bIsUseBackupSaveData": "USE_BACKUP_SAVE_DATA",
    "LogFormatType": "LOG_FORMAT_TYPE",
    "SupplyDropSpan": "SUPPLY_DROP_SPAN",
    "ChatPostLimitPerMinute": "CHAT_POST_LIMIT",
    "bInvisibleOtherGuildBaseCampAreaFX": "INVISIBLE_OTHER_GUILD_BASE",
    "AutoSaveSpan": "AUTO_SAVE_SPAN",
    "RandomizerType": "RANDOMIZER_TYPE",
    "RandomizerSeed": "RANDOMIZER_SEED",
    "BuildObjectHpRate": "BUILD_OBJECT_HP_RATE",
    "bHardcore": "HARDCORE",
    "bPalLost": "PAL_LOST",
    "bBuildAreaLimit": "BUILD_AREA_LIMIT",
    "ItemWeightRate": "ITEM_WEIGHT_RATE",
    "EnablePredatorBossPal": "ENABLE_PREDATOR_BOSS_PAL",
    "MaxBuildingLimitNum": "MAX_BUILDING_LIMIT_NUM",
    "ServerReplicatePawnCullDistance": "SERVER_REPLICATE_PAWN_CULL_DISTANCE",
    "bIsRandomizerPalLevelRandom": "IS_RANDOMIZER_PAL_LEVEL_RANDOM",
    "bAllowGlobalPalboxExport": "ALLOW_GLOBAL_PALBOX_EXPORT",
    "bAllowGlobalPalboxImport": "ALLOW_GLOBAL_PALBOX_IMPORT",
    "bCharacterRecreateInHardcore": "CHARACTER_RECREATE_IN_HARDCORE",
    "EquipmentDurabilityDamageRate": "EQUIPMENT_DURABILITY_DAMAGE_RATE",
    "ItemContainerForceMarkDirtyInterval": "ITEM_CONTAINER_FORCE_MARK_DIRTY_INTERVAL",
    "ItemCorruptionMultiplier": "ITEM_CORRUPTION_MULTIPLIER",
    "CrossplayPlatforms": "CROSSPLAY_PLATFORMS",
    "bEnableFastTravelOnlyBaseCamp": "ENABLE_FAST_TRAVEL_ONLY_BASE_CAMP",
    "bAllowClientMod": "ALLOW_CLIENT_MOD",
    "bIsShowJoinLeftMessage": "SHOW_JOIN_LEFT_MESSAGE",
    "DenyTechnologyList": "DENY_TECHNOLOGY_LIST",
    "GuildRejoinCooldownMinutes": "GUILD_REJOIN_COOLDOWN_MINUTES",
    "BlockRespawnTime": "BLOCK_RESPAWN_TIME",
    "RespawnPenaltyDurationThreshold": "RESPAWN_PENALTY_DURATION_THRESHOLD",
    "RespawnPenaltyTimeScale": "RESPAWN_PENALTY_TIME_SCALE",
    "bDisplayPvPItemNumOnWorldMap_BaseCamp": "DISPLAY_PVP_ITEM_NUM_ON_WORLD_MAP_BASE_CAMP",
    "bDisplayPvPItemNumOnWorldMap_Player": "DISPLAY_PVP_ITEM_NUM_ON_WORLD_MAP_PLAYER",
    "AdditionalDropItemWhenPlayerKillingInPvPMode": "ADDITIONAL_DROP_ITEM_WHEN_PLAYER_KILLING_IN_PVP_MODE",
    "AdditionalDropItemNumWhenPlayerKillingInPvPMode": "ADDITIONAL_DROP_ITEM_NUM_WHEN_PLAYER_KILLING_IN_PVP_MODE",
    "bAdditionalDropItemWhenPlayerKillingInPvPMode": "ADDITIONAL_DROP_ITEM_WHEN_PLAYER_KILLING_IN_PVP_MODE_ENABLED",
    "bAllowEnhanceStat_Health": "ALLOW_ENHANCE_STAT_HEALTH",
    "bAllowEnhanceStat_Attack": "ALLOW_ENHANCE_STAT_ATTACK",
    "bAllowEnhanceStat_Stamina": "ALLOW_ENHANCE_STAT_STAMINA",
    "bAllowEnhanceStat_Weight": "ALLOW_ENHANCE_STAT_WEIGHT",
    "bAllowEnhanceStat_WorkSpeed": "ALLOW_ENHANCE_STAT_WORK_SPEED",
}

ENV_VARS_VALIDATION_RULES = {
    "Difficulty": "String",
    "DayTimeSpeedRate": "Floating",
    "NightTimeSpeedRate": "Floating",
    "ExpRate": "Floating",
    "PalCaptureRate": "Floating",
    "PalSpawnNumRate": "Floating",
    "PalDamageRateAttack": "Floating",
    "PalDamageRateDefense": "Floating",
    "PlayerDamageRateAttack": "Floating",
    "PlayerDamageRateDefense": "Floating",
    "PlayerStomachDecreaceRate": "Floating",
    "PlayerStaminaDecreaceRate": "Floating",
    "PlayerAutoHPRegeneRate": "Floating",
    "PlayerAutoHpRegeneRateInSleep": "Floating",
    "PalStaminaDecreaceRate": "Floating",
    "PalStomachDecreaceRate": "Floating",
    "PalAutoHPRegeneRate": "Floating",
    "PalAutoHpRegeneRateInSleep": "Floating",
    "BuildObjectDamageRate": "Floating",
    "BuildObjectDeteriorationDamageRate": "Floating",
    "CollectionDropRate": "Floating",
    "CollectionObjectHpRate": "Floating",
    "CollectionObjectRespawnSpeedRate": "Floating",
    "EnemyDropItemRate": "Floating",
    "DeathPenalty": "String",
    "bEnablePlayerToPlayerDamage": "TrueFalse",
    "bEnableFriendlyFire": "TrueFalse",
    "bEnableInvaderEnemy": "TrueFalse",
    "bActiveUNKO": "TrueFalse",
    "bEnableAimAssistPad": "TrueFalse",
    "bEnableAimAssistKeyboard": "TrueFalse",
    "DropItemMaxNum": "Numeric",
    "DropItemMaxNum_UNKO": "Numeric",
    "BaseCampMaxNum": "Numeric",
    "BaseCampWorkerMaxNum": "Numeric",
    "DropItemAliveMaxHours": "Floating",
    "AutoResetGuildTimeNoOnlinePlayers": "Floating",
    "bAutoResetGuildNoOnlinePlayers": "TrueFalse",
    "GuildPlayerMaxNum": "Numeric",
    "BaseCampMaxNumInGuild": "Numeric",
    "PalEggDefaultHatchingTime": "Floating",
    "WorkSpeedRate": "Floating",
    "bIsMultiplay": "TrueFalse",
    "bIsPvP": "TrueFalse",
    "bCanPickupOtherGuildDeathPenaltyDrop": "TrueFalse",
    "bEnableNonLoginPenalty": "TrueFalse",
    "bEnableFastTravel": "TrueFalse",
    "bIsStartLocationSelectByMap": "TrueFalse",
    "bExistPlayerAfterLogout": "TrueFalse",
    "bEnableDefenseOtherGuildPlayer": "TrueFalse",
    "CoopPlayerMaxNum": "Numeric",
    "ServerPlayerMaxNum": "Numeric",
    "ServerName": "String",
    "ServerDescription": "String",
    "ServerPassword": "AlphaDash",
    "AdminPassword": "AlphaDash",
    "PublicIP": "String",
    "PublicPort": "Numeric",
    "RCONPort": "Numeric",
    "RCONEnabled": "TrueFalse",
    "bUseAuth": "TrueFalse",
    "BanListURL": "String",
    "Region": "String",
    "bShowPlayerList": "TrueFalse",
    "RESTAPIEnabled": "TrueFalse",
    "RESTAPIPort": "Numeric",
    "bIsUseBackupSaveData": "TrueFalse",
    "LogFormatType": "String",
    "SupplyDropSpan": "Numeric",
    "ChatPostLimitPerMinute": "Numeric",
    "bInvisibleOtherGuildBaseCampAreaFX": "TrueFalse",
    "AutoSaveSpan": "Floating",
    "RandomizerType": "String",
    "RandomizerSeed": "String",
    "BuildObjectHpRate": "Floating",
    "bHardcore": "TrueFalse",
    "bPalLost": "TrueFalse",
    "bBuildAreaLimit": "TrueFalse",
    "ItemWeightRate": "Floating",
    "EnablePredatorBossPal": "TrueFalse",
    "MaxBuildingLimitNum": "Numeric",
    "ServerReplicatePawnCullDistance": "Floating",
    "bIsRandomizerPalLevelRandom": "TrueFalse",
    "bAllowGlobalPalboxExport": "TrueFalse",
    "bAllowGlobalPalboxImport": "TrueFalse",
    "bCharacterRecreateInHardcore": "TrueFalse",
    "EquipmentDurabilityDamageRate": "Floating",
    "ItemContainerForceMarkDirtyInterval": "Floating",
    "ItemCorruptionMultiplier": "Floating",
    "CrossplayPlatforms": "CrossplayPlatforms",
    "bEnableFastTravelOnlyBaseCamp": "TrueFalse",
    "bAllowClientMod": "TrueFalse",
    "bIsShowJoinLeftMessage": "TrueFalse",
    "DenyTechnologyList": "String",
    "GuildRejoinCooldownMinutes": "Numeric",
    "BlockRespawnTime": "Floating",
    "RespawnPenaltyDurationThreshold": "Floating",
    "RespawnPenaltyTimeScale": "Floating",
    "bDisplayPvPItemNumOnWorldMap_BaseCamp": "TrueFalse",
    "bDisplayPvPItemNumOnWorldMap_Player": "TrueFalse",
    "AdditionalDropItemWhenPlayerKillingInPvPMode": "String",
    "AdditionalDropItemNumWhenPlayerKillingInPvPMode": "Numeric",
    "bAdditionalDropItemWhenPlayerKillingInPvPMode": "TrueFalse",
    "bAllowEnhanceStat_Health": "TrueFalse",
    "bAllowEnhanceStat_Attack": "TrueFalse",
    "bAllowEnhanceStat_Stamina": "TrueFalse",
    "bAllowEnhanceStat_Weight": "TrueFalse",
    "bAllowEnhanceStat_WorkSpeed": "TrueFalse",
}

ENV_VARS_QUOTES = {
    "ServerName",
    "ServerPassword",
    "AdminPassword",
    "ServerDescription",
    "BanListURL",
    "PublicIP",
    "RandomizerSeed",
    "AdditionalDropItemWhenPlayerKillingInPvPMode",
}


def get_ip_address_key():
    public_ip_value = os.environ.get("PUBLIC_IP")
    if public_ip_value is not None and public_ip_value != "":
        return "PUBLIC_IP"
    return "SERVER_IP"


def copy_file(source, destination):
    destination_path = Path(destination)
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def detect_os_folder():
    current_os = platform.system()
    if current_os == "Windows":
        return "WindowsServer"
    elif current_os == "Linux":
        wine_prefix = os.environ.get("WINEPREFIX")
        if wine_prefix is not None:
            return "WindowsServer"
        if shutil.which("proton") is not None:
            return "WindowsServer"
        return "LinuxServer"
    else:
        print("Unsupported operating system")
        sys.exit(1)


def set_ini_value(content, key, value, add_quotes):
    search_string = f"{key}="
    position = content.find(search_string)
    if position == -1:
        print(f"Key not found: {key}")
        return content

    start = position + len(search_string)
    remaining = content[position:]

    if key == "CrossplayPlatforms":
        if remaining[len(search_string):].startswith("("):
            paren_close = remaining.find(")", len(search_string))
            if paren_close != -1:
                end_absolute = position + paren_close + 1
            else:
                end_absolute = len(content)
        else:
            end_pos_comma = remaining.find(",")
            end_pos_paren = remaining.find(")")
            if end_pos_comma == -1 and end_pos_paren == -1:
                end_absolute = len(content)
            else:
                if end_pos_comma == -1:
                    end_pos_comma = len(content) + 1
                if end_pos_paren == -1:
                    end_pos_paren = len(content) + 1
                end_absolute = position + min(end_pos_comma, end_pos_paren)
    else:
        end_pos_comma = remaining.find(",")
        end_pos_paren = remaining.find(")")
        if end_pos_comma == -1 and end_pos_paren == -1:
            end_absolute = len(content)
        else:
            if end_pos_comma == -1:
                end_pos_comma = len(content) + 1
            if end_pos_paren == -1:
                end_pos_paren = len(content) + 1
            end_absolute = position + min(end_pos_comma, end_pos_paren)

    if key == "CrossplayPlatforms" and value != "":
        value = value.strip("() ")
        if value:
            value = f"({value})"

    if add_quotes:
        value = f'"{value}"'

    if end_absolute > len(content):
        end_absolute = len(content)

    return content[:start] + value + content[end_absolute:]


def main():
    print("Program Version:", VERSION)

    ENV_VARS["PublicIP"] = get_ip_address_key()

    os_folder = detect_os_folder()

    ini_file_path = Path(f"Pal/Saved/Config/{os_folder}/PalWorldSettings.ini").resolve()

    if not ini_file_path.exists():
        default_ini_path = Path("DefaultPalWorldSettings.ini")
        if default_ini_path.exists():
            relative_new_path = f"Pal/Saved/Config/{os_folder}/PalWorldSettings.ini"
            copy_file(str(default_ini_path), str(ini_file_path))
            print("DefaultPalWorldSettings.ini copied to:", relative_new_path)
        else:
            print("PalWorldSettings.ini not found and DefaultPalWorldSettings.ini does not exist in the current directory.")
            return
    else:
        file_size = ini_file_path.stat().st_size
        if file_size == 0 or file_size < 1200:
            default_ini_path = Path("DefaultPalWorldSettings.ini")
            relative_new_path = f"Pal/Saved/Config/{os_folder}/PalWorldSettings.ini"
            try:
                copy_file(str(default_ini_path), str(ini_file_path))
                print("DefaultPalWorldSettings.ini copied to:", relative_new_path)
            except Exception as file_copy_error:
                print(f"Error copying file: {file_copy_error}")
                return
        else:
            print("PalWorldSettings.ini found at:", ini_file_path)

    try:
        ini_content = ini_file_path.read_text(encoding="utf-8")
    except Exception as file_read_error:
        print(f"Error reading INI file: {file_read_error}")
        return

    for config_key, env_var_name in ENV_VARS.items():
        env_var_value = os.environ.get(env_var_name)

        if env_var_value is None:
            continue

        if env_var_value == "":
            print(f"Updating empty key: {config_key}")
            ini_content = set_ini_value(ini_content, config_key, "", config_key in ENV_VARS_QUOTES)
            continue

        if config_key in ENV_VARS_VALIDATION_RULES:
            rule_name = ENV_VARS_VALIDATION_RULES[config_key]
            if rule_name in VALIDATION_RULES:
                validation_function = VALIDATION_RULES[rule_name]
                if not validation_function(env_var_value):
                    print(f"Validation failed for key: {config_key}, value: {env_var_value}")
                    continue
            else:
                print(f"No validation rule found for key: {config_key}")
        else:
            print(f"No validation rule specified for key: {config_key}")

        print(f"Updating key: {config_key} with value: {env_var_value}")
        ini_content = set_ini_value(ini_content, config_key, env_var_value, config_key in ENV_VARS_QUOTES)

    try:
        ini_file_path.write_text(ini_content, encoding="utf-8")
    except Exception as file_write_error:
        print(f"Error writing updated INI file: {file_write_error}")
        return

    print("INI file updated successfully.")

if __name__ == "__main__":
    main()