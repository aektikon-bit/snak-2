import streamlit as st
import random

st.title("🎲 เกมทายเลขสนุกๆ")

# กำหนดช่วงตัวเลข
min_number = 1
max_number = 10

# สุ่มเลขลับ
if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(min_number, max_number)
    st.session_state.guesses = 0

st.write(f"ลองทายเลขระหว่าง {min_number} ถึง {max_number}")

# รับค่าอินพุตจากผู้เล่น
user_guess = st.number_input("ใส่เลขของคุณ:", min_value=min_number, max_value=max_number, step=1)

if st.button("ทายเลย!"):
    st.session_state.guesses += 1
    if user_guess < st.session_state.secret_number:
        st.warning("🔼 มากกว่าอีกหน่อย!")
    elif user_guess > st.session_state.secret_number:
        st.warning("🔽 น้อยกว่านี้อีกหน่อย!")
    else:
        st.success(f"🎉 ถูกต้อง! คุณทายเลข {st.session_state.secret_number} ถูกต้องใน {st.session_state.guesses} ครั้ง!")
        # รีเซ็ตเกม
        if st.button("เล่นอีกครั้ง"):
            st.session_state.secret_number = random.randint(min_number, max_number)
            st.session_state.guesses = 0
