import re

REQUIRED_KEYS = {
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "PERFECT"
}

PATTERNS = {
    "WIDTH": r"^\d+$",
    "HEIGHT": r"^\d+$",
    "ENTRY": r"^\d+,\d+$",
    "EXIT": r"^\d+,\d+$",
    "OUTPUT_FILE": r"^[\w\-.]+$",
    "PERFECT": r"^(True|False)$"
}


def parse_config(filename):

    config = {}

    with open(filename) as f:

        for line_num, line in enumerate(f, 1):

            line = line.strip()

            # skip empty lines
            if not line:
                continue

            # skip comments
            if line.startswith("#"):
                continue

            if "=" not in line:
                raise ValueError(f"Invalid line {line_num}: {line}")

            key, value = line.split("=", 1)

            key = key.strip()
            value = value.strip()

            if key not in PATTERNS:
                raise ValueError(f"Unknown key '{key}' at line {line_num}")

            if not re.fullmatch(PATTERNS[key], value):
                raise ValueError(f"Invalid value '{value}' for {key}")

            config[key] = value

    # check mandatory keys
    missing = REQUIRED_KEYS - config.keys()

    if missing:
        raise ValueError(f"Missing keys: {missing}")

    # default OUTPUT_FILE if not provided
    if "OUTPUT_FILE" not in config:
        config["OUTPUT_FILE"] = "maze.txt"

    # convert types
    config["WIDTH"] = int(config["WIDTH"])
    config["HEIGHT"] = int(config["HEIGHT"])

    config["ENTRY"] = tuple(map(int, config["ENTRY"].split(",")))
    config["EXIT"] = tuple(map(int, config["EXIT"].split(",")))

    config["PERFECT"] = config["PERFECT"] == "True"

    # logic validation
    width = config["WIDTH"]
    height = config["HEIGHT"]

    ex, ey = config["ENTRY"]
    xx, xy = config["EXIT"]

    if not (0 <= ex < width and 0 <= ey < height):
        raise ValueError("ENTRY out of maze bounds")

    if not (0 <= xx < width and 0 <= xy < height):
        raise ValueError("EXIT out of maze bounds")

    if config["ENTRY"] == config["EXIT"]:
        raise ValueError("ENTRY and EXIT cannot be the same")

    return config


config = parse_config("config.txt")

print(config)