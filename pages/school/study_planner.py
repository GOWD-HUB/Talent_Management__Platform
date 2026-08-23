import html as html_lib
from datetime import datetime

import streamlit as st

from components.back_button import (
    render_back_to_school_dashboard,
)

from database.school_repository import (
    get_school_profile,
)

from services.study_planner_service import (
    WEEK_DAYS,
    clean_subjects,
    generate_weekly_plan,
    calculate_plan_progress,
    get_next_pending_task,
)

from styles.study_planner_theme import (
    apply_study_planner_theme,
)


def safe(value):
    return html_lib.escape(str(value or ""))


def get_plan_state_key(user_id):
    return f"study_plan_{user_id}"


def get_completed_state_key(user_id):
    return f"study_plan_completed_{user_id}"


def render_setup(profile, user_id):

    st.html(
        """
<div class="study-hero">
    <div class="study-eyebrow">PERSONALISED HIGH SCHOOL PLANNING</div>
    <div class="study-title">📅 Build Your Weekly Study Plan</div>
    <div class="study-description">
        Tell TalentSphere how many days and how much time you can study.
        Weak subjects receive extra priority so your plan stays balanced.
    </div>
</div>
"""
    )

    profile_subjects = (
        profile.get("favourite_subjects")
        or ""
    )

    academic_goal = (
        profile.get("academic_goal")
        or "Improve academic performance"
    )

    st.info(
        f"🎯 Academic goal: {academic_goal}"
    )

    with st.form(
        "study_planner_setup_form",
        clear_on_submit=False,
    ):

        study_days = st.multiselect(
            "Study days",
            WEEK_DAYS,
            default=[
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
            ],
        )

        daily_minutes = st.slider(
            "How much time can you study per day?",
            min_value=30,
            max_value=240,
            value=120,
            step=15,
            format="%d minutes",
        )

        weak_subjects = st.multiselect(
            "Subjects that need more attention",
            [
                "Mathematics",
                "Physics",
                "Chemistry",
                "Biology",
                "English",
                "Computer Science",
                "Social Science",
                "General Knowledge",
            ],
        )

        extra_subjects = st.text_input(
            "Other subjects",
            placeholder="Example: Telugu, Hindi",
        )

        submitted = st.form_submit_button(
            "✨ Generate My Weekly Plan",
            use_container_width=True,
        )

    if submitted:

        if not study_days:
            st.error(
                "Please select at least one study day."
            )
            return

        plan = generate_weekly_plan(
            study_days=study_days,
            daily_minutes=daily_minutes,
            favourite_subjects=profile_subjects,
            weak_subjects=weak_subjects,
            extra_subjects=extra_subjects,
        )

        st.session_state[
            get_plan_state_key(user_id)
        ] = {
            "tasks": plan,
            "study_days": study_days,
            "daily_minutes": daily_minutes,
            "weak_subjects": weak_subjects,
            "academic_goal": academic_goal,
        }

        st.session_state[
            get_completed_state_key(user_id)
        ] = []

        st.rerun()


def render_plan(plan_data, user_id):

    tasks = plan_data.get(
        "tasks",
        [],
    )

    completed_key = (
        get_completed_state_key(
            user_id
        )
    )

    if completed_key not in st.session_state:
        st.session_state[
            completed_key
        ] = []

    completed_ids = list(
        st.session_state[
            completed_key
        ]
    )

    progress = calculate_plan_progress(
        tasks,
        completed_ids,
    )

    study_days = plan_data.get(
        "study_days",
        [],
    )

    daily_minutes = plan_data.get(
        "daily_minutes",
        0,
    )

    weak_subjects = plan_data.get(
        "weak_subjects",
        [],
    )

    st.html(
        """
<div class="study-hero">
    <div class="study-eyebrow">YOUR PERSONALISED WEEK</div>
    <div class="study-title">📅 Weekly Study Planner</div>
    <div class="study-description">
        Complete each study block and track your weekly progress.
        You can regenerate the plan whenever your schedule changes.
    </div>
</div>
"""
    )

    st.html(
        f"""
<div class="study-summary-grid">

    <div class="study-summary-card">
        <div class="study-summary-label">Study Days</div>
        <div class="study-summary-value">{len(study_days)}</div>
    </div>

    <div class="study-summary-card">
        <div class="study-summary-label">Daily Study Time</div>
        <div class="study-summary-value">{daily_minutes} min</div>
    </div>

    <div class="study-summary-card">
        <div class="study-summary-label">Plan Progress</div>
        <div class="study-summary-value">{progress}%</div>
    </div>

    <div class="study-summary-card">
        <div class="study-summary-label">Priority Subjects</div>
        <div class="study-summary-value">{len(weak_subjects)}</div>
    </div>

</div>
"""
    )

    st.progress(
        progress / 100
    )

    next_task = get_next_pending_task(
        tasks,
        completed_ids,
    )

    if next_task:

        st.html(
            f"""
<div class="study-next-card">
    <div class="study-next-label">Recommended Next Study Block</div>
    <div class="study-next-title">{safe(next_task["subject"])}</div>
    <div class="study-next-text">
        {safe(next_task["day"])} · {next_task["minutes"]} minutes
    </div>
</div>
"""
        )

    else:

        st.success(
            "🎉 Excellent! You completed every study block in this plan."
        )

    st.markdown("## 📚 Weekly Schedule")

    for day in study_days:

        day_tasks = [
            task
            for task in tasks
            if task["day"] == day
        ]

        if not day_tasks:
            continue

        st.html(
            f"""
<div class="study-day-card">
    <div class="study-day-title">📆 {safe(day)}</div>
</div>
"""
        )

        for task in day_tasks:

            completed = (
                task["id"]
                in completed_ids
            )

            icon = "✅" if completed else "📘"

            st.html(
                f"""
<div class="study-task-card">
    <div class="study-task-title">
        {icon} {safe(task["subject"])}
    </div>
    <div class="study-task-meta">
        {task["minutes"]} minutes · {safe(task["task"])}
    </div>
</div>
"""
            )

            label = (
                "✓ Completed"
                if completed
                else "Mark as Completed"
            )

            if st.button(
                label,
                key=f'study_task_{task["id"]}',
                use_container_width=True,
            ):

                current = list(
                    st.session_state[
                        completed_key
                    ]
                )

                if task["id"] in current:
                    current.remove(
                        task["id"]
                    )
                else:
                    current.append(
                        task["id"]
                    )

                st.session_state[
                    completed_key
                ] = current

                st.rerun()

    st.divider()

    st.markdown(
        "## ⚙️ Planner Controls"
    )

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "🔄 Regenerate Study Plan",
            key="regenerate_study_plan",
            use_container_width=True,
        ):

            st.session_state.pop(
                get_plan_state_key(user_id),
                None,
            )

            st.session_state.pop(
                completed_key,
                None,
            )

            st.rerun()

    with c2:

        if st.button(
            "📝 Open Subject Quiz",
            key="planner_open_quiz",
            use_container_width=True,
        ):

            st.session_state.school_navigation = (
                "📝 Subject Quiz"
            )

            st.rerun()


def render():

    apply_study_planner_theme()

    render_back_to_school_dashboard(
        key="study_planner_dashboard_back",
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

        profile = get_school_profile(
            user_id
        ) or {}

    except Exception:

        profile = {}

    plan_key = get_plan_state_key(
        user_id
    )

    plan_data = st.session_state.get(
        plan_key
    )

    if plan_data:

        render_plan(
            plan_data,
            user_id,
        )

    else:

        render_setup(
            profile,
            user_id,
        )
