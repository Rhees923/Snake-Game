"""
storage.py - High score and settings local storage manager.
Uses standard JSON file I/O with fallback error handling.
"""

import json
import os
from typing import Dict, Any

SETTINGS_FILE = "settings.json"
HIGHSCORE_FILE = "highscore.json"

DEFAULT_SETTINGS: Dict[str, Any] = {
    "difficulty": "Normal",
    "grid": True,
    "sound": True,
    "theme": "Dark"
}

DEFAULT_HIGHSCORE: Dict[str, Any] = {
    "high_score": 0,
    "player_name": "Player"
}


class StorageManager:
    """Manages reading and writing data safely to disk using JSON."""

    @staticmethod
    def load_settings() -> Dict[str, Any]:
        """Loads settings from JSON or returns defaults if file missing or corrupted."""
        if not os.path.exists(SETTINGS_FILE):
            StorageManager.save_settings(DEFAULT_SETTINGS)
            return DEFAULT_SETTINGS.copy()
        
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Ensure all key properties exist
                settings = DEFAULT_SETTINGS.copy()
                settings.update(data)
                return settings
        except (json.JSONDecodeError, OSError):
            return DEFAULT_SETTINGS.copy()

    @staticmethod
    def save_settings(settings: Dict[str, Any]) -> bool:
        """Saves settings dictionary to JSON file."""
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=4)
            return True
        except OSError:
            return False

    @staticmethod
    def load_highscore() -> int:
        """Loads high score value from JSON."""
        if not os.path.exists(HIGHSCORE_FILE):
            StorageManager.save_highscore(0)
            return 0
        
        try:
            with open(HIGHSCORE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return int(data.get("high_score", 0))
        except (json.JSONDecodeError, ValueError, OSError):
            return 0

    @staticmethod
    def save_highscore(score: int) -> bool:
        """Saves new high score to JSON."""
        try:
            data = {"high_score": score}
            with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            return True
        except OSError:
            return False

    @staticmethod
    def reset_highscore() -> bool:
        """Resets stored high score to 0."""
        return StorageManager.save_highscore(0)