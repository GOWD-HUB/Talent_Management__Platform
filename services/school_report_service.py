# ==========================================================
# TALENTSPHERE - SCHOOL REPORT SERVICE
# ==========================================================

from datetime import datetime


PROFILE_FIELDS = [
    "school_name",
    "current_class",
    "board",
    "city",
    "favourite_subjects",
    "interests",
    "skills",
    "dream_career",
    "academic_goal",
]


def profile_completion(profile):
    profile = profile or {}

    completed = sum(
        1
        for field in PROFILE_FIELDS
        if str(profile.get(field) or "").strip()
    )

    if not PROFILE_FIELDS:
        return 0

    return round(
        completed / len(PROFILE_FIELDS) * 100
    )


def get_top_interest(interest_results):
    if not interest_results:
        return None

    try:
        first = interest_results[0]

        if isinstance(first, dict):
            area = (
                first.get("area")
                or first.get("name")
                or first.get("category")
            )
            score = first.get("score")

            return {
                "area": area,
                "score": score,
            }

        if isinstance(first, (list, tuple)) and first:
            return {
                "area": first[0],
                "score": (
                    first[1]
                    if len(first) > 1
                    else None
                ),
            }

    except Exception:
        pass

    return None


def goal_summary(goals):
    goals = goals or []

    total = len(goals)

    active = sum(
        1
        for goal in goals
        if goal.get("status") == "Active"
    )

    completed = sum(
        1
        for goal in goals
        if goal.get("status") == "Completed"
    )

    return {
        "total": total,
        "active": active,
        "completed": completed,
    }


def study_plan_summary(
    study_plan_data,
    completed_ids,
):
    if not study_plan_data:
        return {
            "exists": False,
            "tasks": 0,
            "completed": 0,
            "progress": 0,
        }

    tasks = (
        study_plan_data.get("tasks", [])
        if isinstance(study_plan_data, dict)
        else []
    )

    completed_ids = completed_ids or []

    completed = sum(
        1
        for task in tasks
        if task.get("id") in completed_ids
    )

    progress = (
        round(completed / len(tasks) * 100)
        if tasks
        else 0
    )

    return {
        "exists": True,
        "tasks": len(tasks),
        "completed": completed,
        "progress": progress,
    }


def quiz_summary(quiz_result):
    if not quiz_result:
        return None

    return {
        "subject": quiz_result.get("subject", ""),
        "correct": quiz_result.get("correct", 0),
        "total": quiz_result.get("total", 0),
        "percentage": quiz_result.get("percentage", 0),
        "level": quiz_result.get("level", ""),
    }


def aptitude_summary(aptitude_result):
    if not aptitude_result:
        return None

    return {
        "category": aptitude_result.get("category", ""),
        "correct": aptitude_result.get("correct", 0),
        "total": aptitude_result.get("total", 0),
        "percentage": aptitude_result.get("percentage", 0),
    }


def build_report(
    profile,
    interest_results=None,
    selected_career_area=None,
    quiz_result=None,
    aptitude_result=None,
    goals=None,
    study_plan_data=None,
    study_completed_ids=None,
):
    profile = profile or {}

    return {
        "generated_at": datetime.now().strftime(
            "%d %B %Y, %I:%M %p"
        ),
        "profile": profile,
        "profile_completion": profile_completion(
            profile
        ),
        "top_interest": get_top_interest(
            interest_results
        ),
        "career_direction": (
            selected_career_area
            or profile.get("dream_career")
            or "Still exploring"
        ),
        "quiz": quiz_summary(
            quiz_result
        ),
        "aptitude": aptitude_summary(
            aptitude_result
        ),
        "goals": goal_summary(
            goals
        ),
        "study_plan": study_plan_summary(
            study_plan_data,
            study_completed_ids,
        ),
    }


def calculate_student_score(report):
    """
    Student Development Score.
    This is a progress indicator, not an admission or career prediction score.
    """

    profile_score = report.get(
        "profile_completion",
        0,
    )

    interest_score = (
        100
        if report.get("top_interest")
        else 0
    )

    quiz = report.get("quiz")
    quiz_score = (
        quiz.get("percentage", 0)
        if quiz
        else 0
    )

    aptitude = report.get("aptitude")
    aptitude_score = (
        aptitude.get("percentage", 0)
        if aptitude
        else 0
    )

    goals = report.get("goals", {})
    goal_score = 0

    if goals.get("total", 0):
        goal_score = min(
            100,
            30
            + goals.get("active", 0) * 10
            + goals.get("completed", 0) * 30,
        )

    study = report.get("study_plan", {})
    study_score = (
        study.get("progress", 0)
        if study.get("exists")
        else 0
    )

    components = [
        profile_score,
        interest_score,
        quiz_score,
        aptitude_score,
        goal_score,
        study_score,
    ]

    return round(
        sum(components)
        / len(components)
    )


def score_label(score):
    if score >= 85:
        return "Excellent Progress"
    if score >= 70:
        return "Strong Progress"
    if score >= 55:
        return "Good Progress"
    if score >= 40:
        return "Developing"
    return "Getting Started"


def build_strengths(report):
    strengths = []

    profile = report.get("profile", {})
    quiz = report.get("quiz")
    aptitude = report.get("aptitude")
    study = report.get("study_plan", {})
    goals = report.get("goals", {})

    if report.get("profile_completion", 0) >= 80:
        strengths.append(
            "Your student profile is well completed."
        )

    if quiz and quiz.get("percentage", 0) >= 70:
        strengths.append(
            f"Strong recent performance in {quiz.get('subject')}."
        )

    if aptitude and aptitude.get("percentage", 0) >= 70:
        strengths.append(
            f"Good aptitude performance in {aptitude.get('category')}."
        )

    if study.get("progress", 0) >= 70:
        strengths.append(
            "You are completing most planned study blocks."
        )

    if goals.get("completed", 0) > 0:
        strengths.append(
            "You have successfully completed one or more tracked goals."
        )

    if report.get("top_interest"):
        strengths.append(
            f"Your strongest recorded interest area is {report['top_interest'].get('area')}."
        )

    if not strengths:
        strengths.append(
            "You have started building your TalentSphere learning profile."
        )

    return strengths


def build_improvement_areas(report):
    areas = []

    if report.get("profile_completion", 0) < 80:
        areas.append(
            "Complete the remaining School Profile fields."
        )

    if not report.get("top_interest"):
        areas.append(
            "Complete the Interest Assessment."
        )

    quiz = report.get("quiz")

    if not quiz:
        areas.append(
            "Take at least one Subject Quiz."
        )
    elif quiz.get("percentage", 0) < 60:
        areas.append(
            f"Revise {quiz.get('subject')} and retake the quiz."
        )

    aptitude = report.get("aptitude")

    if not aptitude:
        areas.append(
            "Complete one Aptitude Practice category."
        )
    elif aptitude.get("percentage", 0) < 60:
        areas.append(
            f"Practise more {aptitude.get('category')} questions."
        )

    goals = report.get("goals", {})

    if goals.get("total", 0) == 0:
        areas.append(
            "Create at least one academic or career goal."
        )

    study = report.get("study_plan", {})

    if not study.get("exists"):
        areas.append(
            "Generate a weekly Study Planner."
        )
    elif study.get("progress", 0) < 60:
        areas.append(
            "Improve Study Planner completion."
        )

    if not areas:
        areas.append(
            "Continue your current routine and increase difficulty gradually."
        )

    return areas


def build_action_plan(report):
    actions = []

    if not report.get("top_interest"):
        actions.append(
            "Complete the Interest Assessment and review your top three areas."
        )

    if report.get("career_direction") == "Still exploring":
        actions.append(
            "Use Career Explorer to compare at least two career areas."
        )

    quiz = report.get("quiz")

    if quiz and quiz.get("percentage", 0) < 70:
        actions.append(
            f"Revise {quiz.get('subject')} for one week and retake the Subject Quiz."
        )
    elif not quiz:
        actions.append(
            "Complete one 25-question Subject Quiz."
        )

    aptitude = report.get("aptitude")

    if aptitude and aptitude.get("percentage", 0) < 70:
        actions.append(
            f"Practise 10-15 {aptitude.get('category')} questions daily."
        )
    elif not aptitude:
        actions.append(
            "Complete one Aptitude Practice category."
        )

    goals = report.get("goals", {})

    if goals.get("active", 0) > 0:
        actions.append(
            "Complete the next milestone from Goal Tracker."
        )
    elif goals.get("total", 0) == 0:
        actions.append(
            "Create one academic goal with 3-5 milestones."
        )

    study = report.get("study_plan", {})

    if not study.get("exists"):
        actions.append(
            "Create a weekly Study Planner."
        )
    elif study.get("progress", 0) < 70:
        actions.append(
            "Complete the next pending study block."
        )

    if len(actions) < 5:
        actions.append(
            "Ask the AI Study Mentor for your next personalised study step."
        )

    return actions[:5]
