import streamlit as st


# ==========================================================
# INITIALIZE SESSION
# ==========================================================

def initialize_session():
    """
    Create session variables only when they do not already exist.

    IMPORTANT:
    Never reset logged_in on every Streamlit rerun.
    """

    defaults = {
        "logged_in": False,
        "user_id": None,
        "user_name": None,
        "user_email": None,
        "user_role": None,

        # Public navigation
        "public_navigation": "🏠 Home",

        # School navigation
        "school_navigation": "🏠 Student Home",

        # College navigation
        "college_navigation": "🏠 College Dashboard",

        # Professional navigation
        "professional_navigation": "🏢 Professional Dashboard",
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


# ==========================================================
# SET LOGGED-IN USER
# ==========================================================

def set_logged_in_user(user):
    """
    Save authenticated user data into Streamlit session.
    """

    st.session_state.logged_in = True

    st.session_state.user_id = user.get("id")

    st.session_state.user_name = (
        user.get("name")
        or user.get("full_name")
        or user.get("username")
        or "User"
    )

    st.session_state.user_email = user.get("email")

    st.session_state.user_role = user.get("role")


    # ======================================================
    # ROLE DEFAULT PAGE
    # ======================================================

    role = st.session_state.user_role


    if role == "School Student":

        st.session_state.school_navigation = (
            "🏠 Student Home"
        )


    elif role == "College Student":

        st.session_state.college_navigation = (
            "🏠 College Dashboard"
        )


    elif role == "Professional":

        st.session_state.professional_navigation = (
            "🏢 Professional Dashboard"
        )


# ==========================================================
# LOGOUT
# ==========================================================

def logout_user():
    """
    Clear authentication session safely.
    """

    st.session_state.logged_in = False

    st.session_state.user_id = None
    st.session_state.user_name = None
    st.session_state.user_email = None
    st.session_state.user_role = None

    st.session_state.public_navigation = "🏠 Home"

    st.session_state.school_navigation = (
        "🏠 Student Home"
    )

    st.session_state.college_navigation = (
        "🏠 College Dashboard"
    )

    st.session_state.professional_navigation = (
        "🏢 Professional Dashboard"
    )