import json

MemoryPath = 'memory.json'


def load() -> dict:
    with open(MemoryPath, 'r', encoding='utf-8') as MemoryFile:
        rawJson = MemoryFile.read()
    return json.loads(rawJson)


def write(memory: dict):
    with open(MemoryPath, 'w', encoding='utf-8') as MemoryFile:
        MemoryFile.write(json.dumps(memory, skipkeys=True))
