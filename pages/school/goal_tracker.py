import html as html_lib
from datetime import date, timedelta

import streamlit as st

from components.back_button import render_back_to_school_dashboard

from database.goal_repository import (
    create_goal,
    delete_goal,
    get_goals,
    update_goal,
    update_goal_progress,
)

from services.goal_service import (
    CATEGORY_ICONS,
    calculate_goal_progress,
    get_deadline_label,
    get_goal_health,
    get_goal_summary,
    get_recommendation,
)

from styles.goal_tracker_theme import apply_goal_tracker_theme


def safe(value):
    return html_lib.escape(str(value or ""))


def parse_milestones(text):
    return [line.strip() for line in str(text or "").splitlines() if line.strip()]


def render_create_goal(user_id):
    with st.expander("➕ Create New Goal", expanded=False):
        with st.form("create_school_goal_form", clear_on_submit=True):
            title = st.text_input(
                "Goal Title",
                placeholder="Example: Score above 90% in Mathematics",
            )

            c1, c2 = st.columns(2)

            with c1:
                category = st.selectbox(
                    "Goal Category",
                    ["Academic", "Career", "Skill", "Personal"],
                )
                priority = st.selectbox(
                    "Priority",
                    ["High", "Medium", "Low"],
                )

            with c2:
                target_date = st.date_input(
                    "Target Date",
                    value=date.today() + timedelta(days=30),
                )

            description = st.text_area(
                "Goal Description",
                placeholder="Describe what you want to achieve and why it matters.",
                height=90,
            )

            milestones_text = st.text_area(
                "Milestones — one per line",
                placeholder="Complete Chapter 1\nPractise 50 questions\nTake a mock test",
                height=130,
            )

            submitted = st.form_submit_button(
                "🎯 Create Goal",
                use_container_width=True,
            )

        if submitted:
            if not title.strip():
                st.error("Please enter a goal title.")
                return

            milestones = parse_milestones(milestones_text)

            if not milestones:
                st.error("Please add at least one milestone.")
                return

            create_goal(
                user_id=user_id,
                title=title,
                category=category,
                description=description,
                target_date=target_date.isoformat(),
                priority=priority,
                milestones=milestones,
            )

            st.success("Goal created successfully.")
            st.rerun()


def render_edit_goal(goal):
    goal_id = goal["id"]

    with st.expander(f'✏️ Edit — {goal["title"]}', expanded=False):
        with st.form(f"edit_goal_{goal_id}"):

            title = st.text_input(
                "Goal Title",
                value=goal.get("title", ""),
            )

            c1, c2 = st.columns(2)

            with c1:
                categories = ["Academic", "Career", "Skill", "Personal"]
                current_category = goal.get("category", "Academic")

                category = st.selectbox(
                    "Category",
                    categories,
                    index=categories.index(current_category)
                    if current_category in categories else 0,
                )

                priorities = ["High", "Medium", "Low"]
                current_priority = goal.get("priority", "Medium")

                priority = st.selectbox(
                    "Priority",
                    priorities,
                    index=priorities.index(current_priority)
                    if current_priority in priorities else 1,
                )

            with c2:
                try:
                    target_value = date.fromisoformat(goal.get("target_date"))
                except Exception:
                    target_value = date.today() + timedelta(days=30)

                target_date = st.date_input(
                    "Target Date",
                    value=target_value,
                )

            description = st.text_area(
                "Description",
                value=goal.get("description", ""),
            )

            milestones_text = st.text_area(
                "Milestones — one per line",
                value="\n".join(goal.get("milestones", [])),
                height=130,
            )

            save = st.form_submit_button(
                "💾 Save Changes",
                use_container_width=True,
            )

        if save:
            milestones = parse_milestones(milestones_text)

            if not title.strip():
                st.error("Goal title cannot be empty.")
                return

            if not milestones:
                st.error("Please keep at least one milestone.")
                return

            update_goal(
                goal_id=goal_id,
                title=title,
                category=category,
                description=description,
                target_date=target_date.isoformat(),
                priority=priority,
                milestones=milestones,
            )

            st.success("Goal updated.")
            st.rerun()


def render_goal(goal):
    goal_id = goal["id"]
    progress = calculate_goal_progress(goal)
    health = get_goal_health(goal)
    deadline = get_deadline_label(goal.get("target_date"))
    icon = CATEGORY_ICONS.get(goal.get("category"), "🎯")

    st.html(
        f"""
<div class="goal-card">
    <div class="goal-category">
        {safe(icon)} {safe(goal.get("category"))}
        · {safe(goal.get("priority"))} Priority
    </div>
    <div class="goal-card-title">{safe(goal.get("title"))}</div>
    <div class="goal-card-text">{safe(goal.get("description"))}</div>
    <div class="goal-meta">{safe(deadline)} · {safe(health)}</div>
</div>
"""
    )

    st.progress(progress / 100)
    st.caption(f"{progress}% complete")

    milestones = goal.get("milestones", [])
    completed = list(goal.get("completed_milestones", []))

    st.markdown("#### ✅ Milestones")

    changed = False

    for index, milestone in enumerate(milestones):
        checked = milestone in completed

        selected = st.checkbox(
            milestone,
            value=checked,
            key=f"goal_{goal_id}_milestone_{index}",
        )

        if selected != checked:
            changed = True

            if selected and milestone not in completed:
                completed.append(milestone)

            if not selected and milestone in completed:
                completed.remove(milestone)

    if changed:
        update_goal_progress(goal_id, completed)
        st.rerun()

    render_edit_goal(goal)

    with st.expander("🗑️ Delete Goal", expanded=False):
        st.warning("Deleting a goal cannot be undone.")

        if st.button(
            "Delete This Goal",
            key=f"delete_goal_{goal_id}",
            use_container_width=True,
        ):
            delete_goal(goal_id)
            st.success("Goal deleted.")
            st.rerun()


def render():
    apply_goal_tracker_theme()

    render_back_to_school_dashboard(
        key="goal_tracker_dashboard_back",
    )

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.error("Unable to identify the logged-in student.")
        return

    goals = get_goals(user_id)
    summary = get_goal_summary(goals)
    recommendation = get_recommendation(goals)

    st.html(
        """
<div class="goal-hero">
    <div class="goal-eyebrow">HIGH SCHOOL GOAL MANAGEMENT</div>
    <div class="goal-title">🎯 Goal Tracker</div>
    <div class="goal-description">
        Turn academic, career and skill goals into clear milestones.
        Track progress, deadlines and completed achievements in one place.
    </div>
</div>
"""
    )

    st.html(
        f"""
<div class="goal-summary-grid">
    <div class="goal-summary-card">
        <div class="goal-summary-label">Total Goals</div>
        <div class="goal-summary-value">{summary["total"]}</div>
    </div>
    <div class="goal-summary-card">
        <div class="goal-summary-label">Active</div>
        <div class="goal-summary-value">{summary["active"]}</div>
    </div>
    <div class="goal-summary-card">
        <div class="goal-summary-label">Completed</div>
        <div class="goal-summary-value">{summary["completed"]}</div>
    </div>
    <div class="goal-summary-card">
        <div class="goal-summary-label">Overall Progress</div>
        <div class="goal-summary-value">{summary["overall_progress"]}%</div>
    </div>
</div>
"""
    )

    st.progress(summary["overall_progress"] / 100)

    st.html(
        f"""
<div class="goal-recommendation">
    <div class="goal-recommendation-title">💡 Recommended Next Step</div>
    <div class="goal-recommendation-text">{safe(recommendation)}</div>
</div>
"""
    )

    render_create_goal(user_id)

    st.markdown("## 📌 Your Goals")

    if not goals:
        st.info("You do not have any goals yet. Create your first goal above.")
        return

    active_goals = [g for g in goals if g.get("status") == "Active"]
    completed_goals = [g for g in goals if g.get("status") == "Completed"]

    if active_goals:
        st.markdown("### 🚀 Active Goals")
        for goal in active_goals:
            render_goal(goal)

    if completed_goals:
        st.markdown("### ✅ Completed Goals")
        for goal in completed_goals:
            render_goal(goal)
