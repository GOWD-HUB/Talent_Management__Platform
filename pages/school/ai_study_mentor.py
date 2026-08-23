import html as html_lib
import streamlit as st

from components.back_button import render_back_to_school_dashboard
from database.school_repository import get_school_profile
from database.goal_repository import get_goals


# ==========================================================
# HELPERS
# ==========================================================

def safe(value):
    return html_lib.escape(str(value or ""))


def normalise(value):
    return str(value or "").strip().lower()


def get_chat_key(user_id):
    return f"ai_study_mentor_chat_{user_id}"


def initialise_chat(user_id):
    key = get_chat_key(user_id)

    if key not in st.session_state:
        st.session_state[key] = [
            {
                "role": "assistant",
                "content": (
                    "Hi! 👋 I’m your TalentSphere Study Mentor. "
                    "Ask me about subjects, study planning, stream selection, "
                    "careers, quizzes or goals."
                ),
            }
        ]

    return key


# ==========================================================
# SUBJECT DETECTION
# ==========================================================

SUBJECT_KEYWORDS = {
    "Mathematics": [
        "math", "maths", "mathematics", "algebra",
        "geometry", "trigonometry", "percentage", "ratio"
    ],
    "Physics": [
        "physics", "force", "motion", "energy",
        "electricity", "light", "sound"
    ],
    "Chemistry": [
        "chemistry", "chemical", "acid", "base",
        "atom", "molecule", "reaction"
    ],
    "Biology": [
        "biology", "cell", "human body", "plant",
        "animal", "genetics", "health"
    ],
    "English": [
        "english", "grammar", "vocabulary", "speaking",
        "writing", "essay", "communication"
    ],
    "Computer Science": [
        "computer", "coding", "programming", "python",
        "software", "algorithm", "technology"
    ],
    "Social Science": [
        "social science", "history", "civics",
        "geography", "economics"
    ],
    "General Knowledge": [
        "gk", "general knowledge", "current affairs"
    ],
}


def detect_subject(message):
    text = normalise(message)

    for subject, keywords in SUBJECT_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return subject

    return None


# ==========================================================
# CONTEXT
# ==========================================================

def build_context(profile, goals):
    return {
        "current_class": profile.get("current_class") or "",
        "favourite_subjects": profile.get("favourite_subjects") or "",
        "interests": profile.get("interests") or "",
        "dream_career": profile.get("dream_career") or "",
        "academic_goal": profile.get("academic_goal") or "",
        "career_area": st.session_state.get("selected_career_area") or "",
        "quiz_result": st.session_state.get("subject_quiz_result") or {},
        "active_goals": [
            goal
            for goal in goals
            if goal.get("status") == "Active"
        ],
    }


# ==========================================================
# RESPONSE ENGINE
# ==========================================================

def generate_response(message, context):
    text = normalise(message)
    subject = detect_subject(message)
    quiz = context.get("quiz_result") or {}

    if not text:
        return "Ask me a study, stream, career, quiz or goal question."

    if subject and any(
        word in text
        for word in [
            "improve", "study", "weak",
            "help", "score", "practice", "learn"
        ]
    ):
        response = (
            f"For **{subject}**, follow this routine:\n\n"
            "1. Revise one concept for 20–30 minutes.\n"
            "2. Solve 10–15 practice questions.\n"
            "3. Write down every mistake.\n"
            "4. Review mistakes the next day.\n"
            "5. Retake the Subject Quiz after practice."
        )

        if quiz.get("subject") == subject:
            percentage = quiz.get("percentage", 0)
            response += (
                f"\n\nYour latest {subject} score is "
                f"**{percentage}%**."
            )

        return response

    if any(
        phrase in text
        for phrase in [
            "stream", "after class 10",
            "after 10", "after 10th",
            "mpc", "pcm", "pcb"
        ]
    ):
        career = normalise(
            context.get("career_area")
            or context.get("dream_career")
        )

        if any(
            word in career
            for word in [
                "engineering",
                "technology",
                "software",
                "computer"
            ]
        ):
            return (
                "Your current direction points toward **Engineering & Technology**. "
                "After Class 10, a Mathematics-based Science stream such as MPC/PCM "
                "is commonly relevant. Focus on Mathematics, Physics and Computer Science."
            )

        if any(
            word in career
            for word in [
                "medicine",
                "medical",
                "doctor",
                "biology"
            ]
        ):
            return (
                "Your current direction points toward **Science & Medicine**. "
                "After Class 10, Science with Biology/PCB is commonly relevant. "
                "Focus on Biology, Chemistry and Physics."
            )

        if any(
            word in career
            for word in [
                "business",
                "commerce",
                "finance"
            ]
        ):
            return (
                "Your current direction points toward **Business & Commerce**. "
                "Commerce is a common choice after Class 10. "
                "Mathematics, Economics, Accountancy and communication are useful foundations."
            )

        return (
            "Choose your stream by comparing subjects you enjoy, your marks, "
            "career interests and course eligibility after Class 12. "
            "Use Career Explorer and Interest Assessment before deciding."
        )

    if any(
        word in text
        for word in [
            "career",
            "future",
            "profession",
            "job",
            "suit me"
        ]
    ):
        area = (
            context.get("career_area")
            or context.get("dream_career")
        )

        if area:
            return (
                f"Your current career direction is **{area}**. "
                "Use Career Explorer to compare careers inside this area, "
                "then open Skills Roadmap to see which skills you can start building now."
            )

        return (
            "Start with the Interest Assessment, then explore your top two career areas."
        )

    if any(
        word in text
        for word in [
            "goal",
            "deadline",
            "milestone",
            "target"
        ]
    ):
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

    if any(
        phrase in text
        for phrase in [
            "today",
            "what should i study",
            "study plan",
            "schedule",
            "timetable"
        ]
    ):
        if quiz and quiz.get("percentage", 100) < 60:
            return (
                f"Today, prioritise **{quiz.get('subject', 'your weak subject')}** "
                f"because your latest score is **{quiz.get('percentage', 0)}%**.\n\n"
                "- 30 min concept revision\n"
                "- 30 min practice questions\n"
                "- 15 min mistake review\n"
                "- 10 min recap"
            )

        academic_goal = context.get("academic_goal")

        if academic_goal:
            return (
                f"Your academic goal is **{academic_goal}**. "
                "Today, complete one focused block for your weakest subject, "
                "one block for a favourite subject and one goal milestone."
            )

        return (
            "For today:\n"
            "- 45 min on your weakest subject\n"
            "- 30 min on a favourite subject\n"
            "- 20 min revision\n"
            "- 15 min quiz practice"
        )

    if any(
        word in text
        for word in [
            "quiz",
            "marks",
            "test",
            "score"
        ]
    ):
        if not quiz:
            return (
                "Take a Subject Quiz first. Then I can use the score "
                "to recommend what to revise next."
            )

        return (
            f"Your latest quiz is **{quiz.get('subject', 'Subject')}** with "
            f"**{quiz.get('percentage', 0)}%**. "
            "Review incorrect answers, revise those concepts and retake the quiz."
        )

    return (
        "I can help with subjects, stream after Class 10, today's study plan, "
        "career guidance, quiz performance and goals. "
        "Try asking: **How can I improve Mathematics?**"
    )


# ==========================================================
# PAGE THEME
# ==========================================================

def apply_page_theme():
    st.markdown(
        """
<style>
.mentor-hero {
    padding: 34px 38px;
    border-radius: 24px;
    background: linear-gradient(135deg,#EEF2FF,#F5F3FF);
    border: 1px solid #DDD6FE;
    box-shadow: 0 12px 34px rgba(15,23,42,.05);
    margin-bottom: 22px;
}
.mentor-eyebrow {
    color: #7C3AED !important;
    font-size: 10px !important;
    font-weight: 800;
    letter-spacing: 1.2px;
}
.mentor-title {
    color: #0F172A !important;
    font-size: 34px !important;
    font-weight: 850;
    margin-top: 7px;
}
.mentor-description {
    color: #64748B !important;
    font-size: 14px !important;
    line-height: 1.7;
    margin-top: 8px;
}
.mentor-context-grid {
    display: grid;
    grid-template-columns: repeat(4,minmax(0,1fr));
    gap: 14px;
    margin-bottom: 20px;
}
.mentor-context-card {
    padding: 17px;
    border-radius: 17px;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
}
.mentor-context-label {
    color: #94A3B8 !important;
    font-size: 9px !important;
    font-weight: 800;
    text-transform: uppercase;
}
.mentor-context-value {
    color: #0F172A !important;
    font-size: 13px !important;
    font-weight: 800;
    margin-top: 6px;
}
</style>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# QUICK PROMPT
# ==========================================================

def queue_prompt(prompt):
    st.session_state["mentor_pending_prompt"] = prompt
    st.rerun()


# ==========================================================
# RENDER
# ==========================================================

def render():
    apply_page_theme()


    st.markdown(
        """
        <style>
        [data-testid="stChatMessage"] {
            background: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 16px !important;
        }

        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] li,
        [data-testid="stChatMessage"] span {
            color: #0f172a !important;
        }

        [data-testid="stChatInput"] textarea,
        [data-testid="stChatInput"] input {
            color: #0f172a !important;
            -webkit-text-fill-color: #0f172a !important;
            background: #ffffff !important;
        }

        [data-testid="stChatInput"] textarea::placeholder,
        [data-testid="stChatInput"] input::placeholder {
            color: #64748b !important;
            opacity: 1 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


    render_back_to_school_dashboard(
        key="ai_mentor_dashboard_back",
    )

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.error("Unable to identify the logged-in student.")
        return

    try:
        profile = get_school_profile(user_id) or {}
    except Exception:
        profile = {}

    try:
        goals = get_goals(user_id) or []
    except Exception:
        goals = []

    context = build_context(
        profile,
        goals,
    )

    chat_key = initialise_chat(
        user_id
    )

    st.html(
        """
<div class="mentor-hero">
    <div class="mentor-eyebrow">
        PERSONALISED HIGH SCHOOL GUIDANCE
    </div>
    <div class="mentor-title">
        🤖 AI Study Mentor
    </div>
    <div class="mentor-description">
        Ask about school subjects, study planning, stream after Class 10,
        career direction, quiz performance and goals.
    </div>
</div>
"""
    )

    current_class = (
        profile.get("current_class")
        or "Not added"
    )

    direction = (
        st.session_state.get("selected_career_area")
        or profile.get("dream_career")
        or "Exploring"
    )

    quiz_result = (
        st.session_state.get("subject_quiz_result")
        or {}
    )

    quiz_text = (
        f'{quiz_result.get("subject", "Subject")} · '
        f'{quiz_result.get("percentage", 0)}%'
        if quiz_result
        else "No recent quiz"
    )

    active_goals = len(
        context.get("active_goals")
        or []
    )

    st.html(
        f"""
<div class="mentor-context-grid">
    <div class="mentor-context-card">
        <div class="mentor-context-label">Current Class</div>
        <div class="mentor-context-value">{safe(current_class)}</div>
    </div>

    <div class="mentor-context-card">
        <div class="mentor-context-label">Career Direction</div>
        <div class="mentor-context-value">{safe(direction)}</div>
    </div>

    <div class="mentor-context-card">
        <div class="mentor-context-label">Latest Quiz</div>
        <div class="mentor-context-value">{safe(quiz_text)}</div>
    </div>

    <div class="mentor-context-card">
        <div class="mentor-context-label">Active Goals</div>
        <div class="mentor-context-value">{active_goals}</div>
    </div>
</div>
"""
    )

    st.markdown("### ⚡ Quick Questions")

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button(
            "📚 Improve Mathematics",
            key="mentor_math",
            use_container_width=True,
        ):
            queue_prompt(
                "How can I improve in Mathematics?"
            )

    with c2:
        if st.button(
            "🎓 Stream After Class 10",
            key="mentor_stream",
            use_container_width=True,
        ):
            queue_prompt(
                "What stream should I choose after Class 10?"
            )

    with c3:
        if st.button(
            "📅 What Should I Study Today?",
            key="mentor_today",
            use_container_width=True,
        ):
            queue_prompt(
                "What should I study today?"
            )

    c4, c5, c6 = st.columns(3)

    with c4:
        if st.button(
            "🔍 Career Guidance",
            key="mentor_career",
            use_container_width=True,
        ):
            queue_prompt(
                "Which career area should I explore?"
            )

    with c5:
        if st.button(
            "📝 Quiz Advice",
            key="mentor_quiz",
            use_container_width=True,
        ):
            queue_prompt(
                "What should I do based on my latest quiz?"
            )

    with c6:
        if st.button(
            "🎯 Goal Guidance",
            key="mentor_goal",
            use_container_width=True,
        ):
            queue_prompt(
                "How can I make progress on my goals?"
            )

    st.divider()

    for message in st.session_state[chat_key]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    pending_prompt = st.session_state.pop(
        "mentor_pending_prompt",
        None,
    )

    typed_prompt = st.chat_input(
        "Ask your Study Mentor..."
    )

    prompt = pending_prompt or typed_prompt

    if prompt:
        st.session_state[chat_key].append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        response = generate_response(
            prompt,
            context,
        )

        st.session_state[chat_key].append(
            {
                "role": "assistant",
                "content": response,
            }
        )

        st.rerun()

    st.divider()

    b1, b2, b3, b4 = st.columns(4)

    with b1:
        if st.button(
            "🗑️ Clear Chat",
            key="mentor_clear",
            use_container_width=True,
        ):
            st.session_state.pop(
                chat_key,
                None,
            )
            st.rerun()

    with b2:
        if st.button(
            "📅 Study Planner",
            key="mentor_planner",
            use_container_width=True,
        ):
            st.session_state.school_navigation = "📅 Study Planner"
            st.rerun()

    with b3:
        if st.button(
            "📝 Subject Quiz",
            key="mentor_quiz_page",
            use_container_width=True,
        ):
            st.session_state.school_navigation = "📝 Subject Quiz"
            st.rerun()

    with b4:
        if st.button(
            "🎯 Goal Tracker",
            key="mentor_goal_page",
            use_container_width=True,
        ):
            st.session_state.school_navigation = "🎯 Goal Tracker"
            st.rerun()
