from datetime import date
import streamlit as st
from services.college.daily_service import challenge_for_day
from styles.college.theme import apply_college_theme

def render():
    apply_college_theme()
    topic, question = challenge_for_day(date.today().toordinal())
    st.html(f'<div class="college-hero"><div class="college-eyebrow">DAILY PRACTICE</div><div class="college-title">🔥 Daily Challenge</div><div class="college-desc">{topic} challenge for today.</div></div>')
    st.markdown(f"## {question}")
    st.text_area("Your Solution / Explanation", height=220)
    if st.button("Mark Completed", use_container_width=True):
        st.session_state["college_daily_done"] = True
        st.success("Challenge completed for this session.")
