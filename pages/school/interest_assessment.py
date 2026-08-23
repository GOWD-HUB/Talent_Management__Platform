import streamlit as st

from components.back_button import (
    render_back_to_school_dashboard,
)

from services.interest_service import (
    QUESTIONS,
    ANSWER_OPTIONS,
    AREA_INFO,
    calculate_interest_scores,
    get_top_interest_areas,
)

from styles.interest_assessment_theme import (
    apply_interest_assessment_theme,
)


# ==========================================================
# RESULT CARD
# ==========================================================

def render_result_card(
    area,
    score,
    rank,
):

    info = AREA_INFO.get(
        area,
        {},
    )

    icon = info.get(
        "icon",
        "🌟",
    )

    description = info.get(
        "description",
        "",
    )

    st.html(
        f"""
<div class="interest-result-card">

    <div class="interest-result-icon">
        {icon}
    </div>

    <div class="interest-result-rank">
        TOP {rank} INTEREST AREA
    </div>

    <div class="interest-result-title">
        {area}
    </div>

    <div class="interest-result-score">
        {score}% Interest Score
    </div>

    <div class="interest-result-description">
        {description}
    </div>

</div>
"""
    )


# ==========================================================
# RESULTS PAGE
# ==========================================================

def render_results():

    ranked_scores = st.session_state.get(
        "interest_assessment_results",
        [],
    )

    if not ranked_scores:

        st.warning(
            "No assessment results found."
        )

        return

    top_areas = get_top_interest_areas(
        ranked_scores,
        limit=3,
    )

    st.markdown(
        "## 🌟 Your Top Interest Areas"
    )

    st.caption(
        "These results show the areas you currently enjoy most. "
        "They are for exploration, not a permanent career decision."
    )

    columns = st.columns(3)

    for index, result in enumerate(
        top_areas
    ):

        area, score = result

        with columns[index]:

            render_result_card(
                area=area,
                score=score,
                rank=index + 1,
            )

    st.divider()

    st.markdown(
        "## 📊 Complete Interest Profile"
    )

    for area, score in ranked_scores:

        st.write(
            f"**{AREA_INFO[area]['icon']} {area}**"
        )

        st.progress(
            score / 100
        )

        st.caption(
            f"{score}%"
        )

    st.divider()

    st.markdown(
        "## 🎯 What should you do next?"
    )

    action1, action2 = st.columns(2)

    with action1:

        if st.button(
            "🔍 Open Career Explorer",
            key="interest_open_career",
            use_container_width=True,
        ):

            if top_areas:

                st.session_state[
                    "selected_career_area"
                ] = top_areas[0][0]

            st.session_state.school_navigation = (
                "🔍 Career Explorer"
            )

            st.rerun()

    with action2:

        if st.button(
            "🔄 Retake Assessment",
            key="interest_retake",
            use_container_width=True,
        ):

            st.session_state.pop(
                "interest_assessment_results",
                None,
            )

            keys_to_remove = [
                key
                for key in st.session_state.keys()
                if str(key).startswith(
                    "interest_answer_"
                )
            ]

            for key in keys_to_remove:
                st.session_state.pop(
                    key,
                    None,
                )

            st.rerun()

    st.info(
        "Interest scores can change as you grow, learn new subjects "
        "and try new activities. You can retake this assessment later."
    )


# ==========================================================
# ASSESSMENT FORM
# ==========================================================

def render_assessment():

    st.markdown(
        "## 📝 Tell us what you enjoy"
    )

    st.caption(
        "Choose the answer that feels most true for you. "
        "There are no right or wrong answers."
    )

    answers = {}

    with st.form(
        "high_school_interest_assessment",
        clear_on_submit=False,
    ):

        for index, question in enumerate(
            QUESTIONS,
            start=1,
        ):

            st.html(
                f"""
<div class="interest-question-card">

    <div class="interest-question-number">
        QUESTION {index} OF {len(QUESTIONS)}
    </div>

    <div class="interest-question-text">
        {question["text"]}
    </div>

</div>
"""
            )

            selected = st.radio(
                "Choose one",
                list(
                    ANSWER_OPTIONS.keys()
                ),
                index=None,
                key=(
                    f"interest_answer_"
                    f"{question['id']}"
                ),
                horizontal=True,
                label_visibility="collapsed",
            )

            if selected:

                answers[
                    question["id"]
                ] = ANSWER_OPTIONS[
                    selected
                ]

        submitted = st.form_submit_button(
            "📊 Calculate My Interest Profile",
            use_container_width=True,
        )

    if submitted:

        if len(answers) != len(
            QUESTIONS
        ):

            st.error(
                "Please answer all questions before submitting."
            )

            return

        ranked_scores = (
            calculate_interest_scores(
                answers
            )
        )

        st.session_state[
            "interest_assessment_results"
        ] = ranked_scores

        st.rerun()


# ==========================================================
# PAGE
# ==========================================================

def render():

    apply_interest_assessment_theme()

    # ======================================================
    # BACK
    # ======================================================

    render_back_to_school_dashboard(
        key="interest_dashboard_back",
    )

    # ======================================================
    # HERO
    # ======================================================

    st.html(
        """
<div class="interest-hero">

    <div class="interest-eyebrow">
        HIGH SCHOOL INTEREST ASSESSMENT
    </div>

    <div class="interest-title">
        📊 Discover What You Enjoy
    </div>

    <div class="interest-description">
        Answer a few simple questions about the activities,
        subjects and situations you enjoy. TalentSphere will
        identify your strongest interest areas and help you
        explore related career directions.
    </div>

</div>
"""
    )

    # ======================================================
    # EXISTING RESULTS
    # ======================================================

    if st.session_state.get(
        "interest_assessment_results"
    ):

        render_results()

    else:

        render_assessment()