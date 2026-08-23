import streamlit as st

from components.back_button import (
    render_back_to_school_dashboard,
)

from services.aptitude_practice_service import (
    get_categories,
    get_questions,
    calculate_score,
    performance_label,
    recommendation,
)

from styles.aptitude_practice_theme import (
    apply_aptitude_theme,
)


def reset_practice():
    keys = [
        key
        for key in list(st.session_state.keys())
        if key.startswith("aptitude_answer_")
    ]

    for key in keys:
        st.session_state.pop(key, None)

    st.session_state.pop(
        "aptitude_result",
        None,
    )


def render():

    apply_aptitude_theme()

    render_back_to_school_dashboard(
        key="aptitude_dashboard_back",
    )

    st.html(
        """
<div class="aptitude-hero">
    <div class="aptitude-eyebrow">
        HIGH SCHOOL APTITUDE DEVELOPMENT
    </div>

    <div class="aptitude-title">
        🧮 Aptitude Practice
    </div>

    <div class="aptitude-description">
        Practise Quantitative Aptitude, Logical Reasoning and Verbal Ability.
        Each category contains 25 questions with scoring, explanations
        and personalised improvement advice.
    </div>
</div>
"""
    )

    st.html(
        """
<div class="aptitude-grid">

    <div class="aptitude-card">
        <div class="aptitude-card-title">🔢 Quantitative Aptitude</div>
        <div class="aptitude-card-text">
            Percentages, averages, ratios, speed, interest,
            arithmetic and basic problem solving.
        </div>
    </div>

    <div class="aptitude-card">
        <div class="aptitude-card-title">🧠 Logical Reasoning</div>
        <div class="aptitude-card-text">
            Number series, analogies, directions, coding,
            classification and pattern recognition.
        </div>
    </div>

    <div class="aptitude-card">
        <div class="aptitude-card-title">📖 Verbal Ability</div>
        <div class="aptitude-card-text">
            Grammar, vocabulary, synonyms, antonyms,
            sentence correction and language usage.
        </div>
    </div>

</div>
"""
    )

    categories = get_categories()

    category = st.selectbox(
        "Choose Practice Category",
        categories,
        key="aptitude_category",
    )

    questions = get_questions(
        category
    )

    st.caption(
        f"{len(questions)} questions · 1 mark each"
    )

    st.divider()

    answers = {}

    with st.form(
        "aptitude_practice_form"
    ):

        for index, item in enumerate(
            questions,
            start=1,
        ):

            st.markdown(
                f"### Q{index}. {item['question']}"
            )

            answer = st.radio(
                "Choose your answer",
                item["options"],
                index=None,
                key=(
                    f"aptitude_answer_"
                    f"{category}_{index}"
                ),
                label_visibility="collapsed",
            )

            answers[
                index - 1
            ] = answer

            st.divider()

        submitted = st.form_submit_button(
            "✅ Submit Aptitude Test",
            use_container_width=True,
        )

    if submitted:

        unanswered = sum(
            1
            for answer in answers.values()
            if answer is None
        )

        if unanswered:

            st.warning(
                f"You have {unanswered} unanswered question(s). "
                "They will be counted as incorrect."
            )

        result = calculate_score(
            questions,
            answers,
        )

        result["category"] = category

        st.session_state[
            "aptitude_result"
        ] = result

    result = st.session_state.get(
        "aptitude_result"
    )

    if result and (
        result.get("category")
        == category
    ):

        percentage = result[
            "percentage"
        ]

        label = performance_label(
            percentage
        )

        st.html(
            f"""
<div class="aptitude-result">
    <h3>🎯 Practice Result</h3>
    <p>
        You scored <strong>{result["correct"]}/{result["total"]}</strong>
        ({percentage}%).
        Performance: <strong>{label}</strong>
    </p>
</div>
"""
        )

        st.progress(
            percentage / 100
        )

        st.html(
            f"""
<div class="aptitude-summary-grid">

    <div class="aptitude-summary-card">
        <div class="aptitude-summary-label">Correct</div>
        <div class="aptitude-summary-value">{result["correct"]}</div>
    </div>

    <div class="aptitude-summary-card">
        <div class="aptitude-summary-label">Incorrect</div>
        <div class="aptitude-summary-value">
            {result["total"] - result["correct"]}
        </div>
    </div>

    <div class="aptitude-summary-card">
        <div class="aptitude-summary-label">Score</div>
        <div class="aptitude-summary-value">{percentage}%</div>
    </div>

    <div class="aptitude-summary-card">
        <div class="aptitude-summary-label">Level</div>
        <div class="aptitude-summary-value">{label}</div>
    </div>

</div>
"""
        )

        st.info(
            "💡 "
            + recommendation(
                category,
                percentage,
            )
        )

        st.markdown(
            "## 📚 Answer Review"
        )

        for index, item in enumerate(
            questions,
            start=1,
        ):

            selected = st.session_state.get(
                f"aptitude_answer_{category}_{index}"
            )

            correct = (
                selected
                == item["answer"]
            )

            icon = (
                "✅"
                if correct
                else "❌"
            )

            with st.expander(
                f"{icon} Q{index}. {item['question']}"
            ):

                st.write(
                    f"**Your answer:** "
                    f"{selected or 'Not answered'}"
                )

                st.write(
                    f"**Correct answer:** "
                    f"{item['answer']}"
                )

                st.write(
                    f"**Explanation:** "
                    f"{item['explanation']}"
                )

        c1, c2 = st.columns(2)

        with c1:

            if st.button(
                "🔄 Retry This Category",
                key="aptitude_retry",
                use_container_width=True,
            ):

                reset_practice()

                st.rerun()

        with c2:

            if st.button(
                "🤖 Ask AI Study Mentor",
                key="aptitude_ai_mentor",
                use_container_width=True,
            ):

                st.session_state.school_navigation = (
                    "🤖 AI Study Mentor"
                )

                st.rerun()
