import streamlit as st


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

from styles.theme import (
    configure_page,
    apply_theme,
)

configure_page()


# ==========================================================
# DATABASE
# ==========================================================

from database.tables import create_tables


# ==========================================================
# SESSION
# ==========================================================

from core.session import (
    initialize_session,
    logout_user,
)


# ==========================================================
# COMPONENTS
# ==========================================================

from components.navbar import render_navbar
from components.sidebar import render_sidebar
from components.footer import render_footer


# ==========================================================
# PUBLIC PAGES
# ==========================================================

from pages.public.home import render as home_page
from pages.public.about import render as about_page


# ==========================================================
# AUTH PAGES
# ==========================================================

from auth.login import render as login_page
from auth.register import render as register_page


# ==========================================================
# SCHOOL PAGES
# ==========================================================

from pages.school.dashboard import (
    render as school_dashboard_page,
)

from pages.school.profile import (
    render as school_profile_page,
)

from pages.school.career_explorer import (
    render as career_explorer_page,
)

from pages.school.interest_assessment import (
    render as interest_assessment_page,
)

from pages.school.skills_roadmap import (
    render as skills_roadmap_page,
)

from pages.school.subject_quiz import (
    render as subject_quiz_page,
)

from pages.school.recommendations import (
    render as recommendations_page,
)

from pages.school.study_planner import (
    render as study_planner_page,
)

from pages.school.goal_tracker import (
    render as goal_tracker_page,
)

from pages.school.ai_study_mentor import (
    render as ai_study_mentor_page,
)

from pages.school.aptitude_practice import (
    render as aptitude_practice_page,
)

from pages.school.school_report import (
    render as school_report_page,
)


from pages.college.dashboard import render as college_dashboard_page
from pages.college.profile import render as college_profile_page
from pages.college.ats_checker import render as college_ats_page
from pages.college.coding_practice import render as college_coding_page
from pages.college.college_report import render as college_report_page
from pages.college.daily_challenge import render as college_daily_page
from pages.college.github_review import render as college_github_page
from pages.college.hackathons import render as college_hackathons_page
from pages.college.internships import render as college_internships_page
from pages.college.interview_prep import render as college_interview_prep_page
from pages.college.job_matching import render as college_job_page
from pages.college.linkedin_review import render as college_linkedin_page
from pages.college.mock_interview import render as college_mock_page
from pages.college.placement_tracker import render as college_tracker_page
from pages.college.resume_builder import render as college_resume_page
from pages.college.skill_gap import render as college_skill_gap_page

# ==========================================================
# PROFESSIONAL PAGES
# ==========================================================

from pages.professional.dashboard import render as professional_dashboard_page
from pages.professional.profile import render as professional_profile_page
from pages.professional.promotion_readiness import render as professional_promotion_page
from pages.professional.career_transition import render as professional_transition_page
from pages.professional.job_matching import render as professional_job_matching_page
from pages.professional.learning_academy import render as professional_learning_page
from pages.professional.salary_insights import render as professional_salary_page
from pages.professional.industry_trends import render as professional_trends_page
from pages.professional.certifications import render as professional_certifications_page
from pages.professional.leadership_evaluation import render as professional_leadership_page
from pages.professional.growth_report import render as professional_growth_report_page

# ==========================================================
# INITIALIZE APPLICATION
# ==========================================================

create_tables()

initialize_session()

apply_theme()


# ==========================================================
# GLOBAL WORKSPACE VISIBILITY FIX
# Keeps sidebar visible and fixes unreadable white text
# ==========================================================

st.markdown(
    """
    <style>

    /* ---------------- SIDEBAR ---------------- */

    section[data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        transform: translateX(0) !important;
        min-width: 300px !important;
        width: 300px !important;
        background: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }

    section[data-testid="stSidebar"] > div {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }

    [data-testid="stSidebarContent"] {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        background: #ffffff !important;
    }

    /* Sidebar text */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div {
        color: #0f172a;
    }

    /* ---------------- MAIN TEXT ---------------- */

    [data-testid="stAppViewContainer"] {
        background: #f8fbff !important;
    }

    [data-testid="stMainBlockContainer"] {
        color: #0f172a !important;
    }

    [data-testid="stMainBlockContainer"] p,
    [data-testid="stMainBlockContainer"] span,
    [data-testid="stMainBlockContainer"] label,
    [data-testid="stMainBlockContainer"] li,
    [data-testid="stMainBlockContainer"] h1,
    [data-testid="stMainBlockContainer"] h2,
    [data-testid="stMainBlockContainer"] h3,
    [data-testid="stMainBlockContainer"] h4 {
        color: #0f172a;
    }

    /* ---------------- CHAT ---------------- */

    [data-testid="stChatMessage"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 16px !important;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] div {
        color: #0f172a !important;
    }

    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInput"] input {
        color: #0f172a !important;
        background: #ffffff !important;
        -webkit-text-fill-color: #0f172a !important;
    }

    [data-testid="stChatInput"] textarea::placeholder,
    [data-testid="stChatInput"] input::placeholder {
        color: #64748b !important;
        opacity: 1 !important;
    }

    /* Make markdown lists readable */
    .stMarkdown,
    .stMarkdown p,
    .stMarkdown li {
        color: #0f172a !important;
    }

    /* Hide only Streamlit's default page navigation, not our custom sidebar */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# PUBLIC NAVIGATION DEFAULT
# ==========================================================

if "public_navigation" not in st.session_state:

    st.session_state.public_navigation = (
        "🏠 Home"
    )


# ==========================================================
# LOGIN STATE
# ==========================================================

logged_in = st.session_state.get(
    "logged_in",
    False,
)


# ==========================================================
# DETERMINE CURRENT MENU
# ==========================================================

if logged_in:

    # Logged-in navbar
    render_navbar()

    # Sidebar controls workspace navigation
    menu = render_sidebar()


else:

    current_page = (
        st.session_state.public_navigation
    )

    # ======================================================
    # SHOW PUBLIC NAVBAR ONLY ON HOME / ABOUT
    # ======================================================

    if current_page in [
        "🏠 Home",
        "ℹ About",
    ]:

        menu = render_navbar()

    else:

        # Login/Register use their own Back to Home button
        menu = current_page


# ==========================================================
# PUBLIC ROUTES
# ==========================================================

if not logged_in:

    # ======================================================
    # HOME
    # ======================================================

    if menu == "🏠 Home":

        home_page()


    # ======================================================
    # LOGIN
    # ======================================================

    elif menu == "🔐 Login":

        login_page()


    # ======================================================
    # REGISTER
    # ======================================================

    elif menu == "📝 Register":

        register_page()


    # ======================================================
    # ABOUT
    # ======================================================

    elif menu == "ℹ About":

        about_page()


    # ======================================================
    # FALLBACK
    # ======================================================

    else:

        st.session_state.public_navigation = (
            "🏠 Home"
        )

        home_page()


# ==========================================================
# LOGGED-IN ROUTES
# ==========================================================

else:

    # ======================================================
    # LOGOUT
    # ======================================================

    if menu == "🚪 Logout":

        logout_user()

        st.session_state.public_navigation = (
            "🏠 Home"
        )

        st.rerun()


    # ======================================================
    # SCHOOL STUDENT DASHBOARD
    # ======================================================

    elif menu == "🏠 Student Home":

        school_dashboard_page()


    # ======================================================
    # SCHOOL PROFILE
    # ======================================================

    elif menu == "👤 School Profile":

        school_profile_page()


    # ======================================================
    # CAREER EXPLORER
    # ======================================================

    elif menu == "🔍 Career Explorer":

        career_explorer_page()


    # ======================================================
    # INTEREST ASSESSMENT
    # ======================================================

    elif menu == "📊 Interest Assessment":

        interest_assessment_page()


    # ======================================================
    # SKILLS ROADMAP
    # ======================================================

    elif menu == "🛣️ Skills Roadmap":

        skills_roadmap_page()


    # ======================================================
    # SUBJECT QUIZ
    # ======================================================

    elif menu == "📝 Subject Quiz":

        subject_quiz_page()


    # ======================================================
    # RECOMMENDATIONS
    # ======================================================

    elif menu == "✨ Recommendations":

        recommendations_page()


    # ======================================================
    # STUDY PLANNER
    # ======================================================

    elif menu == "📅 Study Planner":

        study_planner_page()


    # ======================================================
    # APTITUDE PRACTICE
    # ======================================================

    elif menu == "🧮 Aptitude Practice":

        aptitude_practice_page()


    # ======================================================
    # GOAL TRACKER
    # ======================================================

    elif menu == "🎯 Goal Tracker":

        goal_tracker_page()


    # ======================================================
    # AI STUDY MENTOR
    # ======================================================

    elif menu == "🤖 AI Study Mentor":

        ai_study_mentor_page()


    # ======================================================
    # SCHOOL REPORT
    # ======================================================

    elif menu == "📄 School Report":

        school_report_page()


    # ======================================================
    # COLLEGE STUDENT
    # ======================================================

    elif st.session_state.get("user_role") == "College Student":

        routes = {
            "🏠 College Dashboard": college_dashboard_page,
            "👤 College Profile": college_profile_page,
            "📄 Resume Builder": college_resume_page,
            "🎯 ATS Checker": college_ats_page,
            "💻 Coding Practice": college_coding_page,
            "🔥 Daily Challenge": college_daily_page,
            "🎤 Interview Prep": college_interview_prep_page,
            "🗣️ Mock Interview": college_mock_page,
            "🧩 Skill Gap": college_skill_gap_page,
            "💼 Job Matching": college_job_page,
            "📌 Placement Tracker": college_tracker_page,
            "🐙 GitHub Review": college_github_page,
            "🔗 LinkedIn Review": college_linkedin_page,
            "🏆 Hackathons": college_hackathons_page,
            "💼 Internships": college_internships_page,
            "📊 College Report": college_report_page,
        }

        page = routes.get(menu)

        if page:
            page()
        else:
            st.error(f"College page not found: {menu}")


    # ======================================================
    # PROFESSIONAL
    # ======================================================

    elif (
        st.session_state.get(
            "user_role"
        )
        == "Professional"
    ):

        professional_routes = {
            "🏠 Professional Dashboard": professional_dashboard_page,
            "👤 Professional Profile": professional_profile_page,
            "📈 Promotion Readiness": professional_promotion_page,
            "🔄 Career Transition": professional_transition_page,
            "💼 Advanced Job Matching": professional_job_matching_page,
            "🎓 Learning Academy": professional_learning_page,
            "💰 Career & Salary Insights": professional_salary_page,
            "📡 Industry Trends": professional_trends_page,
            "🏅 Certifications": professional_certifications_page,
            "🧭 Leadership Evaluation": professional_leadership_page,
            "📄 AI Growth Report": professional_growth_report_page,
        }

        page = professional_routes.get(menu)

        if page:
            page()
        else:
            st.error(
                f"Professional page not found: {menu}"
            )


    # ======================================================
    # UNKNOWN PAGE
    # ======================================================

    else:

        st.error(
            f"Page not found: {menu}"
        )


# ==========================================================
# FOOTER
# ==========================================================

render_footer()