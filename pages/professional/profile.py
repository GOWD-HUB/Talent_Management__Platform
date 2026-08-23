import streamlit as st

from database.professional_repository import (
    get_professional_profile,
    save_professional_profile,
)
from services.professional.profile_service import (
    profile_completion,
    split_items,
    safe_float,
)
from styles.professional.theme import (
    apply_professional_theme,
    hero,
    section,
    metrics,
)


def render():
    apply_professional_theme()

    uid = st.session_state.get("user_id")

    if not uid:
        st.error("User session not found. Please login again.")
        return

    profile = get_professional_profile(uid) or {}

    name = (
        st.session_state.get("user_name")
        or profile.get("full_name")
        or "Professional"
    )

    completion = profile_completion(profile)

    hero(
        f"{name}'s Professional Profile",
        "Build a complete professional profile covering your role, experience, "
        "technology stack, leadership exposure, career goals, salary goals and professional presence.",
        "👔 PROFESSIONAL PROFILE",
    )

    metrics(
        [
            ("👤", "PROFILE COMPLETION", f"{completion}%", "Complete details to improve recommendations."),
            ("💼", "CURRENT ROLE", profile.get("current_role") or "Not added", "Your present professional position."),
            ("🎯", "TARGET ROLE", profile.get("target_role") or "Not added", "Your next career destination."),
            ("📈", "EXPERIENCE", f"{safe_float(profile.get('experience_years')):.1f} yrs", "Total professional experience."),
        ]
    )

    st.progress(completion / 100)

    section(
        "🏢 Professional Information",
        "Tell TalentSphere where you are today.",
        "Current Position",
    )

    with st.form("professional_profile_form"):

        c1, c2 = st.columns(2)

        with c1:
            full_name = st.text_input(
                "Full Name",
                value=str(profile.get("full_name") or name),
            )

            current_role = st.text_input(
                "Current Role",
                value=str(profile.get("current_role") or ""),
                placeholder="Software Engineer",
            )

            company = st.text_input(
                "Company / Organization",
                value=str(profile.get("company") or ""),
                placeholder="Current company",
            )

            industry = st.selectbox(
                "Industry",
                [
                    "Not selected",
                    "Information Technology",
                    "Software / SaaS",
                    "AI / Data",
                    "FinTech",
                    "Healthcare",
                    "E-commerce",
                    "Consulting",
                    "Manufacturing",
                    "Telecommunications",
                    "Education",
                    "Other",
                ],
                index=0,
            )

            if profile.get("industry") in [
                "Information Technology", "Software / SaaS", "AI / Data",
                "FinTech", "Healthcare", "E-commerce", "Consulting",
                "Manufacturing", "Telecommunications", "Education", "Other"
            ]:
                industry = profile.get("industry")

            experience_years = st.number_input(
                "Total Experience (Years)",
                min_value=0.0,
                max_value=50.0,
                value=float(safe_float(profile.get("experience_years"))),
                step=0.5,
            )

            highest_education = st.text_input(
                "Highest Education",
                value=str(profile.get("highest_education") or ""),
                placeholder="B.Tech / M.Tech / MBA / M.S.",
            )

        with c2:
            target_role = st.text_input(
                "Target Role",
                value=str(profile.get("target_role") or ""),
                placeholder="Senior Software Engineer",
            )

            target_industry = st.text_input(
                "Target Industry",
                value=str(profile.get("target_industry") or ""),
                placeholder="AI / SaaS / FinTech",
            )

            current_salary = st.number_input(
                "Current Salary (LPA)",
                min_value=0.0,
                max_value=500.0,
                value=float(safe_float(profile.get("current_salary_lpa"))),
                step=0.5,
            )

            target_salary = st.number_input(
                "Target Salary (LPA)",
                min_value=0.0,
                max_value=500.0,
                value=float(safe_float(profile.get("target_salary_lpa"))),
                step=0.5,
            )

            learning_hours = st.number_input(
                "Learning Hours per Week",
                min_value=1.0,
                max_value=40.0,
                value=max(
                    1.0,
                    float(safe_float(profile.get("preferred_learning_hours"), 5))
                ),
                step=1.0,
            )

        section(
            "🧠 Skills & Capability",
            "Capture your technology stack and current professional capability.",
        )

        tech_stack = st.text_area(
            "Technology Stack / Skills",
            value=str(profile.get("tech_stack") or ""),
            placeholder="Python, FastAPI, React, Node.js, SQL, AWS, Docker...",
            height=120,
        )

        c3, c4, c5 = st.columns(3)

        technical_options = ["Beginner", "Intermediate", "Advanced", "Expert"]
        leadership_options = ["None", "Limited", "Moderate", "High"]
        communication_options = ["Needs Improvement", "Average", "Good", "Excellent"]

        with c3:
            current_technical = str(profile.get("technical_level") or "Intermediate")
            technical_level = st.selectbox(
                "Technical Level",
                technical_options,
                index=technical_options.index(current_technical)
                if current_technical in technical_options else 1,
            )

        with c4:
            current_leadership = str(profile.get("leadership_exposure") or "Limited")
            leadership_exposure = st.selectbox(
                "Leadership Exposure",
                leadership_options,
                index=leadership_options.index(current_leadership)
                if current_leadership in leadership_options else 1,
            )

        with c5:
            current_comm = str(profile.get("communication_level") or "Good")
            communication_level = st.selectbox(
                "Communication Level",
                communication_options,
                index=communication_options.index(current_comm)
                if current_comm in communication_options else 2,
            )

        section(
            "🚀 Career Direction",
            "Define what growth, promotion or transition means for you.",
        )

        career_goal = st.text_area(
            "Career Goal",
            value=str(profile.get("career_goal") or ""),
            placeholder="Example: Move into a senior engineering role and own backend architecture.",
            height=100,
        )

        c6, c7 = st.columns(2)

        with c6:
            promotion_goal = st.text_area(
                "Promotion Goal",
                value=str(profile.get("promotion_goal") or ""),
                placeholder="Example: Become Senior Software Engineer within 12 months.",
                height=100,
            )

        with c7:
            transition_goal = st.text_area(
                "Career Transition Goal",
                value=str(profile.get("transition_goal") or ""),
                placeholder="Example: Transition from backend development to AI engineering.",
                height=100,
            )

        section(
            "🏆 Professional Evidence",
            "Add evidence that supports your growth and promotion readiness.",
        )

        certifications = st.text_area(
            "Certifications",
            value=str(profile.get("certifications") or ""),
            placeholder="AWS, Azure, Google Cloud, Infosys, NPTEL...",
            height=100,
        )

        achievements = st.text_area(
            "Achievements / Impact",
            value=str(profile.get("achievements") or ""),
            placeholder="Reduced response time by 30%, mentored 3 interns, led migration...",
            height=110,
        )

        projects = st.text_area(
            "Important Projects",
            value=str(profile.get("projects") or ""),
            placeholder="Describe major production or portfolio projects.",
            height=110,
        )

        responsibilities = st.text_area(
            "Current Responsibilities",
            value=str(profile.get("responsibilities") or ""),
            placeholder="Architecture, APIs, code reviews, mentoring, deployment...",
            height=110,
        )

        section(
            "🔗 Professional Presence",
            "Add recruiter-facing links and portfolio evidence.",
        )

        l1, l2 = st.columns(2)

        with l1:
            linkedin_url = st.text_input(
                "LinkedIn URL",
                value=str(profile.get("linkedin_url") or ""),
                placeholder="https://linkedin.com/in/username",
            )

            github_url = st.text_input(
                "GitHub URL",
                value=str(profile.get("github_url") or ""),
                placeholder="https://github.com/username",
            )

        with l2:
            portfolio_url = st.text_input(
                "Portfolio URL",
                value=str(profile.get("portfolio_url") or ""),
                placeholder="https://yourportfolio.com",
            )

        submitted = st.form_submit_button(
            "💾 Save Professional Profile",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        data = {
            "full_name": full_name,
            "current_role": current_role,
            "company": company,
            "industry": industry if industry != "Not selected" else "",
            "experience_years": experience_years,
            "highest_education": highest_education,
            "tech_stack": tech_stack,
            "technical_level": technical_level,
            "leadership_exposure": leadership_exposure,
            "communication_level": communication_level,
            "current_salary_lpa": current_salary,
            "target_salary_lpa": target_salary,
            "target_role": target_role,
            "target_industry": target_industry,
            "career_goal": career_goal,
            "promotion_goal": promotion_goal,
            "transition_goal": transition_goal,
            "certifications": certifications,
            "achievements": achievements,
            "projects": projects,
            "responsibilities": responsibilities,
            "linkedin_url": linkedin_url,
            "github_url": github_url,
            "portfolio_url": portfolio_url,
            "preferred_learning_hours": learning_hours,
        }

        try:
            save_professional_profile(uid, data)
            st.success("Professional profile saved successfully.")
            st.rerun()
        except Exception as error:
            st.error(f"Unable to save professional profile: {error}")
