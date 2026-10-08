"""
main.py - Main entry point for Python Snake Game desktop application.
"""

import sys
import tkinter as tk
from storage import StorageManager
from settings import CANVAS_WIDTH, CANVAS_HEIGHT
from menu import MenuManager
from game import GameEngine


class PythonSnakeApp:
    """Main Application Controller."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PYTHON SNAKE")
        self.root.geometry(f"{CANVAS_WIDTH}x{CANVAS_HEIGHT}")
        self.root.resizable(False, False)

        # Center Window on Screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_crd = (screen_width // 2) - (CANVAS_WIDTH // 2)
        y_crd = (screen_height // 2) - (CANVAS_HEIGHT // 2)
        self.root.geometry(f"{CANVAS_WIDTH}x{CANVAS_HEIGHT}+{x_crd}+{y_crd}")

        # Persistent Storage Data
        self.settings = StorageManager.load_settings()
        self.highscore = StorageManager.load_highscore()

        # Canvas Creation
        self.canvas = tk.Canvas(
            self.root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # Controllers
        self.menu_manager = MenuManager(
            self.canvas,
            callbacks={
                "start_game": self.start_game,
                "show_settings": self.show_settings,
                "show_how_to_play": self.show_how_to_play,
                "show_highscore": self.show_highscore,
                "show_main_menu": self.show_main_menu,
                "exit": self.quit_app
            },
            current_settings=self.settings
        )

        self.game_engine = None

        # Bind Global Keyboard Inputs
        self.root.bind("<Key>", self.handle_keypress)

        # Show initial menu
        self.show_main_menu()

    def show_main_menu(self) -> None:
        """Displays main menu."""
        if self.game_engine:
            self.game_engine.is_running = False
        self.menu_manager.show_main_menu()

    def start_game(self) -> None:
        """Initializes and runs gameplay engine."""
        self.game_engine = GameEngine(
            canvas=self.canvas,
            settings=self.settings,
            highscore=self.highscore,
            on_game_over=self.handle_game_over,
            return_menu_cb=self.show_main_menu
        )
        self.game_engine.start()

    def show_settings(self) -> None:
        """Displays settings configuration screen."""
        self.menu_manager.show_settings(
            save_callback=self.save_settings,
            reset_score_callback=self.reset_highscore
        )

    def show_how_to_play(self) -> None:
        """Displays instructions."""
        self.menu_manager.show_how_to_play()

    def show_highscore(self) -> None:
        """Displays high scores."""
        self.menu_manager.show_highscore(self.highscore)

    def handle_keypress(self, event: tk.Event) -> None:
        """Delegates input handling to active game loop if running."""
        if self.game_engine and self.game_engine.is_running:
            self.game_engine.handle_keypress(event)

    def save_settings(self) -> None:
        """Persists current settings to disk."""
        StorageManager.save_settings(self.settings)

    def reset_highscore(self) -> None:
        """Resets high score on disk and in-memory state."""
        StorageManager.reset_highscore()
        self.highscore = 0
        self.show_settings()

    def handle_game_over(self, final_score: int) -> None:
        """Checks and saves new high score on game over."""
        if final_score > self.highscore:
            self.highscore = final_score
            StorageManager.save_highscore(final_score)

    def quit_app(self) -> None:
        """Terminates desktop application."""
        self.root.destroy()
        sys.exit(0)

    def run(self) -> None:
        """Starts main Tkinter event loop."""
        self.root.mainloop()


if __name__ == "__main__":
    app = PythonSnakeApp()
    app.run()