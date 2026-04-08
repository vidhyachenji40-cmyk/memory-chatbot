import json
import os
from typing import Any

class ShortTermMemory:
    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        self._messages = []

    def add(self, role: str, content: Any):
        self._messages.append({"role": role, "content": content})
        if len(self._messages) > self.max_turns * 2:
            self._messages = self._messages[-(self.max_turns * 2):]

    def get_messages(self) -> list:
        return self._messages

    def clear(self):
        self._messages = []

class LongTermMemory:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._facts = {}
        self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    self._facts = json.load(f)
            except: self._facts = {}
        else: self._facts = {}

    def _save(self):
        with open(self.filepath, "w") as f:
            json.dump(self._facts, f, indent=2)

    def save_fact(self, key: str, value: str):
        normalized_key = key.lower().strip().replace(" ", "_")
        self._facts[normalized_key] = value
        self._save()

    def get_all_facts(self) -> dict:
        return dict(self._facts)