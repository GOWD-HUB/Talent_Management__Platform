import streamlit as st

from database.professional_repository import get_professional_profile
from services.professional.salary_service import salary_gap, ninety_day_salary_plan
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

    result = salary_gap(p)

    hero(
        "Career & Salary Insights",
        "Compare your current and target compensation goals and build a practical "
        "90-day professional-growth plan around skills, evidence and opportunity conversion.",
        "💰 CAREER & SALARY GROWTH",
    )

    metrics(
        [
            ("💵", "CURRENT SALARY", f"{result['current']:.1f} LPA", "Saved current compensation."),
            ("🎯", "TARGET SALARY", f"{result['target']:.1f} LPA", "Your compensation goal."),
            ("📈", "ABSOLUTE GAP", f"{result['gap']:.1f} LPA", "Difference to target."),
            ("🚀", "GROWTH NEEDED", f"{result['growth_percent']}%", "Required increase from current salary."),
        ]
    )

    if result["target"] <= 0:
        st.warning("Add your target salary in Professional Profile for a complete analysis.")
    elif result["current"] <= 0:
        st.info("Add current salary to calculate the growth percentage.")
    elif result["target"] <= result["current"]:
        st.success("Your target salary is already at or below your current compensation.")
    else:
        st.info(
            "Use the salary goal as a development target, not a guarantee. "
            "Actual compensation depends on role, market, location, company and interview performance."
        )

    section(
        "🗺️ 90-Day Growth Plan",
        "Build the skills and evidence needed to improve career leverage.",
        "Action Plan",
    )

    cols = st.columns(3)

    for col, phase in zip(cols, ninety_day_salary_plan(p)):
        with col:
            items = "".join(
                f"<li>{action}</li>"
                for action in phase["actions"]
            )

            st.html(
                f"""<div class="pro-panel" style="min-height:270px;">
                <div class="pro-row-kicker">{phase['period']}</div>
                <div class="pro-row-title">{phase['title']}</div>
                <ul class="pro-row-sub" style="padding-left:18px;line-height:1.8;">
                    {items}
                </ul>
                </div>"""
            )
