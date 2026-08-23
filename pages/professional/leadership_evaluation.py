import streamlit as st

from services.professional.leadership_service import QUESTIONS, evaluate
from styles.professional.theme import (
    apply_professional_theme,
    hero,
    section,
    metrics,
)


def render():
    apply_professional_theme()

    hero(
        "Leadership Evaluation",
        "Assess delegation, coaching, conflict management, stakeholder communication, "
        "ownership, mentoring, execution and decision-making.",
        "🧭 LEADERSHIP ASSESSMENT",
    )

    section(
        "📝 Leadership Self-Assessment",
        "Rate each statement from 1 (strongly disagree) to 5 (strongly agree).",
        "10 Questions",
    )

    responses = []

    with st.form("professional_leadership_assessment"):
        for index, question in enumerate(QUESTIONS, start=1):
            st.markdown(
                f"**{index}. {question['text']}**"
            )

            value = st.slider(
                question["area"],
                min_value=1,
                max_value=5,
                value=3,
                key=f"leadership_q_{index}",
            )

            responses.append(value)

        submitted = st.form_submit_button(
            "🧭 Evaluate Leadership Readiness",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        st.session_state["professional_leadership_result"] = evaluate(responses)

    result = st.session_state.get("professional_leadership_result")

    if not result:
        st.info("Complete the assessment to view your leadership profile.")
        return

    metrics(
        [
            ("🧭", "LEADERSHIP SCORE", f"{result['score']}%", "Overall self-assessment result."),
            ("✅", "STRONG AREAS", len(result["strengths"]), "Areas at or above 75%."),
            ("🎯", "IMPROVEMENTS", len(result["improvements"]), "Areas below 60%."),
            ("📊", "CAPABILITIES", len(result["areas"]), "Leadership dimensions assessed."),
        ]
    )

    st.progress(result["score"] / 100)

    section(
        "📊 Capability Breakdown",
        "Review your leadership dimensions.",
    )

    for area, score in result["areas"].items():
        c1, c2 = st.columns([5, 1])

        with c1:
            st.markdown(f"**{area}**")

        with c2:
            st.markdown(f"**{score}%**")

        st.progress(score / 100)

    if result["improvements"]:
        section(
            "🎯 Development Priorities",
            "Focus on these areas during your next growth cycle.",
        )

        for item in result["improvements"]:
            st.warning(item)
