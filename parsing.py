import re

REQUIRED_KEYS = {
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "PERFECT",
    "OUTPUT_FILE"
}

PATTERNS = {
    "WIDTH": r"^\d+$",
    "HEIGHT": r"^\d+$",
    "ENTRY": r"^\d+,\d+$",
    "EXIT": r"^\d+,\d+$",
    "OUTPUT_FILE": r"^[\w\-.]+$",
    "PERFECT": r"^(True|False)$",
    "SEED": r"^\d+$"
}


def parse_config(filename):
    config = {}

    with open(filename) as f:
        for line_num, line in enumerate(f, 1):

            line = line.strip()

            # skip empty or comment
            if not line or line.startswith("#"):
                continue

            # لازم يكون فيها =
            if "=" not in line:
                raise ValueError(f"[Line {line_num}] Missing '=' in line: {line}")

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            # key خاصها تكون معروفة
            if key not in PATTERNS:
                raise ValueError(f"[Line {line_num}] Unknown key: {key}")

            # value خاصها تكون موجودة
            if value == "":
                raise ValueError(f"[Line {line_num}] Missing value for key: {key}")

            # duplicate key
            if key in config:
                raise ValueError(f"[Line {line_num}] Duplicate key: {key}")

            # validate format
            if not re.fullmatch(PATTERNS[key], value):
                raise ValueError(f"[Line {line_num}] Invalid value '{value}' for key '{key}'")

            config[key] = value

    # check required keys
    missing = REQUIRED_KEYS - config.keys()
    if missing:
        raise ValueError(f"Missing required keys: {missing}")

    # default
    config.setdefault("OUTPUT_FILE", "maze.txt")

    # convert types
    config["WIDTH"] = int(config["WIDTH"])
    config["HEIGHT"] = int(config["HEIGHT"])
    config["ENTRY"] = tuple(map(int, config["ENTRY"].split(",")))
    config["EXIT"] = tuple(map(int, config["EXIT"].split(",")))
    config["PERFECT"] = config["PERFECT"] == "True"

    if "SEED" in config:
        config["SEED"] = int(config["SEED"])

    # logical validation
    width, height = config["WIDTH"], config["HEIGHT"]
    ex, ey = config["ENTRY"]
    xx, xy = config["EXIT"]

    if not (0 <= ex < width and 0 <= ey < height):
        raise ValueError("ENTRY out of maze bounds")

    if not (0 <= xx < width and 0 <= xy < height):
        raise ValueError("EXIT out of maze bounds")

    if config["ENTRY"] == config["EXIT"]:
        raise ValueError("ENTRY and EXIT cannot be the same")
    output_file = config["OUTPUT_FILE"]

    if not output_file.endswith(".txt"):
        raise ValueError("OUTPUT_FILE must end with '.txt'")

    if output_file.lower() == "config.txt":
        raise ValueError("OUTPUT_FILE cannot be 'config.txt'")
    return config
