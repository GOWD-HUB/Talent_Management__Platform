import streamlit as st
from database.college_repository import get_college_profile
from services.college.ats_service import ats_match
from styles.college.theme import apply_college_theme

def render():
    apply_college_theme()
    uid = st.session_state.get("user_id")
    p = get_college_profile(uid) if uid else {}
    st.html('<div class="college-hero"><div class="college-eyebrow">ATS ANALYSIS</div><div class="college-title">🎯 ATS Checker</div><div class="college-desc">Compare profile keywords with a job description.</div></div>')
    resume = " ".join(str(p.get(k) or "") for k in ["technical_skills","projects","internships","certifications","preferred_role"])
    jd = st.text_area("Paste Job Description", height=220)
    if st.button("Check ATS Match", use_container_width=True):
        score, missing = ats_match(resume, jd)
        st.metric("ATS Match", f"{score}%")
        st.progress(score/100)
        if missing:
            st.write("Missing keywords:", ", ".join(missing))
