QUESTIONS = [
    {
        "text": "I can delegate work clearly based on team members' strengths.",
        "area": "Delegation",
    },
    {
        "text": "I give useful feedback that helps teammates improve.",
        "area": "Coaching",
    },
    {
        "text": "I handle disagreement without making it personal.",
        "area": "Conflict Management",
    },
    {
        "text": "I communicate technical decisions to non-technical stakeholders.",
        "area": "Stakeholder Communication",
    },
    {
        "text": "I make decisions even when information is incomplete.",
        "area": "Decision Making",
    },
    {
        "text": "I take responsibility when the team misses an outcome.",
        "area": "Ownership",
    },
    {
        "text": "I can mentor a junior teammate with a structured growth plan.",
        "area": "Mentoring",
    },
    {
        "text": "I prioritize work based on impact, urgency and dependencies.",
        "area": "Execution",
    },
    {
        "text": "I can align a team around a clear technical or business goal.",
        "area": "Alignment",
    },
    {
        "text": "I communicate risks early and propose alternatives.",
        "area": "Risk Management",
    },
]


def evaluate(responses):
    if not responses:
        return {
            "score": 0,
            "areas": {},
            "strengths": [],
            "improvements": [],
        }

    area_scores = {}
    for item, value in zip(QUESTIONS, responses):
        area_scores[item["area"]] = round((value - 1) / 4 * 100)

    score = round(sum(area_scores.values()) / len(area_scores))

    strengths = [
        area
        for area, value in area_scores.items()
        if value >= 75
    ]

    improvements = [
        area
        for area, value in area_scores.items()
        if value < 60
    ]

    return {
        "score": score,
        "areas": area_scores,
        "strengths": strengths,
        "improvements": improvements,
    }
