from .profile_service import safe_float, split_items


LEVEL_MAP = {
    "Beginner": 35,
    "Intermediate": 60,
    "Advanced": 82,
    "Expert": 95,
    "None": 20,
    "Limited": 40,
    "Moderate": 65,
    "High": 85,
    "Excellent": 95,
    "Good": 75,
    "Average": 55,
    "Needs Improvement": 35,
}


def _level(value, fallback=45):
    return LEVEL_MAP.get(str(value or "").strip(), fallback)


def promotion_readiness(profile):
    technical = _level(profile.get("technical_level"), 45)
    leadership = _level(profile.get("leadership_exposure"), 35)
    communication = _level(profile.get("communication_level"), 50)

    experience = safe_float(profile.get("experience_years"))
    experience_score = min(100, round(experience / 8 * 100))

    achievements = len(split_items(profile.get("achievements")))
    achievement_score = min(100, achievements * 18)

    certifications = len(split_items(profile.get("certifications")))
    certification_score = min(100, certifications * 15)

    score = round(
        technical * 0.28
        + leadership * 0.22
        + communication * 0.18
        + experience_score * 0.15
        + achievement_score * 0.10
        + certification_score * 0.07
    )

    score = max(0, min(100, score))

    factors = {
        "Technical": technical,
        "Leadership": leadership,
        "Communication": communication,
        "Experience": experience_score,
        "Impact Evidence": achievement_score,
        "Certifications": certification_score,
    }

    gaps = [
        name
        for name, value in factors.items()
        if value < 65
    ]

    return {
        "score": score,
        "factors": factors,
        "gaps": gaps,
    }
