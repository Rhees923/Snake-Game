```python
"""
main.py - Streamlit Web Version of Python Snake Game
"""

import streamlit as st
import random
import time

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="PYTHON SNAKE",
    page_icon="🐍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background: #050505;
        color: white;
    }

    .snake-title {
        text-align: center;
        font-size: 48px;
        font-weight: 900;
        margin-bottom: 5px;
    }

    .snake-subtitle {
        text-align: center;
        color: #888;
        margin-bottom: 25px;
    }

    .score-box {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        padding: 10px;
        border-radius: 12px;
        background: #111;
        border: 1px solid #333;
        margin-bottom: 20px;
    }

    .game-over {
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        margin: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# CONSTANTS
# --------------------------------------------------

BOARD_SIZE = 15

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "snake" not in st.session_state:
    st.session_state.snake = [(7, 7), (6, 7), (5, 7)]

if "direction" not in st.session_state:
    st.session_state.direction = (1, 0)

if "food" not in st.session_state:
    st.session_state.food = (10, 10)

if "score" not in st.session_state:
    st.session_state.score = 0

if "highscore" not in st.session_state:
    st.session_state.highscore = 0

if "game_running" not in st.session_state:
    st.session_state.game_running = False

if "game_over" not in st.session_state:
    st.session_state.game_over = False


# --------------------------------------------------
# FUNCTIONS
# --------------------------------------------------

def create_food():
    """Create food at a free position."""

    while True:
        position = (
            random.randint(0, BOARD_SIZE - 1),
            random.randint(0, BOARD_SIZE - 1)
        )

        if position not in st.session_state.snake:
            return position


def start_game():
    """Start a new game."""

    st.session_state.snake = [
        (7, 7),
        (6, 7),
        (5, 7)
    ]

    st.session_state.direction = (1, 0)
    st.session_state.food = create_food()
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.game_running = True


def change_direction(direction):
    """Change snake direction."""

    current = st.session_state.direction

    # Prevent direct reverse movement
    if (
        direction[0] == -current[0]
        and direction[1] == -current[1]
    ):
        return

    st.session_state.direction = direction


def move_snake():
    """Move the snake one step."""

    snake = st.session_state.snake
    direction = st.session_state.direction

    head_x, head_y = snake[0]

    new_head = (
        head_x + direction[0],
        head_y + direction[1]
    )

    # Wall collision
    if (
        new_head[0] < 0
        or new_head[0] >= BOARD_SIZE
        or new_head[1] < 0
        or new_head[1] >= BOARD_SIZE
    ):
        end_game()
        return

    # Body collision
    if new_head in snake:
        end_game()
        return

    snake.insert(0, new_head)

    # Food collision
    if new_head == st.session_state.food:

        st.session_state.score += 1

        if st.session_state.score > st.session_state.highscore:
            st.session_state.highscore = st.session_state.score

        st.session_state.food = create_food()

    else:
        snake.pop()


def end_game():
    """End the current game."""

    st.session_state.game_running = False
    st.session_state.game_over = True


def draw_board():
    """Draw the Snake game board using HTML."""

    snake = st.session_state.snake
    food = st.session_state.food

    html = """
    <div style="
        width: 360px;
        height: 360px;
        margin: auto;
        display: grid;
        grid-template-columns: repeat(15, 1fr);
        grid-template-rows: repeat(15, 1fr);
        background: #111;
        border: 4px solid #333;
        border-radius: 12px;
        overflow: hidden;
    ">
    """

    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):

            position = (x, y)

            if position == food:

                cell = """
                <div style="
                    background:#111;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:17px;
                ">🍎</div>
                """

            elif position in snake:

                if position == snake[0]:
                    cell = """
                    <div style="
                        background:#39ff14;
                        border-radius:6px;
                    "></div>
                    """
                else:
                    cell = """
                    <div style="
                        background:#18b800;
                        border-radius:4px;
                    "></div>
                    """

            else:

                cell = """
                <div style="
                    background:#0a0a0a;
                    border:1px solid #151515;
                "></div>
                """

            html += cell

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)


# --------------------------------------------------
# UI
# --------------------------------------------------

st.markdown(
    '<div class="snake-title">🐍 PYTHON SNAKE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="snake-subtitle">Classic Snake Game • Web Edition</div>',
    unsafe_allow_html=True
)

# Score

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f'<div class="score-box">SCORE<br>{st.session_state.score}</div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f'<div class="score-box">BEST<br>{st.session_state.highscore}</div>',
        unsafe_allow_html=True
    )

# Board

draw_board()

st.write("")

# --------------------------------------------------
# CONTROLS
# --------------------------------------------------

if not st.session_state.game_running:

    if st.session_state.game_over:

        st.markdown(
            '<div class="game-over">💀 GAME OVER</div>',
            unsafe_allow_html=True
        )

    if st.button(
        "🎮 START GAME",
        use_container_width=True
    ):
        start_game()
        st.rerun()

else:

    st.markdown("### 🎮 Controls")

    col1, col2, col3 = st.columns(3)

    with col2:
        if st.button("⬆️", use_container_width=True):
            change_direction((0, -1))
            move_snake()
            st.rerun()

    with col1:
        if st.button("⬅️", use_container_width=True):
            change_direction((-1, 0))
            move_snake()
            st.rerun()

    with col2:
        if st.button("⬇️", use_container_width=True):
            change_direction((0, 1))
            move_snake()
            st.rerun()

    with col3:
        if st.button("➡️", use_container_width=True):
            change_direction((1, 0))
            move_snake()
            st.rerun()

    st.write("")

    if st.button(
        "⏹️ STOP GAME",
        use_container_width=True
    ):
        st.session_state.game_running = False
        st.rerun()

# --------------------------------------------------
# AUTO REFRESH
# --------------------------------------------------

if st.session_state.game_running:

    time.sleep(0.15)

    move_snake()

    st.rerun()
```
