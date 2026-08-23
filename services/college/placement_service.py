# ==========================================================
# TALENTSPHERE
# COLLEGE PLACEMENT READINESS SERVICE
# ==========================================================


def safe_float(value, default=0.0):

    try:

        if value is None:
            return default

        if isinstance(
            value,
            (int, float),
        ):
            return float(value)

        value = str(
            value
        ).strip()

        if not value:
            return default

        value = value.replace(
            "%",
            "",
        )

        value = value.replace(
            ",",
            "",
        )

        return float(
            value
        )

    except (
        ValueError,
        TypeError,
    ):

        return default


# ==========================================================
# SAFE INTEGER
# ==========================================================

def safe_int(
    value,
    default=0,
):

    try:

        return int(
            safe_float(
                value,
                default,
            )
        )

    except Exception:

        return default


# ==========================================================
# SPLIT LIST VALUES
# ==========================================================

def split_items(
    value,
):

    if not value:

        return []

    if isinstance(
        value,
        list,
    ):

        return value

    return [

        item.strip()

        for item in str(
            value
        ).split(",")

        if item.strip()

    ]


# ==========================================================
# PLACEMENT READINESS
# ==========================================================

def readiness(
    profile,
):

    if not isinstance(
        profile,
        dict,
    ):

        profile = {}


    # ======================================================
    # CGPA SCORE
    # ======================================================

    cgpa = safe_float(
        profile.get(
            "cgpa"
        ),
        0.0,
    )

    cgpa = max(
        0.0,
        min(
            10.0,
            cgpa,
        ),
    )

    academic_score = round(
        cgpa * 10
    )


    # ======================================================
    # BACKLOG SCORE
    # ======================================================

    backlogs = safe_int(
        profile.get(
            "backlogs"
        ),
        0,
    )

    backlog_score = max(
        0,
        100 - (
            backlogs * 20
        ),
    )


    # ======================================================
    # TECHNICAL SKILLS
    # ======================================================

    technical_skills = split_items(
        profile.get(
            "technical_skills"
        )
    )

    skills_score = min(
        100,
        len(
            technical_skills
        ) * 12,
    )


    # ======================================================
    # PROJECTS
    # ======================================================

    projects = str(
        profile.get(
            "projects"
        )
        or ""
    ).strip()

    if projects:

        projects_score = 100

    else:

        projects_score = 20


    # ======================================================
    # INTERNSHIPS
    # ======================================================

    internships = str(
        profile.get(
            "internships"
        )
        or ""
    ).strip()

    if internships:

        internship_score = 100

    else:

        internship_score = 20


    # ======================================================
    # PROFESSIONAL PRESENCE
    # ======================================================

    professional_links = [

        profile.get(
            "github_url"
        ),

        profile.get(
            "linkedin_url"
        ),

        profile.get(
            "portfolio_url"
        ),

    ]

    valid_links = sum(

        1

        for link in professional_links

        if str(
            link or ""
        ).strip()

    )

    visibility_score = min(
        100,
        valid_links * 34,
    )


    # ======================================================
    # CAREER DIRECTION
    # ======================================================

    career_fields = [

        profile.get(
            "preferred_role"
        ),

        profile.get(
            "placement_goal"
        ),

    ]

    career_completed = sum(

        1

        for value in career_fields

        if str(
            value or ""
        ).strip()

    )

    career_score = round(
        (
            career_completed
            / len(
                career_fields
            )
        )
        * 100
    )


    # ======================================================
    # OVERALL SCORE
    # ======================================================

    overall = round(
        (
            academic_score
            + backlog_score
            + skills_score
            + projects_score
            + internship_score
            + visibility_score
            + career_score
        )
        / 7
    )

    overall = max(
        0,
        min(
            100,
            overall,
        ),
    )


    # ======================================================
    # RETURN DICTIONARY
    # ======================================================

    return {

        "overall":
            overall,

        "academic":
            academic_score,

        "backlogs":
            backlog_score,

        "skills":
            skills_score,

        "projects":
            projects_score,

        "internship":
            internship_score,

        "visibility":
            visibility_score,

        "career":
            career_score,

    }


# ==========================================================
# READINESS LEVEL
# ==========================================================

def readiness_level(
    score,
):

    score = safe_float(
        score,
        0,
    )

    if score >= 85:

        return (
            "Placement Ready"
        )

    elif score >= 70:

        return (
            "Strong Progress"
        )

    elif score >= 55:

        return (
            "Developing Well"
        )

    elif score >= 40:

        return (
            "Needs Improvement"
        )

    else:

        return (
            "Getting Started"
        )


# ==========================================================
# READINESS MESSAGE
# ==========================================================

def readiness_message(
    score,
):

    score = safe_float(
        score,
        0,
    )

    if score >= 85:

        return (
            "Excellent preparation. "
            "Focus on company-specific interview preparation "
            "and placement applications."
        )

    elif score >= 70:

        return (
            "You are making strong progress. "
            "Continue coding practice, resume improvement "
            "and mock interviews."
        )

    elif score >= 55:

        return (
            "Your placement preparation is developing well. "
            "Improve technical skills, projects "
            "and interview preparation."
        )

    elif score >= 40:

        return (
            "Focus on strengthening your profile, "
            "technical skills, projects and resume."
        )

    else:

        return (
            "Complete your College Profile first. "
            "Add CGPA, technical skills, projects, "
            "internships and professional links."
        )