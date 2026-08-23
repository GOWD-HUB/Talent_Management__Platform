# ==========================================================
# TALENTSPHERE ELEVATE
# FINAL COLLEGE PLACEMENT REPORT
# pages/college/college_report.py
# ==========================================================

from io import BytesIO
from datetime import datetime
import html
import re

import streamlit as st

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
)

import database.college_repository as college_repo
from styles.college.theme import apply_college_theme


# ==========================================================
# ROLE REQUIREMENTS
# Used only for final-report role-fit calculations.
# ==========================================================

ROLE_REQUIREMENTS = {
    "Software Development Engineer": [
        "Python", "Java", "C++", "DSA", "OOP",
        "DBMS", "SQL", "Git", "REST API"
    ],
    "Full Stack Developer": [
        "HTML", "CSS", "JavaScript", "React",
        "Node.js", "Express", "MongoDB", "SQL",
        "REST API", "Git"
    ],
    "Frontend Developer": [
        "HTML", "CSS", "JavaScript", "React",
        "Responsive Design", "Git", "REST API"
    ],
    "Backend Developer": [
        "Python", "Java", "Node.js", "FastAPI",
        "Django", "SQL", "MongoDB", "REST API",
        "Authentication", "Git"
    ],
    "Data Analyst": [
        "Python", "SQL", "Excel", "Pandas",
        "NumPy", "Power BI", "Tableau",
        "Statistics", "Data Visualization"
    ],
    "Data Scientist": [
        "Python", "SQL", "Pandas", "NumPy",
        "Statistics", "Machine Learning",
        "Data Visualization", "Scikit-learn"
    ],
    "Machine Learning Engineer": [
        "Python", "Machine Learning", "Deep Learning",
        "Scikit-learn", "TensorFlow", "PyTorch",
        "Pandas", "NumPy", "Git"
    ],
    "AI Engineer": [
        "Python", "Machine Learning", "Deep Learning",
        "NLP", "Computer Vision", "TensorFlow",
        "PyTorch", "REST API", "Git"
    ],
    "Cloud Engineer": [
        "AWS", "Azure", "GCP", "Linux",
        "Networking", "Docker", "Cloud Computing", "Git"
    ],
    "DevOps Engineer": [
        "Linux", "Git", "Docker", "Kubernetes",
        "CI/CD", "Jenkins", "AWS", "Shell Scripting"
    ],
    "Cybersecurity Engineer": [
        "Networking", "Linux", "Cybersecurity",
        "Cryptography", "Web Security", "OWASP",
        "Python", "Security Testing"
    ],
    "QA / Test Engineer": [
        "Software Testing", "Manual Testing",
        "Automation Testing", "Selenium",
        "API Testing", "Postman", "SQL", "Git"
    ],
    "Business Analyst": [
        "Communication", "SQL", "Excel", "Data Analysis",
        "Requirement Analysis", "Documentation", "Power BI"
    ],
}


# ==========================================================
# GENERAL HELPERS
# ==========================================================

def safe_text(value, fallback="Not added"):
    if value is None:
        return fallback

    if isinstance(value, (list, tuple, set)):
        value = ", ".join(str(x) for x in value)

    if isinstance(value, dict):
        return fallback

    value = str(value).strip()

    if not value:
        return fallback

    if value.lower() in {
        "none", "null", "n/a", "na",
        "not added", "untouched", "unknown", "-"
    }:
        return fallback

    return value


def safe_float(value, default=0.0):
    try:
        if value is None:
            return default

        if isinstance(value, (int, float)):
            return float(value)

        value = str(value).strip().replace("%", "").replace(",", "")

        if not value:
            return default

        return float(value)

    except (ValueError, TypeError):
        return default


def safe_int(value, default=0):
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default


def clamp(value):
    try:
        value = int(round(float(value)))
    except Exception:
        value = 0

    return max(0, min(100, value))


def html_escape(value):
    return html.escape(str(value or ""))


def normalize_skill(value):
    return (
        str(value or "")
        .strip()
        .lower()
        .replace(".", "")
        .replace("-", " ")
    )


def split_items(value):
    if not value:
        return []

    if isinstance(value, (list, tuple, set)):
        values = list(value)
    else:
        text = str(value).replace(";", ",").replace("\n", ",")
        values = text.split(",")

    result = []

    for item in values:
        item = str(item).strip()
        if item and item not in result:
            result.append(item)

    return result


def extract_profile_skills(profile):
    skills = []

    for field in ("technical_skills", "soft_skills"):
        skills.extend(split_items(profile.get(field)))

    # Remove duplicates while preserving order
    unique = []
    seen = set()

    for skill in skills:
        key = normalize_skill(skill)
        if key and key not in seen:
            seen.add(key)
            unique.append(skill)

    return unique


# ==========================================================
# SAFE DATABASE ACCESS
# ==========================================================

def load_profile(user_id):
    try:
        return college_repo.get_college_profile(user_id) or {}
    except Exception:
        return {}


def load_placements(user_id):
    try:
        if hasattr(college_repo, "get_placements"):
            return college_repo.get_placements(user_id) or []
    except Exception:
        pass

    return []


def load_internships(user_id):
    try:
        if hasattr(college_repo, "get_internships"):
            return college_repo.get_internships(user_id) or []
    except Exception:
        pass

    return []


def load_hackathons(user_id):
    try:
        if hasattr(college_repo, "get_hackathons"):
            return college_repo.get_hackathons(user_id) or []
    except Exception:
        pass

    return []


# ==========================================================
# PROFILE COMPLETION
# ==========================================================

def calculate_profile_completion(profile):
    fields = [
        "college_name",
        "degree",
        "branch",
        "current_year",
        "semester",
        "graduation_year",
        "cgpa",
        "technical_skills",
        "projects",
        "internships",
        "preferred_role",
        "github_url",
        "linkedin_url",
    ]

    completed = 0

    for field in fields:
        value = profile.get(field)

        if field == "cgpa":
            if safe_float(value, 0.0) > 0:
                completed += 1
        elif safe_text(value, ""):
            completed += 1

    return clamp(
        completed / len(fields) * 100
        if fields
        else 0
    )


# ==========================================================
# RESUME READINESS
# ==========================================================

def calculate_resume_score(profile):
    score = 0

    checks = [
        ("college_name", 8),
        ("degree", 7),
        ("branch", 7),
        ("cgpa", 8),
        ("technical_skills", 15),
        ("projects", 15),
        ("internships", 12),
        ("certifications", 8),
        ("preferred_role", 7),
        ("github_url", 6),
        ("linkedin_url", 7),
    ]

    for field, weight in checks:
        value = profile.get(field)

        if field == "cgpa":
            if safe_float(value, 0.0) > 0:
                score += weight
        elif safe_text(value, ""):
            score += weight

    return clamp(score)


# ==========================================================
# ROLE MATCHING
# ==========================================================

def calculate_role_matches(profile):
    student_skills = extract_profile_skills(profile)

    normalized_student = {
        normalize_skill(skill)
        for skill in student_skills
        if normalize_skill(skill)
    }

    matches = []

    for role, required in ROLE_REQUIREMENTS.items():
        present = []
        missing = []

        for required_skill in required:
            target = normalize_skill(required_skill)

            found = any(
                target == current
                or target in current
                or current in target
                for current in normalized_student
            )

            if found:
                present.append(required_skill)
            else:
                missing.append(required_skill)

        score = clamp(
            len(present) / len(required) * 100
            if required
            else 0
        )

        matches.append(
            {
                "role": role,
                "score": score,
                "present": present,
                "missing": missing,
            }
        )

    matches.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return matches


# ==========================================================
# CODING READINESS
# ==========================================================

def calculate_coding_readiness():
    completed = st.session_state.get(
        "college_completed_problems",
        []
    )

    if not isinstance(completed, list):
        completed = []

    total = 15
    solved = len(set(completed))

    score = clamp(
        solved / total * 100
        if total
        else 0
    )

    return {
        "score": score,
        "solved": solved,
        "total": total,
    }


# ==========================================================
# INTERVIEW READINESS
# ==========================================================

def calculate_interview_readiness():
    prepared = st.session_state.get(
        "interview_completed",
        []
    )

    if not isinstance(prepared, list):
        prepared = []

    # Current interview module contains approximately 65 questions.
    # We avoid depending on that page's module import.
    total = max(65, len(prepared))
    count = len(set(prepared))

    score = clamp(
        count / total * 100
        if total
        else 0
    )

    return {
        "score": score,
        "prepared": count,
        "total": total,
    }


# ==========================================================
# GITHUB RESULT
# ==========================================================

def load_github_result():
    result = st.session_state.get(
        "github_analysis",
        {}
    )

    if not isinstance(result, dict):
        return {}

    return result


# ==========================================================
# LINKEDIN RESULT
# ==========================================================

def load_linkedin_result():
    # This key matches the LinkedIn PDF Review page.
    result = st.session_state.get(
        "linkedin_pdf_analysis",
        {}
    )

    if not isinstance(result, dict):
        return {}

    return result


# ==========================================================
# PLACEMENT TRACKER SUMMARY
# ==========================================================

def placement_summary(placements):
    total = len(placements)
    interviews = 0
    offers = 0
    rejected = 0

    for placement in placements:
        status = safe_text(
            placement.get("status"),
            ""
        ).lower()

        if any(word in status for word in [
            "interview", "round", "shortlist"
        ]):
            interviews += 1

        if any(word in status for word in [
            "offer", "selected", "placed"
        ]):
            offers += 1

        if any(word in status for word in [
            "reject", "not selected"
        ]):
            rejected += 1

    return {
        "total": total,
        "interviews": interviews,
        "offers": offers,
        "rejected": rejected,
    }


# ==========================================================
# OVERALL PLACEMENT READINESS
# ==========================================================

def calculate_overall_readiness(
    profile_score,
    resume_score,
    role_fit,
    coding_score,
    interview_score,
    github_score,
    linkedin_score,
):
    # Weighted final readiness index
    score = (
        profile_score * 0.15
        + resume_score * 0.15
        + role_fit * 0.20
        + coding_score * 0.15
        + interview_score * 0.15
        + github_score * 0.10
        + linkedin_score * 0.10
    )

    return clamp(score)


def readiness_label(score):
    if score >= 85:
        return "Placement Ready"

    if score >= 70:
        return "Strong"

    if score >= 55:
        return "Developing Well"

    if score >= 40:
        return "Needs Focus"

    return "Foundation Stage"


# ==========================================================
# STRENGTHS / IMPROVEMENTS / ACTION PLAN
# ==========================================================

def build_strengths(
    profile,
    role_match,
    coding,
    interview,
    github_score,
    linkedin_score,
    placements,
):
    strengths = []

    cgpa = safe_float(profile.get("cgpa"), 0.0)

    if cgpa >= 8:
        strengths.append(
            "Strong academic performance based on current CGPA."
        )

    if len(split_items(profile.get("technical_skills"))) >= 6:
        strengths.append(
            "Good technical skill coverage in the College Profile."
        )

    if safe_text(profile.get("projects"), ""):
        strengths.append(
            "Project experience provides practical technical evidence."
        )

    if safe_text(profile.get("internships"), ""):
        strengths.append(
            "Internship/training experience strengthens placement readiness."
        )

    if role_match and role_match["score"] >= 60:
        strengths.append(
            f"Strong alignment with {role_match['role']} at "
            f"{role_match['score']}% role fit."
        )

    if coding["score"] >= 60:
        strengths.append(
            "Coding practice progress is at a good placement-preparation level."
        )

    if interview["score"] >= 50:
        strengths.append(
            "Interview question preparation shows consistent progress."
        )

    if github_score >= 60:
        strengths.append(
            "GitHub portfolio provides useful recruiter-facing technical evidence."
        )

    if linkedin_score >= 60:
        strengths.append(
            "LinkedIn profile has a good professional readiness score."
        )

    if placements:
        strengths.append(
            "Placement applications are being actively tracked."
        )

    if not strengths:
        strengths.append(
            "The College Workspace has been started; completing more modules "
            "will create a stronger placement profile."
        )

    return strengths


def build_improvements(
    profile,
    role_match,
    coding,
    interview,
    github_score,
    linkedin_score,
):
    improvements = []

    if safe_float(profile.get("cgpa"), 0.0) <= 0:
        improvements.append(
            "Add your current CGPA to improve profile and resume completeness."
        )

    if len(split_items(profile.get("technical_skills"))) < 6:
        improvements.append(
            "Expand the technical skills section with role-relevant technologies."
        )

    if not safe_text(profile.get("projects"), ""):
        improvements.append(
            "Add at least 2 strong projects with technologies, features and your contribution."
        )

    if not safe_text(profile.get("internships"), ""):
        improvements.append(
            "Add internship, training, volunteering or practical experience."
        )

    if role_match and role_match["missing"]:
        priority = role_match["missing"][:3]
        improvements.append(
            "Priority skill gaps: " + ", ".join(priority) + "."
        )

    if coding["score"] < 60:
        improvements.append(
            "Increase coding practice, especially arrays, strings, searching, "
            "hashing, stacks and linked lists."
        )

    if interview["score"] < 50:
        improvements.append(
            "Prepare more HR, technical, coding, project and behavioral interview questions."
        )

    if github_score < 60:
        improvements.append(
            "Improve GitHub with 4–6 meaningful projects, README files, "
            "descriptions and pinned repositories."
        )

    if linkedin_score < 60:
        improvements.append(
            "Improve LinkedIn profile sections, skills, projects and recruiter-focused keywords."
        )

    return improvements


def build_action_plan(
    role_match,
    coding,
    interview,
    github_score,
    linkedin_score,
):
    missing = (
        role_match.get("missing", [])
        if role_match
        else []
    )

    first_skills = ", ".join(missing[:2]) if missing else "core role skills"
    second_skills = ", ".join(missing[2:4]) if len(missing) > 2 else "applied practice"

    return [
        {
            "period": "Days 1–30",
            "title": "Close Core Skill Gaps",
            "actions": [
                f"Focus first on {first_skills}.",
                "Study fundamentals and practice every day.",
                "Update College Profile after completing new skills.",
                "Solve at least 5 coding problems each week.",
            ],
        },
        {
            "period": "Days 31–60",
            "title": "Build Placement Evidence",
            "actions": [
                f"Work on {second_skills}.",
                "Build or improve one portfolio project.",
                "Strengthen GitHub README, project descriptions and repository quality.",
                "Improve resume and re-check target-role alignment.",
            ],
        },
        {
            "period": "Days 61–90",
            "title": "Become Interview Ready",
            "actions": [
                "Complete interview question preparation and mock interviews.",
                "Revise DSA, OOP, DBMS, SQL, OS, Networks and project explanations.",
                "Improve LinkedIn professional presence.",
                "Apply to suitable roles and update the Placement Tracker.",
            ],
        },
    ]


# ==========================================================
# PDF HELPERS
# ==========================================================

def pdf_safe(value, fallback=""):
    value = safe_text(value, fallback)

    if value == "Not added":
        return fallback

    return html.escape(str(value))


def build_college_report_pdf(data):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=14 * mm,
        bottomMargin=14 * mm,
        title="TalentSphere Elevate College Placement Report",
        author="TalentSphere Elevate",
    )

    styles = getSampleStyleSheet()

    NAVY = colors.HexColor("#0F172A")
    BLUE = colors.HexColor("#4F46E5")
    PURPLE = colors.HexColor("#7C3AED")
    GRAY = colors.HexColor("#475569")
    LIGHT = colors.HexColor("#F8FAFC")
    LINE = colors.HexColor("#E2E8F0")
    GREEN = colors.HexColor("#047857")
    ORANGE = colors.HexColor("#C2410C")
    RED = colors.HexColor("#B91C1C")

    title_style = ParagraphStyle(
        "TS_Title",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=NAVY,
        alignment=TA_CENTER,
        spaceAfter=5,
    )

    subtitle_style = ParagraphStyle(
        "TS_Subtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=GRAY,
        alignment=TA_CENTER,
        spaceAfter=10,
    )

    section_style = ParagraphStyle(
        "TS_Section",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=BLUE,
        spaceBefore=10,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        "TS_Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=NAVY,
    )

    small_style = ParagraphStyle(
        "TS_Small",
        parent=body_style,
        fontSize=8,
        leading=11,
        textColor=GRAY,
    )

    bullet_style = ParagraphStyle(
        "TS_Bullet",
        parent=body_style,
        leftIndent=10,
        firstLineIndent=-6,
        bulletIndent=3,
        spaceAfter=3,
    )

    metric_label_style = ParagraphStyle(
        "TS_MetricLabel",
        parent=body_style,
        fontName="Helvetica-Bold",
        fontSize=7.5,
        textColor=GRAY,
        alignment=TA_CENTER,
    )

    metric_value_style = ParagraphStyle(
        "TS_MetricValue",
        parent=body_style,
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=NAVY,
        alignment=TA_CENTER,
    )

    story = []

    # ------------------------------------------------------
    # COVER / HEADER
    # ------------------------------------------------------

    story.append(
        Paragraph(
            "TalentSphere Elevate",
            ParagraphStyle(
                "Brand",
                parent=title_style,
                fontSize=12,
                textColor=BLUE,
            ),
        )
    )

    story.append(
        Paragraph(
            "College Student Placement Report",
            title_style,
        )
    )

    story.append(
        Paragraph(
            f"Generated for {pdf_safe(data['student_name'], 'College Student')} "
            f"• {datetime.now().strftime('%d %B %Y')}",
            subtitle_style,
        )
    )

    header_line = Table(
        [[""]],
        colWidths=[180 * mm],
        rowHeights=[1.5],
    )

    header_line.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), BLUE),
            ]
        )
    )

    story.append(header_line)
    story.append(Spacer(1, 5 * mm))

    # ------------------------------------------------------
    # PROFILE SUMMARY
    # ------------------------------------------------------

    story.append(
        Paragraph(
            "1. Student Profile",
            section_style,
        )
    )

    profile_rows = [
        [
            Paragraph("<b>Name</b>", body_style),
            Paragraph(pdf_safe(data["student_name"], "Not added"), body_style),
            Paragraph("<b>Target Role</b>", body_style),
            Paragraph(pdf_safe(data["preferred_role"], "Not added"), body_style),
        ],
        [
            Paragraph("<b>College</b>", body_style),
            Paragraph(pdf_safe(data["profile"].get("college_name"), "Not added"), body_style),
            Paragraph("<b>Degree</b>", body_style),
            Paragraph(pdf_safe(data["profile"].get("degree"), "Not added"), body_style),
        ],
        [
            Paragraph("<b>Branch</b>", body_style),
            Paragraph(pdf_safe(data["profile"].get("branch"), "Not added"), body_style),
            Paragraph("<b>Year / Semester</b>", body_style),
            Paragraph(
                pdf_safe(
                    f"{safe_text(data['profile'].get('current_year'), '')} "
                    f"{safe_text(data['profile'].get('semester'), '')}".strip(),
                    "Not added",
                ),
                body_style,
            ),
        ],
        [
            Paragraph("<b>CGPA</b>", body_style),
            Paragraph(f"{data['cgpa']:.1f}", body_style),
            Paragraph("<b>Backlogs</b>", body_style),
            Paragraph(str(data["backlogs"]), body_style),
        ],
        [
            Paragraph("<b>Graduation</b>", body_style),
            Paragraph(pdf_safe(data["profile"].get("graduation_year"), "Not added"), body_style),
            Paragraph("<b>Profile Completion</b>", body_style),
            Paragraph(f"{data['profile_score']}%", body_style),
        ],
    ]

    profile_table = Table(
        profile_rows,
        colWidths=[
            29 * mm,
            61 * mm,
            29 * mm,
            61 * mm,
        ],
        hAlign="LEFT",
    )

    profile_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(profile_table)

    # ------------------------------------------------------
    # READINESS INDEX
    # ------------------------------------------------------

    story.append(
        Paragraph(
            "2. Placement Readiness Overview",
            section_style,
        )
    )

    metrics = [
        ("Overall", f"{data['overall_readiness']}%"),
        ("Resume", f"{data['resume_score']}%"),
        ("Role Fit", f"{data['role_fit']}%"),
        ("Coding", f"{data['coding']['score']}%"),
        ("Interview", f"{data['interview']['score']}%"),
        ("GitHub", f"{data['github_score']}%"),
        ("LinkedIn", f"{data['linkedin_score']}%"),
    ]

    metric_cells = []

    for label, value in metrics:
        metric_cells.append(
            [
                Paragraph(label.upper(), metric_label_style),
                Paragraph(value, metric_value_style),
            ]
        )

    metric_table = Table(
        [
            [
                Table(
                    [[cell[0]], [cell[1]]],
                    colWidths=[24 * mm],
                )
                for cell in metric_cells[:4]
            ],
            [
                Table(
                    [[cell[0]], [cell[1]]],
                    colWidths=[24 * mm],
                )
                for cell in metric_cells[4:]
            ],
        ],
        colWidths=[44 * mm] * 4,
        hAlign="LEFT",
    )

    metric_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.4, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(metric_table)
    story.append(Spacer(1, 2 * mm))

    story.append(
        Paragraph(
            f"<b>Current Readiness Level:</b> "
            f"{pdf_safe(readiness_label(data['overall_readiness']))}",
            body_style,
        )
    )

    # ------------------------------------------------------
    # SKILLS / ROLE FIT
    # ------------------------------------------------------

    story.append(
        Paragraph(
            "3. Skill Gap & Target Role Analysis",
            section_style,
        )
    )

    role_match = data["preferred_match"] or data["best_match"]

    if role_match:
        story.append(
            Paragraph(
                f"<b>Role:</b> {pdf_safe(role_match['role'])} "
                f"&nbsp;&nbsp; | &nbsp;&nbsp; "
                f"<b>Fit:</b> {role_match['score']}%",
                body_style,
            )
        )

        story.append(Spacer(1, 2 * mm))

        story.append(
            Paragraph(
                "<b>Skills Present:</b> "
                + pdf_safe(", ".join(role_match["present"]) or "None"),
                body_style,
            )
        )

        story.append(
            Paragraph(
                "<b>Missing Skills:</b> "
                + pdf_safe(", ".join(role_match["missing"]) or "No major gaps"),
                body_style,
            )
        )

    # ------------------------------------------------------
    # BEST JOB MATCHES
    # ------------------------------------------------------

    story.append(
        Paragraph(
            "4. Top Job Matches",
            section_style,
        )
    )

    top_matches = data["role_matches"][:5]

    match_rows = [
        [
            Paragraph("<b>Rank</b>", body_style),
            Paragraph("<b>Role</b>", body_style),
            Paragraph("<b>Match</b>", body_style),
            Paragraph("<b>Priority Missing Skills</b>", body_style),
        ]
    ]

    for idx, match in enumerate(top_matches, start=1):
        match_rows.append(
            [
                Paragraph(str(idx), body_style),
                Paragraph(pdf_safe(match["role"]), body_style),
                Paragraph(f"{match['score']}%", body_style),
                Paragraph(
                    pdf_safe(
                        ", ".join(match["missing"][:3])
                        or "No major gaps"
                    ),
                    small_style,
                ),
            ]
        )

    match_table = Table(
        match_rows,
        colWidths=[
            15 * mm,
            57 * mm,
            24 * mm,
            84 * mm,
        ],
    )

    match_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EEF2FF")),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    story.append(match_table)

    # ------------------------------------------------------
    # CODING / INTERVIEW
    # ------------------------------------------------------

    story.append(
        Paragraph(
            "5. Coding & Interview Preparation",
            section_style,
        )
    )

    prep_rows = [
        [
            Paragraph("<b>Area</b>", body_style),
            Paragraph("<b>Progress</b>", body_style),
            Paragraph("<b>Status</b>", body_style),
        ],
        [
            Paragraph("Coding Practice", body_style),
            Paragraph(
                f"{data['coding']['solved']} / {data['coding']['total']} "
                f"({data['coding']['score']}%)",
                body_style,
            ),
            Paragraph(
                "Strong" if data["coding"]["score"] >= 60 else "Needs more practice",
                body_style,
            ),
        ],
        [
            Paragraph("Interview Preparation", body_style),
            Paragraph(
                f"{data['interview']['prepared']} prepared "
                f"({data['interview']['score']}%)",
                body_style,
            ),
            Paragraph(
                "Strong" if data["interview"]["score"] >= 50 else "Needs more preparation",
                body_style,
            ),
        ],
    ]

    prep_table = Table(
        prep_rows,
        colWidths=[60 * mm, 60 * mm, 60 * mm],
    )

    prep_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F8FAFC")),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(prep_table)

    # ------------------------------------------------------
    # GITHUB
    # ------------------------------------------------------

    story.append(
        Paragraph(
            "6. GitHub Portfolio Review",
            section_style,
        )
    )

    github_result = data["github_result"]

    if github_result:
        github_profile = github_result.get("profile", {})
        github_scores = github_result.get("scores", {})
        quality = github_result.get("quality", {})
        languages = github_result.get("languages", {})

        story.append(
            Paragraph(
                f"<b>GitHub Score:</b> {data['github_score']}% "
                f"&nbsp;&nbsp; | &nbsp;&nbsp; "
                f"<b>Repositories:</b> "
                f"{len(github_result.get('repository_details', []))} "
                f"&nbsp;&nbsp; | &nbsp;&nbsp; "
                f"<b>Technologies:</b> {len(languages)}",
                body_style,
            )
        )

        if github_result.get("strengths"):
            story.append(Spacer(1, 2 * mm))
            story.append(
                Paragraph(
                    "<b>Strengths</b>",
                    body_style,
                )
            )

            for item in github_result.get("strengths", [])[:5]:
                story.append(
                    Paragraph(
                        pdf_safe(item),
                        bullet_style,
                        bulletText="•",
                    )
                )

        if github_result.get("improvements"):
            story.append(
                Paragraph(
                    "<b>Recommended Improvements</b>",
                    body_style,
                )
            )

            for item in github_result.get("improvements", [])[:5]:
                story.append(
                    Paragraph(
                        pdf_safe(item),
                        bullet_style,
                        bulletText="•",
                    )
                )

    else:
        story.append(
            Paragraph(
                "GitHub review has not been completed in the current session.",
                body_style,
            )
        )

    # ------------------------------------------------------
    # LINKEDIN
    # ------------------------------------------------------

    story.append(
        Paragraph(
            "7. LinkedIn Profile Review",
            section_style,
        )
    )

    linkedin_result = data["linkedin_result"]

    if linkedin_result:
        linkedin_scores = linkedin_result.get("scores", {})
        technical = linkedin_result.get("technical_skills", [])
        soft = linkedin_result.get("soft_skills", [])
        sections = linkedin_result.get("sections", {})

        story.append(
            Paragraph(
                f"<b>LinkedIn Score:</b> {data['linkedin_score']}% "
                f"&nbsp;&nbsp; | &nbsp;&nbsp; "
                f"<b>Technical Skills:</b> {len(technical)} "
                f"&nbsp;&nbsp; | &nbsp;&nbsp; "
                f"<b>Soft Skills:</b> {len(soft)}",
                body_style,
            )
        )

        story.append(
            Paragraph(
                "<b>Detected Sections:</b> "
                + pdf_safe(
                    ", ".join(
                        key.replace("_", " ").title()
                        for key, value in sections.items()
                        if value
                    )
                    or "None"
                ),
                body_style,
            )
        )

        if linkedin_result.get("strengths"):
            story.append(Spacer(1, 2 * mm))
            story.append(
                Paragraph(
                    "<b>Strengths</b>",
                    body_style,
                )
            )

            for item in linkedin_result.get("strengths", [])[:5]:
                story.append(
                    Paragraph(
                        pdf_safe(item),
                        bullet_style,
                        bulletText="•",
                    )
                )

        if linkedin_result.get("recommendations"):
            story.append(
                Paragraph(
                    "<b>Recommended Improvements</b>",
                    body_style,
                )
            )

            for item in linkedin_result.get("recommendations", [])[:5]:
                story.append(
                    Paragraph(
                        pdf_safe(item),
                        bullet_style,
                        bulletText="•",
                    )
                )

    else:
        story.append(
            Paragraph(
                "LinkedIn PDF review has not been completed in the current session.",
                body_style,
            )
        )

    # ------------------------------------------------------
    # PLACEMENT TRACKER
    # ------------------------------------------------------

    story.append(
        Paragraph(
            "8. Placement Tracker",
            section_style,
        )
    )

    placement = data["placement_summary"]

    placement_rows = [
        [
            Paragraph("<b>Applications</b>", body_style),
            Paragraph("<b>Interview / Shortlist</b>", body_style),
            Paragraph("<b>Offers / Selected</b>", body_style),
            Paragraph("<b>Rejected</b>", body_style),
        ],
        [
            Paragraph(str(placement["total"]), metric_value_style),
            Paragraph(str(placement["interviews"]), metric_value_style),
            Paragraph(str(placement["offers"]), metric_value_style),
            Paragraph(str(placement["rejected"]), metric_value_style),
        ],
    ]

    placement_table = Table(
        placement_rows,
        colWidths=[45 * mm] * 4,
    )

    placement_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(placement_table)

    # ------------------------------------------------------
    # STRENGTHS
    # ------------------------------------------------------

    story.append(
        Paragraph(
            "9. Key Strengths",
            section_style,
        )
    )

    for strength in data["strengths"]:
        story.append(
            Paragraph(
                pdf_safe(strength),
                bullet_style,
                bulletText="•",
            )
        )

    # ------------------------------------------------------
    # IMPROVEMENTS
    # ------------------------------------------------------

    story.append(
        Paragraph(
            "10. Priority Improvement Areas",
            section_style,
        )
    )

    for improvement in data["improvements"]:
        story.append(
            Paragraph(
                pdf_safe(improvement),
                bullet_style,
                bulletText="•",
            )
        )

    # ------------------------------------------------------
    # 90-DAY PLAN
    # ------------------------------------------------------

    story.append(
        Paragraph(
            "11. Personalized 90-Day Action Plan",
            section_style,
        )
    )

    for phase in data["action_plan"]:
        phase_elements = [
            Paragraph(
                f"<b>{pdf_safe(phase['period'])} — "
                f"{pdf_safe(phase['title'])}</b>",
                body_style,
            )
        ]

        for action in phase["actions"]:
            phase_elements.append(
                Paragraph(
                    pdf_safe(action),
                    bullet_style,
                    bulletText="•",
                )
            )

        story.append(
            KeepTogether(
                phase_elements
            )
        )

        story.append(
            Spacer(1, 2 * mm)
        )

    # ------------------------------------------------------
    # FINAL ASSESSMENT
    # ------------------------------------------------------

    story.append(
        Paragraph(
            "12. Final Placement Assessment",
            section_style,
        )
    )

    final_level = readiness_label(
        data["overall_readiness"]
    )

    final_message = (
        f"Current placement readiness is <b>{data['overall_readiness']}%</b> "
        f"({pdf_safe(final_level)}). "
        f"The recommended target is to close the highest-priority skill gaps, "
        f"strengthen coding and interview preparation, and maintain a strong "
        f"resume, GitHub and LinkedIn presence."
    )

    story.append(
        Paragraph(
            final_message,
            body_style,
        )
    )

    story.append(Spacer(1, 5 * mm))

    footer_box = Table(
        [
            [
                Paragraph(
                    "<b>TalentSphere Elevate</b><br/>"
                    "College Student Placement Readiness Report",
                    small_style,
                ),
                Paragraph(
                    f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
                    small_style,
                ),
            ]
        ],
        colWidths=[120 * mm, 60 * mm],
    )

    footer_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(footer_box)

    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf


# ==========================================================
# COLLECT REPORT DATA
# ==========================================================

def collect_report_data(user_id):
    profile = load_profile(user_id)

    student_name = (
        st.session_state.get("user_name")
        or safe_text(profile.get("name"), "College Student")
    )

    preferred_role = safe_text(
        profile.get("preferred_role"),
        "Not added",
    )

    profile_score = calculate_profile_completion(profile)
    resume_score = calculate_resume_score(profile)

    role_matches = calculate_role_matches(profile)

    best_match = (
        role_matches[0]
        if role_matches
        else None
    )

    preferred_match = next(
        (
            item
            for item in role_matches
            if item["role"] == preferred_role
        ),
        None,
    )

    selected_match = preferred_match or best_match
    role_fit = selected_match["score"] if selected_match else 0

    coding = calculate_coding_readiness()
    interview = calculate_interview_readiness()

    github_result = load_github_result()
    linkedin_result = load_linkedin_result()

    github_score = clamp(
        github_result.get(
            "scores",
            {}
        ).get(
            "overall",
            0
        )
        if github_result
        else 0
    )

    linkedin_score = clamp(
        linkedin_result.get(
            "scores",
            {}
        ).get(
            "overall",
            0
        )
        if linkedin_result
        else 0
    )

    placements = load_placements(user_id)
    internships = load_internships(user_id)
    hackathons = load_hackathons(user_id)

    overall_readiness = calculate_overall_readiness(
        profile_score=profile_score,
        resume_score=resume_score,
        role_fit=role_fit,
        coding_score=coding["score"],
        interview_score=interview["score"],
        github_score=github_score,
        linkedin_score=linkedin_score,
    )

    strengths = build_strengths(
        profile=profile,
        role_match=selected_match,
        coding=coding,
        interview=interview,
        github_score=github_score,
        linkedin_score=linkedin_score,
        placements=placements,
    )

    improvements = build_improvements(
        profile=profile,
        role_match=selected_match,
        coding=coding,
        interview=interview,
        github_score=github_score,
        linkedin_score=linkedin_score,
    )

    action_plan = build_action_plan(
        role_match=selected_match,
        coding=coding,
        interview=interview,
        github_score=github_score,
        linkedin_score=linkedin_score,
    )

    return {
        "student_name": student_name,
        "profile": profile,
        "preferred_role": preferred_role,
        "profile_score": profile_score,
        "resume_score": resume_score,
        "role_matches": role_matches,
        "best_match": best_match,
        "preferred_match": preferred_match,
        "role_fit": role_fit,
        "coding": coding,
        "interview": interview,
        "github_result": github_result,
        "github_score": github_score,
        "linkedin_result": linkedin_result,
        "linkedin_score": linkedin_score,
        "placements": placements,
        "placement_summary": placement_summary(placements),
        "internships": internships,
        "hackathons": hackathons,
        "overall_readiness": overall_readiness,
        "strengths": strengths,
        "improvements": improvements,
        "action_plan": action_plan,
        "cgpa": max(
            0.0,
            min(
                10.0,
                safe_float(
                    profile.get("cgpa"),
                    0.0,
                )
            )
        ),
        "backlogs": max(
            0,
            safe_int(
                profile.get("backlogs"),
                0,
            )
        ),
    }


# ==========================================================
# PAGE UI
# ==========================================================

def render():
    apply_college_theme()

    user_id = st.session_state.get(
        "user_id"
    )

    if not user_id:
        st.error(
            "Unable to identify the logged-in college student."
        )
        return

    data = collect_report_data(
        user_id
    )

    overall = data["overall_readiness"]
    level = readiness_label(overall)

    # ======================================================
    # HERO
    # ======================================================

    st.html(
        f"""<div class="college-hero">
            <div class="college-hero-badge">
                📊 FINAL COLLEGE PLACEMENT REPORT
            </div>

            <div class="college-hero-title">
                {html_escape(data["student_name"])}'s Placement Report
            </div>

            <div class="college-hero-description">
                A consolidated TalentSphere Elevate report covering
                academic profile, resume readiness, role fit, coding,
                interview preparation, GitHub, LinkedIn and placement progress.
            </div>
        </div>"""
    )

    # ======================================================
    # TOP METRICS
    # ======================================================

    st.html(
        f"""<div class="college-metric-grid">
            <div class="college-metric-card">
                <div class="college-metric-icon">🏆</div>
                <div class="college-metric-label">OVERALL READINESS</div>
                <div class="college-metric-value">{overall}%</div>
                <div class="college-metric-caption">{level}</div>
            </div>

            <div class="college-metric-card">
                <div class="college-metric-icon">📄</div>
                <div class="college-metric-label">RESUME SCORE</div>
                <div class="college-metric-value">{data["resume_score"]}%</div>
                <div class="college-metric-caption">Profile-based resume readiness</div>
            </div>

            <div class="college-metric-card">
                <div class="college-metric-icon">🎯</div>
                <div class="college-metric-label">TARGET ROLE FIT</div>
                <div class="college-metric-value">{data["role_fit"]}%</div>
                <div class="college-metric-caption">
                    {html_escape(
                        data["preferred_match"]["role"]
                        if data["preferred_match"]
                        else (
                            data["best_match"]["role"]
                            if data["best_match"]
                            else "No role"
                        )
                    )}
                </div>
            </div>

            <div class="college-metric-card">
                <div class="college-metric-icon">📈</div>
                <div class="college-metric-label">PROFILE COMPLETION</div>
                <div class="college-metric-value">{data["profile_score"]}%</div>
                <div class="college-metric-caption">College profile completeness</div>
            </div>
        </div>"""
    )

    st.progress(
        overall / 100
    )

    # ======================================================
    # STUDENT PROFILE
    # ======================================================

    st.html(
        """<div class="college-section-header">
            <div>
                <div class="college-section-title">
                    👤 Student Profile Summary
                </div>
                <div class="college-section-subtitle">
                    Core academic and placement information.
                </div>
            </div>
            <div class="college-section-tag">
                Profile
            </div>
        </div>"""
    )

    p = data["profile"]

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Degree",
            safe_text(
                p.get("degree"),
                "Not added",
            )
        )

    with c2:
        st.metric(
            "Branch",
            safe_text(
                p.get("branch"),
                "Not added",
            )
        )

    with c3:
        st.metric(
            "CGPA",
            f'{data["cgpa"]:.1f}'
        )

    with c4:
        st.metric(
            "Backlogs",
            data["backlogs"]
        )

    st.write(
        "**College:**",
        safe_text(
            p.get("college_name"),
            "Not added",
        )
    )

    st.write(
        "**Target Role:**",
        data["preferred_role"]
    )

    # ======================================================
    # READINESS BREAKDOWN
    # ======================================================

    st.html(
        """<div class="college-section-header">
            <div>
                <div class="college-section-title">
                    📊 Placement Readiness Breakdown
                </div>
                <div class="college-section-subtitle">
                    Performance across major placement-preparation areas.
                </div>
            </div>
        </div>"""
    )

    readiness_items = [
        ("👤 Profile", data["profile_score"]),
        ("📄 Resume", data["resume_score"]),
        ("🎯 Role Fit", data["role_fit"]),
        ("💻 Coding", data["coding"]["score"]),
        ("🎤 Interview", data["interview"]["score"]),
        ("🐙 GitHub", data["github_score"]),
        ("💼 LinkedIn", data["linkedin_score"]),
    ]

    for label, score in readiness_items:
        left, right = st.columns([5, 1])

        with left:
            st.markdown(
                f"**{label}**"
            )

        with right:
            st.markdown(
                f"**{score}%**"
            )

        st.progress(
            score / 100
        )

    # ======================================================
    # SKILL GAP / ROLE FIT
    # ======================================================

    role_match = (
        data["preferred_match"]
        or data["best_match"]
    )

    st.html(
        """<div class="college-section-header">
            <div>
                <div class="college-section-title">
                    🧩 Skill Gap Analysis
                </div>
                <div class="college-section-subtitle">
                    Current role alignment and priority missing skills.
                </div>
            </div>
        </div>"""
    )

    if role_match:
        st.markdown(
            f"### {role_match['role']} — {role_match['score']}% Match"
        )

        st.progress(
            role_match["score"] / 100
        )

        left, right = st.columns(2)

        with left:
            st.markdown(
                "#### ✅ Skills Present"
            )

            if role_match["present"]:
                for skill in role_match["present"]:
                    st.success(skill)
            else:
                st.caption("No matching skills detected.")

        with right:
            st.markdown(
                "#### ❌ Missing Skills"
            )

            if role_match["missing"]:
                for skill in role_match["missing"]:
                    st.warning(skill)
            else:
                st.success("No major skill gaps.")

    # ======================================================
    # JOB MATCHES
    # ======================================================

    st.html(
        """<div class="college-section-header">
            <div>
                <div class="college-section-title">
                    💼 Top Job Matches
                </div>
                <div class="college-section-subtitle">
                    Highest role-fit percentages based on current skills.
                </div>
            </div>
            <div class="college-section-tag">
                Top 5
            </div>
        </div>"""
    )

    for index, match in enumerate(
        data["role_matches"][:5],
        start=1,
    ):
        st.html(
            f"""<div style="
                background:#ffffff;
                border:1px solid #e2e8f0;
                border-radius:18px;
                padding:18px 20px;
                margin-bottom:10px;
                box-shadow:0 6px 18px rgba(15,23,42,.035);
            ">
                <div style="
                    color:#94a3b8;
                    font-size:10px;
                    font-weight:900;
                    letter-spacing:1px;
                ">
                    MATCH #{index}
                </div>

                <div style="
                    display:flex;
                    align-items:center;
                    justify-content:space-between;
                    gap:20px;
                    margin-top:6px;
                ">
                    <div>
                        <div style="
                            color:#0f172a;
                            font-size:16px;
                            font-weight:800;
                        ">
                            {html_escape(match["role"])}
                        </div>
                        <div style="
                            color:#64748b;
                            font-size:12px;
                            margin-top:5px;
                        ">
                            Missing:
                            {html_escape(
                                ", ".join(match["missing"][:3])
                                or "No major gaps"
                            )}
                        </div>
                    </div>

                    <div style="
                        color:#4f46e5;
                        font-size:24px;
                        font-weight:900;
                    ">
                        {match["score"]}%
                    </div>
                </div>
            </div>"""
        )

    # ======================================================
    # CODING + INTERVIEW
    # ======================================================

    st.html(
        """<div class="college-section-header">
            <div>
                <div class="college-section-title">
                    💻 Coding & Interview Preparation
                </div>
                <div class="college-section-subtitle">
                    Progress from the practice modules in this session.
                </div>
            </div>
        </div>"""
    )

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Coding Problems Solved",
            f'{data["coding"]["solved"]} / {data["coding"]["total"]}'
        )
        st.progress(
            data["coding"]["score"] / 100
        )

    with c2:
        st.metric(
            "Interview Questions Prepared",
            data["interview"]["prepared"]
        )
        st.progress(
            data["interview"]["score"] / 100
        )

    # ======================================================
    # GITHUB
    # ======================================================

    st.html(
        """<div class="college-section-header">
            <div>
                <div class="college-section-title">
                    🐙 GitHub Portfolio Summary
                </div>
                <div class="college-section-subtitle">
                    Results from the GitHub Portfolio Review module.
                </div>
            </div>
        </div>"""
    )

    github = data["github_result"]

    if github:
        g1, g2, g3 = st.columns(3)

        with g1:
            st.metric(
                "GitHub Score",
                f'{data["github_score"]}%'
            )

        with g2:
            st.metric(
                "Repositories",
                len(
                    github.get(
                        "repository_details",
                        []
                    )
                )
            )

        with g3:
            st.metric(
                "Technologies",
                len(
                    github.get(
                        "languages",
                        {}
                    )
                )
            )

        if github.get("strengths"):
            st.markdown(
                "#### ✅ Strengths"
            )

            for item in github.get("strengths", [])[:5]:
                st.success(item)

        if github.get("improvements"):
            st.markdown(
                "#### 🎯 Improvements"
            )

            for item in github.get("improvements", [])[:5]:
                st.info(item)

    else:
        st.info(
            "Run **GitHub Review** in this session to include "
            "GitHub portfolio analysis in the final report."
        )

    # ======================================================
    # LINKEDIN
    # ======================================================

    st.html(
        """<div class="college-section-header">
            <div>
                <div class="college-section-title">
                    💼 LinkedIn Profile Summary
                </div>
                <div class="college-section-subtitle">
                    Results from the uploaded LinkedIn PDF analysis.
                </div>
            </div>
        </div>"""
    )

    linkedin = data["linkedin_result"]

    if linkedin:
        l1, l2, l3 = st.columns(3)

        with l1:
            st.metric(
                "LinkedIn Score",
                f'{data["linkedin_score"]}%'
            )

        with l2:
            st.metric(
                "Technical Skills",
                len(
                    linkedin.get(
                        "technical_skills",
                        []
                    )
                )
            )

        with l3:
            st.metric(
                "Soft Skills",
                len(
                    linkedin.get(
                        "soft_skills",
                        []
                    )
                )
            )

        if linkedin.get("strengths"):
            st.markdown(
                "#### ✅ Strengths"
            )

            for item in linkedin.get("strengths", [])[:5]:
                st.success(item)

        if linkedin.get("recommendations"):
            st.markdown(
                "#### 🎯 Recommendations"
            )

            for item in linkedin.get("recommendations", [])[:5]:
                st.info(item)

    else:
        st.info(
            "Upload and analyze your LinkedIn PDF in **LinkedIn Review** "
            "to include LinkedIn analysis in this report."
        )

    # ======================================================
    # PLACEMENT TRACKER
    # ======================================================

    st.html(
        """<div class="college-section-header">
            <div>
                <div class="college-section-title">
                    📌 Placement Tracker Summary
                </div>
                <div class="college-section-subtitle">
                    Current application and selection progress.
                </div>
            </div>
        </div>"""
    )

    ps = data["placement_summary"]

    p1, p2, p3, p4 = st.columns(4)

    with p1:
        st.metric(
            "Applications",
            ps["total"]
        )

    with p2:
        st.metric(
            "Interview / Shortlist",
            ps["interviews"]
        )

    with p3:
        st.metric(
            "Offers",
            ps["offers"]
        )

    with p4:
        st.metric(
            "Rejected",
            ps["rejected"]
        )

    # ======================================================
    # STRENGTHS
    # ======================================================

    st.html(
        """<div class="college-section-header">
            <div>
                <div class="college-section-title">
                    ✅ Key Strengths
                </div>
                <div class="college-section-subtitle">
                    Positive signals identified across your placement profile.
                </div>
            </div>
        </div>"""
    )

    for strength in data["strengths"]:
        st.success(strength)

    # ======================================================
    # IMPROVEMENTS
    # ======================================================

    st.html(
        """<div class="college-section-header">
            <div>
                <div class="college-section-title">
                    🎯 Priority Improvement Areas
                </div>
                <div class="college-section-subtitle">
                    Areas that can most improve your placement readiness.
                </div>
            </div>
        </div>"""
    )

    for improvement in data["improvements"]:
        st.warning(improvement)

    # ======================================================
    # 90-DAY PLAN
    # ======================================================

    st.html(
        """<div class="college-section-header">
            <div>
                <div class="college-section-title">
                    🗺️ Personalized 90-Day Action Plan
                </div>
                <div class="college-section-subtitle">
                    A practical path from current readiness to placement readiness.
                </div>
            </div>
            <div class="college-section-tag">
                30 / 60 / 90 Days
            </div>
        </div>"""
    )

    plan_cols = st.columns(3)

    colors_data = [
        ("#eef2ff", "#e0e7ff", "#4338ca", "📘"),
        ("#ecfdf5", "#d1fae5", "#047857", "💻"),
        ("#fff7ed", "#ffedd5", "#c2410c", "🎯"),
    ]

    for column, phase, style in zip(
        plan_cols,
        data["action_plan"],
        colors_data,
    ):
        bg, border, accent, icon = style

        actions_html = "".join(
            f"<li>{html_escape(action)}</li>"
            for action in phase["actions"]
        )

        with column:
            st.html(
                f"""<div style="
                    background:{bg};
                    border:1px solid {border};
                    border-radius:22px;
                    padding:23px;
                    min-height:300px;
                ">
                    <div style="font-size:25px;">
                        {icon}
                    </div>

                    <div style="
                        color:{accent};
                        font-size:11px;
                        font-weight:900;
                        letter-spacing:1px;
                        margin-top:12px;
                    ">
                        {html_escape(phase["period"]).upper()}
                    </div>

                    <div style="
                        color:#0f172a;
                        font-size:17px;
                        font-weight:800;
                        margin-top:6px;
                    ">
                        {html_escape(phase["title"])}
                    </div>

                    <ul style="
                        color:#64748b;
                        font-size:12px;
                        line-height:1.8;
                        padding-left:18px;
                        margin-top:12px;
                    ">
                        {actions_html}
                    </ul>
                </div>"""
            )

    # ======================================================
    # FINAL ASSESSMENT
    # ======================================================

    st.html(
        """<div class="college-section-header">
            <div>
                <div class="college-section-title">
                    🏆 Final Placement Assessment
                </div>
            </div>
        </div>"""
    )

    if overall >= 85:
        st.success(
            "🏆 Placement Ready — your profile shows strong overall "
            "alignment across skills, portfolio and preparation."
        )
    elif overall >= 70:
        st.success(
            "🚀 Strong readiness — close the remaining skill gaps and "
            "continue coding/interview practice."
        )
    elif overall >= 55:
        st.info(
            "👍 Developing well — focus on the priority gaps and build "
            "stronger placement evidence."
        )
    elif overall >= 40:
        st.warning(
            "📚 Needs focused preparation — strengthen skills, coding, "
            "interviews and professional profiles."
        )
    else:
        st.error(
            "🎯 Foundation stage — complete the College Profile, build "
            "core skills and use each preparation module consistently."
        )

    # ======================================================
    # PDF DOWNLOAD
    # ======================================================

    st.html(
        """<div class="college-section-header">
            <div>
                <div class="college-section-title">
                    📥 Download Final Report
                </div>
                <div class="college-section-subtitle">
                    Export the complete TalentSphere Elevate placement report as PDF.
                </div>
            </div>
        </div>"""
    )

    try:
        pdf_bytes = build_college_report_pdf(
            data
        )

        safe_name = re.sub(
            r"[^A-Za-z0-9_-]+",
            "_",
            data["student_name"].strip()
        ).strip("_")

        if not safe_name:
            safe_name = "College_Student"

        st.download_button(
            "📥 Download College Placement Report PDF",
            data=pdf_bytes,
            file_name=f"{safe_name}_TalentSphere_College_Report.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True,
        )

    except Exception as error:
        st.error(
            f"Unable to generate College Report PDF: {error}"
        )


# ==========================================================
# DIRECT RUN
# ==========================================================

if __name__ == "__main__":
    render()
