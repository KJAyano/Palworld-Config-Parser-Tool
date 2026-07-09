import re

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
        return True
    except ValueError:
        return False

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

ValidationRules = {
    "Numeric": validate_numeric,
    "Floating": validate_floating,
    "TrueFalse": validate_true_false,
    "String": validate_string,
    "AlphaDash": validate_alpha_dash,
    "CrossplayPlatforms": validate_crossplay_platforms,
}