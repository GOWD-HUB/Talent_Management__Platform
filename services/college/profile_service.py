# ==========================================================
# TALENTSPHERE ELEVATE
# COLLEGE PROFILE SERVICE
# ==========================================================


def safe_float(value, default=0.0):
    """
    Safely convert values such as:
    None
    ""
    "Not added"
    "Untouched"
    "N/A"
    numeric strings
    into a float.
    """

    try:
        if value is None:
            return default

        if isinstance(value, (int, float)):
            return float(value)

        value = str(value).strip()

        if not value:
            return default

        value = value.replace("%", "")
        value = value.replace(",", "")

        return float(value)

    except (ValueError, TypeError):
        return default


def has_value(value):
    """
    Returns True only when the profile field
    contains meaningful information.
    """

    if value is None:
        return False

    value = str(value).strip()

    if not value:
        return False

    invalid_values = {
        "none",
        "null",
        "n/a",
        "na",
        "not added",
        "notadded",
        "untouched",
        "unknown",
        "-",
    }

    return value.lower() not in invalid_values


# ==========================================================
# PROFILE COMPLETION
# ==========================================================

def completion(profile):

    if not isinstance(profile, dict):
        profile = {}

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

        # CGPA must be numeric and above 0
        if field == "cgpa":

            cgpa = safe_float(
                value,
                0.0,
            )

            if cgpa > 0:
                completed += 1

        else:

            if has_value(value):
                completed += 1

    if not fields:
        return 0

    percentage = round(
        completed
        / len(fields)
        * 100
    )

    return max(
        0,
        min(
            100,
            percentage,
        ),
    )


# ==========================================================
# PROFILE STATUS
# ==========================================================

def profile_status(profile):

    score = completion(profile)

    if score >= 90:
        return "Excellent"

    if score >= 75:
        return "Strong"

    if score >= 50:
        return "Developing"

    if score >= 25:
        return "Incomplete"

    return "Getting Started"


# ==========================================================
# MISSING FIELDS
# ==========================================================

def missing_fields(profile):

    if not isinstance(profile, dict):
        profile = {}

    labels = {
        "college_name": "College Name",
        "degree": "Degree",
        "branch": "Branch / Specialization",
        "current_year": "Current Year",
        "semester": "Semester",
        "graduation_year": "Graduation Year",
        "cgpa": "CGPA",
        "technical_skills": "Technical Skills",
        "projects": "Projects",
        "internships": "Internships",
        "preferred_role": "Preferred Role",
        "github_url": "GitHub URL",
        "linkedin_url": "LinkedIn URL",
    }

    missing = []

    for field, label in labels.items():

        value = profile.get(field)

        if field == "cgpa":

            if safe_float(value, 0.0) <= 0:
                missing.append(label)

        elif not has_value(value):

            missing.append(label)

    return missing