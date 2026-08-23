import streamlit as st

from database.professional_repository import get_professional_profile
from services.professional.promotion_service import promotion_readiness
from styles.professional.theme import (
    apply_professional_theme,
    hero,
    section,
    metrics,
)


def render():
    apply_professional_theme()

    uid = st.session_state.get("user_id")
    p = get_professional_profile(uid) if uid else {}

    result = promotion_readiness(p)

    hero(
        "Promotion Readiness",
        "Evaluate whether your technical capability, leadership exposure, "
        "communication, experience and professional evidence support your next promotion.",
        "📈 CAREER PROGRESSION",
    )

    metrics(
        [
            ("📈", "READINESS SCORE", f"{result['score']}%", "Overall promotion readiness."),
            ("💻", "TECHNICAL", f"{result['factors']['Technical']}%", "Current technical maturity."),
            ("🧭", "LEADERSHIP", f"{result['factors']['Leadership']}%", "Leadership and ownership exposure."),
            ("🎙️", "COMMUNICATION", f"{result['factors']['Communication']}%", "Professional communication strength."),
        ]
    )

    st.progress(result["score"] / 100)

    if result["score"] >= 80:
        st.success("Strong promotion readiness. Focus on measurable impact and sponsorship.")
    elif result["score"] >= 60:
        st.info("Good foundation. Close the remaining gaps before your next promotion discussion.")
    else:
        st.warning("Promotion readiness needs focused development across the weakest factors.")

    section(
        "📊 Readiness Factors",
        "Detailed capability breakdown.",
    )

    for name, score in result["factors"].items():
        c1, c2 = st.columns([5, 1])

        with c1:
            st.markdown(f"**{name}**")

        with c2:
            st.markdown(f"**{score}%**")

        st.progress(score / 100)

    section(
        "🎯 Promotion Gap Plan",
        "Prioritize the factors below during your next development cycle.",
        "Action Plan",
    )

    if result["gaps"]:
        for index, gap in enumerate(result["gaps"], start=1):
            st.html(
                f"""<div class="pro-row">
                <div class="pro-row-kicker">PRIORITY {index:02d}</div>
                <div class="pro-row-title">{gap}</div>
                <div class="pro-row-sub">
                    Create one measurable development goal and one piece of evidence
                    that demonstrates improvement in {gap.lower()}.
                </div>
                </div>"""
            )
    else:
        st.success("No major promotion-readiness gaps detected.")
