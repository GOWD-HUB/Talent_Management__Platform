# ==========================================================
# HIGH SCHOOL INTEREST ASSESSMENT
# ==========================================================

QUESTIONS = [
    {
        "id": 1,
        "text": "I enjoy learning how the human body, plants or animals work.",
        "area": "Science & Medicine",
    },
    {
        "id": 2,
        "text": "I enjoy experiments, science activities and discovering why things happen.",
        "area": "Science & Medicine",
    },

    {
        "id": 3,
        "text": "I enjoy computers, coding, robots or understanding how technology works.",
        "area": "Engineering & Technology",
    },
    {
        "id": 4,
        "text": "I like solving Mathematics or logical problems.",
        "area": "Engineering & Technology",
    },

    {
        "id": 5,
        "text": "I am interested in business, money, selling products or starting something of my own.",
        "area": "Business & Commerce",
    },
    {
        "id": 6,
        "text": "I enjoy planning, organising activities or taking leadership responsibilities.",
        "area": "Business & Commerce",
    },

    {
        "id": 7,
        "text": "I enjoy drawing, designing, creating visuals or making things look attractive.",
        "area": "Arts & Design",
    },
    {
        "id": 8,
        "text": "I enjoy imagination, storytelling, animation, fashion or creative activities.",
        "area": "Arts & Design",
    },

    {
        "id": 9,
        "text": "I enjoy debates, discussions about society, laws, history or government.",
        "area": "Law & Public Services",
    },
    {
        "id": 10,
        "text": "I like helping people solve problems and speaking up for what is fair.",
        "area": "Law & Public Services",
    },

    {
        "id": 11,
        "text": "I enjoy speaking, writing, presenting or communicating ideas to others.",
        "area": "Media & Communication",
    },
    {
        "id": 12,
        "text": "I enjoy creating videos, writing stories, reporting events or sharing information.",
        "area": "Media & Communication",
    },

    {
        "id": 13,
        "text": "I enjoy sports, exercise, fitness or physical activities.",
        "area": "Sports & Fitness",
    },
    {
        "id": 14,
        "text": "I enjoy teamwork, competition and improving physical performance.",
        "area": "Sports & Fitness",
    },

    {
        "id": 15,
        "text": "I enjoy nature, farming, plants, animals or protecting the environment.",
        "area": "Agriculture & Environment",
    },
    {
        "id": 16,
        "text": "I am interested in how food is grown and how we can protect natural resources.",
        "area": "Agriculture & Environment",
    },
]


ANSWER_OPTIONS = {
    "Not like me": 1,
    "A little like me": 2,
    "Mostly like me": 3,
    "Very much like me": 4,
}


AREA_INFO = {
    "Science & Medicine": {
        "icon": "🧪",
        "description": "You may enjoy science, biology, health, experiments and understanding living systems.",
    },
    "Engineering & Technology": {
        "icon": "⚙️",
        "description": "You may enjoy Mathematics, computers, coding, machines, robotics and logical problem solving.",
    },
    "Business & Commerce": {
        "icon": "💼",
        "description": "You may enjoy business, finance, leadership, economics, marketing and entrepreneurship.",
    },
    "Arts & Design": {
        "icon": "🎨",
        "description": "You may enjoy creativity, drawing, visual design, storytelling and imagination.",
    },
    "Law & Public Services": {
        "icon": "⚖️",
        "description": "You may enjoy society, justice, debate, government, leadership and public service.",
    },
    "Media & Communication": {
        "icon": "🎙️",
        "description": "You may enjoy speaking, writing, presenting, storytelling and sharing ideas.",
    },
    "Sports & Fitness": {
        "icon": "🏏",
        "description": "You may enjoy sports, fitness, teamwork, discipline and physical activity.",
    },
    "Agriculture & Environment": {
        "icon": "🌱",
        "description": "You may enjoy nature, farming, plants, animals, sustainability and environmental topics.",
    },
}


# ==========================================================
# CALCULATE SCORES
# ==========================================================

def calculate_interest_scores(answers):

    raw_scores = {
        area: 0
        for area in AREA_INFO.keys()
    }

    max_scores = {
        area: 0
        for area in AREA_INFO.keys()
    }

    for question in QUESTIONS:

        area = question["area"]

        answer_value = answers.get(
            question["id"],
            0,
        )

        raw_scores[area] += answer_value

        max_scores[area] += 4

    percentages = {}

    for area in raw_scores:

        max_score = max_scores[area]

        if max_score == 0:
            percentages[area] = 0
        else:
            percentages[area] = round(
                raw_scores[area]
                / max_score
                * 100
            )

    ranked = sorted(
        percentages.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    return ranked


# ==========================================================
# TOP AREAS
# ==========================================================

def get_top_interest_areas(
    ranked_scores,
    limit=3,
):

    return ranked_scores[:limit]