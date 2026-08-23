import streamlit as st

from auth.service import login_user

from core.session import (
    set_logged_in_user,
)

from styles.login_theme import (
    apply_login_theme,
)


# ==========================================================
# LOGIN PAGE
# ==========================================================

def render():

    apply_login_theme()


    # ======================================================
    # BACK TO HOME
    # ======================================================

    back_col, empty_col = st.columns(
        [1.1, 8.9]
    )


    with back_col:

        if st.button(
            "‹‹ Home",
            key="login_back_home",
            use_container_width=True,
        ):

            st.session_state.public_navigation = (
                "🏠 Home"
            )

            st.rerun()


    # ======================================================
    # LOGIN CARD
    # ======================================================

    left_col, login_col, right_col = st.columns(
        [
            1.35,
            1.55,
            1.35,
        ]
    )


    with login_col:

        # ==================================================
        # HEADER
        # ==================================================

        header_html = (
            '<div class="auth-card-header">'
            '<div class="auth-logo">🎯</div>'
            '<div class="auth-eyebrow">'
            'TALENTSPHERE ELEVATE'
            '</div>'
            '<div class="auth-title">'
            'Welcome back'
            '</div>'
            '<div class="auth-description">'
            'Sign in to continue to your personalised '
            'learning and career workspace.'
            '</div>'
            '</div>'
        )


        st.markdown(
            header_html,
            unsafe_allow_html=True,
        )


        # ==================================================
        # FORM
        # ==================================================

        with st.form(
            "talentsphere_login_form",
            clear_on_submit=False,
        ):

            email = st.text_input(
                "Email address",
                placeholder="name@example.com",
            )


            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
            )


            sign_in = (
                st.form_submit_button(
                    "Sign in to TalentSphere",
                    use_container_width=True,
                )
            )


        # ==================================================
        # SIGN IN
        # ==================================================

        if sign_in:

            email = email.strip()


            # ------------------------------------------------
            # VALIDATION
            # ------------------------------------------------

            if not email:

                st.error(
                    "Please enter your email address."
                )

                return


            if not password:

                st.error(
                    "Please enter your password."
                )

                return


            # ------------------------------------------------
            # AUTHENTICATION
            # ------------------------------------------------

            try:

                user = login_user(
                    email=email,
                    password=password,
                )

            except Exception as error:

                st.error(
                    f"Unable to sign in: {error}"
                )

                return


            # ------------------------------------------------
            # INVALID LOGIN
            # ------------------------------------------------

            if user is None:

                st.error(
                    "Incorrect email or password."
                )

                return


            # ------------------------------------------------
            # LOGIN SUCCESS
            # ------------------------------------------------

            set_logged_in_user(
                user
            )


            st.success(
                "Login successful."
            )


            st.rerun()


        # ==================================================
        # SECURITY NOTE
        # ==================================================

        footer_html = (
            '<div class="auth-card-footer">'
            '<div class="auth-security">'
            '🔒 Secure account access'
            '</div>'
            '</div>'
        )


        st.markdown(
            footer_html,
            unsafe_allow_html=True,
        )