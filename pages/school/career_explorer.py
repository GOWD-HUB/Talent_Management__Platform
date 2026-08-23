import html as html_lib

import streamlit as st

from components.back_button import render_back_to_school_dashboard
from database.school_repository import get_school_profile
from services.career_service import recommend_categories
from styles.career_explorer_theme import apply_career_explorer_theme


# ==========================================================
# HELPERS
# ==========================================================

def safe(value):
    if value is None:
        return ""

    return html_lib.escape(str(value))


def find_category(categories, category_name):

    for category in categories:

        if category.get("category") == category_name:
            return category

    return None


# ==========================================================
# CATEGORY CARD
# ==========================================================

def render_category_card(category):

    reasons = category.get(
        "reasons",
        ["A career area worth exploring"],
    )

    reasons_text = " • ".join(reasons)

    st.html(
        f"""
<div class="hs-category-card">

    <div class="hs-category-icon">
        {safe(category.get("icon", "🌟"))}
    </div>

    <div class="hs-category-title">
        {safe(category.get("category", "Career Area"))}
    </div>

    <div class="hs-category-description">
        {safe(category.get("description", ""))}
    </div>

    <div class="hs-match">
        {safe(category.get("match_score", 0))}% Exploration Match
    </div>

    <div class="hs-stream">
        💡 {safe(reasons_text)}
    </div>

</div>
"""
    )


# ==========================================================
# CAREER DETAIL
# ==========================================================

def render_career_detail(career):

    st.html(
        f"""
<div class="hs-career-option">

    <div class="hs-career-option-title">
        {safe(career.get("icon", "🚀"))}
        {safe(career.get("title", "Career"))}
    </div>

    <div class="hs-career-option-text">
        {safe(career.get("description", ""))}
    </div>

</div>
"""
    )

    left, right = st.columns(2)

    # ======================================================
    # SUBJECTS / SKILLS
    # ======================================================

    with left:

        st.markdown("#### 📚 Subjects to Focus On")

        subjects = career.get(
            "subjects",
            [],
        )

        if subjects:

            for subject in subjects:
                st.write(f"✅ {subject}")

        else:

            st.caption(
                "Subject guidance will be added soon."
            )

        st.markdown("#### 🧠 Skills to Start Building")

        skills = career.get(
            "skills",
            [],
        )

        if skills:

            for skill in skills:
                st.write(f"✅ {skill}")

        else:

            st.caption(
                "Skill guidance will be added soon."
            )

    # ======================================================
    # STUDY PATH
    # ======================================================

    with right:

        after_10 = safe(
            career.get(
                "after_10",
                "Explore suitable streams based on your interests.",
            )
        )

        after_12 = safe(
            career.get(
                "after_12",
                "Explore suitable higher education options.",
            )
        )

        st.html(
            f"""
<div class="hs-path-box">

    <div class="hs-path-label">
        After Class 10
    </div>

    <div class="hs-path-value">
        {after_10}
    </div>

</div>
"""
        )

        st.html(
            f"""
<div class="hs-path-box">

    <div class="hs-path-label">
        After Class 12
    </div>

    <div class="hs-path-value">
        {after_12}
    </div>

</div>
"""
        )


# ==========================================================
# SELECTED CATEGORY PAGE
# ==========================================================

def render_selected_category(category):

    # ======================================================
    # NAVIGATION
    # ======================================================

    back_col, dashboard_col, spacer = st.columns(
        [1.5, 1.7, 6.8]
    )

    with back_col:

        if st.button(
            "← Career Areas",
            key="career_back_to_areas",
            use_container_width=True,
        ):

            st.session_state.pop(
                "selected_school_category",
                None,
            )

            st.rerun()

    with dashboard_col:

        if st.button(
            "🏠 Dashboard",
            key="career_detail_dashboard",
            use_container_width=True,
        ):

            st.session_state.pop(
                "selected_school_category",
                None,
            )

            st.session_state.school_navigation = (
                "🏠 Student Home"
            )

            st.rerun()

    # ======================================================
    # CATEGORY HEADER
    # ======================================================

    st.html(
        f"""
<div class="hs-detail-card">

    <div class="hs-category-icon">
        {safe(category.get("icon", "🌟"))}
    </div>

    <div class="hs-detail-title">
        {safe(category.get("category", "Career Area"))}
    </div>

    <div class="hs-detail-description">
        {safe(category.get("description", ""))}
    </div>

</div>
"""
    )

    # ======================================================
    # OVERVIEW
    # ======================================================

    st.markdown("## 📊 Career Area Overview")

    metric1, metric2, metric3 = st.columns(3)

    with metric1:

        st.metric(
            "Exploration Match",
            f'{category.get("match_score", 0)}%',
        )

    with metric2:

        st.metric(
            "Career Options",
            len(
                category.get(
                    "careers",
                    [],
                )
            ),
        )

    with metric3:

        st.metric(
            "Important Subjects",
            len(
                category.get(
                    "subjects",
                    [],
                )
            ),
        )

    # ======================================================
    # WHY MATCHED
    # ======================================================

    st.markdown("## 💡 Why This Area May Suit You")

    reasons = category.get(
        "reasons",
        [],
    )

    if reasons:

        for reason in reasons:
            st.write(f"✅ {reason}")

    else:

        st.info(
            "Complete your School Profile and Interest "
            "Assessment for better matching."
        )

    # ======================================================
    # SUBJECTS
    # ======================================================

    st.markdown("## 📚 Subjects Connected to This Area")

    subjects = category.get(
        "subjects",
        [],
    )

    if subjects:

        subject_columns = st.columns(
            min(
                len(subjects),
                4,
            )
        )

        for index, subject in enumerate(subjects):

            with subject_columns[
                index % len(subject_columns)
            ]:

                st.info(subject)

    # ======================================================
    # STREAM AFTER CLASS 10
    # ======================================================

    st.markdown("## 🎓 Direction After Class 10")

    st.success(
        category.get(
            "stream_after_10",
            (
                "Choose the stream that best matches "
                "your strengths and interests."
            ),
        )
    )

    # ======================================================
    # CAREER OPTIONS
    # ======================================================

    st.markdown("## 🚀 Careers You Can Explore")

    st.caption(
        "These are examples within this career area. "
        "You do not need to choose one permanently now."
    )

    careers = category.get(
        "careers",
        [],
    )

    if careers:

        for career in careers:

            render_career_detail(career)

            st.divider()

    else:

        st.info(
            "Career options will be added soon."
        )

    # ======================================================
    # NEXT ACTIONS
    # ======================================================

    st.markdown("## 🎯 Continue Your Exploration")

    action1, action2 = st.columns(2)

    with action1:

        if st.button(
            "📊 Take Interest Assessment",
            key="career_open_interest",
            use_container_width=True,
        ):

            st.session_state.pop(
                "selected_school_category",
                None,
            )

            st.session_state.school_navigation = (
                "📊 Interest Assessment"
            )

            st.rerun()

    with action2:

        if st.button(
            "🗺️ View Skills Roadmap",
            key="career_open_roadmap",
            use_container_width=True,
        ):

            st.session_state[
                "selected_career_area"
            ] = category.get(
                "category"
            )

            st.session_state.pop(
                "selected_school_category",
                None,
            )

            st.session_state.school_navigation = (
                "🗺️ Skills Roadmap"
            )

            st.rerun()

    # ======================================================
    # FINAL NOTE
    # ======================================================

    st.html(
        """
<div class="hs-explore-note">

    <div class="hs-explore-note-title">
        🌱 Keep Exploring
    </div>

    <div class="hs-explore-note-text">
        Your interests may change as you learn new subjects
        and gain new experiences. Use school projects,
        competitions, clubs and activities to understand
        your strengths before making major academic choices.
    </div>

</div>
"""
    )


# ==========================================================
# MAIN PAGE
# ==========================================================

def render():

    # ======================================================
    # THEME
    # ======================================================

    apply_career_explorer_theme()

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

    except Exception as error:

        st.error(
            f"Unable to load your School Profile: {error}"
        )

        return

    if not profile:
        profile = {}

    # ======================================================
    # CATEGORIES
    # ======================================================

    try:

        categories = recommend_categories(
            profile
        )

    except Exception as error:

        st.error(
            f"Unable to generate career recommendations: {error}"
        )

        return

    # ======================================================
    # SELECTED CATEGORY
    # ======================================================

    selected_category_name = (
        st.session_state.get(
            "selected_school_category"
        )
    )

    if selected_category_name:

        selected_category = find_category(
            categories,
            selected_category_name,
        )

        if selected_category:

            render_selected_category(
                selected_category
            )

            return

        else:

            st.session_state.pop(
                "selected_school_category",
                None,
            )

    # ======================================================
    # BACK TO DASHBOARD
    # ======================================================

    render_back_to_school_dashboard(
        key="career_main_dashboard",
    )

    # ======================================================
    # PROFILE VALUES
    # ======================================================

    current_class = safe(
        profile.get(
            "current_class"
        )
        or "Not added"
    )

    favourite_subjects = safe(
        profile.get(
            "favourite_subjects"
        )
        or "Not added"
    )

    interests = safe(
        profile.get(
            "interests"
        )
        or "Not added"
    )

    dream_career = safe(
        profile.get(
            "dream_career"
        )
        or "Still exploring"
    )

    # ======================================================
    # HERO
    # ======================================================

    st.html(
        """
<div class="hs-career-hero">

    <div class="hs-career-badge">
        HIGH SCHOOL CAREER DISCOVERY
    </div>

    <div class="hs-career-title">
        🔍 Explore Your Future
    </div>

    <div class="hs-career-description">
        Discover career areas based on your interests
        and favourite subjects. Learn which subjects
        to focus on, what options are available after
        Class 10 and what study paths you can consider
        after Class 12.
    </div>

</div>
"""
    )

    # ======================================================
    # PROFILE SNAPSHOT
    # ======================================================

    st.html(
        f"""
<div class="hs-profile-grid">

    <div class="hs-profile-card">

        <div class="hs-profile-label">
            Current Class
        </div>

        <div class="hs-profile-value">
            {current_class}
        </div>

    </div>


    <div class="hs-profile-card">

        <div class="hs-profile-label">
            Favourite Subjects
        </div>

        <div class="hs-profile-value">
            {favourite_subjects}
        </div>

    </div>


    <div class="hs-profile-card">

        <div class="hs-profile-label">
            Interests
        </div>

        <div class="hs-profile-value">
            {interests}
        </div>

    </div>


    <div class="hs-profile-card">

        <div class="hs-profile-label">
            Dream Career
        </div>

        <div class="hs-profile-value">
            {dream_career}
        </div>

    </div>

</div>
"""
    )

    # ======================================================
    # GUIDANCE
    # ======================================================

    st.html(
        """
<div class="hs-guidance-strip">

    <div class="hs-guidance-icon">
        💡
    </div>

    <div>

        <div class="hs-guidance-title">
            Explore before you decide
        </div>

        <div class="hs-guidance-text">
            Use the Explore buttons below to understand
            different career areas, subjects, skills
            and future study options.
        </div>

    </div>

</div>
"""
    )

    # ======================================================
    # INCOMPLETE PROFILE
    # ======================================================

    profile_subjects = (
        profile.get(
            "favourite_subjects"
        )
        or ""
    )

    profile_interests = (
        profile.get(
            "interests"
        )
        or ""
    )

    if (
        not profile_subjects.strip()
        and not profile_interests.strip()
    ):

        st.warning(
            "Your career matches are currently general. "
            "Complete Favourite Subjects and Interests "
            "in School Profile for personalised results."
        )

    # ======================================================
    # SECTION TITLE
    # ======================================================

    st.html(
        """
<div class="hs-section-title">
    🌟 Career Areas to Explore
</div>

<div class="hs-section-description">
    Click Explore to open a career area and see
    its subjects, careers and study pathway.
</div>
"""
    )

    # ======================================================
    # CAREER GRID
    # ======================================================

    for start_index in range(
        0,
        len(categories),
        3,
    ):

        row = categories[
            start_index:
            start_index + 3
        ]

        columns = st.columns(
            len(row)
        )

        for column_index, category in enumerate(
            row
        ):

            with columns[column_index]:

                render_category_card(
                    category
                )

                clicked = st.button(
                    (
                        f'Explore '
                        f'{category.get("category")} →'
                    ),
                    key=(
                        f"career_explore_"
                        f"{start_index}_"
                        f"{column_index}"
                    ),
                    use_container_width=True,
                )

                if clicked:

                    st.session_state[
                        "selected_school_category"
                    ] = category.get(
                        "category"
                    )

                    st.rerun()