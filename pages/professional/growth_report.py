import re
import streamlit as st

from database.professional_repository import get_professional_profile
from services.professional.report_service import build_growth_report, make_pdf
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

    leadership_result = st.session_state.get(
        "professional_leadership_result",
        {}
    )

    report = build_growth_report(
        p,
        leadership_result,
    )

    best = report["best_match"]

    hero(
        "AI Growth Report",
        "Your consolidated professional development report covering promotion readiness, "
        "role fit, leadership, salary goals and a 90-day action plan.",
        "📄 PROFESSIONAL GROWTH REPORT",
    )

    metrics(
        [
            ("🚀", "GROWTH READINESS", f"{report['readiness']}%", "Combined professional development index."),
            ("📈", "PROMOTION", f"{report['promotion']['score']}%", "Promotion-readiness score."),
            ("🎯", "BEST ROLE MATCH", f"{best['score']}%", best["role"]),
            ("🧭", "LEADERSHIP", f"{leadership_result.get('score', 0)}%", "Leadership evaluation result."),
        ]
    )

    st.progress(report["readiness"] / 100)

    section(
        "🎯 Priority Growth Gaps",
        "Highest-value development areas from your role match.",
    )

    if best.get("missing"):
        for item in best["missing"][:6]:
            st.warning(item)
    else:
        st.success("No major target-role gaps detected.")

    section(
        "💰 Salary Goal",
        "Saved compensation target.",
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Current", f"{report['salary']['current']:.1f} LPA")

    with c2:
        st.metric("Target", f"{report['salary']['target']:.1f} LPA")

    with c3:
        st.metric("Gap", f"{report['salary']['gap']:.1f} LPA")

    section(
        "🗺️ 90-Day Development Plan",
        "A practical professional-growth sequence.",
        "90 Days",
    )

    phases = [
        ("Days 1–30", "Foundation & Positioning", "Close the most important technical gap and document measurable work impact."),
        ("Days 31–60", "Evidence & Leadership", "Build portfolio evidence, improve visibility and practice leadership or system-design scenarios."),
        ("Days 61–90", "Opportunity Conversion", "Apply to matched roles, collect feedback and strengthen negotiation readiness."),
    ]

    cols = st.columns(3)

    for col, phase in zip(cols, phases):
        with col:
            st.html(
                f"""<div class="pro-panel" style="min-height:220px;">
                <div class="pro-row-kicker">{phase[0]}</div>
                <div class="pro-row-title">{phase[1]}</div>
                <div class="pro-row-sub">{phase[2]}</div>
                </div>"""
            )

    section(
        "📥 Download Report",
        "Export your professional growth report as PDF.",
    )

    try:
        pdf = make_pdf(
            p,
            report,
        )

        name = (
            p.get("full_name")
            or st.session_state.get("user_name")
            or "Professional"
        )

        safe_name = re.sub(
            r"[^A-Za-z0-9_-]+",
            "_",
            str(name),
        ).strip("_") or "Professional"

        st.download_button(
            "📥 Download Professional Growth Report PDF",
            data=pdf,
            file_name=f"{safe_name}_TalentSphere_Professional_Growth_Report.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True,
        )

    except Exception as error:
        st.error(
            f"Unable to generate PDF: {error}. Install ReportLab using: pip install reportlab"
        )
