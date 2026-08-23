import streamlit as st

from database.college_repository import (
    get_college_profile,
    get_placements,
)

from services.college.placement_service import (
    readiness,
    readiness_level,
    readiness_message,
)

from services.college.resume_service import (
    score_profile,
)

from services.college.career_service import (
    gap,
)

from styles.college.theme import (
    apply_college_theme,
)


# ==========================================================
# NAVIGATION
# ==========================================================

def open_college_page(
    page_name,
):

    st.session_state[
        "college_navigation"
    ] = page_name

    st.rerun()


# ==========================================================
# FEATURE CARD
# ==========================================================

def render_feature_card(
    icon,
    title,
    description,
    page,
    key,
    card_class,
):

    st.html(
        f"""
<div class="
    college-feature-card
    {card_class}
">

    <div class="
        college-feature-icon
    ">
        {icon}
    </div>

    <div class="
        college-feature-title
    ">
        {title}
    </div>

    <div class="
        college-feature-description
    ">
        {description}
    </div>

</div>
"""
    )

    if st.button(
        f"Open {title} →",
        key=key,
        use_container_width=True,
    ):

        open_college_page(
            page
        )


# ==========================================================
# DASHBOARD
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


    # ======================================================
    # DATA
    # ======================================================

    try:

        profile = (
            get_college_profile(
                user_id
            )
            or {}
        )

    except Exception:

        profile = {}


    try:

        placements = (
            get_placements(
                user_id
            )
            or []
        )

    except Exception:

        placements = []


    readiness_data = readiness(
        profile
    )


    # Resume score

    try:

        resume_result = (
            score_profile(
                profile
            )
        )

        if isinstance(
            resume_result,
            tuple,
        ):

            resume_score = (
                resume_result[0]
            )

        else:

            resume_score = (
                resume_result
            )

    except Exception:

        resume_score = 0


    # Role fit

    try:

        skill_gap = gap(
            profile
        )

        role_fit = (
            skill_gap.get(
                "fit",
                0,
            )
        )

    except Exception:

        role_fit = 0


    overall = (
        readiness_data.get(
            "overall",
            0,
        )
    )


    user_name = (
        st.session_state.get(
            "user_name"
        )
        or "Student"
    )


    # ======================================================
    # HERO
    # ======================================================

    st.html(
        f"""
<div class="college-hero">

    <div class="
        college-hero-badge
    ">
        🎓 TALENTSPHERE
        COLLEGE PLACEMENT PORTAL
    </div>

    <div class="
        college-hero-title
    ">
        Hello, {user_name} 👋
        <br>
        Build your placement future.
    </div>

    <div class="
        college-hero-description
    ">
        Your personalised workspace brings
        together placement preparation,
        coding practice, resume development,
        interview preparation, internships,
        hackathons and job applications.
    </div>

</div>
"""
    )


    # ======================================================
    # OVERVIEW TITLE
    # ======================================================

    st.html(
        """
<div class="college-section-header">

    <div>

        <div class="
            college-section-title
        ">
            📊 Placement Overview
        </div>

        <div class="
            college-section-subtitle
        ">
            Your current placement
            preparation status
        </div>

    </div>

    <div class="
        college-section-tag
    ">
        Placement Intelligence
    </div>

</div>
"""
    )


    # ======================================================
    # METRICS
    # ======================================================

    st.html(
        f"""
<div class="
    college-metric-grid
">

    <div class="
        college-metric-card
    ">

        <div class="
            college-metric-icon
        ">
            🚀
        </div>

        <div class="
            college-metric-label
        ">
            Placement Readiness
        </div>

        <div class="
            college-metric-value
        ">
            {overall}%
        </div>

        <div class="
            college-metric-caption
        ">
            Overall preparation score
        </div>

    </div>


    <div class="
        college-metric-card
    ">

        <div class="
            college-metric-icon
        ">
            📄
        </div>

        <div class="
            college-metric-label
        ">
            Resume Score
        </div>

        <div class="
            college-metric-value
        ">
            {resume_score}%
        </div>

        <div class="
            college-metric-caption
        ">
            Resume completeness
            and professional profile
        </div>

    </div>


    <div class="
        college-metric-card
    ">

        <div class="
            college-metric-icon
        ">
            🎯
        </div>

        <div class="
            college-metric-label
        ">
            Role Fit
        </div>

        <div class="
            college-metric-value
        ">
            {role_fit}%
        </div>

        <div class="
            college-metric-caption
        ">
            Match with your
            preferred career role
        </div>

    </div>


    <div class="
        college-metric-card
    ">

        <div class="
            college-metric-icon
        ">
            💼
        </div>

        <div class="
            college-metric-label
        ">
            Applications
        </div>

        <div class="
            college-metric-value
        ">
            {len(placements)}
        </div>

        <div class="
            college-metric-caption
        ">
            Placement applications tracked
        </div>

    </div>

</div>
"""
    )


    # ======================================================
    # READINESS
    # ======================================================

    st.html(
        """
<div class="college-section-header">

    <div>

        <div class="
            college-section-title
        ">
            🚀 Placement Readiness
        </div>

        <div class="
            college-section-subtitle
        ">
            Your overall preparation
            across key placement areas
        </div>

    </div>

</div>
"""
    )

    st.progress(
        overall / 100
    )

    level = readiness_level(
        overall
    )

    message = readiness_message(
        overall
    )

    st.info(
        f"**{level}** — {message}"
    )


    # ======================================================
    # QUICK ACCESS
    # ======================================================

    st.html(
        """
<div class="college-section-header">

    <div>

        <div class="
            college-section-title
        ">
            ⚡ Quick Access
        </div>

        <div class="
            college-section-subtitle
        ">
            Open your placement
            and career development tools
        </div>

    </div>

    <div class="
        college-section-tag
    ">
        College Workspace
    </div>

</div>
"""
    )


    # ======================================================
    # ROW 1
    # ======================================================

    c1, c2, c3 = st.columns(
        3
    )

    with c1:

        render_feature_card(

            "👤",

            "College Profile",

            (
                "Manage academics, CGPA, "
                "skills, projects, internships "
                "and professional links."
            ),

            "👤 College Profile",

            "college_profile_card",

            "card-purple",
        )


    with c2:

        render_feature_card(

            "📄",

            "Resume Builder",

            (
                "Build a placement-ready "
                "resume using your saved "
                "student profile."
            ),

            "📄 Resume Builder",

            "college_resume_card",

            "card-orange",
        )


    with c3:

        render_feature_card(

            "🎯",

            "ATS Checker",

            (
                "Compare your profile "
                "against job descriptions "
                "and identify missing keywords."
            ),

            "🎯 ATS Checker",

            "college_ats_card",

            "card-blue",
        )


    # ======================================================
    # ROW 2
    # ======================================================

    c1, c2, c3 = st.columns(
        3
    )

    with c1:

        render_feature_card(

            "💻",

            "Coding Practice",

            (
                "Practise Python, "
                "Data Structures and DBMS "
                "for placement preparation."
            ),

            "💻 Coding Practice",

            "college_coding_card",

            "card-green",
        )


    with c2:

        render_feature_card(

            "🔥",

            "Daily Challenge",

            (
                "Complete one focused "
                "technical challenge every day."
            ),

            "🔥 Daily Challenge",

            "college_daily_card",

            "card-pink",
        )


    with c3:

        render_feature_card(

            "🎤",

            "Interview Prep",

            (
                "Prepare HR, technical "
                "and behavioural interview "
                "questions."
            ),

            "🎤 Interview Prep",

            "college_interview_card",

            "card-cyan",
        )


    # ======================================================
    # ROW 3
    # ======================================================

    c1, c2, c3 = st.columns(
        3
    )

    with c1:

        render_feature_card(

            "🗣️",

            "Mock Interview",

            (
                "Practise structured "
                "interview answers and "
                "receive feedback."
            ),

            "🗣️ Mock Interview",

            "college_mock_card",

            "card-blue",
        )


    with c2:

        render_feature_card(

            "🧩",

            "Skill Gap",

            (
                "Compare your technical "
                "skills with your target role."
            ),

            "🧩 Skill Gap",

            "college_gap_card",

            "card-purple",
        )


    with c3:

        render_feature_card(

            "💼",

            "Job Matching",

            (
                "Discover entry-level roles "
                "that match your current skills."
            ),

            "💼 Job Matching",

            "college_job_card",

            "card-green",
        )


    # ======================================================
    # ROW 4
    # ======================================================

    c1, c2, c3 = st.columns(
        3
    )

    with c1:

        render_feature_card(

            "📌",

            "Placement Tracker",

            (
                "Track companies, roles, "
                "selection rounds and offers."
            ),

            "📌 Placement Tracker",

            "college_tracker_card",

            "card-orange",
        )


    with c2:

        render_feature_card(

            "🐙",

            "GitHub Review",

            (
                "Evaluate your GitHub "
                "presence, projects and "
                "technical portfolio."
            ),

            "🐙 GitHub Review",

            "college_github_card",

            "card-cyan",
        )


    with c3:

        render_feature_card(

            "🔗",

            "LinkedIn Review",

            (
                "Improve your professional "
                "LinkedIn presence and profile."
            ),

            "🔗 LinkedIn Review",

            "college_linkedin_card",

            "card-pink",
        )


    # ======================================================
    # ROW 5
    # ======================================================

    c1, c2, c3 = st.columns(
        3
    )

    with c1:

        render_feature_card(

            "🏆",

            "Hackathons",

            (
                "Track hackathons, "
                "projects, teams and results."
            ),

            "🏆 Hackathons",

            "college_hackathon_card",

            "card-purple",
        )


    with c2:

        render_feature_card(

            "💼",

            "Internships",

            (
                "Track internship applications, "
                "training and work experience."
            ),

            "💼 Internships",

            "college_internship_card",

            "card-blue",
        )


    with c3:

        render_feature_card(

            "📊",

            "College Report",

            (
                "View your complete "
                "placement readiness and "
                "development report."
            ),

            "📊 College Report",

            "college_report_card",

            "card-green",
        )