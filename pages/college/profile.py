import html as html_lib

import streamlit as st

from database.college_repository import (
    get_college_profile,
    save_college_profile,
)

from services.college.profile_service import (
    completion,
    safe_float,
)

from styles.college.theme import (
    apply_college_theme,
)


# ==========================================================
# SAFE INTEGER
# ==========================================================

def safe_int(
    value,
    default=0,
):

    try:

        if value is None:
            return default

        if isinstance(
            value,
            int,
        ):
            return value

        if isinstance(
            value,
            float,
        ):
            return int(
                value
            )

        value = str(
            value
        ).strip()

        if not value:
            return default

        return int(
            float(
                value
            )
        )

    except (
        ValueError,
        TypeError,
    ):

        return default


# ==========================================================
# SAFE DISPLAY VALUE
# ==========================================================

def clean_display_value(
    value,
    fallback="Not added",
):

    if value is None:

        return fallback


    # Do not show lists such as
    # ["GitHub", "VS Code", "Postman"]
    # inside Target Role card.

    if isinstance(
        value,
        (
            list,
            tuple,
            set,
            dict,
        ),
    ):

        return fallback


    value = str(
        value
    ).strip()


    if not value:

        return fallback


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


    if (
        value.lower()
        in invalid_values
    ):

        return fallback


    # Detect accidentally stored
    # list-like strings.

    if (
        value.startswith("[")
        and value.endswith("]")
    ):

        return fallback


    return value


# ==========================================================
# SAFE HTML
# ==========================================================

def safe_html(
    value,
):

    return html_lib.escape(
        str(
            value
            or ""
        )
    )


# ==========================================================
# VALID URL
# ==========================================================

def clean_url(
    value,
):

    value = clean_display_value(
        value,
        "",
    )

    if not value:
        return ""

    return value


# ==========================================================
# PAGE
# ==========================================================

def render():

    apply_college_theme()


    # ======================================================
    # USER
    # ======================================================

    user_id = (
        st.session_state.get(
            "user_id"
        )
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

        profile = {}


    # ======================================================
    # PROFILE SCORE
    # ======================================================

    try:

        profile_score = (
            completion(
                profile
            )
        )

    except Exception:

        profile_score = 0


    # ======================================================
    # SAFE VALUES
    # ======================================================

    current_cgpa = safe_float(
        profile.get(
            "cgpa"
        ),
        0.0,
    )


    current_cgpa = max(
        0.0,
        min(
            10.0,
            current_cgpa,
        ),
    )


    current_backlogs = max(
        0,
        safe_int(
            profile.get(
                "backlogs"
            ),
            0,
        ),
    )


    target_role = (
        clean_display_value(
            profile.get(
                "preferred_role"
            ),
            "Not added",
        )
    )


    # ======================================================
    # USER NAME
    # ======================================================

    user_name = (
        st.session_state.get(
            "user_name"
        )
        or "College Student"
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
        👤 COLLEGE STUDENT PROFILE
    </div>

    <div class="
        college-hero-title
    ">
        {safe_html(user_name)}'s Placement Profile
    </div>

    <div class="
        college-hero-description
    ">
        Add your academic information,
        CGPA, technical skills, projects,
        internships, certifications,
        placement goals and professional links.
        TalentSphere uses this information
        throughout your College Workspace.
    </div>

</div>
"""
    )


    # ======================================================
    # SUMMARY CARDS
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
            👤
        </div>

        <div class="
            college-metric-label
        ">
            Profile Completion
        </div>

        <div class="
            college-metric-value
        ">
            {profile_score}%
        </div>

        <div class="
            college-metric-caption
        ">
            Complete all sections
            for better recommendations.
        </div>

    </div>


    <div class="
        college-metric-card
    ">

        <div class="
            college-metric-icon
        ">
            🎓
        </div>

        <div class="
            college-metric-label
        ">
            Current CGPA
        </div>

        <div class="
            college-metric-value
        ">
            {current_cgpa:.1f}
        </div>

        <div class="
            college-metric-caption
        ">
            Your current academic performance.
        </div>

    </div>


    <div class="
        college-metric-card
    ">

        <div class="
            college-metric-icon
        ">
            📚
        </div>

        <div class="
            college-metric-label
        ">
            Active Backlogs
        </div>

        <div class="
            college-metric-value
        ">
            {current_backlogs}
        </div>

        <div class="
            college-metric-caption
        ">
            Current uncleared subjects.
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
            Target Role
        </div>

        <div
            class="
                college-metric-value
            "
            title="{safe_html(target_role)}"
        >
            {safe_html(target_role)}
        </div>

        <div class="
            college-metric-caption
        ">
            Your current placement direction.
        </div>

    </div>

</div>
"""
    )


    # ======================================================
    # PROFILE PROGRESS
    # ======================================================

    st.progress(
        profile_score
        / 100
    )


    # ======================================================
    # SELECT OPTIONS
    # ======================================================

    year_options = [

        "1st Year",
        "2nd Year",
        "3rd Year",
        "4th Year",

    ]


    semester_options = [

        "Semester 1",
        "Semester 2",
        "Semester 3",
        "Semester 4",
        "Semester 5",
        "Semester 6",
        "Semester 7",
        "Semester 8",

    ]


    role_options = [

        "Software Development Engineer",

        "Full Stack Developer",

        "Frontend Developer",

        "Backend Developer",

        "Data Analyst",

        "Data Scientist",

        "Machine Learning Engineer",

        "AI Engineer",

        "Cloud Engineer",

        "DevOps Engineer",

        "Cybersecurity Engineer",

        "QA / Test Engineer",

        "Business Analyst",

        "Other",

    ]


    # ======================================================
    # CURRENT YEAR
    # ======================================================

    saved_year = clean_display_value(
        profile.get(
            "current_year"
        ),
        "",
    )


    if (
        saved_year
        in year_options
    ):

        year_index = (
            year_options.index(
                saved_year
            )
        )

    else:

        year_index = 0


    # ======================================================
    # CURRENT SEMESTER
    # ======================================================

    saved_semester = clean_display_value(
        profile.get(
            "semester"
        ),
        "",
    )


    if (
        saved_semester
        in semester_options
    ):

        semester_index = (
            semester_options.index(
                saved_semester
            )
        )

    else:

        semester_index = 0


    # ======================================================
    # CURRENT ROLE
    # ======================================================

    saved_role = clean_display_value(
        profile.get(
            "preferred_role"
        ),
        "",
    )


    if (
        saved_role
        in role_options
    ):

        role_index = (
            role_options.index(
                saved_role
            )
        )

    else:

        role_index = 0


    # ======================================================
    # COMPLETE PROFILE FORM
    # ======================================================

    with st.form(
        "college_profile_form",
        clear_on_submit=False,
    ):


        # ==================================================
        # ACADEMIC INFORMATION
        # ==================================================

        st.html(
            """
<div class="college-section-header">

    <div>

        <div class="
            college-section-title
        ">
            🎓 Academic Information
        </div>

        <div class="
            college-section-subtitle
        ">
            Add your current college
            and academic details.
        </div>

    </div>

</div>
"""
        )


        academic_left, academic_right = (
            st.columns(
                2
            )
        )


        with academic_left:

            college_name = (
                st.text_input(
                    "College Name",
                    value=clean_display_value(
                        profile.get(
                            "college_name"
                        ),
                        "",
                    ),
                    placeholder=(
                        "Example: "
                        "Sri Venkateswara "
                        "College of Engineering"
                    ),
                )
            )


            degree = (
                st.text_input(
                    "Degree",
                    value=clean_display_value(
                        profile.get(
                            "degree"
                        ),
                        "",
                    ),
                    placeholder=(
                        "Example: B.Tech"
                    ),
                )
            )


            branch = (
                st.text_input(
                    "Branch / Specialization",
                    value=clean_display_value(
                        profile.get(
                            "branch"
                        ),
                        "",
                    ),
                    placeholder=(
                        "Example: "
                        "CSE (AI & ML)"
                    ),
                )
            )


            current_year = (
                st.selectbox(
                    "Current Year",
                    year_options,
                    index=year_index,
                )
            )


        with academic_right:

            semester = (
                st.selectbox(
                    "Current Semester",
                    semester_options,
                    index=semester_index,
                )
            )


            graduation_year = (
                st.text_input(
                    "Graduation Year",
                    value=clean_display_value(
                        profile.get(
                            "graduation_year"
                        ),
                        "",
                    ),
                    placeholder=(
                        "Example: 2027"
                    ),
                )
            )


            cgpa = (
                st.number_input(
                    "Current CGPA",
                    min_value=0.0,
                    max_value=10.0,
                    value=current_cgpa,
                    step=0.1,
                    format="%.1f",
                )
            )


            backlogs = (
                st.number_input(
                    "Active Backlogs",
                    min_value=0,
                    max_value=50,
                    value=current_backlogs,
                    step=1,
                )
            )


        st.divider()


        # ==================================================
        # SKILLS
        # ==================================================

        st.html(
            """
<div class="college-section-header">

    <div>

        <div class="
            college-section-title
        ">
            💻 Skills
        </div>

        <div class="
            college-section-subtitle
        ">
            Add technical and
            professional skills.
        </div>

    </div>

</div>
"""
        )


        technical_skills = (
            st.text_area(
                "Technical Skills",
                value=clean_display_value(
                    profile.get(
                        "technical_skills"
                    ),
                    "",
                ),
                placeholder=(
                    "Python, Java, C++, "
                    "DSA, React, Node.js, "
                    "MongoDB, SQL"
                ),
                height=115,
            )
        )


        soft_skills = (
            st.text_area(
                "Soft Skills",
                value=clean_display_value(
                    profile.get(
                        "soft_skills"
                    ),
                    "",
                ),
                placeholder=(
                    "Communication, "
                    "Teamwork, Leadership, "
                    "Problem Solving"
                ),
                height=95,
            )
        )


        st.divider()


        # ==================================================
        # PROJECTS
        # ==================================================

        st.html(
            """
<div class="college-section-header">

    <div>

        <div class="
            college-section-title
        ">
            🚀 Projects & Experience
        </div>

        <div class="
            college-section-subtitle
        ">
            Build evidence of your
            technical and practical experience.
        </div>

    </div>

</div>
"""
        )


        projects = (
            st.text_area(
                "Projects",
                value=clean_display_value(
                    profile.get(
                        "projects"
                    ),
                    "",
                ),
                placeholder=(
                    "Mention project name, "
                    "technology, main features "
                    "and your contribution."
                ),
                height=140,
            )
        )


        internships = (
            st.text_area(
                "Internships / Training",
                value=clean_display_value(
                    profile.get(
                        "internships"
                    ),
                    "",
                ),
                placeholder=(
                    "Example: Infosys "
                    "Springboard Internship"
                ),
                height=120,
            )
        )


        certifications = (
            st.text_area(
                "Certifications",
                value=clean_display_value(
                    profile.get(
                        "certifications"
                    ),
                    "",
                ),
                placeholder=(
                    "NPTEL, Infosys Springboard, "
                    "Google Cloud, Coursera"
                ),
                height=100,
            )
        )


        achievements = (
            st.text_area(
                "Achievements",
                value=clean_display_value(
                    profile.get(
                        "achievements"
                    ),
                    "",
                ),
                placeholder=(
                    "Hackathons, coding competitions, "
                    "awards and academic achievements"
                ),
                height=100,
            )
        )


        st.divider()


        # ==================================================
        # PLACEMENT GOALS
        # ==================================================

        st.html(
            """
<div class="college-section-header">

    <div>

        <div class="
            college-section-title
        ">
            🎯 Placement Goals
        </div>

        <div class="
            college-section-subtitle
        ">
            Define your target role
            and placement direction.
        </div>

    </div>

</div>
"""
        )


        placement_left, placement_right = (
            st.columns(
                2
            )
        )


        with placement_left:

            preferred_role = (
                st.selectbox(
                    "Preferred Job Role",
                    role_options,
                    index=role_index,
                )
            )


        with placement_right:

            coding_platforms = (
                st.text_area(
                    "Coding Platform Links",
                    value=clean_display_value(
                        profile.get(
                            "coding_platforms"
                        ),
                        "",
                    ),
                    placeholder=(
                        "LeetCode, HackerRank, "
                        "CodeChef profile links"
                    ),
                    height=100,
                )
            )


        placement_goal = (
            st.text_area(
                "Placement Goal",
                value=clean_display_value(
                    profile.get(
                        "placement_goal"
                    ),
                    "",
                ),
                placeholder=(
                    "Example: Become placement-ready "
                    "for product-based companies."
                ),
                height=110,
            )
        )


        st.divider()


        # ==================================================
        # PROFESSIONAL LINKS
        # ==================================================

        st.html(
            """
<div class="college-section-header">

    <div>

        <div class="
            college-section-title
        ">
            🔗 Professional Presence
        </div>

        <div class="
            college-section-subtitle
        ">
            Add your professional
            portfolio and social links.
        </div>

    </div>

</div>
"""
        )


        link_left, link_right = (
            st.columns(
                2
            )
        )


        with link_left:

            github_url = (
                st.text_input(
                    "GitHub Profile URL",
                    value=clean_url(
                        profile.get(
                            "github_url"
                        )
                    ),
                    placeholder=(
                        "https://github.com/username"
                    ),
                )
            )


            linkedin_url = (
                st.text_input(
                    "LinkedIn Profile URL",
                    value=clean_url(
                        profile.get(
                            "linkedin_url"
                        )
                    ),
                    placeholder=(
                        "https://linkedin.com/in/username"
                    ),
                )
            )


        with link_right:

            portfolio_url = (
                st.text_input(
                    "Portfolio URL",
                    value=clean_url(
                        profile.get(
                            "portfolio_url"
                        )
                    ),
                    placeholder=(
                        "https://yourportfolio.com"
                    ),
                )
            )


        st.write("")


        # ==================================================
        # SAVE BUTTON
        # ==================================================

        submitted = (
            st.form_submit_button(
                "💾 Save College Profile",
                use_container_width=True,
            )
        )


    # ======================================================
    # SAVE PROFILE
    # ======================================================

    if submitted:


        # ==================================================
        # VALIDATION
        # ==================================================

        if not college_name.strip():

            st.error(
                "Please enter your college name."
            )

            return


        if not degree.strip():

            st.error(
                "Please enter your degree."
            )

            return


        if not branch.strip():

            st.error(
                "Please enter your branch or specialization."
            )

            return


        # ==================================================
        # SAVE
        # ==================================================

        try:

            save_college_profile(

                user_id,

                college_name=
                    college_name.strip(),

                degree=
                    degree.strip(),

                branch=
                    branch.strip(),

                current_year=
                    current_year,

                semester=
                    semester,

                graduation_year=
                    graduation_year.strip(),

                cgpa=
                    float(
                        cgpa
                    ),

                backlogs=
                    int(
                        backlogs
                    ),

                technical_skills=
                    technical_skills.strip(),

                soft_skills=
                    soft_skills.strip(),

                projects=
                    projects.strip(),

                internships=
                    internships.strip(),

                certifications=
                    certifications.strip(),

                preferred_role=
                    preferred_role,

                placement_goal=
                    placement_goal.strip(),

                github_url=
                    github_url.strip(),

                linkedin_url=
                    linkedin_url.strip(),

                portfolio_url=
                    portfolio_url.strip(),

                coding_platforms=
                    coding_platforms.strip(),

                achievements=
                    achievements.strip(),

            )


            st.success(
                "✅ College profile saved successfully."
            )


            st.rerun()


        except Exception as error:

            st.error(
                (
                    "Unable to save college profile: "
                    f"{error}"
                )
            )