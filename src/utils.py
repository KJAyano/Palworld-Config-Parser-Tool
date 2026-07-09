import os
import shutil
import platform
import sys
from pathlib import Path

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
