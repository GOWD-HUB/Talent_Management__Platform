import streamlit as st

from database.college_repository import get_college_profile
from services.college.career_service import gap
from styles.college.theme import apply_college_theme


# ==========================================================
# HELPERS
# ==========================================================

def safe_list(value):
    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, (tuple, set)):
        return list(value)

    if isinstance(value, str):
        return [
            item.strip()
            for item in value.split(",")
            if item.strip()
        ]

    return []


def skill_badge(skill, status="present"):

    styles = {
        "present": {
            "bg": "#ECFDF5",
            "border": "#A7F3D0",
            "text": "#047857",
            "icon": "✅",
        },
        "missing": {
            "bg": "#FEF2F2",
            "border": "#FECACA",
            "text": "#B91C1C",
            "icon": "❌",
        },
        "priority": {
            "bg": "#FFF7ED",
            "border": "#FED7AA",
            "text": "#C2410C",
            "icon": "🔥",
        },
    }

    style = styles.get(
        status,
        styles["present"],
    )

    return f"""
    <span style="
        display:inline-block;
        background:{style["bg"]};
        border:1px solid {style["border"]};
        color:{style["text"]};
        padding:7px 12px;
        border-radius:999px;
        margin:4px 5px 4px 0;
        font-size:12px;
        font-weight:700;
    ">
        {style["icon"]} {skill}
    </span>
    """


def recommendation_for_skill(skill):

    skill_lower = skill.lower()

    mapping = {
        "python": (
            "Practice Python fundamentals, OOP, file handling, "
            "APIs and problem solving."
        ),
        "java": (
            "Revise OOP, collections, exception handling, "
            "JDBC and core Java interview concepts."
        ),
        "c++": (
            "Focus on STL, OOP, pointers, recursion and DSA."
        ),
        "dsa": (
            "Practice arrays, strings, linked lists, stacks, queues, "
            "trees, graphs and dynamic programming."
        ),
        "data structures": (
            "Practice arrays, linked lists, stacks, queues, trees, "
            "hashing and graphs."
        ),
        "sql": (
            "Practice SELECT, JOINs, GROUP BY, subqueries, "
            "normalization and indexing."
        ),
        "dbms": (
            "Revise normalization, transactions, ACID properties, "
            "keys and SQL."
        ),
        "react": (
            "Build projects using components, hooks, routing, "
            "API integration and state management."
        ),
        "node.js": (
            "Practice Express, REST APIs, middleware, "
            "authentication and database integration."
        ),
        "mongodb": (
            "Practice CRUD, schema design, aggregation and indexing."
        ),
        "machine learning": (
            "Learn supervised/unsupervised learning, preprocessing, "
            "evaluation metrics and model deployment."
        ),
        "ml": (
            "Learn supervised/unsupervised learning, preprocessing, "
            "evaluation metrics and model deployment."
        ),
        "ai": (
            "Strengthen ML fundamentals, NLP/CV basics and "
            "AI project implementation."
        ),
        "cloud": (
            "Learn cloud fundamentals, deployment, storage, "
            "compute and basic DevOps workflows."
        ),
        "aws": (
            "Practice EC2, S3, IAM, RDS and application deployment."
        ),
        "git": (
            "Practice branching, merging, pull requests, "
            "conflict resolution and GitHub workflows."
        ),
        "communication": (
            "Practice self-introduction, project explanation, "
            "group discussion and mock interviews."
        ),
        "system design": (
            "Learn scalability, caching, databases, load balancing "
            "and API design."
        ),
    }

    for key, value in mapping.items():
        if key in skill_lower:
            return value

    return (
        f"Study the fundamentals of {skill}, complete hands-on "
        "practice and build one small portfolio project."
    )


# ==========================================================
# PAGE
# ==========================================================

def render():

    apply_college_theme()

    uid = st.session_state.get("user_id")

    if not uid:
        st.error(
            "Unable to identify the logged-in college student."
        )
        return


    # ======================================================
    # LOAD PROFILE
    # ======================================================

    try:
        profile = (
            get_college_profile(uid)
            or {}
        )

    except Exception as error:
        st.error(
            f"Unable to load college profile: {error}"
        )
        return


    # ======================================================
    # ANALYZE
    # ======================================================

    try:
        result = gap(profile) or {}

    except Exception as error:
        st.error(
            f"Unable to calculate skill gap: {error}"
        )
        return


    fit = int(
        result.get("fit", 0)
        or 0
    )

    fit = max(
        0,
        min(
            100,
            fit,
        ),
    )


    present = safe_list(
        result.get("present")
    )

    missing = safe_list(
        result.get("missing")
    )


    preferred_role = (
        profile.get("preferred_role")
        or "Target Role"
    )


    # ======================================================
    # HERO
    # ======================================================

    st.html(
        f"""
<div class="college-hero">

    <div class="college-hero-badge">
        🧩 ROLE READINESS ANALYSIS
    </div>

    <div class="college-hero-title">
        Skill Gap Analysis
    </div>

    <div class="college-hero-description">
        Compare your current skills with the requirements for
        <b>{preferred_role}</b>. Identify strengths, missing skills,
        priority gaps and the next learning steps needed to improve
        your placement readiness.
    </div>

</div>
"""
    )


    # ======================================================
    # METRICS
    # ======================================================

    total_required = len(
        present
    ) + len(
        missing
    )


    present_count = len(
        present
    )

    missing_count = len(
        missing
    )


    status = (
        "Strong"
        if fit >= 80
        else
        "Good"
        if fit >= 60
        else
        "Developing"
        if fit >= 40
        else
        "Needs Focus"
    )


    st.html(
        f"""
<div class="college-metric-grid">

    <div class="college-metric-card">

        <div class="college-metric-icon">
            🎯
        </div>

        <div class="college-metric-label">
            ROLE FIT
        </div>

        <div class="college-metric-value">
            {fit}%
        </div>

        <div class="college-metric-caption">
            Match with target role
        </div>

    </div>


    <div class="college-metric-card">

        <div class="college-metric-icon">
            ✅
        </div>

        <div class="college-metric-label">
            SKILLS PRESENT
        </div>

        <div class="college-metric-value">
            {present_count}
        </div>

        <div class="college-metric-caption">
            Required skills already available
        </div>

    </div>


    <div class="college-metric-card">

        <div class="college-metric-icon">
            ❌
        </div>

        <div class="college-metric-label">
            SKILL GAPS
        </div>

        <div class="college-metric-value">
            {missing_count}
        </div>

        <div class="college-metric-caption">
            Skills requiring development
        </div>

    </div>


    <div class="college-metric-card">

        <div class="college-metric-icon">
            📈
        </div>

        <div class="college-metric-label">
            READINESS
        </div>

        <div class="college-metric-value">
            {status}
        </div>

        <div class="college-metric-caption">
            Current preparation level
        </div>

    </div>

</div>
"""
    )


    st.progress(
        fit / 100
    )


    # ======================================================
    # READINESS MESSAGE
    # ======================================================

    if fit >= 80:

        st.success(
            "🚀 Excellent role alignment. Focus mainly on advanced practice, projects and interview preparation."
        )

    elif fit >= 60:

        st.info(
            "👍 Good foundation. Closing a few important skill gaps can significantly improve your role readiness."
        )

    elif fit >= 40:

        st.warning(
            "📚 You have a developing foundation. Focus on the highest-priority missing skills before applying."
        )

    else:

        st.error(
            "🎯 Your current skill match is low. Build the core requirements first and then move to projects and interview preparation."
        )


    # ======================================================
    # CURRENT VS REQUIRED
    # ======================================================

    st.html(
        """
<div class="college-section-header">

    <div>

        <div class="college-section-title">
            🔍 Current Skill Comparison
        </div>

        <div class="college-section-subtitle">
            Understand which required skills you already have
            and which ones are missing.
        </div>

    </div>

    <div class="college-section-tag">
        Gap Overview
    </div>

</div>
"""
    )


    left, right = st.columns(2)


    # ======================================================
    # PRESENT SKILLS
    # ======================================================

    with left:

        st.markdown(
            "### ✅ Skills You Already Have"
        )

        if present:

            present_html = "".join(
                skill_badge(
                    skill,
                    "present",
                )
                for skill in present
            )

            st.html(
                f"""
<div style="
    background:#ffffff;
    border:1px solid #d1fae5;
    border-radius:20px;
    padding:22px;
    min-height:200px;
">
    {present_html}
</div>
"""
            )

        else:

            st.info(
                "No matching role skills have been identified yet."
            )


    # ======================================================
    # MISSING SKILLS
    # ======================================================

    with right:

        st.markdown(
            "### ❌ Missing Skills"
        )

        if missing:

            missing_html = "".join(
                skill_badge(
                    skill,
                    "missing",
                )
                for skill in missing
            )

            st.html(
                f"""
<div style="
    background:#ffffff;
    border:1px solid #fecaca;
    border-radius:20px;
    padding:22px;
    min-height:200px;
">
    {missing_html}
</div>
"""
            )

        else:

            st.success(
                "🎉 No major skill gaps detected for your current target role."
            )


    # ======================================================
    # PRIORITY GAPS
    # ======================================================

    if missing:

        st.html(
            """
<div class="college-section-header">

    <div>

        <div class="college-section-title">
            🔥 Priority Skill Gaps
        </div>

        <div class="college-section-subtitle">
            Start with these skills before moving to lower-priority areas.
        </div>

    </div>

    <div class="college-section-tag">
        High Priority
    </div>

</div>
"""
        )


        priority_skills = missing[:5]


        for index, skill in enumerate(
            priority_skills,
            start=1,
        ):

            recommendation = (
                recommendation_for_skill(
                    skill
                )
            )

            st.html(
                f"""
<div style="
    background:#ffffff;
    border:1px solid #e2e8f0;
    border-radius:18px;
    padding:20px 22px;
    margin-bottom:12px;
    box-shadow:0 7px 20px rgba(15,23,42,.04);
">

    <div style="
        display:flex;
        align-items:center;
        justify-content:space-between;
        gap:20px;
    ">

        <div>

            <div style="
                color:#f97316;
                font-size:11px;
                font-weight:900;
                letter-spacing:1px;
            ">
                PRIORITY {index}
            </div>

            <div style="
                color:#0f172a;
                font-size:17px;
                font-weight:800;
                margin-top:6px;
            ">
                {skill}
            </div>

            <div style="
                color:#64748b;
                font-size:12px;
                line-height:1.65;
                margin-top:7px;
            ">
                {recommendation}
            </div>

        </div>

        <div style="
            background:#fff7ed;
            border:1px solid #fed7aa;
            color:#c2410c;
            padding:8px 12px;
            border-radius:999px;
            font-size:11px;
            font-weight:800;
            white-space:nowrap;
        ">
            🔥 Priority
        </div>

    </div>

</div>
"""
            )


    # ======================================================
    # LEARNING ROADMAP
    # ======================================================

    st.html(
        """
<div class="college-section-header">

    <div>

        <div class="college-section-title">
            🗺️ Skill Development Roadmap
        </div>

        <div class="college-section-subtitle">
            A structured 30/60/90-day plan to close your skill gaps.
        </div>

    </div>

    <div class="college-section-tag">
        Action Plan
    </div>

</div>
"""
    )


    roadmap1, roadmap2, roadmap3 = (
        st.columns(3)
    )


    # ======================================================
    # 30 DAYS
    # ======================================================

    with roadmap1:

        first_phase = (
            missing[:2]
            if missing
            else present[:2]
        )

        first_text = (
            ", ".join(first_phase)
            if first_phase
            else "Core fundamentals"
        )

        st.html(
            f"""
<div style="
    background:#eef2ff;
    border:1px solid #e0e7ff;
    border-radius:22px;
    padding:24px;
    min-height:250px;
">

    <div style="
        font-size:26px;
    ">
        📘
    </div>

    <div style="
        color:#4338ca;
        font-size:11px;
        font-weight:900;
        letter-spacing:1px;
        margin-top:12px;
    ">
        DAYS 1–30
    </div>

    <div style="
        color:#0f172a;
        font-size:18px;
        font-weight:800;
        margin-top:7px;
    ">
        Build Fundamentals
    </div>

    <div style="
        color:#64748b;
        font-size:12px;
        line-height:1.75;
        margin-top:12px;
    ">
        Focus on <b>{first_text}</b>.<br><br>
        • Learn core concepts<br>
        • Practice daily<br>
        • Complete mini exercises<br>
        • Track progress weekly
    </div>

</div>
"""
        )


    # ======================================================
    # 60 DAYS
    # ======================================================

    with roadmap2:

        second_phase = (
            missing[2:4]
            if len(missing) > 2
            else missing[:2]
        )

        second_text = (
            ", ".join(second_phase)
            if second_phase
            else "Applied practice"
        )

        st.html(
            f"""
<div style="
    background:#ecfdf5;
    border:1px solid #d1fae5;
    border-radius:22px;
    padding:24px;
    min-height:250px;
">

    <div style="
        font-size:26px;
    ">
        💻
    </div>

    <div style="
        color:#047857;
        font-size:11px;
        font-weight:900;
        letter-spacing:1px;
        margin-top:12px;
    ">
        DAYS 31–60
    </div>

    <div style="
        color:#0f172a;
        font-size:18px;
        font-weight:800;
        margin-top:7px;
    ">
        Apply Through Projects
    </div>

    <div style="
        color:#64748b;
        font-size:12px;
        line-height:1.75;
        margin-top:12px;
    ">
        Focus on <b>{second_text}</b>.<br><br>
        • Build one mini project<br>
        • Solve practical problems<br>
        • Use GitHub regularly<br>
        • Improve documentation
    </div>

</div>
"""
        )


    # ======================================================
    # 90 DAYS
    # ======================================================

    with roadmap3:

        st.html(
            f"""
<div style="
    background:#fff7ed;
    border:1px solid #ffedd5;
    border-radius:22px;
    padding:24px;
    min-height:250px;
">

    <div style="
        font-size:26px;
    ">
        🎯
    </div>

    <div style="
        color:#c2410c;
        font-size:11px;
        font-weight:900;
        letter-spacing:1px;
        margin-top:12px;
    ">
        DAYS 61–90
    </div>

    <div style="
        color:#0f172a;
        font-size:18px;
        font-weight:800;
        margin-top:7px;
    ">
        Become Interview Ready
    </div>

    <div style="
        color:#64748b;
        font-size:12px;
        line-height:1.75;
        margin-top:12px;
    ">
        Target role: <b>{preferred_role}</b>.<br><br>
        • Complete portfolio project<br>
        • Revise interview fundamentals<br>
        • Practice mock interviews<br>
        • Improve resume and GitHub
    </div>

</div>
"""
        )


    # ======================================================
    # RECOMMENDED PROJECTS
    # ======================================================

    st.html(
        """
<div class="college-section-header">

    <div>

        <div class="college-section-title">
            🚀 Recommended Practice
        </div>

        <div class="college-section-subtitle">
            Convert your missing skills into portfolio evidence.
        </div>

    </div>

</div>
"""
    )


    if missing:

        for skill in missing[:4]:

            st.info(
                f"**{skill} Project:** Build one small hands-on project "
                f"that demonstrates practical use of {skill}."
            )

    else:

        st.success(
            "You have strong alignment. Focus on advanced projects, "
            "system design, coding practice and mock interviews."
        )


    # ======================================================
    # NEXT STEPS
    # ======================================================

    st.html(
        """
<div class="college-section-header">

    <div>

        <div class="college-section-title">
            ✅ Recommended Next Steps
        </div>

        <div class="college-section-subtitle">
            Follow these actions to improve your placement readiness.
        </div>

    </div>

</div>
"""
    )


    steps = []

    if missing:

        steps.append(
            f"Start learning **{missing[0]}** as your highest-priority gap."
        )

        if len(missing) > 1:

            steps.append(
                f"Add **{missing[1]}** after completing the first skill."
            )

    steps.extend(
        [
            "Complete at least one project relevant to your target role.",
            "Update your College Profile whenever you learn a new skill.",
            "Practice coding and interview questions every week.",
            "Use Mock Interview to test your communication and technical explanation.",
            "Review Job Matching after improving your skill set.",
        ]
    )


    for number, step in enumerate(
        steps,
        start=1,
    ):

        st.markdown(
            f"**{number}.** {step}"
        )


if __name__ == "__main__":
    render()