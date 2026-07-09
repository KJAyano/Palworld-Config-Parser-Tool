<p align="center">
  <img src="https://img.shields.io/badge/Palworld-Config%20Parser-blue?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCI+PHBhdGggZD0iTTEyIDJ2NCIvPjxwYXRoIGQ9Ik0xMiAxOHY0Ii8+PHBhdGggZD0iTTQuOTMgNC45M2wyLjgzIDIuODMiLz48cGF0aCBkPSJNMTYuMjQgMTYuMjRsMi44MyAyLjgzIi8+PHBhdGggZD0iTTIgMTJoNCIvPjxwYXRoIGQ9Ik0xOCAxMmg0Ii8+PHBhdGggZD0iTTQuOTMgMTkuMDdsMi44My0yLjgzIi8+PHBhdGggZD0iTTE2LjI0IDcuNzZsMi44My0yLjgzIi8+PC9zdmc+" alt="Palworld Config Parser"/>
</p>

<p align="center">
  <a href="https://github.com/KJAyano/Palworld-Config-Parser-Tool/releases/latest"><img src="https://img.shields.io/github/v/release/KJAyano/Palworld-Config-Parser-Tool?style=flat-square&color=brightgreen&label=Latest%20Release" alt="Latest Release"/></a>
  <a href="https://github.com/KJAyano/Palworld-Config-Parser-Tool/blob/main/LICENSE"><img src="https://img.shields.io/github/license/KJAyano/Palworld-Config-Parser-Tool?style=flat-square&color=blue" alt="License"/></a>
  <img src="https://img.shields.io/badge/python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+"/>
  <img src="https://img.shields.io/badge/platform-linux%20%7C%20windows-lightgrey?style=flat-square" alt="Platform"/>
</p>

<p align="center">
  A lightweight, zero-dependency tool that updates your Palworld dedicated server config (<code>PalWorldSettings.ini</code>) directly from environment variables.<br/>
  Built for <strong>Pterodactyl</strong>, <strong>Pelican</strong>, and <strong>Docker</strong> panels — but works perfectly standalone on any Linux or Windows host.
</p>

---

## 📑 Table of Contents

- [✨ Features](#-features)
- [📥 Installation & Usage](#-installation--usage)
  - [Standalone Example](#standalone-example)
  - [Pterodactyl / Pelican Integration](#pterodactyl--pelican-integration)
- [📋 Environment Variables](#-environment-variables)
- [🛡️ Validation Rules](#️-validation-rules)
- [📝 Notes & Edge Cases](#-notes--edge-cases)
- [🔨 Building from Source](#-building-from-source)

---

## ✨ Features

- 🔄 **100% Coverage** — Supports all **108 config keys** introduced up to the latest Palworld patches.
- ✅ **Strict Input Validation** — 6 intelligent rule types (Numeric, Boolean, String, AlphaDash, etc.) prevent misconfigurations before they reach the server.
- 📁 **Smart Auto-Bootstrap** — Intelligently detects empty or missing config files (< 1200 bytes) and copies a fresh `DefaultPalWorldSettings.ini` to guarantee successful boot.
- 🐧 **Wine/Proton Aware** — Automatically detects `WINEPREFIX` or the presence of Proton and injects the config into the `WindowsServer` directory path if you're running the Windows binary on Linux.
- 📦 **Zero Dependencies** — Pure Python standard library logic. No `pip install` required for the source.
- 🚀 **Pre-built Binaries** — Ultra-fast, single-file executables pre-compiled with PyInstaller for Linux and Windows (`amd64`).

---

## 📥 Installation & Usage

### Pre-built Binaries

Download the standalone binary from the [Releases](https://github.com/KJAyano/Palworld-Config-Parser-Tool/releases) page — **no Python installation needed**.

```bash
# Linux
wget https://github.com/KJAyano/Palworld-Config-Parser-Tool/releases/latest/download/PalworldServerConfigParser-linux-amd64
chmod +x PalworldServerConfigParser-linux-amd64
./PalworldServerConfigParser-linux-amd64

# Windows
# Just download PalworldServerConfigParser-windows-amd64.exe and run it!
```

### Standalone Example

You can easily use this on a bare-metal Linux/Windows server or in a standard bash script. Just set the environment variables before running the binary!

```bash
# 1. Export your desired variables
export SERVER_NAME="My Awesome Palworld Server"
export MAX_PLAYERS="32"
export DIFFICULTY="Hard"
export EXP_RATE="2.0"

# 2. Run the parser
./PalworldServerConfigParser-linux-amd64

# Result: Your PalWorldSettings.ini is instantly updated with these exact values!
```

### Pterodactyl / Pelican Integration

This tool was designed natively for Docker-based game server panels. 

Just include the parser download and execution command in your egg's install/startup script:

```bash
echo "Downloading Palworld Config Parser..."
curl -sL https://github.com/KJAyano/Palworld-Config-Parser-Tool/releases/latest/download/PalworldServerConfigParser-linux-amd64 -o PalworldServerConfigParser
chmod +x PalworldServerConfigParser

echo "Updating PalWorldSettings.ini from Egg variables..."
./PalworldServerConfigParser
```

---

## 📋 Environment Variables

Set any of these environment variables before running the parser. **If a variable is not set, the parser leaves that specific config value untouched.**

### 🎮 Gameplay

| Config Key | ENV Variable |
|---|---|
| `Difficulty` | `DIFFICULTY` |
| `DayTimeSpeedRate` | `DAY_TIME_SPEED_RATE` |
| `NightTimeSpeedRate` | `NIGHT_TIME_SPEED_RATE` |
| `ExpRate` | `EXP_RATE` |
| `PalCaptureRate` | `PAL_CAPTURE_RATE` |
| `PalSpawnNumRate` | `PAL_SPAWN_NUM_RATE` |
| `PalDamageRateAttack` | `PAL_DAMAGE_RATE_ATTACK` |
| `PalDamageRateDefense` | `PAL_DAMAGE_RATE_DEFENSE` |
| `PlayerDamageRateAttack` | `PLAYER_DAMAGE_RATE_ATTACK` |
| `PlayerDamageRateDefense` | `PLAYER_DAMAGE_RATE_DEFENSE` |
| `PlayerStomachDecreaceRate` | `PLAYER_STOMACH_DECREACE_RATE` |
| `PlayerStaminaDecreaceRate` | `PLAYER_STAMINA_DECREACE_RATE` |
| `PlayerAutoHPRegeneRate` | `PLAYER_AUTO_HP_REGENE_RATE` |
| `PlayerAutoHpRegeneRateInSleep` | `PLAYER_AUTO_HP_REGENE_RATE_IN_SLEEP` |
| `PalStomachDecreaceRate` | `PAL_STOMACH_DECREACE_RATE` |
| `PalStaminaDecreaceRate` | `PAL_STAMINA_DECREACE_RATE` |
| `PalAutoHPRegeneRate` | `PAL_AUTO_HP_REGENE_RATE` |
| `PalAutoHpRegeneRateInSleep` | `PAL_AUTO_HP_REGENE_RATE_IN_SLEEP` |
| `DeathPenalty` | `DEATH_PENALTY` |
| `ItemWeightRate` | `ITEM_WEIGHT_RATE` |
| `WorkSpeedRate` | `WORK_SPEED_RATE` |
| `EquipmentDurabilityDamageRate` | `EQUIPMENT_DURABILITY_DAMAGE_RATE` |
| `ItemCorruptionMultiplier` | `ITEM_CORRUPTION_MULTIPLIER` |

### 🏗️ Building & World

| Config Key | ENV Variable |
|---|---|
| `BuildObjectDamageRate` | `BUILD_OBJECT_DAMAGE_RATE` |
| `BuildObjectDeteriorationDamageRate` | `BUILD_OBJECT_DETERIORATION_DAMAGE_RATE` |
| `BuildObjectHpRate` | `BUILD_OBJECT_HP_RATE` |
| `CollectionDropRate` | `COLLECTION_DROP_RATE` |
| `CollectionObjectHpRate` | `COLLECTION_OBJECT_HP_RATE` |
| `CollectionObjectRespawnSpeedRate` | `COLLECTION_OBJECT_RESPAWN_SPEED_RATE` |
| `EnemyDropItemRate` | `ENEMY_DROP_ITEM_RATE` |
| `DropItemMaxNum` | `DROP_ITEM_MAX_NUM` |
| `DropItemMaxNum_UNKO` | `DROP_ITEM_MAX_NUM_UNKO` |
| `DropItemAliveMaxHours` | `DROP_ITEM_ALIVE_MAX_HOURS` |
| `MaxBuildingLimitNum` | `MAX_BUILDING_LIMIT_NUM` |
| `bBuildAreaLimit` | `BUILD_AREA_LIMIT` |
| `SupplyDropSpan` | `SUPPLY_DROP_SPAN` |
| `EnablePredatorBossPal` | `ENABLE_PREDATOR_BOSS_PAL` |
| `ItemContainerForceMarkDirtyInterval` | `ITEM_CONTAINER_FORCE_MARK_DIRTY_INTERVAL` |

### 🤝 Multiplayer & PvP

| Config Key | ENV Variable |
|---|---|
| `bIsMultiplay` | `IS_MULTIPLAY` |
| `bIsPvP` | `IS_PVP` |
| `bEnablePlayerToPlayerDamage` | `ENABLE_PLAYER_TO_PLAYER_DAMAGE` |
| `bEnableFriendlyFire` | `ENABLE_FRIENDLY_FIRE` |
| `bCanPickupOtherGuildDeathPenaltyDrop` | `CAN_PICKUP_OTHER_GUILD_DEATH_PENALTY_DROP` |
| `bEnableDefenseOtherGuildPlayer` | `ENABLE_DEFENSE_OTHER_GUILD_PLAYER` |
| `bDisplayPvPItemNumOnWorldMap_BaseCamp` | `DISPLAY_PVP_ITEM_NUM_ON_WORLD_MAP_BASE_CAMP` |
| `bDisplayPvPItemNumOnWorldMap_Player` | `DISPLAY_PVP_ITEM_NUM_ON_WORLD_MAP_PLAYER` |
| `AdditionalDropItemWhenPlayerKillingInPvPMode` | `ADDITIONAL_DROP_ITEM_WHEN_PLAYER_KILLING_IN_PVP_MODE` |
| `AdditionalDropItemNumWhenPlayerKillingInPvPMode` | `ADDITIONAL_DROP_ITEM_NUM_WHEN_PLAYER_KILLING_IN_PVP_MODE` |
| `bAdditionalDropItemWhenPlayerKillingInPvPMode` | `ADDITIONAL_DROP_ITEM_WHEN_PLAYER_KILLING_IN_PVP_MODE_ENABLED` |

### 🏰 Guilds & Bases

| Config Key | ENV Variable |
|---|---|
| `BaseCampMaxNum` | `BASE_CAMP_MAX_NUM` |
| `BaseCampWorkerMaxNum` | `BASE_CAMP_WORKER_MAX_NUM` |
| `BaseCampMaxNumInGuild` | `BASE_CAMP_MAX_NUM_IN_GUILD` |
| `GuildPlayerMaxNum` | `GUILD_PLAYER_MAX_NUM` |
| `bAutoResetGuildNoOnlinePlayers` | `AUTO_RESET_GUILD_NO_ONLINE_PLAYERS` |
| `AutoResetGuildTimeNoOnlinePlayers` | `AUTO_RESET_GUILD_TIME_NO_ONLINE_PLAYERS` |
| `bInvisibleOtherGuildBaseCampAreaFX` | `INVISIBLE_OTHER_GUILD_BASE` |
| `GuildRejoinCooldownMinutes` | `GUILD_REJOIN_COOLDOWN_MINUTES` |

### 🥚 Pals & Breeding

| Config Key | ENV Variable |
|---|---|
| `PalEggDefaultHatchingTime` | `PAL_EGG_DEFAULT_HATCHING_TIME` |
| `bActiveUNKO` | `ACTIVE_UNKO` |
| `bPalLost` | `PAL_LOST` |
| `bAllowGlobalPalboxExport` | `ALLOW_GLOBAL_PALBOX_EXPORT` |
| `bAllowGlobalPalboxImport` | `ALLOW_GLOBAL_PALBOX_IMPORT` |

### 💀 Hardcore & Respawn

| Config Key | ENV Variable |
|---|---|
| `bHardcore` | `HARDCORE` |
| `bCharacterRecreateInHardcore` | `CHARACTER_RECREATE_IN_HARDCORE` |
| `BlockRespawnTime` | `BLOCK_RESPAWN_TIME` |
| `RespawnPenaltyDurationThreshold` | `RESPAWN_PENALTY_DURATION_THRESHOLD` |
| `RespawnPenaltyTimeScale` | `RESPAWN_PENALTY_TIME_SCALE` |

### 🎯 Controls & UI

| Config Key | ENV Variable |
|---|---|
| `bEnableAimAssistPad` | `ENABLE_AIM_ASSIST_PAD` |
| `bEnableAimAssistKeyboard` | `ENABLE_AIM_ASSIST_KEYBOARD` |
| `bShowPlayerList` | `SHOW_PLAYER_LIST` |
| `bIsShowJoinLeftMessage` | `SHOW_JOIN_LEFT_MESSAGE` |
| `ChatPostLimitPerMinute` | `CHAT_POST_LIMIT` |
| `bEnableFastTravel` | `ENABLE_FAST_TRAVEL` |
| `bEnableFastTravelOnlyBaseCamp` | `ENABLE_FAST_TRAVEL_ONLY_BASE_CAMP` |
| `bIsStartLocationSelectByMap` | `IS_START_LOCATION_SELECT_BY_MAP` |
| `bExistPlayerAfterLogout` | `EXIST_PLAYER_AFTER_LOGOUT` |
| `bEnableNonLoginPenalty` | `ENABLE_NON_LOGIN_PENALTY` |
| `bEnableInvaderEnemy` | `ENABLE_ENEMY` |

### 📊 Player Stats

| Config Key | ENV Variable |
|---|---|
| `bAllowEnhanceStat_Health` | `ALLOW_ENHANCE_STAT_HEALTH` |
| `bAllowEnhanceStat_Attack` | `ALLOW_ENHANCE_STAT_ATTACK` |
| `bAllowEnhanceStat_Stamina` | `ALLOW_ENHANCE_STAT_STAMINA` |
| `bAllowEnhanceStat_Weight` | `ALLOW_ENHANCE_STAT_WEIGHT` |
| `bAllowEnhanceStat_WorkSpeed` | `ALLOW_ENHANCE_STAT_WORK_SPEED` |

### 🎲 Randomizer

| Config Key | ENV Variable |
|---|---|
| `RandomizerType` | `RANDOMIZER_TYPE` |
| `RandomizerSeed` | `RANDOMIZER_SEED` |
| `bIsRandomizerPalLevelRandom` | `IS_RANDOMIZER_PAL_LEVEL_RANDOM` |

### ⚙️ Server Settings

| Config Key | ENV Variable |
|---|---|
| `ServerPlayerMaxNum` | `MAX_PLAYERS` |
| `CoopPlayerMaxNum` | `COOP_PLAYER_MAX_NUM` |
| `ServerName` | `SERVER_NAME` |
| `ServerDescription` | `SERVER_DESCRIPTION` |
| `ServerPassword` | `SERVER_PASSWORD` |
| `AdminPassword` | `ADMIN_PASSWORD` |
| `PublicIP` | `PUBLIC_IP` / `SERVER_IP` |
| `PublicPort` | `SERVER_PORT` |
| `RCONPort` | `RCON_PORT` |
| `RCONEnabled` | `RCON_ENABLE` |
| `RESTAPIEnabled` | `REST_API_ENABLED` |
| `RESTAPIPort` | `REST_API_PORT` |
| `bUseAuth` | `USE_AUTH` |
| `BanListURL` | `BAN_LIST_URL` |
| `Region` | `SERVER_REGION` |
| `AutoSaveSpan` | `AUTO_SAVE_SPAN` |
| `bIsUseBackupSaveData` | `USE_BACKUP_SAVE_DATA` |
| `LogFormatType` | `LOG_FORMAT_TYPE` |
| `ServerReplicatePawnCullDistance` | `SERVER_REPLICATE_PAWN_CULL_DISTANCE` |
| `bAllowClientMod` | `ALLOW_CLIENT_MOD` |
| `CrossplayPlatforms` | `CROSSPLAY_PLATFORMS` |
| `DenyTechnologyList` | `DENY_TECHNOLOGY_LIST` |

---

## 🛡️ Validation Rules

All values are validated before being written to the config file. Invalid values are rejected and trigger a terminal warning, protecting your server from crashing.

| Rule | Accepts | Example |
|---|---|---|
| **Numeric** | Positive integers (≥ 0) | `123`, `25565` |
| **Floating** | Positive decimals with a `.` | `0.005`, `3.14` |
| **TrueFalse** | Exactly `True` or `False` | `True`, `False` |
| **String** | Any text | `Hello World` |
| **AlphaDash** | Alphanumeric, dashes, underscores | `abc123`, `test-pass_1` |
| **CrossplayPlatforms** | Comma-separated platform list | `Steam,Xbox,PS5,Mac` |

> **CrossplayPlatforms Note:** Valid platforms are `Steam`, `Xbox`, `PS5`, `Mac`. An empty value disables crossplay. Parentheses are automatically injected into the INI file by the parser (e.g., `CrossplayPlatforms=(Steam,Xbox)`).

---

## 📝 Notes & Edge Cases

- **Smart Merging:** If a variable is completely missing from your environment, the parser leaves the pre-existing config value untouched. It does not blindly overwrite with empty data!
- **Auto-Restoration:** If `PalWorldSettings.ini` is accidentally wiped, empty, or under `1200 bytes`, the tool will automatically overwrite it with `DefaultPalWorldSettings.ini` to save your server from throwing exceptions.
- **Proton/Wine Fallback:** If `WINEPREFIX` is set or `proton` is detected on a Linux host, the binary maps the config target path to `WindowsServer` instead of `LinuxServer` automatically.
- **Windows Subtlety:** On Windows, empty environment variables are treated as "unset" by the OS. The parser handles this correctly.

---

## 🔨 Building from Source

You can build the single-file executables yourself using `pyinstaller`.

```bash
git clone https://github.com/KJAyano/Palworld-Config-Parser-Tool.git
cd Palworld-Config-Parser-Tool
pip install pyinstaller

# Build the executable from the src directory
pyinstaller --onefile --name PalworldServerConfigParser src/main.py
```

Your standalone binary will be generated inside the `dist/` folder.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
