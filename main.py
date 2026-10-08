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
# STREAMLIT CSS
# ============================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&display=swap');

    * {
        font-family: 'Orbitron', sans-serif;
    }

    .stApp {
        min-height: 100vh;

        background:
            radial-gradient(
                circle at 50% -10%,
                rgba(0,255,90,.16),
                transparent 35%
            ),
            radial-gradient(
                circle at 10% 90%,
                rgba(0,200,255,.08),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 70%,
                rgba(140,0,255,.08),
                transparent 30%
            ),
            #020402;

        color: white;
    }

    header {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    .block-container {
        max-width: 1000px !important;
        padding-top: 18px !important;
        padding-bottom: 10px !important;
    }

    .snake-title {
        text-align: center;

        font-size: clamp(35px, 7vw, 65px);

        font-weight: 900;

        letter-spacing: 8px;

        margin: 0;

        background:
            linear-gradient(
                90deg,
                #39ff14,
                #00ff88,
                #00eaff,
                #39ff14
            );

        background-size: 300% auto;

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        animation: titleGlow 5s linear infinite;

        filter:
            drop-shadow(0 0 10px rgba(57,255,20,.4))
            drop-shadow(0 0 30px rgba(0,255,150,.15));
    }

    @keyframes titleGlow {

        0% {
            background-position: 0% center;
        }

        100% {
            background-position: 300% center;
        }

    }

    .snake-subtitle {
        text-align: center;

        color: #6f8075;

        font-size: 12px;

        letter-spacing: 5px;

        margin-top: -5px;

        margin-bottom: 18px;
    }

    .online-badge {
        width: fit-content;

        margin: 0 auto 14px auto;

        padding: 6px 14px;

        border-radius: 100px;

        border: 1px solid rgba(57,255,20,.3);

        background: rgba(57,255,20,.05);

        color: #62ff3e;

        font-size: 10px;

        letter-spacing: 2px;

        box-shadow:
            0 0 20px rgba(57,255,20,.08);
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="online-badge">● ONLINE WEB EDITION</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="snake-title">🐍 PYTHON SNAKE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="snake-subtitle">CLASSIC ARCADE • NEON EDITION</div>',
    unsafe_allow_html=True
)

# ============================================================
# GAME HTML
# ============================================================

game_html = r"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<style>

* {
    box-sizing: border-box;
}

html,
body {

    margin: 0;
    padding: 0;

    width: 100%;

    background: transparent;

    color: white;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    overflow: hidden;
}

.game {

    width: 100%;

    max-width: 680px;

    margin: auto;

    padding: 5px;

}


/* ============================================================
   HUD
============================================================ */

.hud {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 9px;

    margin-bottom: 12px;
}

.card {

    position: relative;

    overflow: hidden;

    background:
        linear-gradient(
            145deg,
            rgba(25,35,28,.95),
            rgba(5,9,6,.96)
        );

    border:
        1px solid
        rgba(255,255,255,.09);

    border-radius: 14px;

    padding: 11px;

    text-align: center;

    box-shadow:
        0 8px 30px rgba(0,0,0,.4),
        inset 0 1px 0
        rgba(255,255,255,.04);

    backdrop-filter: blur(12px);
}

.card::after {

    content: "";

    position: absolute;

    left: 15%;

    right: 15%;

    bottom: 0;

    height: 1px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #39ff14,
            transparent
        );

    opacity: .5;
}

.card-label {

    color: #617064;

    font-size: 9px;

    font-weight: 700;

    letter-spacing: 2px;

    margin-bottom: 5px;
}

.card-value {

    font-size: 22px;

    font-weight: 900;

    color: #eaffea;

    text-shadow:
        0 0 12px
        rgba(57,255,20,.25);
}


/* ============================================================
   LEVEL SELECTOR
============================================================ */

.level-selector {

    display: flex;

    justify-content: center;

    align-items: center;

    gap: 10px;

    flex-wrap: wrap;

    margin: 0 auto 12px;

    color: #68766c;

    font-size: 10px;

    font-weight: bold;

    letter-spacing: 1px;
}

.level-selector select {

    background:
        linear-gradient(
            145deg,
            #151b16,
            #080c09
        );

    color: #7dff63;

    border:
        1px solid
        rgba(57,255,20,.3);

    border-radius: 10px;

    padding: 9px 12px;

    font-size: 10px;

    font-weight: bold;

    outline: none;

    cursor: pointer;

    box-shadow:
        0 0 15px
        rgba(57,255,20,.04);
}

.level-selector select:hover {

    border-color:
        #39ff14;

    box-shadow:
        0 0 18px
        rgba(57,255,20,.15);
}

.level-selector option {

    background: #080c09;

    color: white;
}


/* ============================================================
   GAME BOARD
============================================================ */

.board-wrap {

    position: relative;

    width: min(92vw, 620px);

    aspect-ratio: 1 / 1;

    margin: auto;

    padding: 5px;

    border-radius: 20px;

    background:
        linear-gradient(
            135deg,
            #26332a,
            #071008,
            #1b2b20
        );

    box-shadow:

        0 0 0 1px
        rgba(255,255,255,.04),

        0 20px 70px
        rgba(0,0,0,.75),

        0 0 45px
        rgba(57,255,20,.07);
}

canvas {

    display: block;

    width: 100%;
    height: 100%;

    border-radius: 16px;

    background:
        radial-gradient(
            circle at center,
            #0b120d,
            #020502
        );
}


/* ============================================================
   OVERLAY
============================================================ */

.overlay {

    position: absolute;

    inset: 5px;

    display: flex;

    align-items: center;

    justify-content: center;

    flex-direction: column;

    border-radius: 16px;

    background:
        rgba(0,0,0,.55);

    backdrop-filter: blur(5px);

    transition: .25s;

    pointer-events: none;
}

.overlay.hidden {

    opacity: 0;

    visibility: hidden;
}

.overlay-title {

    font-size:
        clamp(26px, 7vw, 46px);

    font-weight: 900;

    letter-spacing: 4px;

    color: #fff;

    text-shadow:
        0 0 15px
        rgba(57,255,20,.6);
}

.overlay-text {

    margin-top: 7px;

    color: #7c8b80;

    font-size: 11px;

    letter-spacing: 2px;
}


/* ============================================================
   MESSAGE
============================================================ */

.message {

    min-height: 25px;

    text-align: center;

    margin-top: 10px;

    font-size: 12px;

    font-weight: 700;

    letter-spacing: 1px;

    color: #6f8075;
}


/* ============================================================
   BUTTONS
============================================================ */

.actions {

    display: flex;

    justify-content: center;

    gap: 8px;

    margin-top: 7px;

    flex-wrap: wrap;
}

button {

    border:
        1px solid
        rgba(255,255,255,.1);

    background:
        linear-gradient(
            145deg,
            #151b16,
            #080c09
        );

    color: #dce9df;

    border-radius: 10px;

    padding: 10px 17px;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: .5px;

    cursor: pointer;

    transition:
        transform .15s,
        border .15s,
        box-shadow .15s,
        background .15s;
}

button:hover {

    border-color:
        rgba(57,255,20,.45);

    box-shadow:
        0 0 20px
        rgba(57,255,20,.12);

    background:
        linear-gradient(
            145deg,
            #1b291d,
            #091009
        );
}

button:active {

    transform:
        scale(.94);
}

.primary {

    border-color:
        rgba(57,255,20,.4);

    color: #5cff3b;

    box-shadow:
        0 0 20px
        rgba(57,255,20,.07);
}


/* ============================================================
   MOBILE CONTROLS
============================================================ */

.controls {

    width: 185px;

    margin:
        13px auto 0;

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 6px;
}

.control {

    width: 57px;

    height: 43px;

    padding: 0;

    font-size: 18px;

    border-radius: 11px;

    color: #8dff77;
}

.empty {

    visibility: hidden;
}


/* ============================================================
   HELP
============================================================ */

.help {

    text-align: center;

    margin-top: 10px;

    color: #4d5c51;

    font-size: 9px;

    letter-spacing: 1px;
}


/* ============================================================
   FOOTER
============================================================ */

.footer {

    text-align: center;

    margin-top: 13px;

    color: #29342d;

    font-size: 8px;

    letter-spacing: 3px;
}


/* ============================================================
   MOBILE
============================================================ */

@media(max-width: 500px) {

    .hud {
        gap: 5px;
    }

    .card {
        padding: 8px 4px;
    }

    .card-value {
        font-size: 18px;
    }

    .card-label {
        font-size: 7px;
    }

    .actions button {
        padding: 9px 12px;
    }

}

</style>

</head>

<body>

<div class="game">


    <!-- =====================================================
         HUD
    ====================================================== -->

    <div class="hud">

        <div class="card">

            <div class="card-label">
                SCORE
            </div>

            <div
                class="card-value"
                id="score">
                0
            </div>

        </div>


        <div class="card">

            <div class="card-label">
                HIGH SCORE
            </div>

            <div
                class="card-value"
                id="highscore">
                0
            </div>

        </div>


        <div class="card">

            <div class="card-label">
                LEVEL
            </div>

            <div
                class="card-value"
                id="level">
                1
            </div>

        </div>

    </div>


    <!-- =====================================================
         LEVEL SELECTOR
    ====================================================== -->

    <div class="level-selector">

        <span>
            🎯 SELECT LEVEL
        </span>

        <select
            id="levelSelect"
            onchange="changeLevel(this.value)"
        >

            <option value="1">
                🟢 LEVEL 1 — EASY
            </option>

            <option value="2">
                🟡 LEVEL 2 — NORMAL
            </option>

            <option value="3">
                🟠 LEVEL 3 — HARD
            </option>

            <option value="4">
                🔴 LEVEL 4 — EXTREME
            </option>

            <option value="5">
                💀 LEVEL 5 — INSANE
            </option>

        </select>

    </div>


    <!-- =====================================================
         BOARD
    ====================================================== -->

    <div class="board-wrap">

        <canvas id="game"></canvas>


        <div
            class="overlay"
            id="overlay">

            <div
                class="overlay-title"
                id="overlayTitle">

                🐍 SNAKE

            </div>

            <div
                class="overlay-text"
                id="overlayText">

                PRESS START TO PLAY

            </div>

        </div>

    </div>


    <!-- =====================================================
         MESSAGE
    ====================================================== -->

    <div
        class="message"
        id="message">

        Ready?

    </div>


    <!-- =====================================================
         ACTION BUTTONS
    ====================================================== -->

    <div class="actions">

        <button
            class="primary"
            onclick="startGame()">

            ▶ START

        </button>


        <button
            onclick="togglePause()">

            ⏸ PAUSE

        </button>


        <button
            onclick="restartGame()">

            ↻ RESTART

        </button>

    </div>


    <!-- =====================================================
         MOBILE CONTROLS
    ====================================================== -->

    <div class="controls">

        <button
            class="control empty">
        </button>


        <button
            class="control"
            onclick="changeDirection(0,-1)">

            ▲

        </button>


        <button
            class="control empty">
        </button>


        <button
            class="control"
            onclick="changeDirection(-1,0)">

            ◀

        </button>


        <button
            class="control"
            onclick="changeDirection(0,1)">

            ▼

        </button>


        <button
            class="control"
            onclick="changeDirection(1,0)">

            ▶

        </button>

    </div>


    <div class="help">

        ARROW KEYS / WASD
        •
        SPACE = PAUSE

    </div>


    <div class="footer">

        PYTHON SNAKE • WEB ARCADE

    </div>

</div>


<script>

/* ============================================================
   CANVAS
============================================================ */

const canvas =
    document.getElementById("game");

const ctx =
    canvas.getContext("2d");


const GRID = 25;

const cellSize = 24;

canvas.width =
    GRID * cellSize;

canvas.height =
    GRID * cellSize;


/* ============================================================
   VARIABLES
============================================================ */

let snake;

let food;

let direction;

let nextDirection;

let score = 0;

let highScore =
    Number(
        localStorage.getItem(
            "pythonSnakeHighScore"
        ) || 0
    );

let selectedLevel = 1;

let level = 1;

let running = false;

let paused = false;

let gameOver = false;

let timer = null;

let foodPulse = 0;


/* ============================================================
   ELEMENTS
============================================================ */

const scoreEl =
    document.getElementById("score");

const highScoreEl =
    document.getElementById("highscore");

const levelEl =
    document.getElementById("level");

const messageEl =
    document.getElementById("message");

const overlay =
    document.getElementById("overlay");

const overlayTitle =
    document.getElementById("overlayTitle");

const overlayText =
    document.getElementById("overlayText");

const levelSelect =
    document.getElementById("levelSelect");


highScoreEl.textContent =
    highScore;


/* ============================================================
   LEVEL CHANGE
============================================================ */

function changeLevel(value) {

    if (running) {

        setMessage(
            "⏸ STOP / RESTART GAME TO CHANGE LEVEL"
        );

        levelSelect.value =
            selectedLevel;

        return;
    }


    selectedLevel =
        Number(value);

    level =
        selectedLevel;


    updateStats();


    const names = {

        1: "🟢 EASY",

        2: "🟡 NORMAL",

        3: "🟠 HARD",

        4: "🔴 EXTREME",

        5: "💀 INSANE"

    };


    setMessage(
        "Selected: " +
        names[selectedLevel]
    );
}


/* ============================================================
   INITIALIZE
============================================================ */

function initializeGame() {

    snake = [

        {x: 12, y: 12},

        {x: 11, y: 12},

        {x: 10, y: 12},

        {x: 9, y: 12}

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

    level =
        selectedLevel;

    running = false;

    paused = false;

    gameOver = false;


    spawnFood();

    updateStats();

    draw();


    showOverlay(
        "🐍 SNAKE",
        "LEVEL " +
        selectedLevel +
        " • PRESS START"
    );


    setMessage(
        "Ready for the challenge?"
    );
}


/* ============================================================
   FOOD
============================================================ */

function spawnFood() {

    do {

        food = {

            x:
                Math.floor(
                    Math.random() * GRID
                ),

            y:
                Math.floor(
                    Math.random() * GRID
                )
        };

    }

    while (

        snake.some(
            part =>
                part.x === food.x &&
                part.y === food.y
        )

    );
}


/* ============================================================
   START
============================================================ */

function startGame() {

    if (running)
        return;


    if (gameOver) {

        initializeGame();

    }


    running = true;

    paused = false;

    hideOverlay();

    setMessage(
        "🔥 LEVEL " +
        selectedLevel +
        " STARTED"
    );

    scheduleNextMove();
}


/* ============================================================
   RESTART
============================================================ */

function restartGame() {

    stopGame();

    initializeGame();

    startGame();
}


/* ============================================================
   STOP
============================================================ */

function stopGame() {

    running = false;


    if (timer) {

        clearTimeout(timer);

        timer = null;
    }
}


/* ============================================================
   PAUSE
============================================================ */

function togglePause() {

    if (!running || gameOver)
        return;


    paused =
        !paused;


    if (paused) {

        if (timer) {

            clearTimeout(timer);

            timer = null;
        }


        showOverlay(
            "⏸ PAUSED",
            "PRESS SPACE TO CONTINUE"
        );


        setMessage(
            "Game paused"
        );

    }

    else {

        hideOverlay();

        setMessage(
            "▶ RESUMED"
        );

        scheduleNextMove();
    }
}


/* ============================================================
   DIRECTION
============================================================ */

function changeDirection(x,y) {

    if (!running || gameOver)
        return;


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


/* ============================================================
   KEYBOARD
============================================================ */

document.addEventListener(
    "keydown",
    function(event) {

        const key =
            event.key.toLowerCase();


        if (
            key === "arrowup" ||
            key === "w"
        ) {

            event.preventDefault();

            changeDirection(
                0,
                -1
            );
        }


        else if (
            key === "arrowdown" ||
            key === "s"
        ) {

            event.preventDefault();

            changeDirection(
                0,
                1
            );
        }


        else if (
            key === "arrowleft" ||
            key === "a"
        ) {

            event.preventDefault();

            changeDirection(
                -1,
                0
            );
        }


        else if (
            key === "arrowright" ||
            key === "d"
        ) {

            event.preventDefault();

            changeDirection(
                1,
                0
            );
        }


        else if (
            key === " "
        ) {

            event.preventDefault();

            togglePause();
        }

    }
);


/* ============================================================
   GAME LOOP
============================================================ */

function scheduleNextMove() {

    if (
        !running ||
        paused ||
        gameOver
    ) {

        return;
    }


    const speeds = {

        1: 180,

        2: 130,

        3: 90,

        4: 65,

        5: 45

    };


    const speed =
        speeds[selectedLevel];


    timer =
        setTimeout(
            function() {

                update();

                draw();

                scheduleNextMove();

            },
            speed
        );
}


/* ============================================================
   UPDATE
============================================================ */

function update() {

    direction =
        nextDirection;


    const head = {

        x:
            snake[0].x +
            direction.x,

        y:
            snake[0].y +
            direction.y

    };


    /* WALL COLLISION */

    if (

        head.x < 0 ||

        head.x >= GRID ||

        head.y < 0 ||

        head.y >= GRID

    ) {

        endGame();

        return;
    }


    /* SELF COLLISION */

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


    /* FOOD */

    if (

        head.x === food.x &&

        head.y === food.y

    ) {

        score++;


        if (score > highScore) {

            highScore =
                score;


            localStorage.setItem(
                "pythonSnakeHighScore",
                highScore
            );
        }


        spawnFood();

        updateStats();


        setMessage(
            "🍎 FOOD +1 • LEVEL " +
            selectedLevel
        );

    }

    else {

        snake.pop();
    }
}


/* ============================================================
   GAME OVER
============================================================ */

function endGame() {

    running = false;

    gameOver = true;


    if (timer) {

        clearTimeout(timer);

        timer = null;
    }


    showOverlay(
        "💀 GAME OVER",
        "SCORE: " +
        score +
        " • LEVEL: " +
        selectedLevel
    );


    setMessage(
        "Press RESTART to try again"
    );


    draw();
}


/* ============================================================
   STATS
============================================================ */

function updateStats() {

    scoreEl.textContent =
        score;

    highScoreEl.textContent =
        highScore;

    levelEl.textContent =
        selectedLevel;
}


/* ============================================================
   MESSAGE
============================================================ */

function setMessage(text) {

    messageEl.textContent =
        text;
}


/* ============================================================
   OVERLAY
============================================================ */

function showOverlay(
    title,
    text
) {

    overlayTitle.textContent =
        title;

    overlayText.textContent =
        text;

    overlay.classList.remove(
        "hidden"
    );
}


function hideOverlay() {

    overlay.classList.add(
        "hidden"
    );
}


/* ============================================================
   DRAW
============================================================ */

function draw() {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    /* BACKGROUND */

    const gradient =
        ctx.createRadialGradient(
            canvas.width / 2,
            canvas.height / 2,
            10,
            canvas.width / 2,
            canvas.height / 2,
            canvas.width
        );


    gradient.addColorStop(
        0,
        "#0d180f"
    );


    gradient.addColorStop(
        1,
        "#020402"
    );


    ctx.fillStyle =
        gradient;


    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    /* GRID */

    ctx.strokeStyle =
        "rgba(80,120,85,.10)";

    ctx.lineWidth = 1;


    for (
        let x = 0;
        x <= canvas.width;
        x += cellSize
    ) {

        ctx.beginPath();

        ctx.moveTo(x,0);

        ctx.lineTo(
            x,
            canvas.height
        );

        ctx.stroke();
    }


    for (
        let y = 0;
        y <= canvas.height;
        y += cellSize
    ) {

        ctx.beginPath();

        ctx.moveTo(0,y);

        ctx.lineTo(
            canvas.width,
            y
        );

        ctx.stroke();
    }


    drawFood();

    drawSnake();
}


/* ============================================================
   FOOD DRAW
============================================================ */

function drawFood() {

    if (!food)
        return;


    foodPulse += .08;


    const fx =
        food.x * cellSize +
        cellSize / 2;


    const fy =
        food.y * cellSize +
        cellSize / 2;


    const pulse =
        Math.sin(foodPulse) * 2;


    ctx.shadowColor =
        "#ff3b30";


    ctx.shadowBlur =
        18 + pulse;


    ctx.beginPath();


    ctx.arc(
        fx,
        fy,
        cellSize * .27 +
        pulse * .1,
        0,
        Math.PI * 2
    );


    ctx.fillStyle =
        "#ff3b30";


    ctx.fill();


    ctx.shadowBlur = 0;


    /* FOOD HIGHLIGHT */

    ctx.beginPath();


    ctx.arc(
        fx - 3,
        fy - 3,
        2,
        0,
        Math.PI * 2
    );


    ctx.fillStyle =
        "#ffffff";


    ctx.fill();
}


/* ============================================================
   SNAKE DRAW
============================================================ */

function drawSnake() {

    snake.forEach(
        function(part,index) {

            const padding =
                index === 0
                    ? 1.5
                    : 2.5;


            const x =
                part.x * cellSize +
                padding;


            const y =
                part.y * cellSize +
                padding;


            const size =
                cellSize -
                padding * 2;


            if (index === 0) {

                ctx.shadowColor =
                    "#39ff14";

                ctx.shadowBlur =
                    15;
            }


            const gradient =
                ctx.createLinearGradient(
                    x,
                    y,
                    x + size,
                    y + size
                );


            if (index === 0) {

                gradient.addColorStop(
                    0,
                    "#b8ff9e"
                );

                gradient.addColorStop(
                    .35,
                    "#39ff14"
                );

                gradient.addColorStop(
                    1,
                    "#0fb800"
                );

            }

            else {

                gradient.addColorStop(
                    0,
                    "#43ef25"
                );

                gradient.addColorStop(
                    1,
                    "#087d00"
                );
            }


            ctx.fillStyle =
                gradient;


            ctx.beginPath();


            ctx.roundRect(
                x,
                y,
                size,
                size,
                index === 0
                    ? 6
                    : 4
            );


            ctx.fill();


            ctx.shadowBlur = 0;


            if (index === 0) {

                drawEyes(
                    part.x,
                    part.y
                );
            }

        }
    );
}


/* ============================================================
   EYES
============================================================ */

function drawEyes(x,y) {

    ctx.fillStyle =
        "#021000";


    const baseX =
        x * cellSize;


    const baseY =
        y * cellSize;


    let eyes;


    if (direction.x > 0) {

        eyes = [

            [baseX+17,baseY+7],

            [baseX+17,baseY+17]

        ];

    }

    else if (direction.x < 0) {

        eyes = [

            [baseX+7,baseY+7],

            [baseX+7,baseY+17]

        ];

    }

    else if (direction.y < 0) {

        eyes = [

            [baseX+7,baseY+7],

            [baseX+17,baseY+7]

        ];

    }

    else {

        eyes = [

            [baseX+7,baseY+17],

            [baseX+17,baseY+17]

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


/* ============================================================
   INITIAL START
============================================================ */

initializeGame();


/* ============================================================
   IDLE ANIMATION
============================================================ */

function animationLoop() {

    if (!running) {

        draw();
    }

    requestAnimationFrame(
        animationLoop
    );
}


animationLoop();

</script>

</body>

</html>
"""

# ============================================================
# RENDER GAME
# ============================================================

components.html(
    game_html,
    height=930,
    scrolling=False,
)

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#344138;
        font-size:10px;
        letter-spacing:2px;
        margin-top:5px;
    ">
        BUILT WITH PYTHON + STREAMLIT 🐍
    </div>
    """,
    unsafe_allow_html=True,
)
