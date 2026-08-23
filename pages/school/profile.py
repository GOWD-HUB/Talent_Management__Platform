import streamlit as st

from database.school_repository import (
    get_school_profile,
    save_school_profile,
)

from styles.school_profile_theme import (
    apply_school_profile_theme,
)


# ==========================================================
# PROFILE COMPLETION
# ==========================================================

def calculate_profile_completion(profile):

    fields = [
        "school_name",
        "current_class",
        "board",
        "city",
        "parent_name",
        "phone",
        "percentage",
        "favourite_subjects",
        "interests",
        "skills",
        "dream_career",
        "academic_goal",
        "target_course",
        "achievements",
    ]

    completed = 0

    for field in fields:

        value = profile.get(field)

        if value and str(value).strip():
            completed += 1

    if not fields:
        return 0

    return int(
        completed / len(fields) * 100
    )


# ==========================================================
# METRIC CARD
# ==========================================================

def metric_card(
    label,
    value,
    description,
):

    return (
        '<div class="profile-metric-card">'
        f'<div class="profile-metric-label">{label}</div>'
        f'<div class="profile-metric-value">{value}</div>'
        f'<div class="profile-metric-text">{description}</div>'
        '</div>'
    )


# ==========================================================
# PROFILE PAGE
# ==========================================================

def render():

    # ======================================================
    # PROFILE PAGE THEME
    # ======================================================

    apply_school_profile_theme()


    # ======================================================
    # BACK TO DASHBOARD
    # ======================================================

    back_col, space_col = st.columns(
        [1.5, 8.5]
    )

    with back_col:

        if st.button(
            "← Dashboard",
            key="school_profile_back_dashboard",
            use_container_width=True,
        ):

            st.session_state.school_navigation = (
                "🏠 Student Home"
            )

            st.rerun()


    # ======================================================
    # USER SESSION
    # ======================================================

    user_id = st.session_state.get(
        "user_id"
    )

    user_name = (
        st.session_state.get(
            "user_name"
        )
        or "Student"
    )


    if not user_id:

        st.error(
            "Unable to identify the logged-in student."
        )

        return


    # ======================================================
    # LOAD PROFILE
    # ======================================================

    try:

        profile = get_school_profile(
            user_id
        )

    except Exception as error:

        st.error(
            f"Unable to load your profile: {error}"
        )

        profile = {}


    if profile is None:

        profile = {}


    # ======================================================
    # PROFILE COMPLETION
    # ======================================================

    completion = calculate_profile_completion(
        profile
    )


    # ======================================================
    # PROFILE HERO
    # ======================================================

    hero_html = (
        '<div class="student-profile-hero">'
        '<div class="student-profile-eyebrow">'
        'STUDENT PROFILE'
        '</div>'
        '<div class="student-profile-title">'
        f'{user_name}&apos;s Profile'
        '</div>'
        '<div class="student-profile-description">'
        'Build your complete academic and career profile. '
        'TalentSphere uses this information to personalise '
        'career exploration, skills roadmaps, learning '
        'recommendations and assessments.'
        '</div>'
        '</div>'
    )

    st.markdown(
        hero_html,
        unsafe_allow_html=True,
    )


    # ======================================================
    # PROFILE METRICS
    # ======================================================

    current_class_display = (
        profile.get("current_class")
        or "Not added"
    )

    dream_career_display = (
        profile.get("dream_career")
        or "Explore"
    )

    academic_goal_display = (
        profile.get("academic_goal")
        or "Not added"
    )


    metrics = [

        metric_card(
            "PROFILE COMPLETION",
            f"{completion}%",
            "Complete all sections for better recommendations.",
        ),

        metric_card(
            "CURRENT CLASS",
            current_class_display,
            "Your current academic level.",
        ),

        metric_card(
            "DREAM CAREER",
            dream_career_display,
            "Your preferred future career direction.",
        ),

        metric_card(
            "ACADEMIC GOAL",
            academic_goal_display,
            "Your current academic target.",
        ),
    ]


    st.markdown(
        (
            '<div class="profile-metric-grid">'
            + "".join(metrics)
            + '</div>'
        ),
        unsafe_allow_html=True,
    )


    # ======================================================
    # PROGRESS BAR
    # ======================================================

    st.progress(
        completion / 100
    )


    if completion == 100:

        st.success(
            "Your School Student profile is complete."
        )

    elif completion >= 60:

        st.info(
            "Your profile is progressing well. "
            "Complete the remaining details for better recommendations."
        )

    else:

        st.warning(
            "Complete more profile details before using "
            "career recommendations and skills roadmaps."
        )


    # ======================================================
    # PROFILE FORM
    # ======================================================

    with st.form(
        "school_student_profile_form",
        clear_on_submit=False,
    ):

        # ==================================================
        # ACADEMIC INFORMATION
        # ==================================================

        st.markdown(
            (
                '<div class="student-profile-section">'
                '<div class="student-profile-section-title">'
                '🏫 Academic Information'
                '</div>'
                '<div class="student-profile-section-description">'
                'Tell TalentSphere about your current education.'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )


        academic_col1, academic_col2 = (
            st.columns(2)
        )


        # --------------------------------------------------
        # ACADEMIC LEFT
        # --------------------------------------------------

        with academic_col1:

            school_name = st.text_input(
                "School Name",
                value=str(
                    profile.get(
                        "school_name",
                        "",
                    )
                    or ""
                ),
                placeholder="Enter your school name",
            )


            class_options = [
                "",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
            ]


            saved_class = str(
                profile.get(
                    "current_class",
                    "",
                )
                or ""
            )


            if saved_class not in class_options:

                saved_class = ""


            current_class = st.selectbox(
                "Current Class",
                class_options,
                index=class_options.index(
                    saved_class
                ),
            )


            percentage = st.text_input(
                "Current Percentage / CGPA",
                value=str(
                    profile.get(
                        "percentage",
                        "",
                    )
                    or ""
                ),
                placeholder="Example: 88% or 8.5 CGPA",
            )


        # --------------------------------------------------
        # ACADEMIC RIGHT
        # --------------------------------------------------

        with academic_col2:

            board_options = [
                "",
                "CBSE",
                "ICSE",
                "State Board",
                "IB",
                "Cambridge",
                "Other",
            ]


            saved_board = str(
                profile.get(
                    "board",
                    "",
                )
                or ""
            )


            if saved_board not in board_options:

                saved_board = ""


            board = st.selectbox(
                "Education Board",
                board_options,
                index=board_options.index(
                    saved_board
                ),
            )


            city = st.text_input(
                "City",
                value=str(
                    profile.get(
                        "city",
                        "",
                    )
                    or ""
                ),
                placeholder="Enter your city",
            )


            favourite_subjects = st.text_input(
                "Favourite Subjects",
                value=str(
                    profile.get(
                        "favourite_subjects",
                        "",
                    )
                    or ""
                ),
                placeholder=(
                    "Mathematics, Science, Computer Science"
                ),
            )


        st.divider()


        # ==================================================
        # CONTACT INFORMATION
        # ==================================================

        st.markdown(
            (
                '<div class="student-profile-section">'
                '<div class="student-profile-section-title">'
                '👨‍👩‍👧 Contact Information'
                '</div>'
                '<div class="student-profile-section-description">'
                'Add your guardian and contact information.'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )


        contact_col1, contact_col2 = (
            st.columns(2)
        )


        with contact_col1:

            parent_name = st.text_input(
                "Parent / Guardian Name",
                value=str(
                    profile.get(
                        "parent_name",
                        "",
                    )
                    or ""
                ),
                placeholder=(
                    "Enter parent or guardian name"
                ),
            )


        with contact_col2:

            phone = st.text_input(
                "Contact Number",
                value=str(
                    profile.get(
                        "phone",
                        "",
                    )
                    or ""
                ),
                placeholder="Enter contact number",
            )


        st.divider()


        # ==================================================
        # INTERESTS AND SKILLS
        # ==================================================

        st.markdown(
            (
                '<div class="student-profile-section">'
                '<div class="student-profile-section-title">'
                '💡 Interests & Skills'
                '</div>'
                '<div class="student-profile-section-description">'
                'These details help TalentSphere understand '
                'your strengths and interests.'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )


        interest_col, skill_col = (
            st.columns(2)
        )


        with interest_col:

            interests = st.text_area(
                "Interests",
                value=str(
                    profile.get(
                        "interests",
                        "",
                    )
                    or ""
                ),
                placeholder=(
                    "Technology, science, robotics, sports, "
                    "drawing, business..."
                ),
                height=125,
            )


        with skill_col:

            skills = st.text_area(
                "Current Skills",
                value=str(
                    profile.get(
                        "skills",
                        "",
                    )
                    or ""
                ),
                placeholder=(
                    "Communication, creativity, coding, "
                    "problem solving, leadership..."
                ),
                height=125,
            )


        st.divider()


        # ==================================================
        # CAREER AND ACADEMIC GOALS
        # ==================================================

        st.markdown(
            (
                '<div class="student-profile-section">'
                '<div class="student-profile-section-title">'
                '🎯 Career & Academic Goals'
                '</div>'
                '<div class="student-profile-section-description">'
                'Tell TalentSphere about your future plans.'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )


        career_col1, career_col2 = (
            st.columns(2)
        )


        with career_col1:

            dream_career = st.text_input(
                "Dream Career",
                value=str(
                    profile.get(
                        "dream_career",
                        "",
                    )
                    or ""
                ),
                placeholder=(
                    "Software Engineer, Doctor, Scientist..."
                ),
            )


            target_course = st.text_input(
                "Target Course",
                value=str(
                    profile.get(
                        "target_course",
                        "",
                    )
                    or ""
                ),
                placeholder=(
                    "B.Tech CSE, MBBS, B.Sc, Design..."
                ),
            )


        with career_col2:

            academic_goal = st.text_area(
                "Academic Goal",
                value=str(
                    profile.get(
                        "academic_goal",
                        "",
                    )
                    or ""
                ),
                placeholder=(
                    "Example: Score above 90% in Class 10"
                ),
                height=125,
            )


        # ==================================================
        # ACHIEVEMENTS
        # ==================================================

        achievements = st.text_area(
            "🏆 Achievements & Activities",
            value=str(
                profile.get(
                    "achievements",
                    "",
                )
                or ""
            ),
            placeholder=(
                "Competitions, certificates, sports, projects, "
                "clubs, leadership activities..."
            ),
            height=120,
        )


        # ==================================================
        # SAVE BUTTON
        # ==================================================

        submitted = (
            st.form_submit_button(
                "💾 Save Student Profile",
                use_container_width=True,
            )
        )


    # ======================================================
    # SAVE PROFILE
    # ======================================================

    if submitted:

        # --------------------------------------------------
        # SCHOOL VALIDATION
        # --------------------------------------------------

        if not school_name.strip():

            st.error(
                "Please enter your school name."
            )

            return


        # --------------------------------------------------
        # CLASS VALIDATION
        # --------------------------------------------------

        if not current_class:

            st.error(
                "Please select your current class."
            )

            return


        # --------------------------------------------------
        # BOARD VALIDATION
        # --------------------------------------------------

        if not board:

            st.error(
                "Please select your education board."
            )

            return


        # --------------------------------------------------
        # PHONE VALIDATION
        # --------------------------------------------------

        if phone.strip():

            cleaned_phone = (
                phone
                .replace(" ", "")
                .replace("-", "")
                .replace("+", "")
            )


            if not cleaned_phone.isdigit():

                st.error(
                    "Please enter a valid contact number."
                )

                return


        # --------------------------------------------------
        # SAVE TO DATABASE
        # --------------------------------------------------

        try:

            success, message = (
                save_school_profile(
                    user_id=user_id,
                    school_name=school_name,
                    current_class=current_class,
                    board=board,
                    city=city,
                    parent_name=parent_name,
                    phone=phone,
                    percentage=percentage,
                    favourite_subjects=favourite_subjects,
                    interests=interests,
                    skills=skills,
                    dream_career=dream_career,
                    academic_goal=academic_goal,
                    target_course=target_course,
                    achievements=achievements,
                )
            )


        except Exception as error:

            st.error(
                f"Unable to save profile: {error}"
            )

            return


        # --------------------------------------------------
        # SUCCESS
        # --------------------------------------------------

        if success:

            st.success(
                message
            )

            st.rerun()


        # --------------------------------------------------
        # ERROR
        # --------------------------------------------------

        else:

            st.error(
                message
            )


    # ======================================================
    # PROFILE SNAPSHOT
    # ======================================================

    st.markdown(
        (
            '<div class="student-profile-section">'
            '<div class="student-profile-section-title">'
            '📋 Your Profile Snapshot'
            '</div>'
            '<div class="student-profile-section-description">'
            'A quick summary of your current learning profile.'
            '</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


    snapshot_html = (
        '<div class="profile-summary-grid">'

        '<div class="profile-summary-card">'
        '<div class="profile-summary-icon">📚</div>'
        '<div class="profile-summary-title">'
        'Favourite Subjects'
        '</div>'
        '<div class="profile-summary-value">'
        f'{profile.get("favourite_subjects") or "Not added yet"}'
        '</div>'
        '</div>'

        '<div class="profile-summary-card">'
        '<div class="profile-summary-icon">💡</div>'
        '<div class="profile-summary-title">'
        'Interests'
        '</div>'
        '<div class="profile-summary-value">'
        f'{profile.get("interests") or "Not added yet"}'
        '</div>'
        '</div>'

        '<div class="profile-summary-card">'
        '<div class="profile-summary-icon">🚀</div>'
        '<div class="profile-summary-title">'
        'Career Direction'
        '</div>'
        '<div class="profile-summary-value">'
        f'{profile.get("dream_career") or "Explore careers"}'
        '</div>'
        '</div>'

        '</div>'
    )


    st.markdown(
        snapshot_html,
        unsafe_allow_html=True,
    )