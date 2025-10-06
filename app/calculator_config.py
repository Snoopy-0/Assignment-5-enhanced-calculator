
"""
Configuration management using environment variables and python-dotenv.
"""
from __future__ import annotations
import os
from dataclasses import dataclass
from dotenv import load_dotenv
from .exceptions import ConfigurationError

load_dotenv()

@dataclass
class Config:
    history_csv: str
    autosave: bool = True

    @staticmethod
    def load() -> "Config":
        csv = os.getenv("HISTORY_CSV", "history.csv")
        autosave_str = os.getenv("AUTOSAVE", "true").lower()
        if autosave_str not in {"true", "false"}:
            raise ConfigurationError("AUTOSAVE must be 'true' or 'false'")
        return Config(history_csv=csv, autosave=(autosave_str == "true"))
