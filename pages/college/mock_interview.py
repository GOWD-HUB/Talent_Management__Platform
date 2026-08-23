import streamlit as st
from services.college.interview_service import BANK, evaluate
from styles.college.theme import apply_college_theme

def render():
    apply_college_theme()
    st.html('<div class="college-hero"><div class="college-eyebrow">MOCK INTERVIEW</div><div class="college-title">🗣️ Mock Interview</div><div class="college-desc">Answer a question and receive structured feedback.</div></div>')
    category = st.selectbox("Type", list(BANK.keys()))
    question = st.selectbox("Question", BANK[category])
    answer = st.text_area("Your Answer", height=220)
    if st.button("Evaluate", use_container_width=True):
        score, feedback = evaluate(answer)
        st.metric("Answer Score", f"{score}%")
        st.info(feedback)
