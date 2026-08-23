import streamlit as st

from services.professional.learning_service import TRACKS, six_week_plan
from styles.professional.theme import (
    apply_professional_theme,
    hero,
    section,
    metrics,
)


def render():
    apply_professional_theme()

    hero(
        "Professional Learning Academy",
        "Choose from six structured development tracks. Each track includes modules, "
        "a six-week roadmap, hands-on practice, a portfolio project and final assessment.",
        "🎓 LEARNING ACADEMY",
    )

    metrics(
        [
            ("🎓", "LEARNING TRACKS", 6, "Backend, System Design, Cloud, DevOps, Leadership and Communication."),
            ("🗓️", "ROADMAP", "6 Weeks", "Structured weekly progression."),
            ("🚀", "PORTFOLIO PROJECT", "1 / Track", "Applied professional evidence."),
            ("✅", "FINAL ASSESSMENT", "Included", "Track-end evaluation."),
        ]
    )

    section(
        "🧭 Choose Your Track",
        "Select a professional growth area.",
        "6 Tracks",
    )

    track_name = st.selectbox(
        "Learning Track",
        list(TRACKS.keys()),
    )

    track = TRACKS[track_name]

    st.html(
        f"""<div class="pro-panel">
        <div style="font-size:30px;">{track['icon']}</div>
        <div class="pro-row-title" style="font-size:22px;margin-top:8px;">{track_name}</div>
        <div class="pro-row-sub">
            Structured professional development track with six modules,
            applied practice and a final assessment.
        </div>
        </div>"""
    )

    section(
        "📘 Modules",
        "Core learning sequence.",
    )

    for index, module in enumerate(track["modules"], start=1):
        st.html(
            f"""<div class="pro-row">
            <div class="pro-row-kicker">MODULE {index:02d}</div>
            <div class="pro-row-title">{module}</div>
            </div>"""
        )

    section(
        "🗓️ Six-Week Roadmap",
        "One focused module per week.",
        "6 Weeks",
    )

    for item in six_week_plan(track_name):
        st.html(
            f"""<div class="pro-row">
            <div class="pro-row-kicker">WEEK {item['week']}</div>
            <div class="pro-row-title">{item['focus']}</div>
            <div class="pro-row-sub">{item['practice']}</div>
            </div>"""
        )

    section(
        "🚀 Portfolio Project",
        "Convert learning into evidence.",
    )
    st.success(track["project"])

    section(
        "✅ Final Assessment",
        "Validate your track completion.",
    )
    st.info(track["assessment"])
