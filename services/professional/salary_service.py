from .profile_service import safe_float


def salary_gap(profile):
    current = safe_float(profile.get("current_salary_lpa"))
    target = safe_float(profile.get("target_salary_lpa"))

    absolute = max(0.0, target - current)

    percent = (
        round(absolute / current * 100)
        if current > 0
        else 0
    )

    return {
        "current": current,
        "target": target,
        "gap": absolute,
        "growth_percent": percent,
    }


def ninety_day_salary_plan(profile):
    target_role = (
        str(profile.get("target_role") or "").strip()
        or "your target role"
    )

    return [
        {
            "period": "Days 1–30",
            "title": "Market Positioning",
            "actions": [
                f"Benchmark skills required for {target_role}.",
                "Identify 2–3 measurable achievements for your resume.",
                "Close one high-priority technical gap.",
            ],
        },
        {
            "period": "Days 31–60",
            "title": "Evidence & Visibility",
            "actions": [
                "Build or improve one portfolio-quality project.",
                "Strengthen GitHub/LinkedIn evidence.",
                "Practice role-specific interviews and salary conversations.",
            ],
        },
        {
            "period": "Days 61–90",
            "title": "Opportunity Conversion",
            "actions": [
                "Apply to carefully matched roles.",
                "Track interviews and feedback.",
                "Negotiate using impact, market fit and role scope.",
            ],
        },
    ]
