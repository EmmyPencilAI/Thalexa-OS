import yaml
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PersonalityConfig:
    name: str
    voice_style: str
    tone: str
    assistant_mode: str
    humor: str
    coding_mode: str
    robotics_mode: str
    persistent_memory: bool
    traits: list[str]

    @classmethod
    def load(cls, path: str) -> "PersonalityConfig":
        with open(path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
        return cls(**data)
