````python
import streamlit as st
import streamlit.components.v1 as components

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PYTHON SNAKE",
    page_icon="🐍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at top, #182018 0%, #050505 45%, #000000 100%);
            color: white;
        }

        header {
            visibility: hidden;
        }

        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            max-width: 900px;
        }

        .title {
            text-align: center;
            font-size: 48px;
            font-weight: 900;
            letter-spacing: 4px;
            margin-bottom: 0;
        }

        .subtitle {
            text-align: center;
            color: #888;
            margin-bottom: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="title">🐍 PYTHON SNAKE</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">Classic Snake • Web Edition</div>',
    unsafe_allow_html=True,
)

# ============================================================
# SNAKE GAME
# ============================================================

game_html = r"""
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 0;
    background: transparent;
    font-family: Arial, Helvetica, sans-serif;
    color: white;
    overflow: hidden;
}

.game-wrapper {
    width: 100%;
    max-width: 650px;
    margin: auto;
    text-align: center;
}

.top-bar {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    margin-bottom: 12px;
}

.stat {
    flex: 1;
    background: #111;
    border: 1px solid #333;
    border-radius: 10px;
    padding: 10px;
}

.stat-title {
    font-size: 11px;
    color: #777;
}

.stat-value {
    font-size: 21px;
    font-weight: bold;
}

canvas {
    display: block;
    width: min(92vw, 600px);
    height: min(92vw, 600px);
    max-width: 600px;
    max-height: 600px;

    margin: auto;

    background: #080808;

    border: 3px solid #333;
    border-radius: 14px;

    box-shadow:
        0 0 30px rgba(0,0,0,.7),
        inset 0 0 30px rgba(0,0,0,.8);
}

.message {
    min-height: 30px;
    margin-top: 10px;
    font-size: 18px;
    font-weight: bold;
}

.buttons {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-top: 12px;
}

button {
    border: 1px solid #444;
    background: #151515;
    color: white;
    border-radius: 9px;
    padding: 10px 18px;
    font-size: 14px;
    font-weight: bold;
    cursor: pointer;
}

button:hover {
    background: #242424;
}

button:active {
    transform: scale(.96);
}

.controls {
    width: 180px;
    margin: 15px auto 0;

    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 7px;
}

.control {
    width: 55px;
    height: 45px;
    padding: 0;
    font-size: 20px;
}

.empty {
    visibility: hidden;
}

.help {
    margin-top: 12px;
    color: #777;
    font-size: 12px;
}

</style>

</head>

<body>

<div class="game-wrapper">

    <div class="top-bar">

        <div class="stat">
            <div class="stat-title">SCORE</div>
            <div class="stat-value" id="score">0</div>
        </div>

        <div class="stat">
            <div class="stat-title">HIGH SCORE</div>
            <div class="stat-value" id="highscore">0</div>
        </div>

        <div class="stat">
            <div class="stat-title">LEVEL</div>
            <div class="stat-value" id="level">1</div>
        </div>

    </div>

    <canvas id="game"></canvas>

    <div class="message" id="message">
        Press START
    </div>

    <div class="buttons">

        <button onclick="startGame()">
            ▶ START
        </button>

        <button onclick="togglePause()">
            ⏸ PAUSE
        </button>

        <button onclick="restartGame()">
            🔄 RESTART
        </button>

    </div>

    <div class="controls">

        <button class="control empty"></button>

        <button
            class="control"
            onclick="changeDirection(0,-1)"
        >
            ⬆
        </button>

        <button class="control empty"></button>

        <button
            class="control"
            onclick="changeDirection(-1,0)"
        >
            ⬅
        </button>

        <button
            class="control"
            onclick="changeDirection(0,1)"
        >
            ⬇
        </button>

        <button
            class="control"
            onclick="changeDirection(1,0)"
        >
            ➡
        </button>

    </div>

    <div class="help">
        Arrow Keys / WASD • SPACE = Pause
    </div>

</div>

<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const GRID = 25;

let cellSize = 24;

canvas.width = GRID * cellSize;
canvas.height = GRID * cellSize;

let snake;
let food;

let direction;
let nextDirection;

let score = 0;
let highScore = Number(localStorage.getItem("snakeHighScore") || 0);

let level = 1;

let running = false;
let paused = false;
let gameOver = false;

let timer = null;

document.getElementById("highscore").textContent = highScore;


// ============================================================
// INITIALIZE
// ============================================================

function initializeGame() {

    snake = [
        {x: 12, y: 12},
        {x: 11, y: 12},
        {x: 10, y: 12}
    ];

    direction = {
        x: 1,
        y: 0
    };

    nextDirection = {
        x: 1,
        y: 0
    };

    score = 0;
    level = 1;

    gameOver = false;
    paused = false;

    spawnFood();

    updateStats();

    draw();

    setMessage("Press START");

}


// ============================================================
// FOOD
// ============================================================

function spawnFood() {

    do {

        food = {
            x: Math.floor(Math.random() * GRID),
            y: Math.floor(Math.random() * GRID)
        };

    } while (
        snake.some(
            part =>
                part.x === food.x &&
                part.y === food.y
        )
    );
}


// ============================================================
// START
// ============================================================

function startGame() {

    if (running) return;

    if (gameOver) {
        initializeGame();
    }

    running = true;
    paused = false;

    setMessage("GO!");

    scheduleNextMove();
}


// ============================================================
// RESTART
// ============================================================

function restartGame() {

    stopGame();

    initializeGame();

    startGame();
}


// ============================================================
// STOP
// ============================================================

function stopGame() {

    running = false;

    if (timer) {
        clearTimeout(timer);
        timer = null;
    }
}


// ============================================================
// PAUSE
// ============================================================

function togglePause() {

    if (!running || gameOver) return;

    paused = !paused;

    if (paused) {

        if (timer) {
            clearTimeout(timer);
            timer = null;
        }

        setMessage("⏸ PAUSED");

    } else {

        setMessage("RESUMED");

        scheduleNextMove();
    }
}


// ============================================================
// DIRECTION
// ============================================================

function changeDirection(x, y) {

    if (!running || gameOver) return;

    if (
        x === -direction.x &&
        y === -direction.y
    ) {
        return;
    }

    nextDirection = {
        x: x,
        y: y
    };
}


// ============================================================
// KEYBOARD
// ============================================================

document.addEventListener(
    "keydown",
    function(event) {

        const key = event.key.toLowerCase();

        if (
            key === "arrowup" ||
            key === "w"
        ) {
            event.preventDefault();
            changeDirection(0, -1);
        }

        else if (
            key === "arrowdown" ||
            key === "s"
        ) {
            event.preventDefault();
            changeDirection(0, 1);
        }

        else if (
            key === "arrowleft" ||
            key === "a"
        ) {
            event.preventDefault();
            changeDirection(-1, 0);
        }

        else if (
            key === "arrowright" ||
            key === "d"
        ) {
            event.preventDefault();
            changeDirection(1, 0);
        }

        else if (key === " ") {

            event.preventDefault();

            togglePause();
        }

    }
);


// ============================================================
// GAME LOOP
// ============================================================

function scheduleNextMove() {

    if (!running || paused || gameOver) {
        return;
    }

    const speed = Math.max(
        55,
        170 - ((level - 1) * 10)
    );

    timer = setTimeout(
        function() {

            update();

            draw();

            scheduleNextMove();

        },
        speed
    );
}


// ============================================================
// UPDATE
// ============================================================

function update() {

    direction = nextDirection;

    const head = {
        x: snake[0].x + direction.x,
        y: snake[0].y + direction.y
    };


    // --------------------------------------------------------
    // WALL COLLISION
    // --------------------------------------------------------

    if (
        head.x < 0 ||
        head.x >= GRID ||
        head.y < 0 ||
        head.y >= GRID
    ) {

        endGame();

        return;
    }


    // --------------------------------------------------------
    // SELF COLLISION
    // --------------------------------------------------------

    if (
        snake.some(
            part =>
                part.x === head.x &&
                part.y === head.y
        )
    ) {

        endGame();

        return;
    }


    snake.unshift(head);


    // --------------------------------------------------------
    // FOOD
    // --------------------------------------------------------

    if (
        head.x === food.x &&
        head.y === food.y
    ) {

        score++;

        level = Math.floor(score / 5) + 1;

        if (score > highScore) {

            highScore = score;

            localStorage.setItem(
                "snakeHighScore",
                highScore
            );
        }

        spawnFood();

        updateStats();

    } else {

        snake.pop();
    }
}


// ============================================================
// GAME OVER
// ============================================================

function endGame() {

    running = false;
    gameOver = true;

    if (timer) {
        clearTimeout(timer);
        timer = null;
    }

    setMessage(
        "💀 GAME OVER — Score: " + score
    );

    draw();
}


// ============================================================
// STATS
// ============================================================

function updateStats() {

    document.getElementById("score")
        .textContent = score;

    document.getElementById("highscore")
        .textContent = highScore;

    document.getElementById("level")
        .textContent = level;
}


// ============================================================
// MESSAGE
// ============================================================

function setMessage(text) {

    document.getElementById("message")
        .textContent = text;
}


// ============================================================
// DRAW
// ============================================================

function draw() {

    ctx.fillStyle = "#080808";

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    // --------------------------------------------------------
    // GRID
    // --------------------------------------------------------

    ctx.strokeStyle = "#151515";
    ctx.lineWidth = 1;

    for (
        let x = 0;
        x <= canvas.width;
        x += cellSize
    ) {

        ctx.beginPath();

        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);

        ctx.stroke();
    }

    for (
        let y = 0;
        y <= canvas.height;
        y += cellSize
    ) {

        ctx.beginPath();

        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);

        ctx.stroke();
    }


    // --------------------------------------------------------
    // FOOD
    // --------------------------------------------------------

    if (food) {

        const fx =
            food.x * cellSize +
            cellSize / 2;

        const fy =
            food.y * cellSize +
            cellSize / 2;

        ctx.beginPath();

        ctx.arc(
            fx,
            fy,
            cellSize * 0.32,
            0,
            Math.PI * 2
        );

        ctx.fillStyle = "#ff3b30";

        ctx.fill();

        ctx.strokeStyle = "#ffffff";

        ctx.stroke();
    }


    // --------------------------------------------------------
    // SNAKE
    // --------------------------------------------------------

    snake.forEach(
        function(part, index) {

            const padding =
                index === 0 ? 1 : 3;

            const x =
                part.x * cellSize +
                padding;

            const y =
                part.y * cellSize +
                padding;

            const size =
                cellSize -
                padding * 2;


            ctx.fillStyle =
                index === 0
                    ? "#39ff14"
                    : "#16a800";


            ctx.fillRect(
                x,
                y,
                size,
                size
            );


            if (index === 0) {

                drawEyes(
                    part.x,
                    part.y
                );
            }
        }
    );
}


// ============================================================
// EYES
// ============================================================

function drawEyes(x, y) {

    ctx.fillStyle = "#000000";

    const baseX =
        x * cellSize;

    const baseY =
        y * cellSize;


    let eyes = [];


    if (direction.x > 0) {

        eyes = [
            [baseX + 17, baseY + 6],
            [baseX + 17, baseY + 18]
        ];

    }

    else if (direction.x < 0) {

        eyes = [
            [baseX + 6, baseY + 6],
            [baseX + 6, baseY + 18]
        ];

    }

    else if (direction.y < 0) {

        eyes = [
            [baseX + 6, baseY + 6],
            [baseX + 18, baseY + 6]
        ];

    }

    else {

        eyes = [
            [baseX + 6, baseY + 18],
            [baseX + 18, baseY + 18]
        ];
    }


    eyes.forEach(
        function(eye) {

            ctx.beginPath();

            ctx.arc(
                eye[0],
                eye[1],
                2.5,
                0,
                Math.PI * 2
            );

            ctx.fill();
        }
    );
}


// ============================================================
// INITIAL DRAW
// ============================================================

initializeGame();

</script>

</body>
</html>
"""

# ============================================================
# RENDER GAME
# ============================================================

components.html(
    game_html,
    height=850,
    scrolling=False,
)
"""

### 2. `requirements.txt`

GitHub-ൽ **new file** ഉണ്ടാക്കി:

:::writing{variant="document" id="31684" title="requirements.txt"}
```txt
streamlit
````
