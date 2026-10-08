"""
settings.py - Project constants, theme palettes, and optional audio support.
"""

import sys
from typing import Dict, Any

# Cross-platform sound effect player using native OS libraries
try:
    if sys.platform == "win32":
        import winsound
        def play_sound(sound_type: str) -> None:
            """Plays native Windows system sounds asynchronously."""
            frequencies = {
                "eat": (600, 50),
                "gameover": (200, 300),
                "click": (800, 30),
                "levelup": (1000, 100)
            }
            if sound_type in frequencies:
                freq, dur = frequencies[sound_type]
                try:
                    winsound.Beep(freq, dur)
                except Exception:
                    pass
    else:
        def play_sound(sound_type: str) -> None:
            # Platform bell fallback for Linux/macOS
            try:
                print("\a", end="")
            except Exception:
                pass
except Exception:
    def play_sound(sound_type: str) -> None:
        pass

# Grid and Canvas Dimensions
GRID_WIDTH = 25
GRID_HEIGHT = 20
CELL_SIZE = 28
GAME_WIDTH = GRID_WIDTH * CELL_SIZE
GAME_HEIGHT = GRID_HEIGHT * CELL_SIZE
HEADER_HEIGHT = 60
CANVAS_WIDTH = GAME_WIDTH
CANVAS_HEIGHT = GAME_HEIGHT + HEADER_HEIGHT

# Speed mappings (Milliseconds per frame)
DIFFICULTY_SPEEDS: Dict[str, int] = {
    "Easy": 140,
    "Normal": 100,
    "Hard": 70,
    "Extreme": 45
}

# Theme Color Definitions
THEMES: Dict[str, Dict[str, Any]] = {
    "Dark": {
        "bg": "#121212",
        "header_bg": "#1E1E1E",
        "grid_line": "#1A1A1A",
        "text": "#FFFFFF",
        "subtext": "#AAAAAA",
        "snake_head": "#00FF88",
        "snake_body": "#00B359",
        "snake_eye": "#000000",
        "food_normal": "#FF3366",
        "food_bonus": "#FFCC00",
        "food_rare": "#00E5FF",
        "panel_bg": "#1E1E1E",
        "button_bg": "#2A2A2A",
        "button_fg": "#00FF88",
        "button_active": "#333333",
        "accent": "#00FF88"
    },
    "Light": {
        "bg": "#F4F6F9",
        "header_bg": "#E2E8F0",
        "grid_line": "#CBD5E1",
        "text": "#1E293B",
        "subtext": "#64748B",
        "snake_head": "#10B981",
        "snake_body": "#059669",
        "snake_eye": "#FFFFFF",
        "food_normal": "#EF4444",
        "food_bonus": "#F59E0B",
        "food_rare": "#06B6D4",
        "panel_bg": "#FFFFFF",
        "button_bg": "#E2E8F0",
        "button_fg": "#0F172A",
        "button_active": "#CBD5E1",
        "accent": "#10B981"
    },
    "Neon": {
        "bg": "#050515",
        "header_bg": "#0A0A28",
        "grid_line": "#0D0D38",
        "text": "#00FFFF",
        "subtext": "#FF00FF",
        "snake_head": "#00FF66",
        "snake_body": "#009933",
        "snake_eye": "#FFFFFF",
        "food_normal": "#FF007F",
        "food_bonus": "#FFE600",
        "food_rare": "#00FFFF",
        "panel_bg": "#0A0A28",
        "button_bg": "#141440",
        "button_fg": "#00FFFF",
        "button_active": "#1F1F60",
        "accent": "#FF007F"
    }
}