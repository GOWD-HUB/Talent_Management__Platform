import streamlit as st
from database.college_repository import add_hackathon, get_hackathons
from styles.college.theme import apply_college_theme

def render():
    apply_college_theme()
    uid = st.session_state.get("user_id")
    st.html('<div class="college-hero"><div class="college-eyebrow">PROJECT COMPETITIONS</div><div class="college-title">🏆 Hackathons</div><div class="college-desc">Track hackathons, teams, projects and results.</div></div>')

    with st.form("hackathon_form"):
        name = st.text_input("Hackathon Name")
        team = st.text_input("Team")
        result = st.text_input("Result / Position")
        project = st.text_input("Project")
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Add Hackathon", use_container_width=True)

    if submitted and name.strip():
        add_hackathon(uid, name, team, result, project, notes)
        st.rerun()

    for item in get_hackathons(uid):
        st.write(f'**{item["name"]}** — {item["project"]} — {item["result"]}')
