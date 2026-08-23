import streamlit as st

from core.constants import (
    SCHOOL_PAGES,
    COLLEGE_PAGES,
    PROFESSIONAL_PAGES,
)


# ==========================================================
# SIDEBAR CSS
# ==========================================================

def apply_sidebar_style():

    st.markdown(
        """
<style>

/* ----------------------------------------------------------
   SIDEBAR
---------------------------------------------------------- */

[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E2E8F0 !important;
}

[data-testid="stSidebarContent"] {
    padding: 18px 14px 24px 14px !important;
}

/* ----------------------------------------------------------
   SIDEBAR BUTTONS
---------------------------------------------------------- */

[data-testid="stSidebar"] .stButton {
    margin-bottom: 7px !important;
}

[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    min-height: 46px !important;

    justify-content: flex-start !important;
    text-align: left !important;

    padding: 10px 14px !important;

    border-radius: 12px !important;
    border: 1px solid #F3C2C9 !important;

    background: #FFF7F8 !important;
    color: #B4233C !important;

    font-size: 13px !important;
    font-weight: 700 !important;

    box-shadow: none !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #FFF0F2 !important;
    border-color: #FDA4AF !important;
    color: #9F1239 !important;
}

/* Logout button stays visually separate */
[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
    transition: all .15s ease !important;
}

/* ----------------------------------------------------------
   TEXT
---------------------------------------------------------- */

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #0F172A !important;
}

[data-testid="stSidebar"] p {
    color: #475569;
}

/* ----------------------------------------------------------
   HIDE STREAMLIT DEFAULT SIDEBAR NAV ARTIFACTS
---------------------------------------------------------- */

[data-testid="stSidebarNav"] {
    display: none !important;
}

</style>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# BRAND
# ==========================================================

def render_brand():

    st.sidebar.markdown("## 🎯 TalentSphere")

    st.sidebar.caption(
        "AI Career Development Platform"
    )

    st.sidebar.divider()


# ==========================================================
# USER CARD
# ==========================================================

def render_user_card():

    name = (
        st.session_state.get("user_name")
        or "User"
    )

    role = (
        st.session_state.get("user_role")
        or "User"
    )

    with st.sidebar.container(
        border=True
    ):

        st.caption(
            "PERSONAL WORKSPACE"
        )

        st.markdown(
            f"### {name}"
        )

        st.caption(
            role
        )


# ==========================================================
# WORKSPACE TITLE
# ==========================================================

def render_workspace_title(
    role
):

    if role == "School Student":

        st.sidebar.markdown(
            "## 🎓 School Workspace"
        )

    elif role == "College Student":

        st.sidebar.markdown(
            "## 🎓 College Workspace"
        )

    elif role == "Professional":

        st.sidebar.markdown(
            "## 💼 Professional Workspace"
        )

    else:

        st.sidebar.markdown(
            "## Workspace"
        )


# ==========================================================
# NAVIGATION HELPER
# ==========================================================

def render_navigation_buttons(
    pages,
    navigation_key,
    default_page,
    key_prefix,
):

    current = st.session_state.get(
        navigation_key,
        default_page,
    )

    if current not in pages:

        current = default_page

        st.session_state[
            navigation_key
        ] = current


    for index, page_name in enumerate(
        pages
    ):

        # Visual active indicator only.
        if page_name == current:

            button_label = (
                f"● {page_name}"
            )

        else:

            button_label = (
                f"  {page_name}"
            )


        if st.sidebar.button(
            button_label,
            key=(
                f"{key_prefix}_"
                f"{index}"
            ),
            use_container_width=True,
        ):

            st.session_state[
                navigation_key
            ] = page_name

            st.rerun()


    return st.session_state.get(
        navigation_key,
        default_page,
    )


# ==========================================================
# LOGOUT
# ==========================================================

def render_logout():

    st.sidebar.divider()

    if st.sidebar.button(
        "🚪 Logout",
        key="global_logout_button",
        use_container_width=True,
    ):

        return "🚪 Logout"

    return None


# ==========================================================
# MAIN SIDEBAR
# ==========================================================

def render_sidebar():

    apply_sidebar_style()


    # ======================================================
    # PUBLIC USER
    # ======================================================

    if not st.session_state.get(
        "logged_in",
        False,
    ):

        return None


    # ======================================================
    # COMMON SIDEBAR
    # ======================================================

    render_brand()

    render_user_card()

    role = st.session_state.get(
        "user_role"
    )

    render_workspace_title(
        role
    )


    selected = None


    # ======================================================
    # SCHOOL STUDENT
    # ======================================================

    if role == "School Student":

        selected = render_navigation_buttons(
            pages=SCHOOL_PAGES,
            navigation_key="school_navigation",
            default_page="🏠 Student Home",
            key_prefix="school_nav",
        )


    # ======================================================
    # COLLEGE STUDENT
    # ======================================================

    elif role == "College Student":

        selected = render_navigation_buttons(
            pages=COLLEGE_PAGES,
            navigation_key="college_navigation",
            default_page="🏠 College Dashboard",
            key_prefix="college_nav",
        )


    # ======================================================
    # PROFESSIONAL
    # ======================================================

    elif role == "Professional":

        selected = render_navigation_buttons(
            pages=PROFESSIONAL_PAGES,
            navigation_key="professional_navigation",
            default_page="🏢 Professional Dashboard",
            key_prefix="professional_nav",
        )


    # ======================================================
    # INVALID ROLE
    # ======================================================

    else:

        st.sidebar.error(
            "Invalid user role."
        )


    # ======================================================
    # LOGOUT
    # ======================================================

    logout_clicked = (
        render_logout()
    )


    if logout_clicked:

        return logout_clicked


    return selected
