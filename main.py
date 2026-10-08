"""
============================================================
🐍 PYTHON SNAKE - ULTIMATE WEB EDITION
============================================================

Merged from:
- storage.py
- snake.py
- settings.py
- menu.py
- game.py
- food.py
- Streamlit Web Edition
- README feature specification

IMPORTANT:
This version does NOT use tkinter.
It is designed for Streamlit Cloud / web browsers.

Features:
- Beautiful Neon UI
- Level 1-5 selection
- Easy / Normal / Hard / Extreme / Insane
- Dynamic speed
- Normal / Bonus / Rare food
- +10 / +25 / +50 points
- High score using browser localStorage
- Dark / Light / Neon themes
- Grid ON / OFF
- Sound ON / OFF
- Pause / Resume
- Restart
- Keyboard controls
- WASD controls
- Mobile controls
- Game over screen
- Countdown
- Snake collision
- Food pulse animation
- Responsive design
- No external Python dependencies except Streamlit
============================================================
"""

import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# STREAMLIT CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PYTHON SNAKE",
    page_icon="🐍",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# STREAMLIT OUTER DESIGN
# ============================================================

st.markdown(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&display=swap'
    );

    * {
        font-family: 'Orbitron', sans-serif;
    }

    html,
    body,
    [data-testid="stAppViewContainer"] {

        background:
            radial-gradient(
                circle at 50% -10%,
                rgba(0,255,90,.18),
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
            #020402 !important;

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

        font-size:
            clamp(35px, 7vw, 65px);

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

        animation:
            titleGlow 5s linear infinite;

        filter:
            drop-shadow(
                0 0 10px
                rgba(57,255,20,.4)
            );
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

        margin:
            0 auto 14px auto;

        padding:
            6px 14px;

        border-radius: 100px;

        border:
            1px solid
            rgba(57,255,20,.3);

        background:
            rgba(57,255,20,.05);

        color: #62ff3e;

        font-size: 10px;

        letter-spacing: 2px;

        box-shadow:
            0 0 20px
            rgba(57,255,20,.08);
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
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="snake-title">🐍 PYTHON SNAKE</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="snake-subtitle">'
    'CLASSIC ARCADE • ULTIMATE NEON EDITION'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# GAME
# ============================================================

game_html = r"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>Python Snake</title>


<style>

/* ============================================================
   GLOBAL
============================================================ */

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

    overflow-x: hidden;
}

body {
    overflow-y: auto;
}

.game {

    width: 100%;

    max-width: 700px;

    margin: auto;

    padding: 5px;
}


/* ============================================================
   TOP HUD
============================================================ */

.hud {

    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 8px;

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

    padding: 10px 5px;

    text-align: center;

    box-shadow:
        0 8px 30px
        rgba(0,0,0,.4),

        inset 0 1px 0
        rgba(255,255,255,.04);

    backdrop-filter:
        blur(12px);
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

    font-size: 8px;

    font-weight: 700;

    letter-spacing: 1px;

    margin-bottom: 5px;
}

.card-value {

    font-size: 19px;

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

    margin:
        0 auto 10px;

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
   DIFFICULTY
============================================================ */

.difficulty {

    display: flex;

    justify-content: center;

    flex-wrap: wrap;

    gap: 5px;

    margin-bottom: 12px;
}

.diff-btn {

    padding:
        7px 10px;

    border-radius: 8px;

    border:
        1px solid
        rgba(255,255,255,.08);

    background:
        rgba(255,255,255,.03);

    color: #728076;

    cursor: pointer;

    font-size: 8px;

    font-weight: bold;
}

.diff-btn.active {

    color: #65ff45;

    border-color:
        rgba(57,255,20,.4);

    background:
        rgba(57,255,20,.07);

    box-shadow:
        0 0 15px
        rgba(57,255,20,.08);
}


/* ============================================================
   BOARD
============================================================ */

.board-wrap {

    position: relative;

    width:
        min(94vw, 620px);

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
        rgba(0,0,0,.62);

    backdrop-filter:
        blur(7px);

    transition: .25s;

    pointer-events: none;

    text-align: center;
}

.overlay.hidden {

    opacity: 0;

    visibility: hidden;
}

.overlay-title {

    font-size:
        clamp(25px, 7vw, 46px);

    font-weight: 900;

    letter-spacing: 4px;

    color: #fff;

    text-shadow:
        0 0 15px
        rgba(57,255,20,.6);
}

.overlay-text {

    margin-top: 8px;

    color: #7c8b80;

    font-size: 10px;

    letter-spacing: 2px;
}


/* ============================================================
   MESSAGE
============================================================ */

.message {

    min-height: 24px;

    text-align: center;

    margin-top: 9px;

    font-size: 11px;

    font-weight: 700;

    letter-spacing: 1px;

    color: #6f8075;
}


/* ============================================================
   ACTION BUTTONS
============================================================ */

.actions {

    display: flex;

    justify-content: center;

    gap: 7px;

    margin-top: 6px;

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

    padding:
        9px 14px;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: .5px;

    cursor: pointer;

    transition:
        transform .15s,
        border .15s,
        box-shadow .15s;
}

button:hover {

    border-color:
        rgba(57,255,20,.45);

    box-shadow:
        0 0 20px
        rgba(57,255,20,.12);
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
   SETTINGS
============================================================ */

.settings {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 6px;

    margin:
        13px auto 0;

    max-width: 520px;
}

.setting {

    padding: 8px;

    border-radius: 9px;

    border:
        1px solid
        rgba(255,255,255,.06);

    background:
        rgba(255,255,255,.02);

    text-align: center;

    color: #718077;

    font-size: 8px;
}

.setting button {

    width: 100%;

    margin-top: 5px;

    padding: 6px;

    font-size: 8px;

    color: #73ff59;
}


/* ============================================================
   HELP
============================================================ */

.help {

    text-align: center;

    margin-top: 10px;

    color: #4d5c51;

    font-size: 8px;

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
   LIGHT THEME
============================================================ */

body.light {

    color: #172019;
}

body.light .card {

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,.95),
            rgba(235,240,237,.96)
        );

    border-color:
        rgba(0,0,0,.12);
}

body.light .card-label {

    color: #66736a;
}

body.light .card-value {

    color: #102015;
}

body.light .board-wrap {

    background:
        linear-gradient(
            135deg,
            #cbd5d0,
            #edf3ef,
            #b8c5bd
        );
}

body.light .message {

    color: #536158;
}


/* ============================================================
   NEON THEME
============================================================ */

body.neon .card {

    background:
        linear-gradient(
            145deg,
            rgba(20,5,40,.95),
            rgba(5,5,25,.98)
        );

    border-color:
        rgba(255,0,255,.2);
}

body.neon .card::after {

    background:
        linear-gradient(
            90deg,
            transparent,
            #ff00ff,
            #00ffff,
            transparent
        );
}

body.neon .board-wrap {

    background:
        linear-gradient(
            135deg,
            #301050,
            #050520,
            #102c40
        );
}

body.neon .level-selector select {

    border-color:
        rgba(0,255,255,.35);

    color: #00ffff;
}


/* ============================================================
   MOBILE
============================================================ */

@media(max-width: 500px) {

    .hud {

        grid-template-columns:
            repeat(2, 1fr);

        gap: 5px;
    }

    .card {

        padding: 8px 4px;
    }

    .card-value {

        font-size: 17px;
    }

    .card-label {

        font-size: 7px;
    }

    .settings {

        grid-template-columns:
            1fr 1fr 1fr;
    }

}

</style>

</head>


<body>


<div class="game">


<!-- ============================================================
     HUD
============================================================ -->

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
            120
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


    <div class="card">

        <div class="card-label">
            SPEED
        </div>

        <div
            class="card-value"
            id="speed">
            1x
        </div>

    </div>

</div>


<!-- ============================================================
     LEVEL SELECTOR
============================================================ -->

<div class="level-selector">

    <span>
        🎯 LEVEL
    </span>

    <select id="levelSelect">

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


<!-- ============================================================
     DIFFICULTY
============================================================ -->

<div class="difficulty">

    <button
        class="diff-btn active"
        data-diff="Easy">

        EASY

    </button>

    <button
        class="diff-btn"
        data-diff="Normal">

        NORMAL

    </button>

    <button
        class="diff-btn"
        data-diff="Hard">

        HARD

    </button>

    <button
        class="diff-btn"
        data-diff="Extreme">

        EXTREME

    </button>

</div>


<!-- ============================================================
     BOARD
============================================================ -->

<div class="board-wrap">

    <canvas id="game"></canvas>


    <div
        class="overlay"
        id="overlay">

        <div
            class="overlay-title"
            id="overlayTitle">

            🐍 PYTHON SNAKE

        </div>

        <div
            class="overlay-text"
            id="overlayText">

            SELECT LEVEL AND PRESS START

        </div>

    </div>

</div>


<!-- ============================================================
     MESSAGE
============================================================ -->

<div
    class="message"
    id="message">

    Ready?

</div>


<!-- ============================================================
     ACTIONS
============================================================ -->

<div class="actions">

    <button
        class="primary"
        id="startBtn">

        ▶ START

    </button>


    <button id="pauseBtn">

        ⏸ PAUSE

    </button>


    <button id="restartBtn">

        ↻ RESTART

    </button>

</div>


<!-- ============================================================
     MOBILE CONTROLS
============================================================ -->

<div class="controls">

    <button
        class="control empty">
    </button>


    <button
        class="control"
        data-dir="up">

        ▲

    </button>


    <button
        class="control empty">
    </button>


    <button
        class="control"
        data-dir="left">

        ◀

    </button>


    <button
        class="control"
        data-dir="down">

        ▼

    </button>


    <button
        class="control"
        data-dir="right">

        ▶

    </button>

</div>


<!-- ============================================================
     SETTINGS
============================================================ -->

<div class="settings">


    <div class="setting">

        GRID

        <button id="gridBtn">
            ON
        </button>

    </div>


    <div class="setting">

        SOUND

        <button id="soundBtn">
            ON
        </button>

    </div>


    <div class="setting">

        THEME

        <button id="themeBtn">
            DARK
        </button>

    </div>

</div>


<div class="help">

    W A S D / ARROW KEYS
    •
    SPACE = PAUSE
    •
    ESC = STOP

</div>


<div class="footer">

    PYTHON SNAKE • WEB ARCADE

</div>


</div>


<script>


/* ============================================================
   CANVAS CONFIG
============================================================ */

const canvas =
    document.getElementById("game");

const ctx =
    canvas.getContext("2d");


const GRID_WIDTH = 25;

const GRID_HEIGHT = 25;

const CELL_SIZE = 24;

canvas.width =
    GRID_WIDTH * CELL_SIZE;

canvas.height =
    GRID_HEIGHT * CELL_SIZE;


/* ============================================================
   STORAGE
============================================================ */

const STORAGE_KEY =
    "pythonSnakeSettings";

const HIGH_SCORE_KEY =
    "pythonSnakeHighScore";


/*
    Original supplied highscore.json:

    {
        "high_score": 120
    }

    Therefore first-time browser score starts at 120.
*/

let highScore =
    Number(
        localStorage.getItem(
            HIGH_SCORE_KEY
        )
    );

if (
    !Number.isFinite(highScore) ||
    highScore < 120
) {

    highScore = 120;

    localStorage.setItem(
        HIGH_SCORE_KEY,
        highScore
    );
}


/* ============================================================
   SETTINGS
============================================================ */

const defaultSettings = {

    difficulty: "Normal",

    grid: true,

    sound: true,

    theme: "Dark"
};


let settings;


try {

    settings =
        JSON.parse(
            localStorage.getItem(
                STORAGE_KEY
            )
        ) || defaultSettings;

}
catch (error) {

    settings =
        {...defaultSettings};
}


function saveSettings() {

    localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify(settings)
    );
}


/* ============================================================
   GAME VARIABLES
============================================================ */

let snake = [];

let food = null;

let direction = {

    x: 1,

    y: 0
};

let nextDirection = {

    x: 1,

    y: 0
};

let score = 0;

let selectedLevel = 1;

let level = 1;

let running = false;

let paused = false;

let gameOver = false;

let timer = null;

let countdownTimer = null;

let foodPulse = 0;

let audioContext = null;


/* ============================================================
   DIFFICULTY SPEEDS
============================================================ */

/*
    Original settings.py speeds:

    Easy     = 140
    Normal   = 100
    Hard     = 70
    Extreme  = 45
*/

const difficultySpeeds = {

    Easy: 140,

    Normal: 100,

    Hard: 70,

    Extreme: 45
};


/* ============================================================
   LEVEL SPEEDS
============================================================ */

const levelSpeeds = {

    1: 180,

    2: 140,

    3: 105,

    4: 75,

    5: 48
};


/* ============================================================
   FOOD TYPES
============================================================ */

/*
    Original food.py:

    Normal = 70% = +10
    Bonus  = 20% = +25
    Rare   = 10% = +50
*/

const foodTypes = [

    {
        type: "normal",

        points: 10,

        chance: 0.70
    },

    {
        type: "bonus",

        points: 25,

        chance: 0.20
    },

    {
        type: "rare",

        points: 50,

        chance: 0.10
    }
];


/* ============================================================
   DOM ELEMENTS
============================================================ */

const scoreEl =
    document.getElementById(
        "score"
    );

const highScoreEl =
    document.getElementById(
        "highscore"
    );

const levelEl =
    document.getElementById(
        "level"
    );

const speedEl =
    document.getElementById(
        "speed"
    );

const messageEl =
    document.getElementById(
        "message"
    );

const overlay =
    document.getElementById(
        "overlay"
    );

const overlayTitle =
    document.getElementById(
        "overlayTitle"
    );

const overlayText =
    document.getElementById(
        "overlayText"
    );

const levelSelect =
    document.getElementById(
        "levelSelect"
    );

const gridBtn =
    document.getElementById(
        "gridBtn"
    );

const soundBtn =
    document.getElementById(
        "soundBtn"
    );

const themeBtn =
    document.getElementById(
        "themeBtn"
    );


/* ============================================================
   SOUND
============================================================ */

function playSound(type) {

    if (!settings.sound)
        return;


    try {

        if (!audioContext) {

            audioContext =
                new (
                    window.AudioContext ||
                    window.webkitAudioContext
                )();
        }


        const oscillator =
            audioContext.createOscillator();

        const gain =
            audioContext.createGain();


        const frequencies = {

            click: 600,

            eat: 750,

            levelup: 1100,

            gameover: 180
        };


        oscillator.frequency.value =
            frequencies[type] || 600;


        oscillator.type =
            "square";


        gain.gain.setValueAtTime(
            0.035,
            audioContext.currentTime
        );


        gain.gain.exponentialRampToValueAtTime(
            0.001,
            audioContext.currentTime + 0.08
        );


        oscillator.connect(gain);

        gain.connect(
            audioContext.destination
        );


        oscillator.start();

        oscillator.stop(
            audioContext.currentTime + 0.08
        );

    }
    catch (error) {

        // Sound is optional.
    }
}


/* ============================================================
   APPLY SETTINGS
============================================================ */

function applySettings() {

    document.body.classList.remove(
        "light",
        "neon"
    );


    if (
        settings.theme === "Light"
    ) {

        document.body.classList.add(
            "light"
        );

    }

    else if (
        settings.theme === "Neon"
    ) {

        document.body.classList.add(
            "neon"
        );
    }


    gridBtn.textContent =
        settings.grid
            ? "ON"
            : "OFF";


    soundBtn.textContent =
        settings.sound
            ? "ON"
            : "OFF";


    themeBtn.textContent =
        settings.theme.toUpperCase();


    document
        .querySelectorAll(".diff-btn")
        .forEach(
            button => {

                button.classList.toggle(
                    "active",
                    button.dataset.diff ===
                    settings.difficulty
                );
            }
        );
}


/* ============================================================
   INITIALIZE
============================================================ */

function initializeGame() {

    snake = [

        {
            x: 12,
            y: 12
        },

        {
            x: 11,
            y: 12
        },

        {
            x: 10,
            y: 12
        },

        {
            x: 9,
            y: 12
        }

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
        "🐍 PYTHON SNAKE",
        "LEVEL " +
        selectedLevel +
        " • PRESS START"
    );


    setMessage(
        "Ready for the challenge?"
    );
}


/* ============================================================
   FOOD SPAWN
============================================================ */

function spawnFood() {

    do {

        food = {

            x:
                Math.floor(
                    Math.random() *
                    GRID_WIDTH
                ),

            y:
                Math.floor(
                    Math.random() *
                    GRID_HEIGHT
                ),

            type: "normal",

            points: 10
        };

    }
    while (
        snake.some(
            part =>
                part.x === food.x &&
                part.y === food.y
        )
    );


    const random =
        Math.random();


    let cumulative = 0;


    for (
        const foodType
        of foodTypes
    ) {

        cumulative +=
            foodType.chance;


        if (
            random <= cumulative
        ) {

            food.type =
                foodType.type;

            food.points =
                foodType.points;

            break;
        }
    }
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

    gameOver = false;


    hideOverlay();


    setMessage(
        "🔥 LEVEL " +
        selectedLevel +
        " • " +
        settings.difficulty.toUpperCase()
    );


    countdown(
        3
    );
}


/* ============================================================
   COUNTDOWN
============================================================ */

function countdown(number) {

    if (!running)
        return;


    if (number > 0) {

        showOverlay(
            String(number),
            "GET READY..."
        );


        playSound("click");


        countdownTimer =
            setTimeout(
                () => {

                    countdown(
                        number - 1
                    );

                },
                650
            );


        return;
    }


    hideOverlay();

    setMessage(
        "GO! 🐍"
    );


    gameLoop();
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

    paused = false;


    if (timer) {

        clearTimeout(timer);

        timer = null;
    }


    if (countdownTimer) {

        clearTimeout(
            countdownTimer
        );

        countdownTimer = null;
    }
}


/* ============================================================
   PAUSE
============================================================ */

function togglePause() {

    if (
        !running ||
        gameOver
    ) {

        return;
    }


    paused =
        !paused;


    if (paused) {

        if (timer) {

            clearTimeout(timer);

            timer = null;
        }


        showOverlay(
            "⏸ PAUSED",
            "PRESS SPACE TO RESUME"
        );


        setMessage(
            "Game paused"
        );


        playSound(
            "click"
        );

    }

    else {

        hideOverlay();


        setMessage(
            "▶ RESUMED"
        );


        gameLoop();
    }
}


/* ============================================================
   DIRECTION
============================================================ */

function changeDirection(
    x,
    y
) {

    if (
        !running ||
        gameOver
    ) {

        return;
    }


    /*
        Prevent 180° turn.
    */

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
            event.code ===
            "Space"
        ) {

            event.preventDefault();

            togglePause();
        }


        else if (
            key === "escape"
        ) {

            stopGame();


            initializeGame();


            setMessage(
                "Stopped • Select a level and press START"
            );
        }

    }
);


/* ============================================================
   GAME LOOP
============================================================ */

function gameLoop() {

    if (
        !running ||
        paused ||
        gameOver
    ) {

        return;
    }


    update();

    draw();


    if (
        !gameOver
    ) {

        const speed =
            getCurrentSpeed();


        timer =
            setTimeout(
                gameLoop,
                speed
            );
    }
}


/* ============================================================
   SPEED
============================================================ */

function getCurrentSpeed() {

    /*
        Combine selected difficulty
        with selected level.

        This keeps the original
        difficulty system while
        adding Level 1-5.
    */

    const difficultyBase =
        difficultySpeeds[
            settings.difficulty
        ] || 100;


    const levelSpeed =
        levelSpeeds[
            selectedLevel
        ] || 100;


    /*
        Blend both systems.
    */

    const speed =
        Math.round(
            (
                difficultyBase +
                levelSpeed
            ) / 2
        );


    return Math.max(
        30,
        speed
    );
}


/* ============================================================
   UPDATE
============================================================ */

function update() {

    if (
        !running ||
        paused ||
        gameOver
    ) {

        return;
    }


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


    /*
        WALL COLLISION
    */

    if (

        head.x < 0 ||

        head.x >= GRID_WIDTH ||

        head.y < 0 ||

        head.y >= GRID_HEIGHT

    ) {

        triggerGameOver();

        return;
    }


    /*
        SELF COLLISION
    */

    if (

        snake.some(
            part =>
                part.x === head.x &&
                part.y === head.y
        )

    ) {

        triggerGameOver();

        return;
    }


    /*
        MOVE
    */

    snake.unshift(
        head
    );


    /*
        FOOD
    */

    if (

        head.x === food.x &&

        head.y === food.y

    ) {

        score +=
            food.points;


        /*
            High score
        */

        if (
            score > highScore
        ) {

            highScore =
                score;


            localStorage.setItem(
                HIGH_SCORE_KEY,
                String(highScore)
            );
        }


        playSound(
            "eat"
        );


        /*
            Food gives
            automatic growth.
        */

        /*
            Do NOT remove tail
            this turn.
        */


        spawnFood();


        /*
            Dynamic level display
            based on score.

            But selected level
            remains the main speed mode.
        */

        const newLevel =
            Math.max(
                selectedLevel,
                Math.floor(
                    score / 50
                ) + selectedLevel
            );


        if (
            newLevel > level
        ) {

            level =
                newLevel;


            playSound(
                "levelup"
            );


            setMessage(
                "🚀 LEVEL UP! LEVEL " +
                level
            );
        }

        else {

            setMessage(
                getFoodMessage()
            );
        }


        updateStats();

    }

    else {

        /*
            Normal movement:
            remove tail.
        */

        snake.pop();
    }
}


/* ============================================================
   FOOD MESSAGE
============================================================ */

function getFoodMessage() {

    if (
        food.type === "bonus"
    ) {

        return "🟡 BONUS FOOD • +25";
    }


    if (
        food.type === "rare"
    ) {

        return "🔵 RARE FOOD • +50";
    }


    return "🍎 NORMAL FOOD • +10";
}


/* ============================================================
   GAME OVER
============================================================ */

function triggerGameOver() {

    running = false;

    gameOver = true;


    if (timer) {

        clearTimeout(timer);

        timer = null;
    }


    playSound(
        "gameover"
    );


    showOverlay(
        "💀 GAME OVER",
        "SCORE: " +
        score +
        " • LEVEL: " +
        level
    );


    setMessage(
        "Press RESTART to try again"
    );


    updateStats();

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
        level;


    const currentSpeed =
        getCurrentSpeed();


    /*
        Convert milliseconds
        into an easy speed value.
    */

    const speedValue =
        Math.max(
            1,
            Math.round(
                200 /
                currentSpeed
            )
        );


    speedEl.textContent =
        speedValue +
        "x";
}


/* ============================================================
   MESSAGE
============================================================ */

function setMessage(
    text
) {

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


    /*
        Background
    */

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


    /*
        GRID
    */

    if (
        settings.grid
    ) {

        ctx.strokeStyle =
            "rgba(80,120,85,.10)";

        ctx.lineWidth = 1;


        for (
            let x = 0;
            x <= canvas.width;
            x += CELL_SIZE
        ) {

            ctx.beginPath();

            ctx.moveTo(
                x,
                0
            );

            ctx.lineTo(
                x,
                canvas.height
            );

            ctx.stroke();
        }


        for (
            let y = 0;
            y <= canvas.height;
            y += CELL_SIZE
        ) {

            ctx.beginPath();

            ctx.moveTo(
                0,
                y
            );

            ctx.lineTo(
                canvas.width,
                y
            );

            ctx.stroke();
        }
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


    foodPulse +=
        0.08;


    const fx =
        food.x *
        CELL_SIZE +
        CELL_SIZE / 2;


    const fy =
        food.y *
        CELL_SIZE +
        CELL_SIZE / 2;


    const pulse =
        Math.sin(
            foodPulse
        ) * 2;


    let color =
        "#ff334f";


    if (
        food.type === "bonus"
    ) {

        color =
            "#ffcc00";
    }


    else if (
        food.type === "rare"
    ) {

        color =
            "#00e5ff";
    }


    ctx.shadowColor =
        color;


    ctx.shadowBlur =
        18 +
        pulse;


    ctx.beginPath();


    ctx.arc(
        fx,
        fy,
        CELL_SIZE * .27 +
        pulse * .1,
        0,
        Math.PI * 2
    );


    ctx.fillStyle =
        color;


    ctx.fill();


    ctx.shadowBlur =
        0;


    /*
        Highlight
    */

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
        function(
            part,
            index
        ) {

            const padding =
                index === 0
                    ? 1.5
                    : 2.5;


            const x =
                part.x *
                CELL_SIZE +
                padding;


            const y =
                part.y *
                CELL_SIZE +
                padding;


            const size =
                CELL_SIZE -
                padding * 2;


            /*
                HEAD
            */

            if (
                index === 0
            ) {

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


            if (
                index === 0
            ) {

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


            /*
                roundRect has
                support in modern
                browsers.
            */

            if (
                ctx.roundRect
            ) {

                ctx.roundRect(
                    x,
                    y,
                    size,
                    size,
                    index === 0
                        ? 6
                        : 4
                );

            }

            else {

                ctx.rect(
                    x,
                    y,
                    size,
                    size
                );
            }


            ctx.fill();


            ctx.shadowBlur =
                0;


            /*
                EYES
            */

            if (
                index === 0
            ) {

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

function drawEyes(
    x,
    y
) {

    ctx.fillStyle =
        "#021000";


    const baseX =
        x *
        CELL_SIZE;


    const baseY =
        y *
        CELL_SIZE;


    let eyes;


    if (
        direction.x > 0
    ) {

        eyes = [

            [
                baseX + 17,
                baseY + 7
            ],

            [
                baseX + 17,
                baseY + 17
            ]

        ];

    }

    else if (
        direction.x < 0
    ) {

        eyes = [

            [
                baseX + 7,
                baseY + 7
            ],

            [
                baseX + 7,
                baseY + 17
            ]

        ];

    }

    else if (
        direction.y < 0
    ) {

        eyes = [

            [
                baseX + 7,
                baseY + 7
            ],

            [
                baseX + 17,
                baseY + 7
            ]

        ];

    }

    else {

        eyes = [

            [
                baseX + 7,
                baseY + 17
            ],

            [
                baseX + 17,
                baseY + 17
            ]

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
   LEVEL SELECTOR
============================================================ */

levelSelect.addEventListener(
    "change",
    function() {

        if (
            running
        ) {

            levelSelect.value =
                selectedLevel;


            setMessage(
                "⏸ Stop / restart before changing level"
            );


            return;
        }


        selectedLevel =
            Number(
                levelSelect.value
            );


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


        showOverlay(
            "LEVEL " +
            selectedLevel,
            names[selectedLevel] +
            " • PRESS START"
        );


        playSound(
            "click"
        );
    }
);


/* ============================================================
   DIFFICULTY BUTTONS
============================================================ */

document
    .querySelectorAll(
        ".diff-btn"
    )
    .forEach(
        button => {

            button.addEventListener(
                "click",
                function() {

                    if (
                        running
                    ) {

                        setMessage(
                            "⏸ Stop game before changing difficulty"
                        );

                        return;
                    }


                    settings.difficulty =
                        button.dataset.diff;


                    saveSettings();

                    applySettings();

                    updateStats();


                    setMessage(
                        "Difficulty: " +
                        settings.difficulty
                    );


                    playSound(
                        "click"
                    );
                }
            );

        }
    );


/* ============================================================
   GRID BUTTON
============================================================ */

gridBtn.addEventListener(
    "click",
    function() {

        settings.grid =
            !settings.grid;


        saveSettings();

        applySettings();

        draw();


        setMessage(
            settings.grid
                ? "Grid enabled"
                : "Grid disabled"
        );


        playSound(
            "click"
        );
    }
);


/* ============================================================
   SOUND BUTTON
============================================================ */

soundBtn.addEventListener(
    "click",
    function() {

        settings.sound =
            !settings.sound;


        saveSettings();

        applySettings();


        setMessage(
            settings.sound
                ? "Sound enabled 🔊"
                : "Sound disabled 🔇"
        );


        if (
            settings.sound
        ) {

            playSound(
                "click"
            );
        }
    }
);


/* ============================================================
   THEME BUTTON
============================================================ */

themeBtn.addEventListener(
    "click",
    function() {

        const themes = [

            "Dark",

            "Light",

            "Neon"
        ];


        const current =
            themes.indexOf(
                settings.theme
            );


        settings.theme =
            themes[
                (current + 1) %
                themes.length
            ];


        saveSettings();

        applySettings();


        setMessage(
            "Theme: " +
            settings.theme
        );


        playSound(
            "click"
        );
    }
);


/* ============================================================
   ACTION BUTTONS
============================================================ */

document
    .getElementById(
        "startBtn"
    )
    .addEventListener(
        "click",
        startGame
    );


document
    .getElementById(
        "pauseBtn"
    )
    .addEventListener(
        "click",
        togglePause
    );


document
    .getElementById(
        "restartBtn"
    )
    .addEventListener(
        "click",
        restartGame
    );


/* ============================================================
   MOBILE CONTROLS
============================================================ */

document
    .querySelectorAll(
        ".control"
    )
    .forEach(
        button => {

            button.addEventListener(
                "click",
                function() {

                    const dir =
                        button.dataset.dir;


                    if (
                        dir === "up"
                    ) {

                        changeDirection(
                            0,
                            -1
                        );
                    }


                    else if (
                        dir === "down"
                    ) {

                        changeDirection(
                            0,
                            1
                        );
                    }


                    else if (
                        dir === "left"
                    ) {

                        changeDirection(
                            -1,
                            0
                        );
                    }


                    else if (
                        dir === "right"
                    ) {

                        changeDirection(
                            1,
                            0
                        );
                    }

                }
            );

        }
    );


/* ============================================================
   INITIALIZE
============================================================ */

levelSelect.value =
    "1";


selectedLevel = 1;

level = 1;


applySettings();

initializeGame();


/* ============================================================
   ANIMATION
============================================================ */

function animationLoop() {

    if (
        !running
    ) {

        /*
            Continue food pulse
            animation when idle.
        */

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
# DISPLAY GAME
# ============================================================

components.html(
    game_html,
    height=1040,
    scrolling=True,
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
        padding-bottom:10px;
    ">
        🐍 PYTHON SNAKE • BUILT WITH PYTHON + STREAMLIT
    </div>
    """,
    unsafe_allow_html=True,
)
