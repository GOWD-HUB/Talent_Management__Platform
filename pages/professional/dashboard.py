import streamlit as st

from database.professional_repository import get_professional_profile
from services.professional.profile_service import profile_completion
from services.professional.promotion_service import promotion_readiness
from services.professional.career_service import role_matches
from services.professional.salary_service import salary_gap
from styles.professional.theme import (
    apply_professional_theme,
    hero,
    section,
    metrics,
)


def render():
    apply_professional_theme()

    uid = st.session_state.get("user_id")

    if not uid:
        st.error("User session not found.")
        return

    p = get_professional_profile(uid) or {}

    name = (
        st.session_state.get("user_name")
        or p.get("full_name")
        or "Professional"
    )

    completion = profile_completion(p)
    promotion = promotion_readiness(p)
    matches = role_matches(p)
    best = matches[0] if matches else {"role": "Not available", "score": 0}
    salary = salary_gap(p)

    hero(
        f"Welcome back, {name} 👋",
        "Your professional growth workspace brings together promotion readiness, "
        "career transitions, job matching, learning, leadership and salary goals.",
        "🚀 TALENTSPHERE PROFESSIONAL PORTAL",
    )

    metrics(
        [
            ("📈", "PROMOTION READINESS", f"{promotion['score']}%", "Technical, leadership and communication readiness."),
            ("🎯", "BEST ROLE MATCH", f"{best['score']}%", best["role"]),
            ("💰", "TARGET SALARY", f"{salary['target']:.1f} LPA", f"Current: {salary['current']:.1f} LPA"),
            ("👤", "PROFILE STRENGTH", f"{completion}%", "Complete profile for stronger recommendations."),
        ]
    )

    section(
        "⚡ Professional Quick Access",
        "Open your core growth and career-development tools.",
        "Growth Workspace",
    )

    pages = [
        ("👤", "Professional Profile", "Build and update your professional growth profile."),
        ("📈", "Promotion Readiness", "Evaluate readiness for your next level."),
        ("🔄", "Career Transition", "Discover realistic transition pathways."),
        ("💼", "Advanced Job Matching", "Compare your stack with senior professional roles."),
        ("🎓", "Learning Academy", "Follow structured six-week development tracks."),
        ("💰", "Career & Salary Insights", "Build a practical 90-day salary-growth plan."),
        ("📡", "Industry Trends", "Review major professional skill trends."),
        ("🏅", "Certifications", "Get role-aligned certification suggestions."),
        ("🧭", "Leadership Evaluation", "Assess leadership and management capability."),
        ("📄", "AI Growth Report", "Download your professional development report."),
    ]

    for i in range(0, len(pages), 2):
        row = pages[i:i+2]
        cols = st.columns(len(row))

        for col, (icon, title, desc) in zip(cols, row):
            with col:
                st.html(
                    f"""<div class="pro-panel" style="min-height:145px;margin-bottom:14px;">
                    <div style="font-size:24px;">{icon}</div>
                    <div class="pro-row-title" style="margin-top:10px;">{title}</div>
                    <div class="pro-row-sub">{desc}</div>
                    </div>"""
                )

    section(
        "🎯 Current Growth Direction",
        "A snapshot based on your saved profile.",
    )

    target_role = p.get("target_role") or "Set your target role"
    promotion_goal = p.get("promotion_goal") or "Add a promotion goal"
    career_goal = p.get("career_goal") or "Add your career goal"

    st.html(
        f"""<div class="pro-mini-grid">
        <div class="pro-card">
            <div class="pro-label">TARGET ROLE</div>
            <div class="pro-value" style="font-size:18px;">{target_role}</div>
            <div class="pro-caption">Your preferred next professional role.</div>
        </div>
        <div class="pro-card">
            <div class="pro-label">PROMOTION GOAL</div>
            <div class="pro-value" style="font-size:18px;">{promotion_goal}</div>
            <div class="pro-caption">Your next-level objective.</div>
        </div>
        <div class="pro-card">
            <div class="pro-label">CAREER GOAL</div>
            <div class="pro-value" style="font-size:18px;">{career_goal}</div>
            <div class="pro-caption">Your longer-term development direction.</div>
        </div>
        </div>"""
    )
