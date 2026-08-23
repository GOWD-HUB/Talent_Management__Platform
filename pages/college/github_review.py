import streamlit as st

from database.college_repository import get_college_profile
from services.college.review_service import review_github_profile
from styles.college.theme import apply_college_theme


# ==========================================================
# HELPERS
# ==========================================================

def get_score_label(score):
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Strong"
    elif score >= 55:
        return "Good"
    elif score >= 40:
        return "Developing"
    return "Needs Improvement"


def render():
    apply_college_theme()

    # ======================================================
    # USER
    # ======================================================

    uid = st.session_state.get("user_id")

    if not uid:
        st.error("User session not found. Please login again.")
        return

    try:
        profile = get_college_profile(uid) or {}
    except Exception:
        profile = {}

    # Existing GitHub URL from College Profile
    saved_github = str(
        profile.get("github_url")
        or profile.get("github")
        or ""
    ).strip()

    # ======================================================
    # HERO
    # ======================================================

    st.html(
        """
        <div class="college-hero">
            <div class="college-eyebrow">
                GITHUB PORTFOLIO ANALYSIS
            </div>

            <div class="college-title">
                🐙 GitHub Review
            </div>

            <div class="college-desc">
                Analyze your real GitHub profile, repositories,
                programming languages, documentation and overall
                placement portfolio readiness.
            </div>
        </div>
        """
    )

    # ======================================================
    # INPUT SECTION
    # ======================================================

    st.markdown("## 🔗 GitHub Profile Analyzer")

    st.caption(
        "Paste your GitHub profile link below. "
        "TalentSphere will analyze your public GitHub portfolio."
    )

    github_url = st.text_input(
        "GitHub Profile URL",
        value=saved_github,
        placeholder="https://github.com/username",
        key="college_github_review_url",
    )

    analyze = st.button(
        "🐙 Analyze GitHub Profile",
        type="primary",
        use_container_width=True,
        key="analyze_github_button",
    )

    # ======================================================
    # ANALYZE
    # ======================================================

    if analyze:

        if not github_url.strip():
            st.warning("Please enter your GitHub profile URL.")
            return

        with st.spinner(
            "Analyzing GitHub profile and repositories..."
        ):
            result = review_github_profile(
                github_url.strip()
            )

        if not result.get("success"):
            st.error(
                result.get(
                    "error",
                    "Unable to analyze GitHub profile."
                )
            )
            return

        st.session_state["github_analysis"] = result

    # ======================================================
    # LOAD RESULT
    # ======================================================

    result = st.session_state.get("github_analysis")

    if not result:
        st.info(
            "Enter a GitHub profile URL and click "
            "**Analyze GitHub Profile** to start the review."
        )
        return

    scores = result.get("scores", {})
    github_profile = result.get("profile", {})
    repositories = result.get("repository_details", [])
    languages = result.get("languages", {})
    quality = result.get("quality", {})
    strengths = result.get("strengths", [])
    improvements = result.get("improvements", [])

    overall = int(scores.get("overall", 0))

    # ======================================================
    # PROFILE INFORMATION
    # ======================================================

    st.markdown("---")
    st.markdown("## 👤 GitHub Profile")

    col1, col2 = st.columns([1, 4])

    with col1:
        avatar = github_profile.get("avatar_url")

        if avatar:
            st.image(
                avatar,
                width=120
            )

    with col2:

        display_name = (
            github_profile.get("name")
            or result.get("username")
            or "GitHub User"
        )

        st.markdown(
            f"### {display_name}"
        )

        st.caption(
            f'@{result.get("username", "")}'
        )

        bio = github_profile.get("bio")

        if bio:
            st.write(bio)
        else:
            st.write(
                "No GitHub bio added."
            )

        github_link = github_profile.get(
            "html_url"
        )

        if github_link:
            st.link_button(
                "↗ Open GitHub Profile",
                github_link
            )

    # ======================================================
    # MAIN SCORE
    # ======================================================

    st.markdown("---")
    st.markdown("## 📊 GitHub Portfolio Score")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "Portfolio Score",
            f"{overall}%"
        )

    with m2:
        st.metric(
            "Repositories",
            len(repositories)
        )

    with m3:
        st.metric(
            "Technologies",
            len(languages)
        )

    with m4:
        st.metric(
            "Total Stars",
            quality.get(
                "star_count",
                0
            )
        )

    st.progress(
        max(
            0.0,
            min(
                1.0,
                overall / 100
            )
        )
    )

    st.info(
        f"Overall portfolio rating: "
        f"**{get_score_label(overall)}**"
    )

    # ======================================================
    # SCORE BREAKDOWN
    # ======================================================

    st.markdown("---")
    st.markdown("## 📈 Detailed Analysis")

    score_data = [
        (
            "👤 Profile Completeness",
            scores.get("profile", 0)
        ),
        (
            "📁 Repository Strength",
            scores.get("repositories", 0)
        ),
        (
            "📖 Documentation",
            scores.get("documentation", 0)
        ),
        (
            "💻 Technology Diversity",
            scores.get("technologies", 0)
        ),
        (
            "🚀 Project Quality",
            scores.get("quality", 0)
        ),
        (
            "📈 GitHub Activity",
            scores.get("activity", 0)
        ),
    ]

    for name, value in score_data:

        value = int(value or 0)

        left, right = st.columns(
            [5, 1]
        )

        with left:
            st.markdown(
                f"**{name}**"
            )

        with right:
            st.markdown(
                f"**{value}%**"
            )

        st.progress(
            max(
                0.0,
                min(
                    1.0,
                    value / 100
                )
            )
        )

    # ======================================================
    # TECHNOLOGY STACK
    # ======================================================

    st.markdown("---")
    st.markdown("## 💻 Technology Stack")

    if languages:

        language_items = list(
            languages.items()
        )

        for i in range(
            0,
            len(language_items),
            4
        ):

            row = language_items[
                i:i + 4
            ]

            cols = st.columns(
                len(row)
            )

            for col, item in zip(
                cols,
                row
            ):

                language, count = item

                with col:
                    st.metric(
                        language,
                        f"{count} repositories"
                    )

    else:
        st.warning(
            "No programming languages detected."
        )

    # ======================================================
    # STRENGTHS
    # ======================================================

    st.markdown("---")
    st.markdown("## ✅ Portfolio Strengths")

    if strengths:

        for strength in strengths:
            st.success(
                f"✓ {strength}"
            )

    else:
        st.info(
            "No major portfolio strengths detected yet."
        )

    # ======================================================
    # IMPROVEMENTS
    # ======================================================

    st.markdown("## 🎯 Recommended Improvements")

    if improvements:

        for number, improvement in enumerate(
            improvements,
            start=1
        ):

            st.markdown(
                f"""
                **{number}. {improvement}**
                """
            )

    else:
        st.success(
            "Your GitHub portfolio is already well optimized."
        )

    # ======================================================
    # REPOSITORIES
    # ======================================================

    st.markdown("---")
    st.markdown("## 📂 Repository Analysis")

    st.caption(
        "TalentSphere reviews your public repositories "
        "for portfolio and placement readiness."
    )

    if not repositories:

        st.warning(
            "No public original repositories found."
        )

    else:

        for index, repo in enumerate(
            repositories[:20],
            start=1
        ):

            repo_name = repo.get(
                "name",
                "Repository"
            )

            language = repo.get(
                "language",
                "Not specified"
            )

            with st.expander(
                f"📁 {index}. {repo_name} • {language}"
            ):

                description = repo.get(
                    "description"
                )

                if description:
                    st.write(
                        description
                    )
                else:
                    st.warning(
                        "No repository description added."
                    )

                c1, c2, c3 = st.columns(3)

                with c1:
                    st.metric(
                        "Language",
                        language
                    )

                with c2:
                    st.metric(
                        "Stars",
                        repo.get(
                            "stars",
                            0
                        )
                    )

                with c3:

                    readme = (
                        "Available"
                        if repo.get(
                            "has_readme"
                        )
                        else "Missing"
                    )

                    st.metric(
                        "README",
                        readme
                    )

                repo_url = repo.get(
                    "url"
                )

                if repo_url:
                    st.link_button(
                        "↗ View Repository",
                        repo_url
                    )

    # ======================================================
    # FINAL ASSESSMENT
    # ======================================================

    st.markdown("---")
    st.markdown("## 🏆 Final Assessment")

    if overall >= 85:

        st.success(
            "Excellent GitHub portfolio. Your profile "
            "provides strong technical evidence for recruiters."
        )

    elif overall >= 70:

        st.success(
            "Strong GitHub portfolio. Improve documentation "
            "and project presentation to make it even better."
        )

    elif overall >= 55:

        st.info(
            "Good portfolio foundation. Add stronger projects, "
            "README files and better repository descriptions."
        )

    elif overall >= 40:

        st.warning(
            "Your portfolio is developing. Focus on meaningful "
            "projects and professional GitHub documentation."
        )

    else:

        st.error(
            "Your GitHub portfolio currently needs improvement. "
            "Build 4–6 strong projects before using GitHub as "
            "a major placement portfolio."
        )