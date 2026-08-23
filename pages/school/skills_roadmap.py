import streamlit as st

from components.back_button import (
    render_back_to_school_dashboard,
)

from database.school_repository import (
    get_school_profile,
)

from services.skills_roadmap_service import (
    get_roadmap,
    calculate_progress,
    get_next_skill,
)

from styles.skills_roadmap_theme import (
    apply_skills_roadmap_theme,
)


# ==========================================================
# GET CAREER AREA
# ==========================================================

def resolve_career_area(
    profile,
):

    selected_area = st.session_state.get(
        "selected_career_area"
    )

    if selected_area:
        return selected_area


    dream_career = (
        profile.get(
            "dream_career"
        )
        or ""
    ).lower()


    mapping = {

        "doctor":
            "Science & Medicine",

        "medicine":
            "Science & Medicine",

        "pharmacist":
            "Science & Medicine",

        "software":
            "Engineering & Technology",

        "engineer":
            "Engineering & Technology",

        "robot":
            "Engineering & Technology",

        "computer":
            "Engineering & Technology",

        "business":
            "Business & Commerce",

        "entrepreneur":
            "Business & Commerce",

        "account":
            "Business & Commerce",

        "designer":
            "Arts & Design",

        "artist":
            "Arts & Design",

        "architect":
            "Arts & Design",

        "lawyer":
            "Law & Public Services",

        "civil service":
            "Law & Public Services",

        "journalist":
            "Media & Communication",

        "media":
            "Media & Communication",

        "writer":
            "Media & Communication",

        "sports":
            "Sports & Fitness",

        "cricket":
            "Sports & Fitness",

        "athlete":
            "Sports & Fitness",

        "agriculture":
            "Agriculture & Environment",

        "environment":
            "Agriculture & Environment",
    }


    for keyword, category in mapping.items():

        if keyword in dream_career:
            return category


    return "General Skill Development"


# ==========================================================
# SESSION PROGRESS
# ==========================================================

def get_completed_skills(
    career_area,
):

    key = (
        "skills_roadmap_completed_"
        + career_area
        .replace(" ", "_")
        .replace("&", "and")
    )

    if key not in st.session_state:

        st.session_state[
            key
        ] = []

    return key, st.session_state[key]


# ==========================================================
# LEVEL DESCRIPTION
# ==========================================================

def level_description(
    level_name,
):

    descriptions = {

        "Beginner":
            "Start with strong school-level foundations.",

        "Intermediate":
            "Apply your foundations through activities and practice.",

        "Advanced":
            "Build projects, portfolios and deeper skills.",
    }

    return descriptions.get(
        level_name,
        ""
    )


# ==========================================================
# PAGE
# ==========================================================

def render():

    apply_skills_roadmap_theme()


    # ======================================================
    # BACK TO DASHBOARD
    # ======================================================

    render_back_to_school_dashboard(
        key="skills_roadmap_dashboard_back",
    )


    # ======================================================
    # USER
    # ======================================================

    user_id = st.session_state.get(
        "user_id"
    )


    if not user_id:

        st.error(
            "Unable to identify the logged-in student."
        )

        return


    # ======================================================
    # PROFILE
    # ======================================================

    try:

        profile = get_school_profile(
            user_id
        )

    except Exception:

        profile = {}


    if not profile:

        profile = {}


    # ======================================================
    # CAREER AREA
    # ======================================================

    career_area = resolve_career_area(
        profile
    )


    # ======================================================
    # ROADMAP
    # ======================================================

    roadmap = get_roadmap(
        career_area
    )


    # ======================================================
    # COMPLETION STATE
    # ======================================================

    progress_key, completed_skills = (
        get_completed_skills(
            career_area
        )
    )


    # ======================================================
    # PROGRESS
    # ======================================================

    progress = calculate_progress(
        roadmap,
        completed_skills,
    )


    next_skill = get_next_skill(
        roadmap,
        completed_skills,
    )


    # ======================================================
    # HERO
    # ======================================================

    st.html(
        f"""
<div class="skills-hero">

    <div class="skills-eyebrow">
        HIGH SCHOOL SKILLS ROADMAP
    </div>

    <div class="skills-title">
        {roadmap["icon"]} Build Your Skills Step by Step
    </div>

    <div class="skills-description">
        Your current roadmap is designed around
        <b>{career_area}</b>. Complete the skills gradually
        during school. You do not need to learn everything
        at once.
    </div>

</div>
"""
    )


    # ======================================================
    # SUMMARY
    # ======================================================

    st.html(
        f"""
<div class="skills-summary-grid">

    <div class="skills-summary-card">

        <div class="skills-summary-label">
            Career Area
        </div>

        <div class="skills-summary-value">
            {career_area}
        </div>

    </div>


    <div class="skills-summary-card">

        <div class="skills-summary-label">
            Roadmap Progress
        </div>

        <div class="skills-summary-value">
            {progress}%
        </div>

    </div>


    <div class="skills-summary-card">

        <div class="skills-summary-label">
            Completed Skills
        </div>

        <div class="skills-summary-value">
            {len(completed_skills)}
        </div>

    </div>

</div>
"""
    )


    # ======================================================
    # PROGRESS BAR
    # ======================================================

    st.progress(
        progress / 100
    )


    st.caption(
        roadmap[
            "description"
        ]
    )


    # ======================================================
    # NEXT SKILL
    # ======================================================

    if next_skill:

        st.html(
            f"""
<div class="next-skill-card">

    <div class="next-skill-label">
        Recommended Next Skill · {next_skill["level"]}
    </div>

    <div class="next-skill-title">
        {next_skill["skill"]}
    </div>

    <div class="next-skill-text">
        {next_skill["description"]}
    </div>

</div>
"""
        )

    else:

        st.success(
            "🎉 You completed this roadmap."
        )


    # ======================================================
    # ROADMAP LEVELS
    # ======================================================

    for level_name, skills in roadmap[
        "levels"
    ].items():

        st.html(
            f"""
<div class="skills-level-header">

    <div class="skills-level-title">
        {level_name} Level
    </div>

    <div class="skills-level-description">
        {level_description(level_name)}
    </div>

</div>
"""
        )


        # ==================================================
        # SKILL ROWS
        # ==================================================

        for start_index in range(
            0,
            len(skills),
            2,
        ):

            row = skills[
                start_index:
                start_index + 2
            ]

            columns = st.columns(
                len(row)
            )


            for column_index, skill in enumerate(
                row
            ):

                with columns[
                    column_index
                ]:

                    skill_name = (
                        skill[
                            "skill"
                        ]
                    )

                    completed = (
                        skill_name
                        in completed_skills
                    )


                    st.html(
                        f"""
<div class="skill-card">

    <div class="skill-card-title">
        {"✅" if completed else "📘"}
        {skill_name}
    </div>

    <div class="skill-card-description">
        {skill["description"]}
    </div>

</div>
"""
                    )


                    # ======================================
                    # COMPLETION BUTTON
                    # ======================================

                    if completed:

                        button_label = (
                            "✓ Completed"
                        )

                    else:

                        button_label = (
                            "Mark as Completed"
                        )


                    if st.button(
                        button_label,
                        key=(
                            "skill_"
                            + level_name
                            + "_"
                            + str(
                                start_index
                            )
                            + "_"
                            + str(
                                column_index
                            )
                        ),
                        use_container_width=True,
                    ):

                        current = list(
                            st.session_state[
                                progress_key
                            ]
                        )


                        if skill_name in current:

                            current.remove(
                                skill_name
                            )

                        else:

                            current.append(
                                skill_name
                            )


                        st.session_state[
                            progress_key
                        ] = current

                        st.rerun()


    # ======================================================
    # NAVIGATION
    # ======================================================

    st.divider()

    st.markdown(
        "## 🚀 Continue Your Journey"
    )


    nav1, nav2 = st.columns(
        2
    )


    # ======================================================
    # CAREER EXPLORER
    # ======================================================

    with nav1:

        if st.button(
            "🔍 Back to Career Explorer",
            key="skills_back_career",
            use_container_width=True,
        ):

            st.session_state.school_navigation = (
                "🔍 Career Explorer"
            )

            st.rerun()


    # ======================================================
    # INTEREST ASSESSMENT
    # ======================================================

    with nav2:

        if st.button(
            "📊 Take Interest Assessment",
            key="skills_interest_assessment",
            use_container_width=True,
        ):

            st.session_state.school_navigation = (
                "📊 Interest Assessment"
            )

            st.rerun()