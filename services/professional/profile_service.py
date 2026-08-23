def safe_float(value, default=0.0):
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return default


def split_items(value):
    if not value:
        return []

    if isinstance(value, (list, tuple, set)):
        raw = list(value)
    else:
        raw = (
            str(value)
            .replace("\n", ",")
            .replace(";", ",")
            .split(",")
        )

    result = []
    seen = set()

    for item in raw:
        item = str(item).strip()

        if not item:
            continue

        key = item.lower()

        if key not in seen:
            seen.add(key)
            result.append(item)

    return result


def profile_completion(profile):
    fields = [
        "current_role",
        "industry",
        "experience_years",
        "tech_stack",
        "technical_level",
        "leadership_exposure",
        "communication_level",
        "target_role",
        "career_goal",
        "certifications",
        "achievements",
        "linkedin_url",
    ]

    completed = 0

    for field in fields:
        value = profile.get(field)

        if field == "experience_years":
            if safe_float(value) > 0:
                completed += 1
        elif str(value or "").strip():
            completed += 1

    return round(completed / len(fields) * 100) if fields else 0
