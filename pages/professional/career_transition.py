import streamlit as st

from database.professional_repository import get_professional_profile
from services.professional.career_service import transition_suggestions
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

    suggestions = transition_suggestions(p)
    best = suggestions[0] if suggestions else {"role": "Not available", "score": 0, "missing": []}

    hero(
        "Career Transition Suggestions",
        "Identify realistic professional transitions based on your current stack, "
        "leadership capability and transferable strengths.",
        "🔄 CAREER TRANSITION",
    )

    metrics(
        [
            ("🎯", "TOP TRANSITION", best["role"], "Highest transferable-skill alignment."),
            ("📊", "ROLE FIT", f"{best['score']}%", "Current transition readiness."),
            ("🧩", "SKILL GAPS", len(best.get("missing", [])), "Priority capabilities to build."),
            ("🛣️", "OPTIONS", len(suggestions), "Suggested transition pathways."),
        ]
    )

    section(
        "🧭 Recommended Transition Paths",
        "Role suggestions ordered by current fit.",
        "Top Matches",
    )

    for rank, item in enumerate(suggestions, start=1):
        st.html(
            f"""<div class="pro-row">
            <div class="pro-row-kicker">PATH #{rank}</div>
            <div style="display:flex;justify-content:space-between;gap:18px;">
                <div>
                    <div class="pro-row-title">{item['role']}</div>
                    <div class="pro-row-sub">
                        Present: {", ".join(item['present']) or "None"}<br/>
                        Missing: {", ".join(item['missing'][:4]) or "No major gaps"}
                    </div>
                </div>
                <div class="pro-value" style="font-size:22px;color:#4f46e5;">
                    {item['score']}%
                </div>
            </div>
            </div>"""
        )

    section(
        "🗓️ Transition Strategy",
        "Use a simple three-phase approach.",
    )

    c1, c2, c3 = st.columns(3)

    phases = [
        ("1–30 Days", "Bridge Fundamentals", "Close the first 1–2 missing skills and map transferable experience."),
        ("31–60 Days", "Build Evidence", "Create a role-relevant project or work sample and improve your professional profile."),
        ("61–90 Days", "Convert Opportunities", "Practice transition interviews, apply to matched roles and track feedback."),
    ]

    for col, phase in zip((c1, c2, c3), phases):
        with col:
            st.html(
                f"""<div class="pro-panel" style="min-height:200px;">
                <div class="pro-row-kicker">{phase[0]}</div>
                <div class="pro-row-title">{phase[1]}</div>
                <div class="pro-row-sub">{phase[2]}</div>
                </div>"""
            )
