import streamlit as st

from styles.school_theme import apply_school_theme
from database.school_repository import get_school_profile


# ==========================================================
# NAVIGATION
# ==========================================================

def open_school_page(page_name):
    """
    Update only the application navigation state.

    IMPORTANT:
    Do not modify st.session_state.school_menu here.
    school_menu belongs to the sidebar radio widget.
    """

    st.session_state.school_navigation = page_name


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
        "favourite_subjects",
        "interests",
        "skills",
        "dream_career",
        "academic_goal",
        "achievements",
    ]

    completed = 0

    for field in fields:

        value = profile.get(field)

        if value and str(value).strip():
            completed += 1

    return int(
        completed / len(fields) * 100
    )


# ==========================================================
# DASHBOARD METRIC CARD
# ==========================================================

def metric_card(
    icon,
    label,
    value,
    description,
):

    return (
        '<div class="dashboard-metric-card">'
        f'<div class="dashboard-metric-icon">{icon}</div>'
        f'<div class="dashboard-metric-label">{label}</div>'
        f'<div class="dashboard-metric-value">{value}</div>'
        f'<div class="dashboard-metric-description">{description}</div>'
        '</div>'
    )


# ==========================================================
# QUICK ACCESS CARD
# ==========================================================

def render_quick_access_card(
    icon,
    title,
    description,
    color_class,
    page_name,
    button_key,
):

    st.markdown(
        (
            f'<div class="quick-card {color_class}">'
            f'<div class="quick-card-icon">{icon}</div>'
            f'<div class="quick-card-title">{title}</div>'
            f'<div class="quick-card-description">{description}</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    if st.button(
        f"Open {title}  →",
        key=button_key,
        use_container_width=True,
    ):

        open_school_page(
            page_name
        )

        st.rerun()


# ==========================================================
# DASHBOARD
# ==========================================================

def render():

    apply_school_theme()

    # ======================================================
    # USER
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

    # ======================================================
    # LOAD PROFILE
    # ======================================================

    profile = {}

    completion = 0

    if user_id:

        try:

            profile = get_school_profile(
                user_id
            )

            completion = (
                calculate_profile_completion(
                    profile
                )
            )

        except Exception:

            profile = {}

            completion = 0

    # ======================================================
    # PROFILE VALUES
    # ======================================================

    current_class = (
        profile.get("current_class")
        or "Not added"
    )

    board = (
        profile.get("board")
        or "Not added"
    )

    city = (
        profile.get("city")
        or "Not added"
    )

    favourite_subjects = (
        profile.get("favourite_subjects")
        or "Not added"
    )

    interests = (
        profile.get("interests")
        or "Not added"
    )

    dream_career = (
        profile.get("dream_career")
        or "Explore careers"
    )

    academic_goal = (
        profile.get("academic_goal")
        or "Set your academic goal"
    )

    # ======================================================
    # HERO
    # ======================================================

    st.markdown(
        (
            '<div class="school-page">'
            '<div class="school-hero">'
            '<div class="school-hero-content">'
            '<div class="school-hero-badge">'
            '🎓 TALENTSPHERE STUDENT PORTAL'
            '</div>'
            f'<h1>Hello, {user_name} 👋<br>'
            'Ready to learn something new today?</h1>'
            '<p>'
            'Your personalised workspace brings together '
            'career discovery, school learning, assessments, '
            'skills, goals and progress in one place.'
            '</p>'
            '</div>'
            '</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    # ======================================================
    # SEARCH
    # ======================================================

    st.markdown(
        (
            '<div class="school-search-wrapper">'
            '<div class="school-search-box">'
            '<div class="school-search-icon">🔍</div>'
            '<div class="school-search-text">'
            'Search careers, subjects, skills, goals '
            'and learning tools...'
            '</div>'
            '</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    # ======================================================
    # QUICK ACCESS HEADER
    # ======================================================

    st.markdown(
        (
            '<div class="school-section-header">'
            '<div>'
            '<div class="school-section-title">'
            '⚡ Quick Access'
            '</div>'
            '<div class="school-section-subtitle">'
            'Open your learning and career tools'
            '</div>'
            '</div>'
            '<div class="school-section-action">'
            'Student Workspace'
            '</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    # ======================================================
    # QUICK ACCESS ROW 1
    # ======================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        render_quick_access_card(
            icon="👤",
            title="My Profile",
            description=(
                "View and update your school, academic "
                "and career information."
            ),
            color_class="quick-purple",
            page_name="👤 School Profile",
            button_key="quick_profile",
        )

    with col2:

        render_quick_access_card(
            icon="🔍",
            title="Career Explorer",
            description=(
                "Explore careers based on your interests, "
                "subjects and strengths."
            ),
            color_class="quick-orange",
            page_name="🔍 Career Explorer",
            button_key="quick_career",
        )

    with col3:

        render_quick_access_card(
            icon="📊",
            title="Interest Assessment",
            description=(
                "Understand your interests and discover "
                "suitable career areas."
            ),
            color_class="quick-blue",
            page_name="📊 Interest Assessment",
            button_key="quick_interest",
        )

    # ======================================================
    # QUICK ACCESS ROW 2
    # ======================================================

    col4, col5, col6 = st.columns(3)

    with col4:

        render_quick_access_card(
            icon="📝",
            title="Subject Quiz",
            description=(
                "Test your knowledge using "
                "subject-wise assessments."
            ),
            color_class="quick-green",
            page_name="📝 Subject Quiz",
            button_key="quick_quiz",
        )

    with col5:

        render_quick_access_card(
            icon="🗺️",
            title="Skills Roadmap",
            description=(
                "Follow a structured roadmap "
                "for future-ready skills."
            ),
            color_class="quick-pink",
            page_name="🛣️ Skills Roadmap",
            button_key="quick_roadmap",
        )

    with col6:

        render_quick_access_card(
            icon="✨",
            title="Recommendations",
            description=(
                "Get personalised next steps from your "
                "profile, interests, goals and quiz activity."
            ),
            color_class="quick-yellow",
            page_name="✨ Recommendations",
            button_key="quick_recommendations",
        )

    # ======================================================
    # QUICK ACCESS ROW 3
    # ======================================================

    col7, col8, col9 = st.columns(3)

    with col7:

        render_quick_access_card(
            icon="📅",
            title="Study Planner",
            description=(
                "Plan daily study activities, "
                "revision and learning tasks."
            ),
            color_class="quick-cyan",
            page_name="📅 Study Planner",
            button_key="quick_planner",
        )

    with col8:

        render_quick_access_card(
            icon="🎯",
            title="Goal Tracker",
            description=(
                "Create academic goals and "
                "monitor your progress."
            ),
            color_class="quick-lavender",
            page_name="🎯 Goal Tracker",
            button_key="quick_goals",
        )

    with col9:

        render_quick_access_card(
            icon="🤖",
            title="AI Study Mentor",
            description=(
                "Ask study questions and receive "
                "personalised guidance."
            ),
            color_class="quick-purple",
            page_name="🤖 AI Study Mentor",
            button_key="quick_mentor",
        )

    # ======================================================
    # QUICK ACCESS ROW 4
    # ======================================================

    col10, col11, col12 = st.columns(3)

    with col10:

        render_quick_access_card(
            icon="🧮",
            title="Aptitude Practice",
            description=(
                "Improve quantitative aptitude, logical "
                "thinking and problem-solving skills."
            ),
            color_class="quick-green",
            page_name="🧮 Aptitude Practice",
            button_key="quick_aptitude",
        )

    with col11:

        render_quick_access_card(
            icon="✨",
            title="Recommendations",
            description=(
                "See personalised guidance based on your "
                "profile and latest learning activity."
            ),
            color_class="quick-orange",
            page_name="✨ Recommendations",
            button_key="quick_recommendations_2",
        )

    with col12:

        render_quick_access_card(
            icon="📄",
            title="School Report",
            description=(
                "Review your profile, assessment, quiz, "
                "goal and study progress in one place."
            ),
            color_class="quick-blue",
            page_name="📄 School Report",
            button_key="quick_report",
        )


    # ======================================================
    # DASHBOARD OVERVIEW
    # ======================================================

    st.markdown(
        (
            '<div class="school-section-header">'
            '<div>'
            '<div class="school-section-title">'
            '📊 Dashboard Overview'
            '</div>'
            '<div class="school-section-subtitle">'
            'Your learning, academic and career progress'
            '</div>'
            '</div>'
            '<div class="school-section-action">'
            'Student Intelligence'
            '</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    metric_cards = [

        metric_card(
            "👤",
            "Profile Strength",
            f"{completion}%",
            "Complete your profile for better recommendations",
        ),

        metric_card(
            "🎓",
            "Current Class",
            current_class,
            "Your present academic level",
        ),

        metric_card(
            "📝",
            "Quiz Performance",
            (
                f'{st.session_state.get("subject_quiz_result", {}).get("percentage", 0)}%'
                if st.session_state.get("subject_quiz_result")
                else "0%"
            ),
            (
                f'Latest: {st.session_state.get("subject_quiz_result", {}).get("subject", "Subject")}'
                if st.session_state.get("subject_quiz_result")
                else "Complete quizzes to build your score"
            ),
        ),

        metric_card(
            "🎯",
            "Career Direction",
            dream_career,
            "Your current career goal",
        ),
    ]

    st.markdown(
        (
            '<div class="dashboard-metric-grid">'
            + "".join(metric_cards)
            + '</div>'
        ),
        unsafe_allow_html=True,
    )

    # ======================================================
    # STUDENT SNAPSHOT
    # ======================================================

    st.markdown(
        (
            '<div class="dashboard-detail-grid">'

            '<div class="dashboard-panel">'
            '<div class="dashboard-panel-heading">'
            '🎓 Student Snapshot'
            '</div>'
            '<div class="dashboard-panel-subtitle">'
            'Information from your saved profile'
            '</div>'

            '<div class="dashboard-info-grid">'

            '<div class="dashboard-info-item">'
            '<span>Class</span>'
            f'<strong>{current_class}</strong>'
            '</div>'

            '<div class="dashboard-info-item">'
            '<span>Board</span>'
            f'<strong>{board}</strong>'
            '</div>'

            '<div class="dashboard-info-item">'
            '<span>City</span>'
            f'<strong>{city}</strong>'
            '</div>'

            '<div class="dashboard-info-item">'
            '<span>Favourite Subjects</span>'
            f'<strong>{favourite_subjects}</strong>'
            '</div>'

            '</div>'
            '</div>'

            '<div class="dashboard-panel">'
            '<div class="dashboard-panel-heading">'
            '🚀 Career Direction'
            '</div>'
            '<div class="dashboard-panel-subtitle">'
            'Your current goals and interests'
            '</div>'

            '<div class="dashboard-goal-box">'
            '<span>Dream Career</span>'
            f'<strong>{dream_career}</strong>'
            '</div>'

            '<div class="dashboard-goal-box">'
            '<span>Academic Goal</span>'
            f'<strong>{academic_goal}</strong>'
            '</div>'

            '<div class="dashboard-goal-box">'
            '<span>Interests</span>'
            f'<strong>{interests}</strong>'
            '</div>'

            '</div>'

            '</div>'
        ),
        unsafe_allow_html=True,
    )

    # ======================================================
    # CONTINUE LEARNING
    # ======================================================

    st.markdown(
        (
            '<div class="school-section-header">'
            '<div>'
            '<div class="school-section-title">'
            '📚 Continue Learning'
            '</div>'
            '<div class="school-section-subtitle">'
            'Recommended learning areas for you'
            '</div>'
            '</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    learn1, learn2 = st.columns(2)

    # ======================================================
    # APTITUDE
    # ======================================================

    with learn1:

        st.markdown(
            (
                '<div class="learning-card">'
                '<div class="learning-icon">🧮</div>'
                '<div>'
                '<div class="learning-title">'
                'Aptitude & Logical Thinking'
                '</div>'
                '<div class="learning-description">'
                'Improve mathematics, logical reasoning '
                'and problem-solving skills.'
                '</div>'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

        if st.button(
            "Start Aptitude Practice →",
            key="dashboard_aptitude",
            use_container_width=True,
        ):

            open_school_page(
                "🧮 Aptitude Practice"
            )

            st.rerun()

    # ======================================================
    # COMMUNICATION
    # ======================================================

    with learn2:

        st.markdown(
            (
                '<div class="learning-card">'
                '<div class="learning-icon">🗣️</div>'
                '<div>'
                '<div class="learning-title">'
                'Communication Skills'
                '</div>'
                '<div class="learning-description">'
                'Improve vocabulary, English, confidence '
                'and presentation ability.'
                '</div>'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

        if st.button(
            "Open School Report →",
            key="dashboard_school_report",
            use_container_width=True,
        ):

            open_school_page(
                "📄 School Report"
            )

            st.rerun()

    # ======================================================
    # DAILY PLAN
    # ======================================================

    st.markdown(
        (
            '<div class="daily-plan">'
            '<div>'
            '<div class="daily-plan-label">'
            'TODAY&apos;S LEARNING PLAN'
            '</div>'
            '<div class="daily-plan-title">'
            'Keep your learning streak moving.'
            '</div>'
            '<div class="daily-plan-text">'
            'Complete one subject topic, one aptitude '
            'activity and review your academic goal.'
            '</div>'
            '</div>'
            '<div class="daily-plan-icon">✅</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )