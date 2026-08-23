from io import BytesIO
from datetime import datetime
import html

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from .profile_service import profile_completion
from .promotion_service import promotion_readiness
from .career_service import role_matches
from .salary_service import salary_gap


def build_growth_report(profile, leadership_result=None):
    promotion = promotion_readiness(profile)
    matches = role_matches(profile)
    salary = salary_gap(profile)

    best = matches[0] if matches else {
        "role": "Not available",
        "score": 0,
        "missing": [],
    }

    leadership_score = (
        leadership_result.get("score", 0)
        if isinstance(leadership_result, dict)
        else 0
    )

    readiness = round(
        profile_completion(profile) * 0.20
        + promotion["score"] * 0.35
        + best["score"] * 0.30
        + leadership_score * 0.15
    )

    return {
        "readiness": max(0, min(100, readiness)),
        "promotion": promotion,
        "matches": matches,
        "best_match": best,
        "salary": salary,
        "leadership": leadership_result or {},
    }


def make_pdf(profile, report):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        title="TalentSphere Professional Growth Report",
    )

    styles = getSampleStyleSheet()

    title = ParagraphStyle(
        "TitleX",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#0F172A"),
    )

    section = ParagraphStyle(
        "SectionX",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#4F46E5"),
        spaceBefore=9,
        spaceAfter=5,
    )

    body = ParagraphStyle(
        "BodyX",
        parent=styles["BodyText"],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
    )

    story = [
        Paragraph("TalentSphere Elevate", section),
        Paragraph("Professional Growth Report", title),
        Paragraph(
            f"Generated {datetime.now().strftime('%d %B %Y')}",
            body
        ),
        Spacer(1, 5 * mm),
        Paragraph("Professional Profile", section),
    ]

    rows = [
        ["Current Role", str(profile.get("current_role") or "Not added")],
        ["Experience", f"{profile.get('experience_years') or 0} years"],
        ["Target Role", str(profile.get("target_role") or "Not added")],
        ["Industry", str(profile.get("industry") or "Not added")],
        ["Technical Stack", str(profile.get("tech_stack") or "Not added")],
    ]

    table = Table(rows, colWidths=[45 * mm, 130 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F8FAFC")),
                ("GRID", (0, 0), (-1, -1), .4, colors.HexColor("#E2E8F0")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(table)

    story += [
        Paragraph("Growth Readiness", section),
        Paragraph(
            f"Overall Growth Readiness: <b>{report['readiness']}%</b><br/>"
            f"Promotion Readiness: <b>{report['promotion']['score']}%</b><br/>"
            f"Best Role Match: <b>{html.escape(report['best_match']['role'])}</b> "
            f"({report['best_match']['score']}%)",
            body
        ),
        Paragraph("Priority Skill Gaps", section),
        Paragraph(
            html.escape(
                ", ".join(report["best_match"].get("missing", [])[:6])
                or "No major gaps detected"
            ),
            body
        ),
        Paragraph("Salary Goal", section),
        Paragraph(
            f"Current: {report['salary']['current']:.1f} LPA<br/>"
            f"Target: {report['salary']['target']:.1f} LPA<br/>"
            f"Gap: {report['salary']['gap']:.1f} LPA",
            body
        ),
        Paragraph("90-Day Development Plan", section),
        Paragraph(
            "Days 1–30: close high-priority technical gaps and identify measurable impact.<br/>"
            "Days 31–60: build portfolio evidence, improve visibility and practice advanced interviews.<br/>"
            "Days 61–90: apply to matched opportunities, collect feedback and strengthen negotiation readiness.",
            body
        ),
    ]

    doc.build(story)

    data = buffer.getvalue()
    buffer.close()
    return data
