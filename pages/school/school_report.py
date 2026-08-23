import html as html_lib

import streamlit as st

from components.back_button import (
    render_back_to_school_dashboard,
)

from database.school_repository import (
    get_school_profile,
)

from database.goal_repository import (
    get_goals,
)

from services.school_report_service import (
    build_action_plan,
    build_improvement_areas,
    build_report,
    build_strengths,
    calculate_student_score,
    score_label,
)

from styles.school_report_theme import (
    apply_school_report_theme,
)


def safe(value):
    return html_lib.escape(
        str(value or "")
    )


def get_study_plan_state(user_id):
    plan_key = f"study_plan_{user_id}"
    completed_key = (
        f"study_plan_completed_{user_id}"
    )

    return (
        st.session_state.get(plan_key),
        st.session_state.get(
            completed_key,
            [],
        ),
    )


def render_list(items):
    for item in items:
        st.markdown(
            f"- {item}"
        )


def build_download_html(
    student_name,
    report,
    score,
    score_text,
    strengths,
    improvements,
    actions,
):
    profile = report.get(
        "profile",
        {},
    )

    quiz = report.get("quiz")
    aptitude = report.get("aptitude")
    interest = report.get("top_interest")
    goals = report.get("goals", {})
    study = report.get("study_plan", {})

    interest_text = (
        interest.get("area")
        if interest
        else "Not assessed"
    )

    quiz_text = (
        f'{quiz.get("subject")} - '
        f'{quiz.get("percentage")}% '
        f'({quiz.get("correct")}/{quiz.get("total")})'
        if quiz
        else "Not completed"
    )

    aptitude_text = (
        f'{aptitude.get("category")} - '
        f'{aptitude.get("percentage")}% '
        f'({aptitude.get("correct")}/{aptitude.get("total")})'
        if aptitude
        else "Not completed"
    )

    strengths_html = "".join(
        f"<li>{safe(item)}</li>"
        for item in strengths
    )

    improvements_html = "".join(
        f"<li>{safe(item)}</li>"
        for item in improvements
    )

    actions_html = "".join(
        f"<li>{safe(item)}</li>"
        for item in actions
    )

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>TalentSphere School Report</title>
<style>
body {{
    font-family: Arial, sans-serif;
    color: #0f172a;
    max-width: 900px;
    margin: auto;
    padding: 40px;
}}
h1, h2 {{
    color: #0f172a;
}}
.card {{
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px;
    margin: 12px 0;
}}
.muted {{
    color: #64748b;
}}
.score {{
    font-size: 36px;
    font-weight: bold;
}}
</style>
</head>
<body>

<h1>TalentSphere Elevate</h1>
<div class="muted">High School Student Development Report</div>

<h2>{safe(student_name)}</h2>
<p>Generated: {safe(report.get("generated_at"))}</p>

<div class="card">
<div class="score">{score}%</div>
<b>{safe(score_text)}</b><br>
Profile Completion: {report.get("profile_completion", 0)}%
</div>

<h2>Student Profile</h2>
<div class="card">
<b>School:</b> {safe(profile.get("school_name") or "Not added")}<br>
<b>Class:</b> {safe(profile.get("current_class") or "Not added")}<br>
<b>Board:</b> {safe(profile.get("board") or "Not added")}<br>
<b>City:</b> {safe(profile.get("city") or "Not added")}<br>
<b>Favourite Subjects:</b> {safe(profile.get("favourite_subjects") or "Not added")}<br>
<b>Interests:</b> {safe(profile.get("interests") or "Not added")}<br>
<b>Skills:</b> {safe(profile.get("skills") or "Not added")}<br>
<b>Dream Career:</b> {safe(profile.get("dream_career") or "Not added")}<br>
<b>Academic Goal:</b> {safe(profile.get("academic_goal") or "Not added")}
</div>

<h2>Career & Interest</h2>
<div class="card">
<b>Top Interest:</b> {safe(interest_text)}<br>
<b>Career Direction:</b> {safe(report.get("career_direction"))}
</div>

<h2>Academic Practice</h2>
<div class="card">
<b>Latest Subject Quiz:</b> {safe(quiz_text)}<br>
<b>Latest Aptitude Practice:</b> {safe(aptitude_text)}
</div>

<h2>Goals</h2>
<div class="card">
Total Goals: {goals.get("total", 0)}<br>
Active Goals: {goals.get("active", 0)}<br>
Completed Goals: {goals.get("completed", 0)}
</div>

<h2>Study Planner</h2>
<div class="card">
Plan Created: {"Yes" if study.get("exists") else "No"}<br>
Completed Blocks: {study.get("completed", 0)} / {study.get("tasks", 0)}<br>
Progress: {study.get("progress", 0)}%
</div>

<h2>Strengths</h2>
<ul>{strengths_html}</ul>

<h2>Areas to Improve</h2>
<ul>{improvements_html}</ul>

<h2>Recommended Next Actions</h2>
<ul>{actions_html}</ul>

<p class="muted">
This report is a learning-progress and career-exploration summary.
It is not an admission, psychological or professional career assessment.
</p>

</body>
</html>
"""


def render():

    apply_school_report_theme()

    render_back_to_school_dashboard(
        key="school_report_back_dashboard",
    )

    user_id = st.session_state.get(
        "user_id"
    )

    if not user_id:
        st.error(
            "Unable to identify the logged-in student."
        )
        return

    try:
        profile = (
            get_school_profile(
                user_id
            )
            or {}
        )
    except Exception:
        profile = {}

    try:
        goals = (
            get_goals(
                user_id
            )
            or []
        )
    except Exception:
        goals = []

    interest_results = (
        st.session_state.get(
            "interest_assessment_results"
        )
    )

    career_area = (
        st.session_state.get(
            "selected_career_area"
        )
    )

    quiz_result = (
        st.session_state.get(
            "subject_quiz_result"
        )
    )

    aptitude_result = (
        st.session_state.get(
            "aptitude_result"
        )
    )

    (
        study_plan_data,
        study_completed_ids,
    ) = get_study_plan_state(
        user_id
    )

    report = build_report(
        profile=profile,
        interest_results=interest_results,
        selected_career_area=career_area,
        quiz_result=quiz_result,
        aptitude_result=aptitude_result,
        goals=goals,
        study_plan_data=study_plan_data,
        study_completed_ids=study_completed_ids,
    )

    score = calculate_student_score(
        report
    )

    score_text = score_label(
        score
    )

    strengths = build_strengths(
        report
    )

    improvements = build_improvement_areas(
        report
    )

    action_plan = build_action_plan(
        report
    )

    student_name = (
        st.session_state.get(
            "user_name"
        )
        or "Student"
    )

    st.html(
        f"""
<div class="report-hero">
    <div class="report-eyebrow">
        PERSONALISED STUDENT DEVELOPMENT SUMMARY
    </div>

    <div class="report-title">
        📄 {safe(student_name)}'s School Report
    </div>

    <div class="report-description">
        Review your academic profile, interests, career direction,
        Subject Quiz, Aptitude Practice, Study Planner and Goal Tracker
        progress in one place.
    </div>
</div>
"""
    )

    # ======================================================
    # SCORE
    # ======================================================

    st.html(
        f"""
<div class="report-score">
    <div class="report-score-label">
        STUDENT DEVELOPMENT SCORE
    </div>

    <div class="report-score-value">
        {score}%
    </div>

    <div class="report-description">
        {safe(score_text)}
    </div>
</div>
"""
    )

    st.progress(
        score / 100
    )

    quiz = report.get("quiz")
    aptitude = report.get("aptitude")
    goals_summary = report.get(
        "goals",
        {},
    )
    study = report.get(
        "study_plan",
        {},
    )

    st.html(
        f"""
<div class="report-grid">

    <div class="report-card">
        <div class="report-label">
            Profile Completion
        </div>
        <div class="report-value">
            {report.get("profile_completion", 0)}%
        </div>
    </div>

    <div class="report-card">
        <div class="report-label">
            Subject Quiz
        </div>
        <div class="report-value">
            {quiz.get("percentage", 0) if quiz else 0}%
        </div>
    </div>

    <div class="report-card">
        <div class="report-label">
            Aptitude
        </div>
        <div class="report-value">
            {aptitude.get("percentage", 0) if aptitude else 0}%
        </div>
    </div>

    <div class="report-card">
        <div class="report-label">
            Study Plan
        </div>
        <div class="report-value">
            {study.get("progress", 0)}%
        </div>
    </div>

</div>
"""
    )

    # ======================================================
    # PROFILE
    # ======================================================

    st.markdown(
        "## 👤 Student Profile"
    )

    c1, c2 = st.columns(2)

    with c1:
        st.write(
            "**School:**",
            profile.get(
                "school_name"
            )
            or "Not added",
        )
        st.write(
            "**Class:**",
            profile.get(
                "current_class"
            )
            or "Not added",
        )
        st.write(
            "**Board:**",
            profile.get(
                "board"
            )
            or "Not added",
        )
        st.write(
            "**City:**",
            profile.get(
                "city"
            )
            or "Not added",
        )

    with c2:
        st.write(
            "**Favourite Subjects:**",
            profile.get(
                "favourite_subjects"
            )
            or "Not added",
        )
        st.write(
            "**Dream Career:**",
            profile.get(
                "dream_career"
            )
            or "Not added",
        )
        st.write(
            "**Academic Goal:**",
            profile.get(
                "academic_goal"
            )
            or "Not added",
        )

    # ======================================================
    # CAREER
    # ======================================================

    st.markdown(
        "## 🔍 Career & Interest"
    )

    top_interest = (
        report.get(
            "top_interest"
        )
    )

    st.write(
        "**Top Interest Area:**",
        (
            top_interest.get(
                "area"
            )
            if top_interest
            else "Not assessed"
        ),
    )

    st.write(
        "**Career Direction:**",
        report.get(
            "career_direction"
        ),
    )

    # ======================================================
    # QUIZ + APTITUDE
    # ======================================================

    st.markdown(
        "## 📝 Academic Practice"
    )

    q1, q2 = st.columns(2)

    with q1:
        st.markdown(
            "### Subject Quiz"
        )

        if quiz:
            st.metric(
                quiz.get(
                    "subject"
                )
                or "Latest Quiz",
                f'{quiz.get("percentage", 0)}%',
            )
            st.caption(
                f'{quiz.get("correct", 0)} / '
                f'{quiz.get("total", 0)} correct'
            )
        else:
            st.info(
                "No Subject Quiz completed in this session."
            )

    with q2:
        st.markdown(
            "### Aptitude Practice"
        )

        if aptitude:
            st.metric(
                aptitude.get(
                    "category"
                )
                or "Latest Aptitude",
                f'{aptitude.get("percentage", 0)}%',
            )
            st.caption(
                f'{aptitude.get("correct", 0)} / '
                f'{aptitude.get("total", 0)} correct'
            )
        else:
            st.info(
                "No Aptitude Practice result available yet."
            )

    # ======================================================
    # GOALS + STUDY
    # ======================================================

    st.markdown(
        "## 🎯 Goals & Study Progress"
    )

    g1, g2 = st.columns(2)

    with g1:
        st.metric(
            "Active Goals",
            goals_summary.get(
                "active",
                0,
            ),
        )
        st.caption(
            f'Completed: '
            f'{goals_summary.get("completed", 0)} '
            f'of {goals_summary.get("total", 0)}'
        )

    with g2:
        st.metric(
            "Study Planner Progress",
            f'{study.get("progress", 0)}%',
        )
        st.caption(
            f'Completed blocks: '
            f'{study.get("completed", 0)} / '
            f'{study.get("tasks", 0)}'
        )

    # ======================================================
    # STRENGTHS
    # ======================================================

    st.markdown(
        "## ✅ Strengths"
    )

    render_list(
        strengths
    )

    # ======================================================
    # IMPROVEMENTS
    # ======================================================

    st.markdown(
        "## 📈 Areas to Improve"
    )

    render_list(
        improvements
    )

    # ======================================================
    # ACTION PLAN
    # ======================================================

    st.markdown(
        "## 🚀 Recommended Next Actions"
    )

    for index, item in enumerate(
        action_plan,
        start=1,
    ):
        st.html(
            f"""
<div class="report-action">
    <strong>Step {index}:</strong>
    {safe(item)}
</div>
"""
        )

    # ======================================================
    # DOWNLOAD
    # ======================================================

    st.divider()

    report_html = build_download_html(
        student_name=student_name,
        report=report,
        score=score,
        score_text=score_text,
        strengths=strengths,
        improvements=improvements,
        actions=action_plan,
    )

    st.download_button(
        "⬇️ Download School Report",
        data=report_html.encode(
            "utf-8"
        ),
        file_name=(
            "TalentSphere_School_Report.html"
        ),
        mime="text/html",
        use_container_width=True,
    )

    # ======================================================
    # NAVIGATION
    # ======================================================

    n1, n2, n3 = st.columns(3)

    with n1:
        if st.button(
            "🤖 AI Study Mentor",
            key="report_ai_mentor",
            use_container_width=True,
        ):
            st.session_state.school_navigation = (
                "🤖 AI Study Mentor"
            )
            st.rerun()

    with n2:
        if st.button(
            "📅 Study Planner",
            key="report_study_planner",
            use_container_width=True,
        ):
            st.session_state.school_navigation = (
                "📅 Study Planner"
            )
            st.rerun()

    with n3:
        if st.button(
            "🎯 Goal Tracker",
            key="report_goal_tracker",
            use_container_width=True,
        ):
            st.session_state.school_navigation = (
                "🎯 Goal Tracker"
            )
            st.rerun()
