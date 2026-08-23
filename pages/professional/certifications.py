import streamlit as st

from database.professional_repository import get_professional_profile
from styles.professional.theme import (
    apply_professional_theme,
    hero,
    section,
    metrics,
)


CERTS = {
    "Cloud / DevOps": [
        ("AWS Certified Solutions Architect", "Cloud architecture and AWS services."),
        ("Microsoft Azure Administrator", "Azure administration and cloud operations."),
        ("Google Associate Cloud Engineer", "GCP deployment and operations."),
        ("Certified Kubernetes Administrator", "Kubernetes administration and operations."),
    ],
    "Data / AI": [
        ("Azure AI Engineer Associate", "Applied AI solutions on Microsoft Azure."),
        ("Google Professional Machine Learning Engineer", "ML systems on Google Cloud."),
        ("Databricks Data Engineer", "Modern data engineering and lakehouse workflows."),
    ],
    "Security": [
        ("CompTIA Security+", "Foundational security concepts and practices."),
        ("Certified Ethical Hacker", "Security testing and ethical hacking concepts."),
    ],
    "Leadership / Product": [
        ("Professional Scrum Master", "Agile leadership and Scrum practices."),
        ("PMP / CAPM", "Project management and delivery fundamentals."),
    ],
}


def render():
    apply_professional_theme()

    uid = st.session_state.get("user_id")
    p = get_professional_profile(uid) if uid else {}

    hero(
        "Certification Suggestions",
        "Explore professional certifications aligned with cloud, data, AI, security, "
        "delivery and leadership development.",
        "🏅 PROFESSIONAL CREDENTIALS",
    )

    metrics(
        [
            ("🏅", "CERTIFICATION AREAS", len(CERTS), "Professional development categories."),
            ("🎯", "TARGET ROLE", p.get("target_role") or "Not added", "Use your goal to prioritize credentials."),
            ("📚", "CURRENT CERTIFICATIONS", len([x for x in str(p.get('certifications') or '').split(',') if x.strip()]), "Saved in Professional Profile."),
            ("⏱️", "LEARNING HOURS", f"{p.get('preferred_learning_hours') or 5}/wk", "Available weekly study time."),
        ]
    )

    st.info(
        "Certifications can support a profile, but hands-on projects, work impact and interview performance remain important."
    )

    section(
        "🎓 Suggested Certification Paths",
        "Choose credentials based on role requirements rather than collecting certificates.",
    )

    for category, items in CERTS.items():
        with st.expander(f"🏅 {category}", expanded=False):
            for name, description in items:
                st.html(
                    f"""<div class="pro-row">
                    <div class="pro-row-title">{name}</div>
                    <div class="pro-row-sub">{description}</div>
                    </div>"""
                )
