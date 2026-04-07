import re
from typing import Dict, Any

REQUIRED_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "PERFECT", "OUTPUT_FILE"}

PATTERNS = {
    "WIDTH": r"^\d+$",
    "HEIGHT": r"^\d+$",
    "ENTRY": r"^\d+,\d+$",
    "EXIT": r"^\d+,\d+$",
    "OUTPUT_FILE": r"^[\w\-.]+$",
    "PERFECT": r"^(True|False)$",
    "SEED": r"^\d+$",
}


def parse_config(filename: str) -> Dict[str, Any]:
    """Parse a maze configuration file and return a validated config dict."""
    config: Dict[str, Any] = {}

    with open(filename) as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                raise ValueError(
                    f"[Line {line_num}] Missing '=' in line: {line}"
                )

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            if key not in PATTERNS:
                raise ValueError(
                    f"[Line {line_num}] Unknown key: {key}"
                )

            if value == "":
                raise ValueError(
                    f"[Line {line_num}] Missing value for key: {key}"
                )

            if key in config:
                raise ValueError(
                    f"[Line {line_num}] Duplicate key: {key}"
                )

            if not re.fullmatch(PATTERNS[key], value):
                raise ValueError(
                    f"[Line {line_num}] Invalid value '{value}' "
                    f"for key '{key}'"
                )

            config[key] = value

    missing = REQUIRED_KEYS - config.keys()
    if missing:
        raise ValueError(f"Missing required keys: {missing}")

    config.setdefault("OUTPUT_FILE", "maze.txt")

    # Convert types
    config["WIDTH"] = int(config["WIDTH"])
    config["HEIGHT"] = int(config["HEIGHT"])
    config["ENTRY"] = tuple(map(int, config["ENTRY"].split(",")))
    config["EXIT"] = tuple(map(int, config["EXIT"].split(",")))
    config["PERFECT"] = config["PERFECT"] == "True"

    if "SEED" in config:
        config["SEED"] = int(config["SEED"])

    width, height = config["WIDTH"], config["HEIGHT"]
    ex, ey = config["ENTRY"]
    xx, xy = config["EXIT"]

    if not (0 <= ex < width
            and 0 <= ey < height):
        raise ValueError("ENTRY out of maze bounds")

    if not (0 <= xx < width
            and 0 <= xy < height):
        raise ValueError("EXIT out of maze bounds")

    if config["ENTRY"] == config["EXIT"]:
        raise ValueError("ENTRY and EXIT cannot be the same")

    output_file = config["OUTPUT_FILE"]
    if not output_file.endswith(".txt"):
        raise ValueError("OUTPUT_FILE must end with '.txt'")

    if output_file.lower() == "config.txt":
        raise ValueError("OUTPUT_FILE cannot be 'config.txt'")

    return config
