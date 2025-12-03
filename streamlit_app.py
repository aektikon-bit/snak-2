# snake_simple.py
import streamlit as st
import numpy as np
import time
import random

# ==============================
# GAME STATE
# ==============================
GRID_SIZE = 10
CELL_SIZE = 40
FPS = 0.3  # ความเร็วงู

if 'snake' not in st.session_state:
    st.session_state.snake = [(5,5)]
if 'direction' not in st.session_state:
    st.session_state.direction = (0,1)  # dx, dy
if 'food' not in st.session_state:
    st.session_state.food = (random.randint(0,GRID_SIZE-1), random.randint(0,GRID_SIZE-1))
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# ==============================
# MOVE SNAKE
# ==============================
def move_snake():
    if st.session_state.game_over:
        return
    head_x, head_y = st.session_state.snake[-1]
    dx, dy = st.session_state.direction
    new_head = (head_x + dx, head_y + dy)

    # ตรวจสอบชนตัวเอง / ชนขอบ
    if (new_head in st.session_state.snake) or not (0 <= new_head[0] < GRID_SIZE) or not (0 <= new_head[1] < GRID_SIZE):
        st.session_state.game_over = True
        return

    st.session_state.snake.append(new_head)

    # ตรวจสอบกินอาหาร
    if new_head == st.session_state.food:
        st.session_state.score += 1
        while True:
            new_food = (random.randint(0,GRID_SIZE-1), random.randint(0,GRID_SIZE-1))
            if new_food not in st.session_state.snake:
                st.session_state.food = new_food
                break
    else:
        st.session_state.snake.pop(0)  # เคลื่อนที่ไปข้างหน้า

# ==============================
# CONTROL BUTTONS
# ==============================
col1,col2,col3 = st.columns(3)
with col1:
    if st.button("⬆️"):
        if st.session_state.direction != (1,0):
            st.session_state.direction = (-1,0)
with col2:
    if st.button("⬅️"):
        if st.session_state.direction != (0,1):
            st.session_state.direction = (0,-1)
    if st.button("➡️"):
        if st.session_state.direction != (0,-1):
            st.session_state.direction = (0,1)
with col3:
    if st.button("⬇️"):
        if st.session_state.direction != (-1,0):
            st.session_state.direction = (1,0)

# ==============================
# DRAW BOARD
# ==============================
def draw_board():
    board = np.zeros((GRID_SIZE*CELL_SIZE, GRID_SIZE*CELL_SIZE, 3), dtype=np.uint8)
    board[:,:,:] = [50,50,50]  # background gray

    # วาดอาหาร
    fx, fy = st.session_state.food
    board[fy*CELL_SIZE:fy*CELL_SIZE+CELL_SIZE, fx*CELL_SIZE:fx*CELL_SIZE+CELL_SIZE] = [255,0,0]

    # วาดงู
    for x,y in st.session_state.snake:
        board[y*CELL_SIZE:y*CELL_SIZE+CELL_SIZE, x*CELL_SIZE:x*CELL_SIZE+CELL_SIZE] = [0,255,0]

    # grid lines
    for i in range(GRID_SIZE):
        board[i*CELL_SIZE:i*CELL_SIZE+1,:] = [80,80,80]
        board[:,i*CELL_SIZE:i*CELL_SIZE+1] = [80,80,80]

    return board

# ==============================
# GAME LOOP
# ==============================
st.write(f"Score: {st.session_state.score}")

if st.session_state.game_over:
    st.warning("💀 Game Over! Press R to Restart")
    if st.button("🔄 Restart"):
        st.session_state.snake = [(5,5)]
        st.session_state.direction = (0,1)
        st.session_state.food = (random.randint(0,GRID_SIZE-1), random.randint(0,GRID_SIZE-1))
        st.session_state.score = 0
        st.session_state.game_over = False
else:
    move_snake()
    board = draw_board()
    st.image(board)
    time.sleep(FPS)
    st.experimental_rerun()
