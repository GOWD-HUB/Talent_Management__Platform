# ==========================================================
# HIGH SCHOOL STUDY PLANNER SERVICE
# ==========================================================

DEFAULT_SUBJECTS = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "English",
    "Computer Science",
    "Social Science",
]

WEEK_DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def clean_subjects(subjects):
    """
    Convert comma-separated text or list input into a clean subject list.
    """

    if not subjects:
        return []

    if isinstance(subjects, str):
        items = subjects.split(",")
    else:
        items = list(subjects)

    result = []

    for item in items:
        value = str(item).strip()

        if value and value not in result:
            result.append(value)

    return result


def build_subject_pool(
    favourite_subjects=None,
    weak_subjects=None,
    extra_subjects=None,
):
    """
    Build one ordered subject pool.
    Weak subjects appear first so they receive more study priority.
    """

    weak = clean_subjects(weak_subjects)
    favourite = clean_subjects(favourite_subjects)
    extra = clean_subjects(extra_subjects)

    combined = []

    for subject in weak + favourite + extra:

        if subject not in combined:
            combined.append(subject)

    if not combined:
        combined = DEFAULT_SUBJECTS.copy()

    return combined


def allocate_minutes(
    subjects,
    total_minutes,
    weak_subjects=None,
):
    """
    Allocate more time to weak subjects.

    Weight:
    weak subject = 1.6
    normal subject = 1.0
    """

    if not subjects:
        return {}

    weak = set(clean_subjects(weak_subjects))

    weights = {
        subject: (1.6 if subject in weak else 1.0)
        for subject in subjects
    }

    total_weight = sum(weights.values())

    allocations = {}

    for subject in subjects:
        share = weights[subject] / total_weight
        minutes = round(total_minutes * share / 5) * 5

        allocations[subject] = max(minutes, 10)

    # Adjust total to be close to requested total.
    current_total = sum(allocations.values())

    if current_total != total_minutes:
        difference = total_minutes - current_total

        first_subject = subjects[0]
        allocations[first_subject] = max(
            10,
            allocations[first_subject] + difference,
        )

    return allocations


def create_daily_blocks(
    day,
    subjects,
    daily_minutes,
    weak_subjects=None,
):
    """
    Create study blocks for a single day.
    """

    if not subjects:
        return []

    # Keep a manageable number of subjects per day.
    max_subjects = 3

    selected = subjects[:max_subjects]

    allocations = allocate_minutes(
        selected,
        daily_minutes,
        weak_subjects=weak_subjects,
    )

    tasks = []

    for index, subject in enumerate(selected, start=1):

        minutes = allocations.get(subject, 30)

        tasks.append({
            "id": f"{day}_{index}_{subject}".replace(" ", "_"),
            "day": day,
            "subject": subject,
            "minutes": minutes,
            "task": f"Study {subject} for {minutes} minutes",
            "completed": False,
        })

    return tasks


def rotate_subjects(subjects, shift):
    """
    Rotate subjects so every day does not show the same first subjects.
    """

    if not subjects:
        return []

    shift = shift % len(subjects)

    return subjects[shift:] + subjects[:shift]


def generate_weekly_plan(
    study_days,
    daily_minutes,
    favourite_subjects=None,
    weak_subjects=None,
    extra_subjects=None,
):
    """
    Generate a weekly study plan.
    """

    subjects = build_subject_pool(
        favourite_subjects=favourite_subjects,
        weak_subjects=weak_subjects,
        extra_subjects=extra_subjects,
    )

    weak = clean_subjects(weak_subjects)

    plan = []

    for day_index, day in enumerate(study_days):

        rotated = rotate_subjects(
            subjects,
            day_index,
        )

        # Weak subjects are pulled forward.
        ordered = []

        for subject in weak:
            if subject in rotated and subject not in ordered:
                ordered.append(subject)

        for subject in rotated:
            if subject not in ordered:
                ordered.append(subject)

        tasks = create_daily_blocks(
            day=day,
            subjects=ordered,
            daily_minutes=daily_minutes,
            weak_subjects=weak,
        )

        plan.extend(tasks)

    return plan


def calculate_plan_progress(plan, completed_ids):
    """
    Return completion percentage for current study plan.
    """

    if not plan:
        return 0

    completed = sum(
        1
        for task in plan
        if task["id"] in completed_ids
    )

    return round(
        completed / len(plan) * 100
    )


def get_today_tasks(plan, day_name):
    return [
        task
        for task in plan
        if task["day"] == day_name
    ]


def get_next_pending_task(plan, completed_ids):
    for task in plan:
        if task["id"] not in completed_ids:
            return task

    return None
