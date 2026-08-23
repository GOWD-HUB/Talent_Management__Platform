import streamlit as st


def render_footer():

    html = (
        '<div class="app-footer">'
        '<div class="footer-title">© 2026 TalentSphere Elevate</div>'
        '<div class="footer-subtitle">'
        'AI-Powered Career Development Platform'
        '</div>'
        '</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True
    )