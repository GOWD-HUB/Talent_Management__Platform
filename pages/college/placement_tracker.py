from datetime import date
import streamlit as st
from database.college_repository import add_placement, get_placements, delete_placement
from styles.college.theme import apply_college_theme

def render():
    apply_college_theme()
    uid = st.session_state.get("user_id")
    st.html('<div class="college-hero"><div class="college-eyebrow">APPLICATION TRACKING</div><div class="college-title">📌 Placement Tracker</div><div class="college-desc">Track applications, rounds and offers.</div></div>')

    with st.form("placement_form"):
        company = st.text_input("Company")
        role = st.text_input("Role")
        status = st.selectbox("Status", ["Applied","Shortlisted","Interview","Rejected","Offer"])
        applied = st.date_input("Applied Date", date.today())
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Add Application", use_container_width=True)

    if submitted and company.strip() and role.strip():
        add_placement(uid, company, role, status, applied.isoformat(), notes)
        st.rerun()

    for item in get_placements(uid):
        with st.expander(f'{item["company"]} — {item["role"]} — {item["status"]}'):
            st.write(item.get("notes") or "No notes")
            if st.button("Delete", key=f'placement_delete_{item["id"]}'):
                delete_placement(item["id"])
                st.rerun()
