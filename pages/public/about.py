import streamlit as st

from components.common import page_header


def render():

    page_header(

        "ℹ About TalentSphere Elevate",

        "One platform for learning, placements and professional career growth."

    )


    st.markdown(
        """
        ### 🎯 Vision

        TalentSphere Elevate provides personalised
        career-development tools for users at
        different stages of their journey.


        ### 🎓 School Student

        - Career Explorer
        - Interest Assessment
        - Skills Roadmap
        - Subject Quiz
        - Daily Study Planner
        - Aptitude Practice
        - Communication Skills
        - Goal Tracker
        - AI Study Mentor


        ### 💻 College Student

        - Coding Practice
        - Daily Coding Challenge
        - Interview Preparation
        - Mock Interviews
        - Skill Gap Analysis
        - Resume Builder
        - ATS Resume Checker
        - LinkedIn Review
        - Internship Recommendations
        - Job Matching
        - Placement Tracker
        - GitHub Review


        ### 💼 Professional

        - Learning & Skills
        - Career Transition
        - Promotion Readiness
        - Career & Salary Insights
        - Industry Trends
        - Certification Suggestions
        - Leadership Evaluation
        - Advanced Job Matching
        - AI Growth Report


        ### 🛠 Technology Stack

        - Python
        - Streamlit
        - SQLite
        - Pandas
        - Plotly
        - HTML & CSS
        """
    )