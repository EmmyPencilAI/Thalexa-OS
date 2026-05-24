from pathlib import Path


class MemoryStore:
    def __init__(self, path: str):
        self.path = path
        self._ensure_store()

    def _ensure_store(self):
        Path(self.path).mkdir(parents=True, exist_ok=True)

    @classmethod
    def initialize(cls, path: str) -> "MemoryStore":
        return cls(path)
