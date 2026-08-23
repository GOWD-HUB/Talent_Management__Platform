# ==========================================================
# HIGH SCHOOL RECOMMENDATION SERVICE
# ==========================================================

CAREER_TO_AREA = {
    "doctor": "Science & Medicine",
    "medicine": "Science & Medicine",
    "pharmacist": "Science & Medicine",
    "veterinarian": "Science & Medicine",

    "software": "Engineering & Technology",
    "engineer": "Engineering & Technology",
    "robot": "Engineering & Technology",
    "computer": "Engineering & Technology",
    "technology": "Engineering & Technology",

    "business": "Business & Commerce",
    "entrepreneur": "Business & Commerce",
    "accountant": "Business & Commerce",
    "finance": "Business & Commerce",

    "designer": "Arts & Design",
    "artist": "Arts & Design",
    "architect": "Arts & Design",
    "animation": "Arts & Design",

    "lawyer": "Law & Public Services",
    "law": "Law & Public Services",
    "civil service": "Law & Public Services",

    "journalist": "Media & Communication",
    "media": "Media & Communication",
    "writer": "Media & Communication",
    "content creator": "Media & Communication",

    "sport": "Sports & Fitness",
    "cricket": "Sports & Fitness",
    "athlete": "Sports & Fitness",

    "agriculture": "Agriculture & Environment",
    "environment": "Agriculture & Environment",
    "farming": "Agriculture & Environment",
}


AREA_GUIDANCE = {
    "Science & Medicine": {
        "icon": "🧪",
        "subjects": ["Biology", "Chemistry", "Physics"],
        "skills": ["Observation", "Scientific thinking", "Communication"],
        "next_action": "Strengthen Biology and Science fundamentals and explore health-related careers.",
    },
    "Engineering & Technology": {
        "icon": "⚙️",
        "subjects": ["Mathematics", "Physics", "Computer Science"],
        "skills": ["Logical thinking", "Problem solving", "Basic coding"],
        "next_action": "Practise Mathematics and start a small coding, electronics or robotics project.",
    },
    "Business & Commerce": {
        "icon": "💼",
        "subjects": ["Mathematics", "Economics", "Business Studies"],
        "skills": ["Communication", "Leadership", "Financial literacy"],
        "next_action": "Learn budgeting, basic business concepts and try a small entrepreneurship activity.",
    },
    "Arts & Design": {
        "icon": "🎨",
        "subjects": ["Art", "English", "Computer Applications"],
        "skills": ["Creativity", "Visual thinking", "Storytelling"],
        "next_action": "Create small design projects and start building a creative portfolio.",
    },
    "Law & Public Services": {
        "icon": "⚖️",
        "subjects": ["Social Science", "English", "History"],
        "skills": ["Reasoning", "Public speaking", "General awareness"],
        "next_action": "Read current affairs and practise debates, essays and structured arguments.",
    },
    "Media & Communication": {
        "icon": "🎙️",
        "subjects": ["English", "Social Science", "Computer Applications"],
        "skills": ["Writing", "Speaking", "Presentation"],
        "next_action": "Practise writing, presentations and small media or storytelling projects.",
    },
    "Sports & Fitness": {
        "icon": "🏏",
        "subjects": ["Physical Education", "Biology"],
        "skills": ["Discipline", "Teamwork", "Fitness"],
        "next_action": "Follow a regular age-appropriate sports routine and track your performance.",
    },
    "Agriculture & Environment": {
        "icon": "🌱",
        "subjects": ["Biology", "Geography", "Chemistry"],
        "skills": ["Observation", "Research", "Environmental awareness"],
        "next_action": "Try a gardening, sustainability or environmental observation project.",
    },
}


def infer_area_from_dream_career(dream_career):
    text = str(dream_career or "").lower()

    for keyword, area in CAREER_TO_AREA.items():
        if keyword in text:
            return area

    return None


def get_interest_top_area(interest_results):
    if not interest_results:
        return None

    try:
        return interest_results[0][0]
    except (IndexError, TypeError):
        return None


def build_recommendations(profile, interest_results=None, selected_area=None, quiz_result=None):
    recommendations = []

    dream_area = infer_area_from_dream_career(
        profile.get("dream_career")
    )

    interest_area = get_interest_top_area(
        interest_results
    )

    primary_area = (
        selected_area
        or interest_area
        or dream_area
    )

    if primary_area and primary_area in AREA_GUIDANCE:
        info = AREA_GUIDANCE[primary_area]

        recommendations.append({
            "type": "career",
            "icon": info["icon"],
            "title": f"Explore {primary_area}",
            "description": (
                "This is currently your strongest direction based on "
                "your saved career choice or assessment activity."
            ),
            "action": info["next_action"],
        })

        recommendations.append({
            "type": "subjects",
            "icon": "📚",
            "title": "Subjects to Prioritise",
            "description": ", ".join(info["subjects"]),
            "action": "Give these subjects regular study time and track your progress.",
        })

        recommendations.append({
            "type": "skills",
            "icon": "🛣️",
            "title": "Skills to Build",
            "description": ", ".join(info["skills"]),
            "action": "Use Skills Roadmap and complete the beginner-level items first.",
        })
    else:
        recommendations.append({
            "type": "profile",
            "icon": "👤",
            "title": "Complete Your Career Profile",
            "description": (
                "Add favourite subjects, interests and a possible dream career "
                "to receive more personalised recommendations."
            ),
            "action": "Open School Profile and complete the missing fields.",
        })

    if not interest_results:
        recommendations.append({
            "type": "assessment",
            "icon": "📊",
            "title": "Take the Interest Assessment",
            "description": (
                "Your interests help TalentSphere identify suitable career areas."
            ),
            "action": "Complete the assessment to discover your top three interest areas.",
        })

    if quiz_result:
        percentage = quiz_result.get("percentage", 0)
        subject = quiz_result.get("subject", "your latest subject")

        if percentage < 60:
            recommendations.append({
                "type": "quiz",
                "icon": "📝",
                "title": f"Revise {subject}",
                "description": (
                    f"Your latest score is {percentage}%. "
                    "Revision will strengthen your subject foundation."
                ),
                "action": "Review incorrect answers and retake the quiz after revision.",
            })
        else:
            recommendations.append({
                "type": "quiz",
                "icon": "✅",
                "title": f"Keep Progressing in {subject}",
                "description": (
                    f"Your latest score is {percentage}%. "
                    "Your current foundation is developing well."
                ),
                "action": "Try another subject or retake later to improve further.",
            })
    else:
        recommendations.append({
            "type": "quiz",
            "icon": "📝",
            "title": "Check Your Subject Strength",
            "description": (
                "Subject Quiz can identify areas where you are already strong "
                "and topics that need more practice."
            ),
            "action": "Take at least one 25-question Subject Quiz.",
        })

    return recommendations
