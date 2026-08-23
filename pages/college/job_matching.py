import streamlit as st

from database.college_repository import get_college_profile
from styles.college.theme import apply_college_theme


# ==========================================================
# ROLE REQUIREMENTS
# ==========================================================

ROLE_REQUIREMENTS = {
    "Software Development Engineer": [
        "Python",
        "Java",
        "C++",
        "DSA",
        "OOP",
        "DBMS",
        "SQL",
        "Git",
        "REST API",
    ],

    "Full Stack Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "Express",
        "MongoDB",
        "SQL",
        "REST API",
        "Git",
    ],

    "Frontend Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Responsive Design",
        "Git",
        "REST API",
    ],

    "Backend Developer": [
        "Python",
        "Java",
        "Node.js",
        "FastAPI",
        "Django",
        "SQL",
        "MongoDB",
        "REST API",
        "Authentication",
        "Git",
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Excel",
        "Pandas",
        "NumPy",
        "Power BI",
        "Tableau",
        "Statistics",
        "Data Visualization",
    ],

    "Data Scientist": [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Statistics",
        "Machine Learning",
        "Data Visualization",
        "Scikit-learn",
    ],

    "Machine Learning Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "Pandas",
        "NumPy",
        "Git",
    ],

    "AI Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "Computer Vision",
        "TensorFlow",
        "PyTorch",
        "REST API",
        "Git",
    ],

    "Cloud Engineer": [
        "AWS",
        "Azure",
        "GCP",
        "Linux",
        "Networking",
        "Docker",
        "Cloud Computing",
        "Git",
    ],

    "DevOps Engineer": [
        "Linux",
        "Git",
        "Docker",
        "Kubernetes",
        "CI/CD",
        "Jenkins",
        "AWS",
        "Shell Scripting",
    ],

    "Cybersecurity Engineer": [
        "Networking",
        "Linux",
        "Cybersecurity",
        "Cryptography",
        "Web Security",
        "OWASP",
        "Python",
        "Security Testing",
    ],

    "QA / Test Engineer": [
        "Software Testing",
        "Manual Testing",
        "Automation Testing",
        "Selenium",
        "API Testing",
        "Postman",
        "SQL",
        "Git",
    ],

    "Business Analyst": [
        "Communication",
        "SQL",
        "Excel",
        "Data Analysis",
        "Requirement Analysis",
        "Documentation",
        "Power BI",
    ],
}


# ==========================================================
# HELPERS
# ==========================================================

def normalize_skill(skill):
    return (
        str(skill or "")
        .strip()
        .lower()
        .replace(".", "")
        .replace("-", " ")
    )


def extract_profile_skills(profile):

    raw_skills = []

    fields = [
        profile.get("technical_skills"),
        profile.get("soft_skills"),
    ]

    for value in fields:

        if not value:
            continue

        if isinstance(value, (list, tuple, set)):
            raw_skills.extend(value)

        else:
            text = str(value)

            text = text.replace(";", ",")
            text = text.replace("\n", ",")

            raw_skills.extend(
                [
                    item.strip()
                    for item in text.split(",")
                    if item.strip()
                ]
            )

    return raw_skills


def calculate_role_match(
    student_skills,
    required_skills,
):

    normalized_student = {
        normalize_skill(skill)
        for skill in student_skills
    }

    matched = []
    missing = []

    for skill in required_skills:

        normalized_required = (
            normalize_skill(skill)
        )

        found = False

        for student_skill in normalized_student:

            if (
                normalized_required
                == student_skill
                or normalized_required
                in student_skill
                or student_skill
                in normalized_required
            ):

                found = True
                break

        if found:
            matched.append(skill)
        else:
            missing.append(skill)

    total = len(required_skills)

    score = (
        round(
            len(matched)
            / total
            * 100
        )
        if total
        else 0
    )

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
    }


def get_readiness_label(score):

    if score >= 85:
        return "Excellent Match"

    if score >= 70:
        return "Strong Match"

    if score >= 55:
        return "Good Potential"

    if score >= 40:
        return "Developing"

    return "Needs Preparation"


def get_readiness_icon(score):

    if score >= 85:
        return "🟢"

    if score >= 70:
        return "🔵"

    if score >= 55:
        return "🟡"

    if score >= 40:
        return "🟠"

    return "🔴"


def skill_badges(
    skills,
    status="match",
):

    if not skills:
        return "<span style='color:#64748b;'>None</span>"

    if status == "match":

        background = "#ECFDF5"
        border = "#A7F3D0"
        text = "#047857"
        icon = "✅"

    else:

        background = "#FEF2F2"
        border = "#FECACA"
        text = "#B91C1C"
        icon = "❌"

    return "".join(
        f"""
<span style="
    display:inline-block;
    background:{background};
    border:1px solid {border};
    color:{text};
    padding:6px 11px;
    margin:4px;
    border-radius:999px;
    font-size:11px;
    font-weight:700;
">
    {icon} {skill}
</span>
"""
        for skill in skills
    )


# ==========================================================
# PAGE
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
    # LOAD PROFILE
    # ======================================================

    try:

        profile = (
            get_college_profile(
                user_id
            )
            or {}
        )

    except Exception as error:

        st.error(
            f"Unable to load college profile: {error}"
        )

        return


    student_skills = (
        extract_profile_skills(
            profile
        )
    )


    # ======================================================
    # CALCULATE ALL MATCHES
    # ======================================================

    role_results = []

    for (
        role,
        requirements,
    ) in ROLE_REQUIREMENTS.items():

        result = (
            calculate_role_match(
                student_skills,
                requirements,
            )
        )

        role_results.append(
            {
                "role": role,
                "score": result["score"],
                "matched": result["matched"],
                "missing": result["missing"],
                "required": requirements,
            }
        )


    role_results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )


    best_match = (
        role_results[0]
        if role_results
        else None
    )


    preferred_role = str(
        profile.get(
            "preferred_role"
        )
        or ""
    ).strip()


    preferred_result = next(
        (
            item
            for item in role_results
            if item["role"]
            == preferred_role
        ),
        None,
    )


    # ======================================================
    # HERO
    # ======================================================

    st.html(
        """<div class="college-hero">

            <div class="college-hero-badge">
                💼 AI-ASSISTED ROLE MATCHING
            </div>

            <div class="college-hero-title">
                Job Matching Engine
            </div>

            <div class="college-hero-description">
                Compare your current skills against popular placement
                roles and identify where your profile has the strongest
                career fit.
            </div>

        </div>"""
    )


    # ======================================================
    # TOP METRICS
    # ======================================================

    best_role_name = (
        best_match["role"]
        if best_match
        else "Not available"
    )

    best_role_score = (
        best_match["score"]
        if best_match
        else 0
    )

    preferred_score = (
        preferred_result["score"]
        if preferred_result
        else 0
    )

    matched_role_count = len(
        [
            role
            for role in role_results
            if role["score"] >= 50
        ]
    )


    st.html(
        f"""<div class="college-metric-grid">

            <div class="college-metric-card">

                <div class="college-metric-icon">
                    🏆
                </div>

                <div class="college-metric-label">
                    BEST ROLE
                </div>

                <div class="college-metric-value"
                     title="{best_role_name}">
                    {best_role_name}
                </div>

                <div class="college-metric-caption">
                    Highest skill alignment
                </div>

            </div>


            <div class="college-metric-card">

                <div class="college-metric-icon">
                    📈
                </div>

                <div class="college-metric-label">
                    BEST MATCH
                </div>

                <div class="college-metric-value">
                    {best_role_score}%
                </div>

                <div class="college-metric-caption">
                    Strongest role-fit score
                </div>

            </div>


            <div class="college-metric-card">

                <div class="college-metric-icon">
                    🎯
                </div>

                <div class="college-metric-label">
                    TARGET ROLE FIT
                </div>

                <div class="college-metric-value">
                    {preferred_score}%
                </div>

                <div class="college-metric-caption">
                    Match with preferred role
                </div>

            </div>


            <div class="college-metric-card">

                <div class="college-metric-icon">
                    💼
                </div>

                <div class="college-metric-label">
                    SUITABLE ROLES
                </div>

                <div class="college-metric-value">
                    {matched_role_count}
                </div>

                <div class="college-metric-caption">
                    Roles above 50% match
                </div>

            </div>

        </div>"""
    )


    # ======================================================
    # PROFILE CHECK
    # ======================================================

    if not student_skills:

        st.warning(
            "Your profile does not contain technical skills yet. "
            "Add your skills in College Profile to get meaningful job matches."
        )

        return


    # ======================================================
    # BEST MATCH
    # ======================================================

    if best_match:

        st.html(
            """<div class="college-section-header">

                <div>
                    <div class="college-section-title">
                        🏆 Best Career Match
                    </div>

                    <div class="college-section-subtitle">
                        Your strongest role based on current skills.
                    </div>
                </div>

                <div class="college-section-tag">
                    Recommended
                </div>

            </div>"""
        )


        readiness = (
            get_readiness_label(
                best_match["score"]
            )
        )

        icon = get_readiness_icon(
            best_match["score"]
        )


        st.html(
            f"""<div style="
                background:linear-gradient(135deg,#eef2ff,#f5f3ff);
                border:1px solid #d8d9ff;
                border-radius:24px;
                padding:28px;
                box-shadow:0 10px 30px rgba(79,70,229,.07);
            ">

                <div style="
                    color:#4f46e5;
                    font-size:11px;
                    font-weight:900;
                    letter-spacing:1px;
                ">
                    TOP RECOMMENDATION
                </div>

                <div style="
                    color:#0f172a;
                    font-size:26px;
                    font-weight:900;
                    margin-top:8px;
                ">
                    {best_match["role"]}
                </div>

                <div style="
                    color:#64748b;
                    font-size:13px;
                    margin-top:8px;
                ">
                    {icon} {readiness}
                </div>

                <div style="
                    color:#4338ca;
                    font-size:34px;
                    font-weight:900;
                    margin-top:15px;
                ">
                    {best_match["score"]}% Match
                </div>

            </div>"""
        )

        st.progress(
            best_match["score"] / 100
        )


    # ======================================================
    # TARGET ROLE
    # ======================================================

    if preferred_result:

        st.html(
            """<div class="college-section-header">

                <div>
                    <div class="college-section-title">
                        🎯 Preferred Role Analysis
                    </div>

                    <div class="college-section-subtitle">
                        See how closely your current profile matches
                        your selected career goal.
                    </div>
                </div>

            </div>"""
        )


        st.markdown(
            f"### {preferred_result['role']}"
        )

        st.progress(
            preferred_result["score"] / 100
        )

        col1, col2 = st.columns(2)


        with col1:

            st.markdown(
                "#### ✅ Matching Skills"
            )

            st.html(
                f"""<div style="
                    background:#ffffff;
                    border:1px solid #d1fae5;
                    border-radius:18px;
                    padding:18px;
                    min-height:150px;
                ">
                    {skill_badges(
                        preferred_result["matched"],
                        "match"
                    )}
                </div>"""
            )


        with col2:

            st.markdown(
                "#### ❌ Missing Skills"
            )

            st.html(
                f"""<div style="
                    background:#ffffff;
                    border:1px solid #fecaca;
                    border-radius:18px;
                    padding:18px;
                    min-height:150px;
                ">
                    {skill_badges(
                        preferred_result["missing"],
                        "missing"
                    )}
                </div>"""
            )


    # ======================================================
    # ALL ROLE MATCHES
    # ======================================================

    st.html(
        """<div class="college-section-header">

            <div>

                <div class="college-section-title">
                    📊 Role Match Ranking
                </div>

                <div class="college-section-subtitle">
                    Compare your profile with multiple placement roles.
                </div>

            </div>

            <div class="college-section-tag">
                Career Explorer
            </div>

        </div>"""
    )


    for rank, result in enumerate(
        role_results,
        start=1,
    ):

        readiness = get_readiness_label(
            result["score"]
        )

        icon = get_readiness_icon(
            result["score"]
        )


        st.html(
            f"""<div style="
                background:#ffffff;
                border:1px solid #e2e8f0;
                border-radius:20px;
                padding:20px 22px;
                margin-bottom:12px;
                box-shadow:0 7px 20px rgba(15,23,42,.04);
            ">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                    gap:20px;
                ">

                    <div>

                        <div style="
                            color:#94a3b8;
                            font-size:10px;
                            font-weight:900;
                            letter-spacing:1px;
                        ">
                            MATCH #{rank}
                        </div>

                        <div style="
                            color:#0f172a;
                            font-size:17px;
                            font-weight:800;
                            margin-top:5px;
                        ">
                            {result["role"]}
                        </div>

                        <div style="
                            color:#64748b;
                            font-size:12px;
                            margin-top:6px;
                        ">
                            {icon} {readiness}
                        </div>

                    </div>


                    <div style="
                        color:#2563eb;
                        font-size:25px;
                        font-weight:900;
                    ">
                        {result["score"]}%
                    </div>

                </div>

            </div>"""
        )


        with st.expander(
            f'View {result["role"]} skill analysis'
        ):

            st.write(
                f'**Matched:** '
                f'{len(result["matched"])} / '
                f'{len(result["required"])}'
            )

            st.progress(
                result["score"] / 100
            )

            c1, c2 = st.columns(2)


            with c1:

                st.markdown(
                    "##### ✅ Matching"
                )

                if result["matched"]:

                    for skill in result["matched"]:
                        st.success(skill)

                else:
                    st.caption(
                        "No matching skills yet."
                    )


            with c2:

                st.markdown(
                    "##### ❌ Missing"
                )

                if result["missing"]:

                    for skill in result["missing"]:
                        st.warning(skill)

                else:
                    st.success(
                        "No major skill gaps."
                    )


    # ======================================================
    # NEXT ACTIONS
    # ======================================================

    st.html(
        """<div class="college-section-header">

            <div>

                <div class="college-section-title">
                    🚀 Recommended Next Actions
                </div>

                <div class="college-section-subtitle">
                    Improve your profile before applying for jobs.
                </div>

            </div>

        </div>"""
    )


    next_steps = []


    if best_match and best_match["missing"]:

        next_steps.append(
            f'Learn **{best_match["missing"][0]}** to improve '
            f'your {best_match["role"]} match.'
        )


        if len(best_match["missing"]) > 1:

            next_steps.append(
                f'Next focus on **{best_match["missing"][1]}**.'
            )


    next_steps.extend(
        [
            "Build at least one portfolio project related to your target role.",
            "Update your technical skills in College Profile after learning new technologies.",
            "Use Skill Gap Analysis to prioritize missing skills.",
            "Practice Coding and Interview Prep regularly.",
            "Review your Resume and ATS Checker before applying.",
        ]
    )


    for number, step in enumerate(
        next_steps,
        start=1,
    ):

        st.markdown(
            f"**{number}.** {step}"
        )


if __name__ == "__main__":
    render()