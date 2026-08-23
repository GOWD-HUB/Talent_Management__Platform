import streamlit as st

from database.professional_repository import get_professional_profile
from styles.professional.theme import (
    apply_professional_theme,
    hero,
    section,
    metrics,
)


TRENDS = [
    ("🤖", "AI-Augmented Engineering", "Developers increasingly benefit from AI-assisted coding, testing, documentation and workflow automation.", ["AI tools", "Prompting", "Code review", "Automation"]),
    ("☁️", "Cloud-Native Development", "Cloud deployment, containers, observability and managed services remain important for modern software delivery.", ["Cloud", "Docker", "Kubernetes", "Observability"]),
    ("🏗️", "System Design & Reliability", "Senior engineering roles expect stronger architecture, scalability, reliability and trade-off reasoning.", ["System Design", "Caching", "Databases", "Messaging"]),
    ("🔐", "Security by Design", "Authentication, authorization, secure APIs, secrets and software supply-chain awareness are increasingly important.", ["Security", "OAuth/JWT", "OWASP", "Secrets"]),
    ("📊", "Data & Experimentation", "Professionals benefit from data-informed decisions, metrics, dashboards and experimentation.", ["SQL", "Analytics", "Metrics", "Experimentation"]),
    ("🧭", "Technical Leadership", "Senior contributors need mentoring, stakeholder communication, ownership and decision-making skills.", ["Leadership", "Mentoring", "Communication", "Ownership"]),
]


def render():
    apply_professional_theme()

    uid = st.session_state.get("user_id")

    p = get_professional_profile(uid) if uid else {}

    hero(
        "Industry Trends",
        "Review broad professional skill trends and map them against your current growth direction.",
        "📡 PROFESSIONAL TRENDS",
    )

    metrics(
        [
            ("📡", "TREND AREAS", len(TRENDS), "Major professional development themes."),
            ("🎯", "TARGET ROLE", p.get("target_role") or "Not added", "Your current career destination."),
            ("🏢", "INDUSTRY", p.get("industry") or "Not added", "Saved professional industry."),
            ("🧠", "TECH LEVEL", p.get("technical_level") or "Not added", "Current self-assessed technical level."),
        ]
    )

    st.caption(
        "These are general development themes included in TalentSphere. "
        "They are not live labor-market statistics."
    )

    section(
        "📈 Development Themes",
        "Skills worth considering in a modern professional development plan.",
    )

    for icon, title, desc, skills in TRENDS:
        chips = "".join(
            f'<span class="pro-chip">{skill}</span>'
            for skill in skills
        )

        st.html(
            f"""<div class="pro-row">
            <div style="font-size:24px;">{icon}</div>
            <div class="pro-row-title">{title}</div>
            <div class="pro-row-sub">{desc}</div>
            <div style="margin-top:9px;">{chips}</div>
            </div>"""
        )
