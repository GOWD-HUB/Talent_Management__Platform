# ==========================================================
# TALENTSPHERE - HIGH SCHOOL AI STUDY MENTOR SERVICE
# No external API key required.
# ==========================================================

SUBJECT_KEYWORDS = {
    "Mathematics": ["math", "maths", "mathematics", "algebra", "geometry", "trigonometry"],
    "Physics": ["physics", "force", "motion", "energy", "electricity", "light"],
    "Chemistry": ["chemistry", "chemical", "acid", "base", "atom", "reaction"],
    "Biology": ["biology", "cell", "plant", "animal", "genetics", "health"],
    "English": ["english", "grammar", "vocabulary", "speaking", "writing", "essay"],
    "Computer Science": ["computer", "coding", "programming", "python", "software", "algorithm"],
    "Social Science": ["social science", "history", "civics", "geography", "economics"],
    "General Knowledge": ["gk", "general knowledge", "current affairs"],
}


def _normalise(value):
    return str(value or "").strip().lower()


def detect_subject(message):
    text = _normalise(message)

    for subject, keywords in SUBJECT_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return subject

    return None


def get_top_interest_area(interest_results):
    if not interest_results:
        return None

    try:
        first = interest_results[0]

        if isinstance(first, dict):
            return first.get("area") or first.get("name") or first.get("category")

        if isinstance(first, (list, tuple)):
            return first[0]

    except Exception:
        pass

    return None


def build_student_context(
    profile=None,
    interest_results=None,
    selected_career_area=None,
    quiz_result=None,
    goals=None,
):
    profile = profile or {}
    goals = goals or []

    return {
        "current_class": profile.get("current_class") or "",
        "favourite_subjects": profile.get("favourite_subjects") or "",
        "interests": profile.get("interests") or "",
        "dream_career": profile.get("dream_career") or "",
        "academic_goal": profile.get("academic_goal") or "",
        "career_area": (
            selected_career_area
            or get_top_interest_area(interest_results)
            or ""
        ),
        "quiz_result": quiz_result or {},
        "active_goals": [
            goal
            for goal in goals
            if goal.get("status") == "Active"
        ],
    }


def generate_mentor_response(message, context):
    text = _normalise(message)

    if not text:
        return "Ask me a study, stream, career, quiz or goal question."

    subject = detect_subject(message)

    if subject and any(word in text for word in ["improve", "study", "weak", "help", "score", "practice", "learn"]):
        quiz = context.get("quiz_result") or {}

        response = (
            f"For **{subject}**, use this routine:\n\n"
            "1. Revise one concept for 20-30 minutes.\n"
            "2. Solve 10-15 practice questions.\n"
            "3. Write down every mistake.\n"
            "4. Review the mistakes the next day.\n"
            "5. Retake the Subject Quiz after practice."
        )

        if quiz.get("subject") == subject:
            response += (
                f"\n\nYour latest {subject} score is "
                f"**{quiz.get('percentage', 0)}%**."
            )

        return response

    if any(phrase in text for phrase in ["stream", "after class 10", "after 10", "after 10th", "mpc", "pcm", "pcb"]):
        career = _normalise(
            context.get("career_area")
            or context.get("dream_career")
        )

        if any(word in career for word in ["engineering", "technology", "software", "computer"]):
            return (
                "Your current direction points toward **Engineering & Technology**. "
                "After Class 10, a Mathematics-based Science stream such as MPC/PCM "
                "is commonly relevant. Focus on Mathematics, Physics and Computer Science."
            )

        if any(word in career for word in ["medicine", "medical", "doctor", "biology"]):
            return (
                "Your current direction points toward **Science & Medicine**. "
                "After Class 10, Science with Biology/PCB is commonly relevant. "
                "Focus on Biology, Chemistry and Physics."
            )

        if any(word in career for word in ["business", "commerce", "finance"]):
            return (
                "Your current direction points toward **Business & Commerce**. "
                "Commerce is a common stream after Class 10."
            )

        return (
            "Choose a stream by comparing the subjects you enjoy, your marks, "
            "your career interests, and course eligibility after Class 12. "
            "Use Career Explorer and Interest Assessment before deciding."
        )

    if any(word in text for word in ["career", "future", "profession", "job", "suit me"]):
        area = context.get("career_area") or context.get("dream_career")

        if area:
            return (
                f"Your current career direction is **{area}**. "
                "Use Career Explorer to compare careers in this area, "
                "then open Skills Roadmap to see which skills you can start building."
            )

        return (
            "Start with the Interest Assessment, then explore your top two career areas."
        )

    if any(word in text for word in ["goal", "deadline", "milestone", "target"]):
        goals = context.get("active_goals") or []

        if not goals:
            return (
                "Create one clear goal in Goal Tracker and break it into small milestones."
            )

        first = goals[0]

        return (
            f"Your active goal is **{first.get('title', 'Goal')}**. "
            "Focus on one milestone at a time and review the deadline every week."
        )

    if any(phrase in text for phrase in ["today", "what should i study", "study plan", "schedule", "timetable"]):
        quiz = context.get("quiz_result") or {}

        if quiz and quiz.get("percentage", 100) < 60:
            return (
                f"Today, prioritise **{quiz.get('subject', 'your weak subject')}** "
                f"because your latest score is **{quiz.get('percentage', 0)}%**.\n\n"
                "- 30 min concept revision\n"
                "- 30 min practice\n"
                "- 15 min mistake review"
            )

        return (
            "For today:\n"
            "- 45 min on your weakest subject\n"
            "- 30 min on a favourite subject\n"
            "- 20 min revision\n"
            "- 15 min quiz practice"
        )

    if any(word in text for word in ["quiz", "marks", "test", "score"]):
        quiz = context.get("quiz_result") or {}

        if not quiz:
            return (
                "Take a Subject Quiz first. Then I can use the result to recommend what to revise."
            )

        return (
            f"Your latest quiz is **{quiz.get('subject', 'Subject')}** with "
            f"**{quiz.get('percentage', 0)}%**. Review incorrect answers, "
            "revise those concepts, and retake the quiz."
        )

    return (
        "I can help with subjects, stream after Class 10, today's study plan, "
        "career guidance, quiz performance and goals. "
        "Try asking: **How can I improve Mathematics?**"
    )
