import streamlit as st

from auth.service import register_user


def render():

    st.title(
        "📝 Create Account"
    )


    with st.form(
        "register_form"
    ):


        fullname = st.text_input(
            "Full Name"
        )


        email = st.text_input(
            "Email"
        )


        password = st.text_input(
            "Password",
            type="password"
        )


        confirm_password = (
            st.text_input(
                "Confirm Password",
                type="password"
            )
        )


        role = st.selectbox(

            "Select User Type",

            [

                "School Student",

                "College Student",

                "Professional"

            ]

        )


        submit = (
            st.form_submit_button(
                "Create Account",
                use_container_width=True
            )
        )


    if submit:


        if not fullname.strip():

            st.error(
                "Enter your name."
            )

            return


        if not email.strip():

            st.error(
                "Enter your email."
            )

            return


        if len(password) < 6:

            st.error(
                "Password requires minimum 6 characters."
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
                "Now open Login."
            )


        else:

            st.error(
                message
            )