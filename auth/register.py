import streamlit as st

from auth.service import register_user

from core.constants import USER_ROLES


def render():

    st.markdown(
        """
        <div class="page-title">
            <h1>Create Your Account 🚀</h1>
            <p>
                Select your career stage and start using TalentSphere.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


    with st.form(
        "registration_form"
    ):

        fullname = st.text_input(
            "Full Name",
            placeholder="Enter your full name"
        )


        email = st.text_input(
            "Email Address",
            placeholder="Enter your email"
        )


        password = st.text_input(
            "Password",
            type="password",
            placeholder="Minimum 6 characters"
        )


        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )


        role = st.selectbox(
            "Select User Type",
            USER_ROLES
        )


        submit = st.form_submit_button(
            "Create Account",
            use_container_width=True
        )


    if submit:

        if not fullname.strip():

            st.error(
                "Please enter your full name."
            )

            return


        if not email.strip():

            st.error(
                "Please enter your email."
            )

            return


        if "@" not in email:

            st.error(
                "Enter a valid email address."
            )

            return


        if len(password) < 6:

            st.error(
                "Password must contain at least 6 characters."
            )

            return


        if password != confirm_password:

            st.error(
                "Passwords do not match."
            )

            return


        success, message = register_user(
            fullname,
            email,
            password,
            role
        )


        if success:

            st.success(
                "✅ Account created successfully."
            )

            st.info(
                "Open Login and use your email and password."
            )


        else:

            st.error(message)