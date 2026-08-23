import streamlit as st
from database.college_repository import add_internship, get_internships
from styles.college.theme import apply_college_theme

def render():
    apply_college_theme()
    uid = st.session_state.get("user_id")
    st.html('<div class="college-hero"><div class="college-eyebrow">EXPERIENCE TRACKER</div><div class="college-title">💼 Internships</div><div class="college-desc">Track internship applications, training and experience.</div></div>')

    with st.form("internship_form"):
        company = st.text_input("Company")
        role = st.text_input("Role")
        duration = st.text_input("Duration")
        status = st.selectbox("Status", ["Planned","Applied","Ongoing","Completed"])
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Add Internship", use_container_width=True)

    if submitted and company.strip() and role.strip():
        add_internship(uid, company, role, duration, status, notes)
        st.rerun()

    for item in get_internships(uid):
        st.write(f'**{item["company"]} — {item["role"]}** | {item["status"]} | {item["duration"]}')
