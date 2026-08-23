import html as html_lib
import streamlit as st

from components.back_button import (
    render_back_to_school_dashboard,
)

from database.school_repository import (
    get_school_profile,
)

from services.recommendation_service import (
    build_recommendations,
)

from styles.recommendation_theme import (
    apply_recommendation_theme,
)


def safe(value):
    return html_lib.escape(str(value or ""))


def render_card(item):
    st.html(
        f"""
<div class="rec-card">
    <div class="rec-icon">{safe(item["icon"])}</div>
    <div class="rec-card-title">{safe(item["title"])}</div>
    <div class="rec-card-text">{safe(item["description"])}</div>
    <div class="rec-action"><b>Next step:</b> {safe(item["action"])}</div>
</div>
"""
    )


def render():

    apply_recommendation_theme()

    render_back_to_school_dashboard(
        key="recommendations_back_dashboard",
    )

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.error("Unable to identify the logged-in student.")
        return

    try:
        profile = get_school_profile(user_id) or {}
    except Exception:
        profile = {}

    interest_results = st.session_state.get(
        "interest_assessment_results"
    )

    selected_area = st.session_state.get(
        "selected_career_area"
    )

    quiz_result = st.session_state.get(
        "subject_quiz_result"
    )

    recommendations = build_recommendations(
        profile=profile,
        interest_results=interest_results,
        selected_area=selected_area,
        quiz_result=quiz_result,
    )

    name = (
        st.session_state.get("user_name")
        or "Student"
    )

    st.html(
        f"""
<div class="rec-hero">
    <div class="rec-eyebrow">PERSONALISED STUDENT GUIDANCE</div>
    <div class="rec-title">✨ Recommendations for {safe(name)}</div>
    <div class="rec-description">
        These recommendations combine your School Profile,
        Interest Assessment, selected career area and recent
        Subject Quiz activity to suggest useful next steps.
    </div>
</div>
"""
    )

    st.markdown("## 🎯 Your Recommended Next Steps")

    for start in range(0, len(recommendations), 3):
        row = recommendations[start:start + 3]
        cols = st.columns(len(row))

        for index, item in enumerate(row):
            with cols[index]:
                render_card(item)

    st.divider()
    st.markdown("## 🚀 Open a Learning Tool")

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button(
            "🔍 Career Explorer",
            key="rec_career",
            use_container_width=True,
        ):
            st.session_state.school_navigation = "🔍 Career Explorer"
            st.rerun()

    with c2:
        if st.button(
            "📊 Interest Assessment",
            key="rec_interest",
            use_container_width=True,
        ):
            st.session_state.school_navigation = "📊 Interest Assessment"
            st.rerun()

    with c3:
        if st.button(
            "🛣️ Skills Roadmap",
            key="rec_roadmap",
            use_container_width=True,
        ):
            st.session_state.school_navigation = "🛣️ Skills Roadmap"
            st.rerun()

    c4, c5 = st.columns(2)

    with c4:
        if st.button(
            "📝 Subject Quiz",
            key="rec_quiz",
            use_container_width=True,
        ):
            st.session_state.school_navigation = "📝 Subject Quiz"
            st.rerun()

    with c5:
        if st.button(
            "👤 Update School Profile",
            key="rec_profile",
            use_container_width=True,
        ):
            st.session_state.school_navigation = "👤 School Profile"
            st.rerun()
