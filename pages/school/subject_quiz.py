import html as html_lib
import streamlit as st

from components.back_button import render_back_to_school_dashboard

from services.subject_quiz_service import (
    get_subjects,
    get_questions,
    get_question_count,
    calculate_result,
)

from styles.subject_quiz_theme import (
    apply_subject_quiz_theme,
)


SUBJECT_ICONS = {
    "Mathematics": "➗",
    "Physics": "⚛️",
    "Chemistry": "🧪",
    "Biology": "🧬",
    "English": "📖",
    "Computer Science": "💻",
    "Social Science": "🌍",
    "General Knowledge": "🧠",
}


def safe(value):
    if value is None:
        return ""
    return html_lib.escape(str(value))


def clear_quiz_answers(subject):
    prefix = f"quiz_answer_{subject}_"
    for key in list(st.session_state.keys()):
        if str(key).startswith(prefix):
            st.session_state.pop(key, None)


def open_subject(subject):
    st.session_state.subject_quiz_selected = subject
    st.session_state.pop("subject_quiz_result", None)
    clear_quiz_answers(subject)
    st.rerun()


def render_subject_selection():

    st.html(
        """
<div class="quiz-hero">
    <div class="quiz-eyebrow">HIGH SCHOOL SUBJECT PRACTICE</div>
    <div class="quiz-title">📝 Subject Quiz</div>
    <div class="quiz-description">
        Choose a subject and complete a 25-question high-school quiz.
        Your result includes score, percentage, performance level,
        correct answers and explanations for revision.
    </div>
</div>
"""
    )

    st.markdown("## 📚 Choose a Subject")

    subjects = get_subjects()

    for start in range(0, len(subjects), 4):
        row = subjects[start:start + 4]
        cols = st.columns(len(row))

        for i, subject in enumerate(row):
            with cols[i]:
                icon = SUBJECT_ICONS.get(subject, "📘")
                count = get_question_count(subject)

                st.html(
                    f"""
<div class="quiz-subject-card">
    <div class="quiz-subject-title">{icon} {safe(subject)}</div>
    <div class="quiz-subject-meta">
        {count} MCQs<br>
        Easy + Medium + Hard<br>
        Instant score & explanations
    </div>
</div>
"""
                )

                if st.button(
                    f"Start {subject}",
                    key=f"quiz_start_{subject}",
                    use_container_width=True,
                ):
                    open_subject(subject)


def render_quiz(subject):

    questions = get_questions(subject)

    top1, top2, spacer = st.columns([1.4, 1.5, 7.1])

    with top1:
        if st.button(
            "← Subjects",
            key="quiz_back_subjects",
            use_container_width=True,
        ):
            clear_quiz_answers(subject)
            st.session_state.pop("subject_quiz_selected", None)
            st.session_state.pop("subject_quiz_result", None)
            st.rerun()

    with top2:
        if st.button(
            "🏠 Dashboard",
            key="quiz_dashboard",
            use_container_width=True,
        ):
            st.session_state.pop("subject_quiz_selected", None)
            st.session_state.pop("subject_quiz_result", None)
            st.session_state.school_navigation = "🏠 Student Home"
            st.rerun()

    st.html(
        f"""
<div class="quiz-hero">
    <div class="quiz-eyebrow">25 QUESTION ASSESSMENT</div>
    <div class="quiz-title">{SUBJECT_ICONS.get(subject, "📘")} {safe(subject)} Quiz</div>
    <div class="quiz-description">
        Answer every question and submit once you are ready.
        There is no negative marking.
    </div>
</div>
"""
    )

    answers = {}

    with st.form(
        f"subject_quiz_form_{subject}",
        clear_on_submit=False,
    ):

        for index, question in enumerate(questions):
            text, options, correct_index, explanation, difficulty = question

            st.html(
                f"""
<div class="quiz-question-card">
    <div class="quiz-question-number">
        QUESTION {index + 1} OF {len(questions)}
    </div>
    <div class="quiz-question-text">
        {safe(text)}
    </div>
    <div class="quiz-difficulty">
        {safe(difficulty)}
    </div>
</div>
"""
            )

            selected = st.radio(
                f"Question {index + 1}",
                options,
                index=None,
                key=f"quiz_answer_{subject}_{index}",
                label_visibility="collapsed",
            )

            if selected is not None:
                answers[index] = options.index(selected)

        submitted = st.form_submit_button(
            "✅ Submit Quiz",
            use_container_width=True,
        )

    if submitted:
        if len(answers) != len(questions):
            st.error(
                f"Please answer all {len(questions)} questions before submitting."
            )
            return

        result = calculate_result(
            subject,
            answers,
        )

        st.session_state.subject_quiz_result = result
        st.rerun()


def render_results(result):

    subject = result["subject"]

    top1, top2, spacer = st.columns([1.4, 1.5, 7.1])

    with top1:
        if st.button(
            "← Subjects",
            key="result_back_subjects",
            use_container_width=True,
        ):
            clear_quiz_answers(subject)
            st.session_state.pop("subject_quiz_selected", None)
            st.session_state.pop("subject_quiz_result", None)
            st.rerun()

    with top2:
        if st.button(
            "🏠 Dashboard",
            key="result_dashboard",
            use_container_width=True,
        ):
            st.session_state.pop("subject_quiz_selected", None)
            st.session_state.pop("subject_quiz_result", None)
            st.session_state.school_navigation = "🏠 Student Home"
            st.rerun()

    st.html(
        f"""
<div class="quiz-result-card">
    <div class="quiz-eyebrow">{safe(subject.upper())} RESULT</div>
    <div class="quiz-result-score">
        {result["correct"]} / {result["total"]}
    </div>
    <div class="quiz-result-label">
        {result["percentage"]}% · {safe(result["level"])}
    </div>
    <div class="quiz-description">
        {safe(result["message"])}
    </div>
</div>
"""
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Correct", result["correct"])

    with c2:
        st.metric(
            "Wrong",
            result["total"] - result["correct"],
        )

    with c3:
        st.metric(
            "Percentage",
            f'{result["percentage"]}%',
        )

    st.progress(
        result["percentage"] / 100
    )

    action1, action2 = st.columns(2)

    with action1:
        if st.button(
            "🔄 Retake This Quiz",
            key="retake_subject_quiz",
            use_container_width=True,
        ):
            clear_quiz_answers(subject)
            st.session_state.pop("subject_quiz_result", None)
            st.rerun()

    with action2:
        if st.button(
            "📚 Choose Another Subject",
            key="choose_another_subject",
            use_container_width=True,
        ):
            clear_quiz_answers(subject)
            st.session_state.pop("subject_quiz_selected", None)
            st.session_state.pop("subject_quiz_result", None)
            st.rerun()

    st.divider()

    st.markdown("## 🔎 Answer Review")

    st.caption(
        "Review every question, including the correct answer and a short explanation."
    )

    for item in result["details"]:

        options = item["options"]
        correct_answer = options[item["correct_index"]]

        if item["selected_index"] is None:
            selected_answer = "Not answered"
        else:
            selected_answer = options[item["selected_index"]]

        card_class = (
            "quiz-review-correct"
            if item["is_correct"]
            else "quiz-review-wrong"
        )

        status = "✅ Correct" if item["is_correct"] else "❌ Incorrect"

        st.html(
            f"""
<div class="{card_class}">
    <div class="quiz-review-title">
        {status} · Q{item["number"]}. {safe(item["question"])}
    </div>
    <div class="quiz-review-text">
        <b>Your answer:</b> {safe(selected_answer)}<br>
        <b>Correct answer:</b> {safe(correct_answer)}<br>
        <b>Explanation:</b> {safe(item["explanation"])}
    </div>
</div>
"""
        )


def render():

    apply_subject_quiz_theme()

    result = st.session_state.get(
        "subject_quiz_result"
    )

    if result:
        render_results(result)
        return

    subject = st.session_state.get(
        "subject_quiz_selected"
    )

    if subject:
        render_quiz(subject)
        return

    render_back_to_school_dashboard(
        key="subject_quiz_back_dashboard",
    )

    render_subject_selection()
