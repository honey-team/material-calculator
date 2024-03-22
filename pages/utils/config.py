import json

ConfigPath = "config.json"


def cload() -> dict:
    with open(ConfigPath, "r", encoding="utf-8") as ConfigFile:
        rawJson = ConfigFile.read()
    return json.loads(rawJson)


def cwrite(config: dict):
    with open(ConfigPath, "w", encoding="utf-8") as ConfigFile:
        ConfigFile.write(json.dumps(config, skipkeys=True))
