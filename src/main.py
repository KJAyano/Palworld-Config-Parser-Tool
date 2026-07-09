import os
from pathlib import Path

from validation import ValidationRules
from mappings import envVars, envVarsValidationRules, envVarsQuotes
from utils import detect_os_folder, set_ini_value, copy_file, get_ip_address_key

VERSION = "v0.7.3"

def main():
    print("Program Version:", VERSION)

    envVars["PublicIP"] = get_ip_address_key()

    os_folder = detect_os_folder()
    ini_file_path = Path(f"Pal/Saved/Config/{os_folder}/PalWorldSettings.ini").resolve()
    default_ini_path = Path("DefaultPalWorldSettings.ini")

    if not ini_file_path.exists():
        if default_ini_path.exists():
            relative_new_path = f"Pal/Saved/Config/{os_folder}/PalWorldSettings.ini"
            copy_file(str(default_ini_path), str(ini_file_path))
            print("DefaultPalWorldSettings.ini copied to:", relative_new_path)
        else:
            print("PalWorldSettings.ini not found and DefaultPalWorldSettings.ini missing.")
            return
    else:
        file_size = ini_file_path.stat().st_size
        if file_size == 0 or file_size < 1200:
            try:
                copy_file(str(default_ini_path), str(ini_file_path))
                print("Replaced empty PalWorldSettings.ini with default.")
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

    for config_key, env_var_name in envVars.items():
        env_var_value = os.environ.get(env_var_name)

        if env_var_value is None:
            continue

        if env_var_value == "":
            print(f"Updating empty key: {config_key}")
            ini_content = set_ini_value(ini_content, config_key, "", config_key in envVarsQuotes)
            continue

        if config_key in envVarsValidationRules:
            rule_name = envVarsValidationRules[config_key]
            if rule_name in ValidationRules:
                validation_function = ValidationRules[rule_name]
                if not validation_function(env_var_value):
                    print(f"Validation failed for key: {config_key}, value: {env_var_value}")
                    continue
            else:
                print(f"No validation rule found for key: {config_key}")
        else:
            print(f"No validation rule specified for key: {config_key}")

        print(f"Updating key: {config_key} with value: {env_var_value}")
        ini_content = set_ini_value(ini_content, config_key, env_var_value, config_key in envVarsQuotes)

    try:
        ini_file_path.write_text(ini_content, encoding="utf-8")
    except Exception as file_write_error:
        print(f"Error writing updated INI file: {file_write_error}")
        return

    print("INI file updated successfully.")

if __name__ == "__main__":
    main()