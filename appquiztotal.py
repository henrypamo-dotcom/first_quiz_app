import streamlit as st
import pandas as pd
import time
import random

# ---------------- CONFIG ---------------- #
st.set_page_config(
    page_title="Advanced English Quiz (B2+/C1)",
    page_icon="🧠",
    layout="centered"
)

QUIZ_TIME = 30  # seconds per question
CSV_FILE = "questions_c1.csv"

# ---------------- LOAD DATA ---------------- #
@st.cache_data
def load_questions():
    df = pd.read_csv(CSV_FILE)
    return df

questions_df = load_questions()

# ---------------- SESSION STATE ---------------- #
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    st.session_state.questions = questions_df.sample(frac=1).reset_index(drop=True)

# ---------------- HEADER ---------------- #
st.title("🧠 Advanced English Quiz (B2+/C1)")
st.caption("Functions • Discourse markers • Condition • Contrast • Purpose")

# ---------------- FINISHED ---------------- #
if st.session_state.current_q >= len(st.session_state.questions):
    st.success("Quiz completed!")
    st.write(f"### Final Score: {st.session_state.score} / {len(st.session_state.questions)}")

    if st.session_state.score >= 35:
        st.balloons()
        st.write("✅ Level achieved: **Strong B2 / C1**")
    else:
        st.write("⚠️ Level: **B2 borderline – more practice recommended**")

    if st.button("Restart quiz"):
        st.session_state.clear()
        st.experimental_rerun()

    st.stop()

# ---------------- CURRENT QUESTION ---------------- #
q = st.session_state.questions.iloc[st.session_state.current_q]

elapsed = int(time.time() - st.session_state.start_time)
remaining = max(QUIZ_TIME - elapsed, 0)

st.progress(remaining / QUIZ_TIME)
st.write(f"⏱ Time left: **{remaining}s**")

st.markdown(f"### Question {st.session_state.current_q + 1}")
st.markdown(f"**Function:** `{q['function']}` | **Level:** `{q['level']}`")
st.markdown(q["question"])

options = {
    "a": q["option_a"],
    "b": q["option_b"],
    "c": q["option_c"]
}

choice = st.radio(
    "Choose the correct option:",
    list(options.keys()),
    format_func=lambda x: f"{x.upper()}) {options[x]}",
    key=f"q_{st.session_state.current_q}"
)

# ---------------- TIME UP ---------------- #
if remaining == 0:
    st.warning("⏰ Time is up!")
    st.write("❌ No answer submitted.")
    st.write("💡", q["feedback_wrong"])

    if st.button("Next question"):
        st.session_state.current_q += 1
        st.session_state.start_time = time.time()
        st.experimental_rerun()

    st.stop()

# ---------------- SUBMIT ---------------- #
if st.button("Submit answer"):
    correct = q["correct"].strip().lower()

    if choice == correct:
        st.success("✅ Correct!")
        st.write("💡", q["feedback_correct"])
        st.session_state.score += 1
    else:
        st.error("❌ Incorrect")
        st.write(f"✔ Correct answer: **{correct.upper()}**")
        st.write("💡", q["feedback_wrong"])

    st.button("Next question", on_click=lambda: None)

    # move to next
    st.session_state.current_q += 1
    st.session_state.start_time = time.time()
    st.experimental_rerun()
