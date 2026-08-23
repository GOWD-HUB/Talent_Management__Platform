import streamlit as st


# ==========================================================
# PUBLIC PAGE CHANGE
# ==========================================================

def change_public_page(page_name):
    st.session_state.public_navigation = page_name


# ==========================================================
# NAVBAR
# ==========================================================

def render_navbar():

    # ======================================================
    # LOGGED-IN NAVBAR
    # ======================================================

    if st.session_state.get("logged_in", False):

        name = st.session_state.get("user_name") or "User"
        role = st.session_state.get("user_role") or ""

        initial = (
            name[0].upper()
            if name
            else "U"
        )

        navbar_html = (
            '<div class="top-navbar">'
            '<div class="top-brand">'
            '<div class="top-logo">T</div>'
            '<div>'
            '<div class="top-brand-name">TalentSphere Elevate</div>'
            '<div class="top-brand-sub">AI CAREER DEVELOPMENT PLATFORM</div>'
            '</div>'
            '</div>'
            '<div class="top-user-area">'
            '<div class="top-user-info">'
            f'<div class="top-user-name">{name}</div>'
            f'<div class="top-user-role">{role}</div>'
            '</div>'
            f'<div class="top-user-avatar">{initial}</div>'
            '</div>'
            '</div>'
        )

        st.markdown(
            navbar_html,
            unsafe_allow_html=True
        )

        return None


    # ======================================================
    # PUBLIC NAVIGATION STATE
    # ======================================================

    if "public_navigation" not in st.session_state:
        st.session_state.public_navigation = "🏠 Home"


    # ======================================================
    # PUBLIC NAVBAR LAYOUT
    # ======================================================

    brand_col, spacer_col, nav_col = st.columns(
        [2.5, 0.6, 4.2],
        vertical_alignment="center"
    )


    # ======================================================
    # BRAND
    # ======================================================

    with brand_col:

        brand_html = (
            '<div class="top-brand">'
            '<div class="top-logo">T</div>'
            '<div>'
            '<div class="top-brand-name">TalentSphere Elevate</div>'
            '<div class="top-brand-sub">AI CAREER DEVELOPMENT PLATFORM</div>'
            '</div>'
            '</div>'
        )

        st.markdown(
            brand_html,
            unsafe_allow_html=True
        )


    # ======================================================
    # NAVIGATION BUTTONS
    # ======================================================

    with nav_col:

        home_col, login_col, register_col, about_col = st.columns(4)


        # --------------------------------------------------
        # HOME
        # --------------------------------------------------

        with home_col:

            if st.button(
                "Home",
                key="navbar_home",
                use_container_width=True
            ):

                change_public_page(
                    "🏠 Home"
                )

                st.rerun()


        # --------------------------------------------------
        # LOGIN
        # --------------------------------------------------

        with login_col:

            if st.button(
                "Login",
                key="navbar_login",
                use_container_width=True
            ):

                change_public_page(
                    "🔐 Login"
                )

                st.rerun()


        # --------------------------------------------------
        # REGISTER
        # --------------------------------------------------

        with register_col:

            if st.button(
                "Register",
                key="navbar_register",
                use_container_width=True
            ):

                change_public_page(
                    "📝 Register"
                )

                st.rerun()


        # --------------------------------------------------
        # ABOUT
        # --------------------------------------------------

        with about_col:

            if st.button(
                "About",
                key="navbar_about",
                use_container_width=True
            ):

                change_public_page(
                    "ℹ About"
                )

                st.rerun()


    st.markdown(
        '<div style="height:14px;"></div>',
        unsafe_allow_html=True
    )

    return st.session_state.public_navigation