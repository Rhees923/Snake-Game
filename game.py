"""
game.py - Primary Snake gameplay logic, rendering, and game state manager.
"""

import math
import tkinter as tk
from typing import Dict, Any, Callable

from settings import (
    THEMES,
    GRID_WIDTH,
    GRID_HEIGHT,
    CELL_SIZE,
    HEADER_HEIGHT,
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
    DIFFICULTY_SPEEDS,
    play_sound,
)

from snake import Snake, UP, DOWN, LEFT, RIGHT
from food import Food


class GameEngine:
    """Controls gameplay lifecycle, updates, and rendering."""

    def __init__(
        self,
        canvas: tk.Canvas,
        settings: Dict[str, Any],
        highscore: int,
        on_game_over: Callable[[int], None],
        return_menu_cb: Callable[[], None],
    ):
        self.canvas = canvas
        self.settings = settings

        self.theme = THEMES[self.settings["theme"]]

        self.high_score = highscore
        self.on_game_over_cb = on_game_over
        self.return_menu_cb = return_menu_cb

        # Create snake
        self.snake = Snake(
            GRID_WIDTH // 2,
            GRID_HEIGHT // 2
        )

        # Create food
        self.food = Food(
            GRID_WIDTH,
            GRID_HEIGHT
        )

        self.food.spawn(self.snake.body)

        # Game state
        self.score = 0
        self.level = 1

        self.is_running = False
        self.is_paused = False
        self.is_game_over = False

        self.countdown_val = 3

        # Speed
        self.base_speed = DIFFICULTY_SPEEDS.get(
            self.settings["difficulty"],
            100
        )

        self.current_speed = self.base_speed

    # ---------------------------------------------------------
    # START GAME
    # ---------------------------------------------------------

    def start(self) -> None:
        """Initializes and starts a new game."""

        self.is_running = True
        self.is_paused = False
        self.is_game_over = False

        self.score = 0
        self.level = 1

        # Reset speed
        self.base_speed = DIFFICULTY_SPEEDS.get(
            self.settings["difficulty"],
            100
        )

        self.current_speed = self.base_speed

        # Reset snake
        self.snake = Snake(
            GRID_WIDTH // 2,
            GRID_HEIGHT // 2
        )

        # Reset food
        self.food.spawn(self.snake.body)

        # Start countdown
        self.run_countdown(3)

    # ---------------------------------------------------------
    # COUNTDOWN
    # ---------------------------------------------------------

    def run_countdown(self, count: int) -> None:
        """Displays the countdown before the game starts."""

        if not self.is_running:
            return

        self.render()

        if count > 0:
            cx = CANVAS_WIDTH // 2
            cy = (
                HEADER_HEIGHT
                + (CANVAS_HEIGHT - HEADER_HEIGHT) // 2
            )

            self.canvas.create_text(
                cx,
                cy,
                text=str(count),
                fill=self.theme["accent"],
                font=("Helvetica", 72, "bold"),
                tags="overlay",
            )

            if self.settings.get("sound", False):
                play_sound("click")

            self.canvas.after(
                700,
                lambda: self.run_countdown(count - 1)
            )

        else:
            self.game_loop()

    # ---------------------------------------------------------
    # KEYBOARD
    # ---------------------------------------------------------

    def handle_keypress(self, event: tk.Event) -> None:
        """Processes keyboard input."""

        key = event.keysym.lower()

        if not self.is_running:
            return

        if key in ("w", "up"):
            self.snake.change_direction(UP)

        elif key in ("s", "down"):
            self.snake.change_direction(DOWN)

        elif key in ("a", "left"):
            self.snake.change_direction(LEFT)

        elif key in ("d", "right"):
            self.snake.change_direction(RIGHT)

        elif key == "space":
            self.toggle_pause()

        elif key == "escape":
            self.is_running = False
            self.is_paused = False
            self.return_menu_cb()

    # ---------------------------------------------------------
    # PAUSE
    # ---------------------------------------------------------

    def toggle_pause(self) -> None:
        """Toggles the pause state."""

        if self.is_game_over or not self.is_running:
            return

        self.is_paused = not self.is_paused

        if self.is_paused:
            self.render_pause_overlay()
        else:
            self.game_loop()

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------

    def update(self) -> None:
        """Executes one game logic update."""

        if (
            self.is_paused
            or not self.is_running
            or self.is_game_over
        ):
            return

        # Move snake
        self.snake.move()

        # ---------------------------------------------
        # Collision
        # ---------------------------------------------

        if (
            self.snake.check_wall_collision(
                GRID_WIDTH,
                GRID_HEIGHT
            )
            or self.snake.check_self_collision()
        ):
            self.trigger_game_over()
            return

        # ---------------------------------------------
        # Food
        # ---------------------------------------------

        if self.snake.head == self.food.position:

            if self.settings.get("sound", False):
                play_sound("eat")

            self.score += self.food.points

            self.snake.grow(1)

            self.food.spawn(self.snake.body)

            # Update high score
            if self.score > self.high_score:
                self.high_score = self.score

            # Check level
            self.check_level_up()

    # ---------------------------------------------------------
    # LEVEL
    # ---------------------------------------------------------

    def check_level_up(self) -> None:
        """Increases level and snake speed."""

        new_level = (self.score // 50) + 1

        if new_level > self.level:

            self.level = new_level

            self.current_speed = max(
                30,
                self.base_speed
                - (self.level - 1) * 8
            )

            if self.settings.get("sound", False):
                play_sound("levelup")

    # ---------------------------------------------------------
    # GAME LOOP
    # ---------------------------------------------------------

    def game_loop(self) -> None:
        """Runs the recurring game loop."""

        if (
            not self.is_running
            or self.is_paused
            or self.is_game_over
        ):
            return

        self.update()

        if not self.is_game_over:
            self.render()

            self.canvas.after(
                self.current_speed,
                self.game_loop
            )

    # ---------------------------------------------------------
    # GAME OVER
    # ---------------------------------------------------------

    def trigger_game_over(self) -> None:
        """Triggers game-over state."""

        self.is_game_over = True
        self.is_running = False

        if self.settings.get("sound", False):
            play_sound("gameover")

        self.on_game_over_cb(self.score)

        self.render_game_over_overlay()

    # ---------------------------------------------------------
    # MAIN RENDER
    # ---------------------------------------------------------

    def render(self) -> None:
        """Renders the complete game screen."""

        self.canvas.delete("all")

        self.theme = THEMES[self.settings["theme"]]

        self.canvas.config(
            bg=self.theme["bg"]
        )

        # ---------------------------------------------
        # HEADER
        # ---------------------------------------------

        self.canvas.create_rectangle(
            0,
            0,
            CANVAS_WIDTH,
            HEADER_HEIGHT,
            fill=self.theme["header_bg"],
            outline="",
        )

        header_font = (
            "Helvetica",
            11,
            "bold"
        )

        self.canvas.create_text(
            20,
            30,
            text=f"SCORE: {self.score}",
            fill=self.theme["text"],
            font=header_font,
            anchor="w",
        )

        self.canvas.create_text(
            150,
            30,
            text=f"HIGH SCORE: {self.high_score}",
            fill=self.theme["accent"],
            font=header_font,
            anchor="w",
        )

        self.canvas.create_text(
            320,
            30,
            text=f"LEVEL: {self.level}",
            fill=self.theme["text"],
            font=header_font,
            anchor="w",
        )

        speed_val = max(
            1,
            11 - (self.current_speed // 10)
        )

        self.canvas.create_text(
            480,
            30,
            text=f"SPEED: {speed_val}",
            fill=self.theme["subtext"],
            font=header_font,
            anchor="w",
        )

        # ---------------------------------------------
        # GRID
        # ---------------------------------------------

        if self.settings.get("grid", True):

            grid_color = self.theme["grid_line"]

            for x in range(
                0,
                CANVAS_WIDTH + 1,
                CELL_SIZE
            ):
                self.canvas.create_line(
                    x,
                    HEADER_HEIGHT,
                    x,
                    CANVAS_HEIGHT,
                    fill=grid_color,
                )

            for y in range(
                HEADER_HEIGHT,
                CANVAS_HEIGHT + 1,
                CELL_SIZE
            ):
                self.canvas.create_line(
                    0,
                    y,
                    CANVAS_WIDTH,
                    y,
                    fill=grid_color,
                )

        # ---------------------------------------------
        # FOOD
        # ---------------------------------------------

        if self.food.position is not None:

            fx, fy = self.food.position

            fx_px = fx * CELL_SIZE

            fy_px = (
                fy * CELL_SIZE
                + HEADER_HEIGHT
            )

            pulse = math.sin(
                self.food.update_pulse()
            ) * 2

            food_color = self.theme.get(
                f"food_{self.food.type}",
                self.theme["food_normal"],
            )

            self.canvas.create_oval(
                fx_px + 3 - pulse,
                fy_px + 3 - pulse,
                fx_px + CELL_SIZE - 3 + pulse,
                fy_px + CELL_SIZE - 3 + pulse,
                fill=food_color,
                outline=self.theme["text"],
                width=1,
            )

        # ---------------------------------------------
        # SNAKE
        # ---------------------------------------------

        for i, (sx, sy) in enumerate(
            self.snake.body
        ):

            px = sx * CELL_SIZE

            py = (
                sy * CELL_SIZE
                + HEADER_HEIGHT
            )

            # -----------------------------------------
            # HEAD
            # -----------------------------------------

            if i == 0:

                self.canvas.create_rectangle(
                    px + 1,
                    py + 1,
                    px + CELL_SIZE - 1,
                    py + CELL_SIZE - 1,
                    fill=self.theme["snake_head"],
                    outline=self.theme["accent"],
                    width=2,
                )

                eye_color = self.theme["snake_eye"]

                dx, dy = self.snake.direction

                if dx == 1:
                    # Right
                    self.canvas.create_oval(
                        px + 18,
                        py + 6,
                        px + 22,
                        py + 10,
                        fill=eye_color,
                    )

                    self.canvas.create_oval(
                        px + 18,
                        py + 18,
                        px + 22,
                        py + 22,
                        fill=eye_color,
                    )

                elif dx == -1:
                    # Left
                    self.canvas.create_oval(
                        px + 6,
                        py + 6,
                        px + 10,
                        py + 10,
                        fill=eye_color,
                    )

                    self.canvas.create_oval(
                        px + 6,
                        py + 18,
                        px + 10,
                        py + 22,
                        fill=eye_color,
                    )

                elif dy == -1:
                    # Up
                    self.canvas.create_oval(
                        px + 6,
                        py + 6,
                        px + 10,
                        py + 10,
                        fill=eye_color,
                    )

                    self.canvas.create_oval(
                        px + 18,
                        py + 6,
                        px + 22,
                        py + 10,
                        fill=eye_color,
                    )

                else:
                    # Down
                    self.canvas.create_oval(
                        px + 6,
                        py + 18,
                        px + 10,
                        py + 22,
                        fill=eye_color,
                    )

                    self.canvas.create_oval(
                        px + 18,
                        py + 18,
                        px + 22,
                        py + 22,
                        fill=eye_color,
                    )

            # -----------------------------------------
            # BODY
            # -----------------------------------------

            else:

                self.canvas.create_rectangle(
                    px + 2,
                    py + 2,
                    px + CELL_SIZE - 2,
                    py + CELL_SIZE - 2,
                    fill=self.theme["snake_body"],
                    outline="",
                )

    # ---------------------------------------------------------
    # PAUSE OVERLAY
    # ---------------------------------------------------------

    def render_pause_overlay(self) -> None:
        """Displays the pause overlay."""

        cx = CANVAS_WIDTH // 2

        cy = (
            HEADER_HEIGHT
            + (CANVAS_HEIGHT - HEADER_HEIGHT) // 2
        )

        self.canvas.create_rectangle(
            cx - 180,
            cy - 80,
            cx + 180,
            cy + 80,
            fill=self.theme["panel_bg"],
            outline=self.theme["accent"],
            width=3,
        )

        self.canvas.create_text(
            cx,
            cy - 20,
            text="GAME PAUSED",
            fill=self.theme["accent"],
            font=("Helvetica", 22, "bold"),
        )

        self.canvas.create_text(
            cx,
            cy + 25,
            text="Press SPACE to Resume",
            fill=self.theme["subtext"],
            font=("Helvetica", 12),
        )

    # ---------------------------------------------------------
    # GAME OVER OVERLAY
    # ---------------------------------------------------------

    def render_game_over_overlay(self) -> None:
        """Displays the game-over screen."""

        cx = CANVAS_WIDTH // 2

        cy = (
            HEADER_HEIGHT
            + (CANVAS_HEIGHT - HEADER_HEIGHT) // 2
        )

        self.canvas.create_rectangle(
            cx - 200,
            cy - 140,
            cx + 200,
            cy + 140,
            fill=self.theme["panel_bg"],
            outline=self.theme["food_normal"],
            width=3,
        )

        # Title
        self.canvas.create_text(
            cx,
            cy - 90,
            text="GAME OVER",
            fill=self.theme["food_normal"],
            font=("Helvetica", 26, "bold"),
        )

        # Score
        self.canvas.create_text(
            cx,
            cy - 40,
            text=f"Final Score: {self.score}",
            fill=self.theme["text"],
            font=("Helvetica", 14, "bold"),
        )

        # High score
        self.canvas.create_text(
            cx,
            cy - 15,
            text=f"High Score: {self.high_score}",
            fill=self.theme["accent"],
            font=("Helvetica", 12),
        )

        # Level
        self.canvas.create_text(
            cx,
            cy + 10,
            text=f"Level Reached: {self.level}",
            fill=self.theme["subtext"],
            font=("Helvetica", 12),
        )

        # -------------------------------------------------
        # BUTTON FUNCTION
        # -------------------------------------------------

        def make_btn(
            x: int,
            y: int,
            w: int,
            h: int,
            text: str,
            command: Callable[[], None],
        ) -> None:

            rect = self.canvas.create_rectangle(
                x - w // 2,
                y - h // 2,
                x + w // 2,
                y + h // 2,
                fill=self.theme["button_bg"],
                outline=self.theme["accent"],
                width=2,
                tags="gameover_button",
            )

            txt = self.canvas.create_text(
                x,
                y,
                text=text,
                fill=self.theme["button_fg"],
                font=("Helvetica", 10, "bold"),
                tags="gameover_button",
            )

            def click_handler(event: tk.Event) -> None:
                command()

            self.canvas.tag_bind(
                rect,
                "<Button-1>",
                click_handler,
            )

            self.canvas.tag_bind(
                txt,
                "<Button-1>",
                click_handler,
            )

        # -------------------------------------------------
        # BUTTONS
        # -------------------------------------------------

        make_btn(
            cx - 90,
            cy + 80,
            120,
            35,
            "AGAIN",
            self.start,
        )

        make_btn(
            cx + 90,
            cy + 80,
            120,
            35,
            "MENU",
            self.return_menu_cb,
        )