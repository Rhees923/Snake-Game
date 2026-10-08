"""
snake.py - Snake entity logic and directional movement.
"""

from typing import List, Tuple

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    """Manages positions, direction state, growth, and collision handling."""

    def __init__(self, start_x: int, start_y: int, length: int = 3):
        self.direction = RIGHT
        self.next_direction = RIGHT

        self.body: List[Tuple[int, int]] = [
            (start_x - i, start_y) for i in range(length)
        ]

        self.grow_pending = 0

    def change_direction(self, new_dir: Tuple[int, int]) -> None:
        """Sets requested direction, preventing instant 180-degree turns."""

        current_dx, current_dy = self.direction
        new_dx, new_dy = new_dir

        # Prevent reversing directly into the snake's body
        if (current_dx + new_dx != 0) or (current_dy + new_dy != 0):
            self.next_direction = new_dir

    def move(self) -> Tuple[int, int]:
        """Advances the snake forward by one grid unit."""

        self.direction = self.next_direction

        head_x, head_y = self.body[0]
        dx, dy = self.direction

        new_head = (head_x + dx, head_y + dy)

        # Add new head
        self.body.insert(0, new_head)

        # Remove tail unless growth is pending
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

        return new_head

    def grow(self, amount: int = 1) -> None:
        """Schedules segment growth."""

        if amount > 0:
            self.grow_pending += amount

    def check_wall_collision(self, max_x: int, max_y: int) -> bool:
        """Checks if the snake's head moved outside the grid."""

        hx, hy = self.body[0]

        return (
            hx < 0
            or hx >= max_x
            or hy < 0
            or hy >= max_y
        )

    def check_self_collision(self) -> bool:
        """Checks if the head collided with the snake's body."""

        head = self.body[0]

        return head in self.body[1:]

    @property
    def head(self) -> Tuple[int, int]:
        """Returns the current head position."""

        return self.body[0]