import streamlit as st


def apply_ai_study_mentor_theme():

    st.markdown(
        """
<style>
.mentor-hero {
    padding: 34px 38px;
    border-radius: 24px;
    background: linear-gradient(135deg,#EEF2FF,#F5F3FF);
    border: 1px solid #DDD6FE;
    box-shadow: 0 12px 34px rgba(15,23,42,.05);
    margin-bottom: 22px;
}
.mentor-eyebrow {
    color: #7C3AED !important;
    font-size: 10px !important;
    font-weight: 800;
    letter-spacing: 1.2px;
}
.mentor-title {
    color: #0F172A !important;
    font-size: 34px !important;
    font-weight: 850;
    margin-top: 7px;
}
.mentor-description {
    color: #64748B !important;
    font-size: 14px !important;
    line-height: 1.7;
    margin-top: 8px;
}
.mentor-context-grid {
    display: grid;
    grid-template-columns: repeat(4,minmax(0,1fr));
    gap: 14px;
    margin-bottom: 20px;
}
.mentor-context-card {
    padding: 17px;
    border-radius: 17px;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
}
.mentor-context-label {
    color: #94A3B8 !important;
    font-size: 9px !important;
    font-weight: 800;
    text-transform: uppercase;
}
.mentor-context-value {
    color: #0F172A !important;
    font-size: 13px !important;
    font-weight: 800;
    margin-top: 6px;
}
</style>
""",
        unsafe_allow_html=True,
    )
