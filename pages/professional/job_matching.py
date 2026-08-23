import streamlit as st

from database.professional_repository import get_professional_profile
from services.professional.career_service import role_matches
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

    matches = role_matches(p)
    best = matches[0] if matches else {"role": "Not available", "score": 0, "present": [], "missing": []}

    hero(
        "Advanced Job Matching",
        "Compare your professional technology stack and transferable strengths "
        "with senior technical and leadership-oriented roles.",
        "💼 PROFESSIONAL ROLE MATCHING",
    )

    suitable = len([item for item in matches if item["score"] >= 50])

    metrics(
        [
            ("🏆", "BEST ROLE", best["role"], "Highest professional role alignment."),
            ("📈", "BEST MATCH", f"{best['score']}%", "Current skill fit."),
            ("💼", "SUITABLE ROLES", suitable, "Roles at or above 50% match."),
            ("🧩", "TOP GAPS", len(best["missing"]), "Missing skills for best match."),
        ]
    )

    section(
        "📊 Role Match Ranking",
        "Review matched and missing capabilities for each role.",
        "Professional Fit",
    )

    for rank, item in enumerate(matches, start=1):
        st.html(
            f"""<div class="pro-row">
            <div class="pro-row-kicker">MATCH #{rank}</div>
            <div style="display:flex;justify-content:space-between;gap:20px;">
                <div>
                    <div class="pro-row-title">{item['role']}</div>
                    <div class="pro-row-sub">
                        {len(item['present'])} matched • {len(item['missing'])} missing
                    </div>
                </div>
                <div class="pro-value" style="font-size:23px;color:#2563eb;">
                    {item['score']}%
                </div>
            </div>
            </div>"""
        )

        with st.expander(f"View {item['role']} skill analysis"):
            left, right = st.columns(2)

            with left:
                st.markdown("#### ✅ Matching")
                if item["present"]:
                    for skill in item["present"]:
                        st.success(skill)
                else:
                    st.caption("No matching skills detected.")

            with right:
                st.markdown("#### ❌ Missing")
                if item["missing"]:
                    for skill in item["missing"]:
                        st.warning(skill)
                else:
                    st.success("No major gaps.")
