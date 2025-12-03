# snake_simple.py
import streamlit as st
import numpy as np
import time
import random

# ==============================
# INIT STATE
# ==============================
GRID = 10
CELL = 40

if "snake" not in st.session_state:
    st.session_state.snake = [(5,5)]
if "dir" not in st.session_state:
    st.session_state.dir = (0,1)  # start moving right
if "food" not in st.session_state:
    st.session_state.food = (random.randint(0,GRID-1), random.randint(0,GRID-1))
if "score" not in st.session_state:
    st.session_state.score = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "speed" not in st.session_state:
    st.session_state.speed = 0.3

# ==============================
# MOVE SNAKE
# ==============================
def move_snake():
    if st.session_state.game_over: return
    head = st.session_state.snake[-1]
    new_head = (head[0]+st.session_state.dir[0], head[1]+st.session_state.dir[1])
    
    # wall collision
    if not (0 <= new_head[0] < GRID and 0 <= new_head[1] < GRID) or new_head in st.session_state.snake:
        st.session_state.game_over = True
        return
    
    st.session_state.snake.append(new_head)
    
    # eat food
    if new_head == st.session_state.food:
        st.session_state.score += 1
        while True:
            st.session_state.food = (random.randint(0,GRID-1), random.randint(0,GRID-1))
            if st.session_state.food not in st.session_state.snake: break
    else:
        st.session_state.snake.pop(0)

# ==============================
# DRAW BOARD
# ==============================
def draw_board():
    board = np.zeros((GRID*CELL, GRID*CELL,3),dtype=np.uint8)+50
    # snake
    for x,y in st.session_state.snake:
        board[y*CELL:y*CELL+CELL, x*CELL:x*CELL+CELL] = [0,255,0]
    # food
    fx,fy = st.session_state.food
    board[fy*CELL:fy*CELL+CELL, fx*CELL:fx*CELL+CELL] = [255,0,0]
    return board

# ==============================
# UI
# ==============================
st.title("🐍 Snake Grid - Simple Version")
st.write(f"Score: {st.session_state.score}")

# control buttons
cols = st.columns(4)
with cols[0]:
    if st.button("⬆️"): st.session_state.dir = (0,-1)
with cols[1]:
    if st.button("⬅️"): st.session_state.dir = (-1,0)
with cols[2]:
    if st.button("➡️"): st.session_state.dir = (1,0)
with cols[3]:
    if st.button("⬇️"): st.session_state.dir = (0,1)

# speed slider
st.session_state.speed = st.slider("Game speed", 0.05, 0.5, st.session_state.speed, 0.05)

# restart
if st.session_state.game_over:
    if st.button("Restart"):
        st.session_state.snake = [(5,5)]
        st.session_state.dir = (0,1)
        st.session_state.food = (random.randint(0,GRID-1), random.randint(0,GRID-1))
        st.session_state.score = 0
        st.session_state.game_over = False

# game loop
move_snake()
board = draw_board()
st.image(board, width=GRID*CELL)

time
