"""
menu.py - Render interfaces for main menu, settings,
instructions, and high scores.
"""

import tkinter as tk
from typing import Callable, Dict, Any

from settings import (
    THEMES,
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
    play_sound,
)


class MenuManager:
    """Renders menus and interactive widgets on a Tkinter Canvas."""

    def __init__(
        self,
        canvas: tk.Canvas,
        callbacks: Dict[str, Callable],
        current_settings: Dict[str, Any],
    ):
        self.canvas = canvas
        self.callbacks = callbacks
        self.settings = current_settings

        self.theme = THEMES[
            self.settings["theme"]
        ]

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self) -> None:
        """Clears all canvas content."""

        self.canvas.delete("all")

    # =========================================================
    # BUTTON
    # =========================================================

    def draw_button(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        command: Callable,
        font_size: int = 14,
    ) -> None:
        """Creates a modern interactive canvas button."""

        bg = self.theme["button_bg"]
        fg = self.theme["button_fg"]

        # -----------------------------------------------------
        # Shadow
        # -----------------------------------------------------

        self.canvas.create_rectangle(
            x - width // 2 + 3,
            y - height // 2 + 3,
            x + width // 2 + 3,
            y + height // 2 + 3,
            fill="#000000",
            outline="",
            tags="button",
        )

        # -----------------------------------------------------
        # Button
        # -----------------------------------------------------

        rect = self.canvas.create_rectangle(
            x - width // 2,
            y - height // 2,
            x + width // 2,
            y + height // 2,
            fill=bg,
            outline=self.theme["accent"],
            width=2,
            tags="button",
        )

        # -----------------------------------------------------
        # Button text
        # -----------------------------------------------------

        btn_text = self.canvas.create_text(
            x,
            y,
            text=text,
            fill=fg,
            font=(
                "Helvetica",
                font_size,
                "bold",
            ),
            tags="button",
        )

        # -----------------------------------------------------
        # Hover
        # -----------------------------------------------------

        def on_enter(event: tk.Event) -> None:
            self.canvas.itemconfig(
                rect,
                fill=self.theme["button_active"],
            )

            if self.settings.get("sound", False):
                play_sound("click")

        def on_leave(event: tk.Event) -> None:
            self.canvas.itemconfig(
                rect,
                fill=bg,
            )

        # -----------------------------------------------------
        # Click
        # -----------------------------------------------------

        def on_click(event: tk.Event) -> None:
            command()

        # Bind both rectangle and text
        for element in (rect, btn_text):

            self.canvas.tag_bind(
                element,
                "<Enter>",
                on_enter,
            )

            self.canvas.tag_bind(
                element,
                "<Leave>",
                on_leave,
            )

            self.canvas.tag_bind(
                element,
                "<Button-1>",
                on_click,
            )

    # =========================================================
    # MAIN MENU
    # =========================================================

    def show_main_menu(self) -> None:
        """Renders the main menu."""

        self.clear()

        self.theme = THEMES[
            self.settings["theme"]
        ]

        self.canvas.config(
            bg=self.theme["bg"]
        )

        cx = CANVAS_WIDTH // 2

        # -----------------------------------------------------
        # Title
        # -----------------------------------------------------

        self.canvas.create_text(
            cx,
            110,
            text="PYTHON SNAKE",
            fill=self.theme["accent"],
            font=(
                "Helvetica",
                32,
                "bold",
            ),
        )

        self.canvas.create_text(
            cx,
            155,
            text="Classic Snake - Rebuilt in Python",
            fill=self.theme["subtext"],
            font=(
                "Helvetica",
                13,
                "italic",
            ),
        )

        # -----------------------------------------------------
        # Buttons
        # -----------------------------------------------------

        self.draw_button(
            cx,
            230,
            220,
            45,
            "PLAY",
            self.callbacks["start_game"],
        )

        self.draw_button(
            cx,
            290,
            220,
            45,
            "SETTINGS",
            self.callbacks["show_settings"],
        )

        self.draw_button(
            cx,
            350,
            220,
            45,
            "HOW TO PLAY",
            self.callbacks["show_how_to_play"],
        )

        self.draw_button(
            cx,
            410,
            220,
            45,
            "HIGH SCORE",
            self.callbacks["show_highscore"],
        )

        self.draw_button(
            cx,
            470,
            220,
            45,
            "EXIT",
            self.callbacks["exit"],
        )

    # =========================================================
    # SETTINGS
    # =========================================================

    def show_settings(
        self,
        save_callback: Callable,
        reset_score_callback: Callable,
    ) -> None:
        """Renders the settings screen."""

        self.clear()

        self.theme = THEMES[
            self.settings["theme"]
        ]

        self.canvas.config(
            bg=self.theme["bg"]
        )

        cx = CANVAS_WIDTH // 2

        # -----------------------------------------------------
        # Title
        # -----------------------------------------------------

        self.canvas.create_text(
            cx,
            60,
            text="SETTINGS",
            fill=self.theme["accent"],
            font=(
                "Helvetica",
                26,
                "bold",
            ),
        )

        # -----------------------------------------------------
        # Difficulty
        # -----------------------------------------------------

        self.canvas.create_text(
            cx - 150,
            130,
            text="Difficulty:",
            fill=self.theme["text"],
            font=(
                "Helvetica",
                13,
                "bold",
            ),
            anchor="w",
        )

        difficulties = [
            "Easy",
            "Normal",
            "Hard",
            "Extreme",
        ]

        current_difficulty = self.settings[
            "difficulty"
        ]

        for i, difficulty in enumerate(
            difficulties
        ):

            self.draw_button(
                cx - 50 + i * 75,
                130,
                70,
                30,
                difficulty,
                lambda value=difficulty:
                    self._update_setting(
                        "difficulty",
                        value,
                        save_callback,
                    ),
                font_size=9,
            )

        # -----------------------------------------------------
        # Grid
        # -----------------------------------------------------

        self.canvas.create_text(
            cx - 150,
            190,
            text="Grid Lines:",
            fill=self.theme["text"],
            font=(
                "Helvetica",
                13,
                "bold",
            ),
            anchor="w",
        )

        grid_text = (
            "ON"
            if self.settings.get("grid", True)
            else "OFF"
        )

        self.draw_button(
            cx + 50,
            190,
            100,
            30,
            grid_text,
            lambda: self._update_setting(
                "grid",
                not self.settings.get(
                    "grid",
                    True,
                ),
                save_callback,
            ),
            font_size=11,
        )

        # -----------------------------------------------------
        # Sound
        # -----------------------------------------------------

        self.canvas.create_text(
            cx - 150,
            250,
            text="Sound Effects:",
            fill=self.theme["text"],
            font=(
                "Helvetica",
                13,
                "bold",
            ),
            anchor="w",
        )

        sound_text = (
            "ON"
            if self.settings.get("sound", True)
            else "OFF"
        )

        self.draw_button(
            cx + 50,
            250,
            100,
            30,
            sound_text,
            lambda: self._update_setting(
                "sound",
                not self.settings.get(
                    "sound",
                    True,
                ),
                save_callback,
            ),
            font_size=11,
        )

        # -----------------------------------------------------
        # Theme
        # -----------------------------------------------------

        self.canvas.create_text(
            cx - 150,
            310,
            text="Visual Theme:",
            fill=self.theme["text"],
            font=(
                "Helvetica",
                13,
                "bold",
            ),
            anchor="w",
        )

        themes = [
            "Dark",
            "Light",
            "Neon",
        ]

        for i, theme_name in enumerate(
            themes
        ):

            self.draw_button(
                cx - 30 + i * 85,
                310,
                80,
                30,
                theme_name,
                lambda value=theme_name:
                    self._update_setting(
                        "theme",
                        value,
                        save_callback,
                    ),
                font_size=10,
            )

        # -----------------------------------------------------
        # High Score Reset
        # -----------------------------------------------------

        self.canvas.create_text(
            cx - 150,
            370,
            text="High Score:",
            fill=self.theme["text"],
            font=(
                "Helvetica",
                13,
                "bold",
            ),
            anchor="w",
        )

        self.draw_button(
            cx + 50,
            370,
            120,
            30,
            "RESET",
            reset_score_callback,
            font_size=10,
        )

        # -----------------------------------------------------
        # Back
        # -----------------------------------------------------

        self.draw_button(
            cx,
            460,
            180,
            40,
            "BACK",
            self.callbacks["show_main_menu"],
        )

    # =========================================================
    # UPDATE SETTINGS
    # =========================================================

    def _update_setting(
        self,
        key: str,
        value: Any,
        save_callback: Callable,
    ) -> None:
        """Updates a setting and redraws the settings screen."""

        self.settings[key] = value

        save_callback()

        self.show_settings(
            save_callback,
            self.callbacks.get(
                "reset_score",
                lambda: None,
            ),
        )

    # =========================================================
    # HOW TO PLAY
    # =========================================================

    def show_how_to_play(self) -> None:
        """Renders the controls and game instructions."""

        self.clear()

        self.theme = THEMES[
            self.settings["theme"]
        ]

        self.canvas.config(
            bg=self.theme["bg"]
        )

        cx = CANVAS_WIDTH // 2

        # -----------------------------------------------------
        # Title
        # -----------------------------------------------------

        self.canvas.create_text(
            cx,
            50,
            text="HOW TO PLAY",
            fill=self.theme["accent"],
            font=(
                "Helvetica",
                24,
                "bold",
            ),
        )

        # -----------------------------------------------------
        # Instructions
        # -----------------------------------------------------

        info_text = (
            "CONTROLS\n\n"
            "W / UP       -> Move Up\n"
            "S / DOWN     -> Move Down\n"
            "A / LEFT     -> Move Left\n"
            "D / RIGHT    -> Move Right\n\n"
            "SPACE        -> Pause / Resume\n"
            "ESC          -> Return to Main Menu\n\n"
            "OBJECTIVES & FOODS\n\n"
            "Normal Food  -> +10 points\n"
            "Bonus Food   -> +25 points\n"
            "Rare Food    -> +50 points\n\n"
            "Avoid walls and your own tail!"
        )

        self.canvas.create_text(
            cx,
            250,
            text=info_text,
            fill=self.theme["text"],
            font=(
                "Consolas",
                12,
            ),
            justify="center",
        )

        # -----------------------------------------------------
        # Back
        # -----------------------------------------------------

        self.draw_button(
            cx,
            470,
            180,
            40,
            "BACK",
            self.callbacks["show_main_menu"],
        )

    # =========================================================
    # HIGH SCORE
    # =========================================================

    def show_highscore(
        self,
        highscore: int,
    ) -> None:
        """Renders the high score screen."""

        self.clear()

        self.theme = THEMES[
            self.settings["theme"]
        ]

        self.canvas.config(
            bg=self.theme["bg"]
        )

        cx = CANVAS_WIDTH // 2

        # -----------------------------------------------------
        # Title
        # -----------------------------------------------------

        self.canvas.create_text(
            cx,
            120,
            text="HIGH SCORE",
            fill=self.theme["accent"],
            font=(
                "Helvetica",
                28,
                "bold",
            ),
        )

        # -----------------------------------------------------
        # Score
        # -----------------------------------------------------

        self.canvas.create_text(
            cx,
            220,
            text=str(highscore),
            fill=self.theme["button_fg"],
            font=(
                "Helvetica",
                60,
                "bold",
            ),
        )

        self.canvas.create_text(
            cx,
            280,
            text="POINTS",
            fill=self.theme["subtext"],
            font=(
                "Helvetica",
                14,
                "bold",
            ),
        )

        # -----------------------------------------------------
        # Back
        # -----------------------------------------------------

        self.draw_button(
            cx,
            410,
            180,
            45,
            "BACK",
            self.callbacks["show_main_menu"],
        )