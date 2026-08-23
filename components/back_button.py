import streamlit as st


def render_back_to_school_dashboard(
    key="back_to_school_dashboard",
):

    if st.button(
        "← Dashboard",
        key=key,
        use_container_width=False,
    ):

        st.session_state.school_navigation = (
            "🏠 Student Home"
        )

        st.rerun()