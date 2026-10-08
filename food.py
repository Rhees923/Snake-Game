"""
food.py - Food entity with multiple rarity types and pulse animation logic.
"""

import random
from typing import Tuple, List

FOOD_TYPES = [
    ("normal", 10, 0.70),  # 70% chance: +10 pts
    ("bonus", 25, 0.20),   # 20% chance: +25 pts
    ("rare", 50, 0.10)     # 10% chance: +50 pts
]


class Food:
    """Manages food items spawned on grid coordinates."""

    def __init__(self, grid_width: int, grid_height: int):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position: Tuple[int, int] = (0, 0)
        self.type = "normal"
        self.points = 10
        self.pulse_phase = 0.0

    def spawn(self, snake_body: List[Tuple[int, int]]) -> None:
        """Spawns food at a random coordinate not occupied by the snake."""
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if (x, y) not in snake_body:
                self.position = (x, y)
                break

        # Select type based on probabilities
        rand_val = random.random()
        cumulative = 0.0
        for ftype, pts, prob in FOOD_TYPES:
            cumulative += prob
            if rand_val <= cumulative:
                self.type = ftype
                self.points = pts
                break

    def update_pulse(self) -> float:
        """Updates animation pulse phase, cycling between 0.0 and 1.0."""
        self.pulse_phase = (self.pulse_phase + 0.15) % (2 * 3.14159)
        return self.pulse_phase