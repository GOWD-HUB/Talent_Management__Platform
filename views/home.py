import streamlit as st


def show_home():

    # Hero Section
    st.markdown(
        """
        <div style="
            background: linear-gradient(90deg,#667eea,#764ba2);
            padding:40px;
            border-radius:15px;
            text-align:center;
            color:white;
        ">
            <h1>🎯 TalentSphere Elevate</h1>
            <h3>AI Powered Career Growth Platform</h3>
            <p>
                Discover your skills, improve your career path,
                and connect with opportunities using Artificial Intelligence.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


    st.write("")


    # Features
    st.subheader("🚀 Platform Features")


    col1, col2, col3 = st.columns(3)


    with col1:
        st.info(
            """
            ### 🧠 AI Recommendations

            Get personalized:
            - Career suggestions
            - Learning paths
            - Skill improvements
            """
        )


    with col2:
        st.success(
            """
            ### 📊 Skill Assessment

            Evaluate your:
            - Technical skills
            - Soft skills
            - Career readiness
            """
        )


    with col3:
        st.warning(
            """
            ### 📈 Career Reports

            Analyze:
            - Performance
            - Progress
            - Future goals
            """
        )


    st.divider()


    # How it works

    st.subheader("⚡ How TalentSphere Works")


    steps = [
        "1️⃣ Create your profile",
        "2️⃣ Complete skill assessment",
        "3️⃣ Get AI-based recommendations",
        "4️⃣ Improve skills and track growth"
    ]


    for step in steps:
        st.write(step)


    st.divider()


    # User Roles

    st.subheader("👥 Our Users")


    col1, col2, col3, col4 = st.columns(4)


    with col1:
        st.write("🎓 Students")
        st.caption(
            "Build skills and find career opportunities"
        )


    with col2:
        st.write("💼 Professionals")
        st.caption(
            "Improve career growth and skills"
        )


    with col3:
        st.write("🏫 Colleges")
        st.caption(
            "Monitor student development"
        )


    with col4:
        st.write("👨‍💼 Admin")
        st.caption(
            "Manage platform activities"
        )


    st.divider()


    st.markdown(
        """
        <center>
        <h3>Start your career journey with TalentSphere Elevate 🚀</h3>
        </center>
        """,
        unsafe_allow_html=True
    )