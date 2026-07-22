import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date


# ==========================================================
# SESSION INITIALIZATION
# ==========================================================

def initialize_student_session():

    defaults = {
        "school_profile": {},
        "student_goals": [],
        "daily_tasks": [
            {"task": "Read for 20 minutes", "completed": False},
            {"task": "Practice 5 aptitude questions", "completed": False},
            {"task": "Learn one coding concept", "completed": False},
            {"task": "Practice English speaking for 10 minutes", "completed": False},
        ],
        "mentor_messages": [],
        "career_quiz_result": None,
        "interest_result": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ==========================================================
# STUDENT PROFILE
# ==========================================================

def show_student_profile():

    st.title("👨‍🎓 School Student Profile")
    st.write("Complete your profile to receive personalized career guidance.")

    existing_profile = st.session_state.get("school_profile", {})

    with st.form("school_student_profile_form"):

        col1, col2 = st.columns(2)

        with col1:

            full_name = st.text_input(
                "Full Name *",
                value=existing_profile.get("full_name", "")
            )

            email = st.text_input(
                "Email *",
                value=existing_profile.get("email", "")
            )

            phone = st.text_input(
                "Phone Number",
                value=existing_profile.get("phone", "")
            )

            date_of_birth = st.date_input(
                "Date of Birth",
                value=existing_profile.get(
                    "date_of_birth",
                    date(2010, 1, 1)
                ),
                min_value=date(2000, 1, 1),
                max_value=date.today()
            )

            gender_options = [
                "Select",
                "Male",
                "Female",
                "Other",
                "Prefer not to say"
            ]

            saved_gender = existing_profile.get("gender", "Select")

            gender = st.selectbox(
                "Gender",
                gender_options,
                index=gender_options.index(saved_gender)
                if saved_gender in gender_options else 0
            )

        with col2:

            school_name = st.text_input(
                "School Name *",
                value=existing_profile.get("school_name", "")
            )

            class_options = [
                "6th Class",
                "7th Class",
                "8th Class",
                "9th Class",
                "10th Class",
                "11th Class",
                "12th Class"
            ]

            saved_class = existing_profile.get(
                "current_class",
                "10th Class"
            )

            current_class = st.selectbox(
                "Current Class *",
                class_options,
                index=class_options.index(saved_class)
                if saved_class in class_options else 4
            )

            board_options = [
                "State Board",
                "CBSE",
                "ICSE",
                "IB",
                "Other"
            ]

            saved_board = existing_profile.get(
                "board",
                "State Board"
            )

            board = st.selectbox(
                "Education Board",
                board_options,
                index=board_options.index(saved_board)
                if saved_board in board_options else 0
            )

            city = st.text_input(
                "City",
                value=existing_profile.get("city", "")
            )

            parent_name = st.text_input(
                "Parent/Guardian Name",
                value=existing_profile.get("parent_name", "")
            )

        st.markdown("### 📚 Academic Interests")

        subjects = st.multiselect(
            "Favourite Subjects *",
            [
                "Mathematics",
                "Physics",
                "Chemistry",
                "Biology",
                "Computer Science",
                "English",
                "Social Studies",
                "Commerce",
                "Economics",
                "Arts"
            ],
            default=existing_profile.get("subjects", [])
        )

        interests = st.multiselect(
            "Interests and Hobbies",
            [
                "Coding",
                "Robotics",
                "Science Experiments",
                "Reading",
                "Writing",
                "Drawing",
                "Music",
                "Sports",
                "Public Speaking",
                "Business",
                "Photography",
                "Social Service"
            ],
            default=existing_profile.get("interests", [])
        )

        skills = st.multiselect(
            "Current Skills",
            [
                "Basic Coding",
                "Problem Solving",
                "Communication",
                "Leadership",
                "Creativity",
                "Teamwork",
                "Mathematics",
                "Presentation",
                "Time Management",
                "Critical Thinking"
            ],
            default=existing_profile.get("skills", [])
        )

        career_goal = st.text_input(
            "Dream Career",
            value=existing_profile.get("career_goal", ""),
            placeholder="Example: Software Engineer, Doctor, Scientist"
        )

        achievements = st.text_area(
            "Achievements",
            value=existing_profile.get("achievements", ""),
            placeholder="Mention competitions, certificates or awards"
        )

        short_term_goal = st.text_area(
            "Short-Term Goal",
            value=existing_profile.get("short_term_goal", ""),
            placeholder="Example: Improve mathematics score to 90%"
        )

        submitted = st.form_submit_button(
            "💾 Save School Student Profile",
            use_container_width=True
        )

        if submitted:

            if not full_name.strip():
                st.error("Full name is required.")

            elif not email.strip():
                st.error("Email is required.")

            elif "@" not in email:
                st.error("Enter a valid email address.")

            elif not school_name.strip():
                st.error("School name is required.")

            elif not subjects:
                st.error("Select at least one favourite subject.")

            else:

                st.session_state.school_profile = {
                    "full_name": full_name.strip(),
                    "email": email.strip().lower(),
                    "phone": phone.strip(),
                    "date_of_birth": date_of_birth,
                    "gender": gender,
                    "school_name": school_name.strip(),
                    "current_class": current_class,
                    "board": board,
                    "city": city.strip(),
                    "parent_name": parent_name.strip(),
                    "subjects": subjects,
                    "interests": interests,
                    "skills": skills,
                    "career_goal": career_goal.strip(),
                    "achievements": achievements.strip(),
                    "short_term_goal": short_term_goal.strip()
                }

                st.success("✅ School student profile saved successfully!")

    display_saved_profile()


def display_saved_profile():

    profile = st.session_state.get("school_profile", {})

    if not profile:
        return

    st.divider()
    st.subheader("📋 Saved Profile")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Student", profile.get("full_name", "-"))
        st.write(f"**Class:** {profile.get('current_class', '-')}")
        st.write(f"**Board:** {profile.get('board', '-')}")

    with col2:
        st.metric("School", profile.get("school_name", "-"))
        st.write(f"**City:** {profile.get('city', '-')}")
        st.write(f"**Dream Career:** {profile.get('career_goal', '-')}")

    with col3:
        st.metric(
            "Selected Subjects",
            len(profile.get("subjects", []))
        )
        st.write(
            "**Subjects:** "
            + ", ".join(profile.get("subjects", []))
        )
        st.write(
            "**Skills:** "
            + ", ".join(profile.get("skills", []))
        )


# ==========================================================
# CAREER EXPLORER
# ==========================================================

def show_career_explorer():

    st.title("🔍 Career Explorer")
    st.write("Discover careers based on your favourite subject and interests.")

    career_data = {
        "Mathematics": [
            {
                "career": "Data Scientist",
                "description": "Uses data and mathematics to solve problems.",
                "skills": "Python, Statistics, Machine Learning"
            },
            {
                "career": "Engineer",
                "description": "Designs and builds systems and products.",
                "skills": "Mathematics, Physics, Problem Solving"
            },
            {
                "career": "Actuary",
                "description": "Uses mathematics to calculate financial risks.",
                "skills": "Statistics, Finance, Analytics"
            }
        ],
        "Physics": [
            {
                "career": "Aerospace Engineer",
                "description": "Designs aircraft, spacecraft and satellites.",
                "skills": "Physics, Mathematics, Engineering"
            },
            {
                "career": "Research Scientist",
                "description": "Studies scientific problems through experiments.",
                "skills": "Research, Analysis, Laboratory Skills"
            }
        ],
        "Chemistry": [
            {
                "career": "Chemical Engineer",
                "description": "Develops chemical processes and products.",
                "skills": "Chemistry, Mathematics, Safety"
            },
            {
                "career": "Pharmacist",
                "description": "Works with medicines and healthcare.",
                "skills": "Chemistry, Biology, Communication"
            }
        ],
        "Biology": [
            {
                "career": "Doctor",
                "description": "Diagnoses and treats health conditions.",
                "skills": "Biology, Communication, Decision Making"
            },
            {
                "career": "Biotechnologist",
                "description": "Uses living systems to develop useful products.",
                "skills": "Biology, Chemistry, Research"
            }
        ],
        "Computer Science": [
            {
                "career": "Software Engineer",
                "description": "Creates software applications and systems.",
                "skills": "Coding, DSA, Databases"
            },
            {
                "career": "AI Engineer",
                "description": "Builds intelligent systems using machine learning.",
                "skills": "Python, Machine Learning, Mathematics"
            },
            {
                "career": "Cybersecurity Analyst",
                "description": "Protects computer systems and information.",
                "skills": "Networking, Security, Linux"
            }
        ],
        "English": [
            {
                "career": "Content Writer",
                "description": "Creates articles, stories and digital content.",
                "skills": "Writing, Research, Creativity"
            },
            {
                "career": "Journalist",
                "description": "Researches and reports important information.",
                "skills": "Communication, Writing, Investigation"
            }
        ],
        "Commerce": [
            {
                "career": "Chartered Accountant",
                "description": "Manages accounting, taxation and auditing.",
                "skills": "Accounting, Finance, Mathematics"
            },
            {
                "career": "Business Analyst",
                "description": "Helps businesses improve their performance.",
                "skills": "Analytics, Communication, Business"
            }
        ],
        "Economics": [
            {
                "career": "Economist",
                "description": "Studies markets, money and economic behaviour.",
                "skills": "Economics, Statistics, Research"
            },
            {
                "career": "Financial Analyst",
                "description": "Evaluates investments and financial performance.",
                "skills": "Finance, Excel, Analytics"
            }
        ],
        "Arts": [
            {
                "career": "Graphic Designer",
                "description": "Creates visual designs for brands and media.",
                "skills": "Creativity, Design Tools, Communication"
            },
            {
                "career": "Animator",
                "description": "Creates animated characters and visual stories.",
                "skills": "Drawing, Animation, Storytelling"
            }
        ],
        "Social Studies": [
            {
                "career": "Civil Services Officer",
                "description": "Works in public administration and governance.",
                "skills": "General Knowledge, Leadership, Communication"
            },
            {
                "career": "Lawyer",
                "description": "Provides legal advice and represents clients.",
                "skills": "Reasoning, Communication, Law"
            }
        ]
    }

    subject = st.selectbox(
        "Choose your favourite subject",
        list(career_data.keys())
    )

    if st.button("Explore Careers", use_container_width=True):

        st.success(f"Recommended careers for {subject}")

        for item in career_data[subject]:

            with st.container(border=True):

                st.subheader(item["career"])
                st.write(item["description"])
                st.write(f"**Important skills:** {item['skills']}")


# ==========================================================
# AI CAREER QUIZ
# ==========================================================

def show_career_quiz():

    st.title("🧠 AI Career Quiz")
    st.write("Answer the questions to discover a suitable career area.")

    with st.form("career_quiz"):

        q1 = st.radio(
            "1. Which activity do you enjoy most?",
            [
                "Solving mathematical problems",
                "Helping people",
                "Creating designs",
                "Using computers",
                "Managing money"
            ]
        )

        q2 = st.radio(
            "2. Which school project would you choose?",
            [
                "Build a science model",
                "Create a mobile application",
                "Organize a social programme",
                "Design a poster",
                "Prepare a business plan"
            ]
        )

        q3 = st.radio(
            "3. What type of problem do you prefer?",
            [
                "Technical problem",
                "Health problem",
                "Creative problem",
                "Social problem",
                "Financial problem"
            ]
        )

        q4 = st.radio(
            "4. Which skill describes you best?",
            [
                "Logical thinking",
                "Communication",
                "Creativity",
                "Leadership",
                "Calculation"
            ]
        )

        quiz_submit = st.form_submit_button(
            "Submit Career Quiz",
            use_container_width=True
        )

    if quiz_submit:

        scores = {
            "Technology": 0,
            "Healthcare": 0,
            "Creative Arts": 0,
            "Public Service": 0,
            "Business": 0,
            "Science and Engineering": 0
        }

        answer_mapping = {
            "Solving mathematical problems": "Science and Engineering",
            "Helping people": "Healthcare",
            "Creating designs": "Creative Arts",
            "Using computers": "Technology",
            "Managing money": "Business",
            "Build a science model": "Science and Engineering",
            "Create a mobile application": "Technology",
            "Organize a social programme": "Public Service",
            "Design a poster": "Creative Arts",
            "Prepare a business plan": "Business",
            "Technical problem": "Technology",
            "Health problem": "Healthcare",
            "Creative problem": "Creative Arts",
            "Social problem": "Public Service",
            "Financial problem": "Business",
            "Logical thinking": "Technology",
            "Communication": "Public Service",
            "Creativity": "Creative Arts",
            "Leadership": "Business",
            "Calculation": "Science and Engineering"
        }

        for answer in [q1, q2, q3, q4]:
            category = answer_mapping.get(answer)
            if category:
                scores[category] += 1

        result = max(scores, key=scores.get)

        st.session_state.career_quiz_result = result

        st.success(f"🎯 Recommended career area: {result}")

        chart_data = pd.DataFrame({
            "Career Area": list(scores.keys()),
            "Score": list(scores.values())
        })

        fig = px.bar(
            chart_data,
            x="Career Area",
            y="Score",
            text="Score",
            title="Career Quiz Result"
        )

        st.plotly_chart(fig, use_container_width=True)


# ==========================================================
# INTEREST ASSESSMENT
# ==========================================================

def show_interest_assessment():

    st.title("📊 Interest Assessment")
    st.write("Rate each area from 1 to 10.")

    mathematics = st.slider("Mathematics", 1, 10, 5)
    science = st.slider("Science", 1, 10, 5)
    technology = st.slider("Technology", 1, 10, 5)
    creativity = st.slider("Creativity and Arts", 1, 10, 5)
    communication = st.slider("Communication", 1, 10, 5)
    business = st.slider("Business and Finance", 1, 10, 5)
    social_service = st.slider("Helping Society", 1, 10, 5)

    if st.button("Analyze My Interests", use_container_width=True):

        interest_scores = {
            "Mathematics": mathematics,
            "Science": science,
            "Technology": technology,
            "Creativity": creativity,
            "Communication": communication,
            "Business": business,
            "Social Service": social_service
        }

        strongest_interest = max(
            interest_scores,
            key=interest_scores.get
        )

        st.session_state.interest_result = strongest_interest

        st.success(
            f"Your strongest interest area is: {strongest_interest}"
        )

        data = pd.DataFrame({
            "Interest": list(interest_scores.keys()),
            "Score": list(interest_scores.values())
        })

        fig = px.bar(
            data,
            x="Interest",
            y="Score",
            text="Score",
            title="Your Interest Assessment"
        )

        fig.update_yaxes(range=[0, 10])

        st.plotly_chart(fig, use_container_width=True)


# ==========================================================
# FUTURE SKILLS ROADMAP
# ==========================================================

def show_future_skills_roadmap():

    st.title("🛣️ Future Skills Roadmap")

    roadmaps = {
        "Software Engineer": [
            "Learn computer fundamentals",
            "Learn Python programming",
            "Practice problem solving",
            "Learn HTML, CSS and JavaScript",
            "Study Data Structures and Algorithms",
            "Build small projects",
            "Learn Git and GitHub",
            "Prepare for coding interviews"
        ],
        "Doctor": [
            "Build strong Biology fundamentals",
            "Improve Chemistry knowledge",
            "Develop communication skills",
            "Prepare for NEET",
            "Practice previous examination papers",
            "Learn basic healthcare concepts",
            "Develop empathy and decision-making skills"
        ],
        "Data Scientist": [
            "Strengthen Mathematics",
            "Learn Python",
            "Study Statistics",
            "Learn NumPy and Pandas",
            "Study Machine Learning",
            "Learn data visualization",
            "Build data projects"
        ],
        "Civil Services Officer": [
            "Improve general knowledge",
            "Read newspapers daily",
            "Develop communication skills",
            "Study history and geography",
            "Improve writing skills",
            "Practice aptitude",
            "Develop leadership skills"
        ],
        "Graphic Designer": [
            "Learn design principles",
            "Practice drawing",
            "Learn Canva",
            "Learn Adobe Photoshop",
            "Study typography and colour theory",
            "Build a design portfolio",
            "Learn UI/UX basics"
        ],
        "Chartered Accountant": [
            "Build accounting fundamentals",
            "Improve mathematics",
            "Learn economics",
            "Learn taxation basics",
            "Develop analytical skills",
            "Practice financial calculations",
            "Prepare for CA Foundation"
        ]
    }

    career = st.selectbox(
        "Select your future career",
        list(roadmaps.keys())
    )

    st.subheader(f"{career} Roadmap")

    for number, skill in enumerate(roadmaps[career], start=1):

        progress = int(
            (number / len(roadmaps[career])) * 100
        )

        with st.container(border=True):
            st.write(f"### Step {number}")
            st.write(skill)
            st.progress(progress)


# ==========================================================
# DAILY LEARNING TASKS
# ==========================================================

def show_daily_learning_tasks():

    st.title("✅ Daily Learning Tasks")

    tasks = st.session_state.daily_tasks

    completed_count = 0

    for index, item in enumerate(tasks):

        completed = st.checkbox(
            item["task"],
            value=item["completed"],
            key=f"daily_task_{index}"
        )

        st.session_state.daily_tasks[index]["completed"] = completed

        if completed:
            completed_count += 1

    total_tasks = len(tasks)

    progress = (
        completed_count / total_tasks
        if total_tasks > 0 else 0
    )

    st.progress(progress)

    st.write(
        f"Completed {completed_count} out of {total_tasks} tasks"
    )

    new_task = st.text_input(
        "Add a new learning task"
    )

    if st.button("Add Task"):

        if new_task.strip():

            st.session_state.daily_tasks.append({
                "task": new_task.strip(),
                "completed": False
            })

            st.success("Task added successfully.")
            st.rerun()

        else:
            st.warning("Enter a task first.")

    if st.button("Reset Daily Tasks"):

        for item in st.session_state.daily_tasks:
            item["completed"] = False

        st.rerun()


# ==========================================================
# CODING BASICS
# ==========================================================

def show_coding_basics():

    st.title("💻 Coding Basics")

    lesson = st.selectbox(
        "Select a coding lesson",
        [
            "Introduction to Python",
            "Variables",
            "Input and Output",
            "Conditions",
            "Loops",
            "Functions"
        ]
    )

    lessons = {
        "Introduction to Python": {
            "explanation": (
                "Python is a simple programming language used for "
                "web development, AI, automation and data science."
            ),
            "code": 'print("Hello, World!")'
        },
        "Variables": {
            "explanation": (
                "Variables store values that can be used later."
            ),
            "code": (
                'student_name = "Thimme"\n'
                'student_class = 10\n'
                'print(student_name)\n'
                'print(student_class)'
            )
        },
        "Input and Output": {
            "explanation": (
                "The input function collects information from a user."
            ),
            "code": (
                'name = input("Enter your name: ")\n'
                'print("Welcome", name)'
            )
        },
        "Conditions": {
            "explanation": (
                "Conditions allow a program to make decisions."
            ),
            "code": (
                'marks = 80\n\n'
                'if marks >= 35:\n'
                '    print("Pass")\n'
                'else:\n'
                '    print("Fail")'
            )
        },
        "Loops": {
            "explanation": (
                "Loops repeat a block of code."
            ),
            "code": (
                'for number in range(1, 6):\n'
                '    print(number)'
            )
        },
        "Functions": {
            "explanation": (
                "Functions are reusable blocks of code."
            ),
            "code": (
                'def greet(name):\n'
                '    return "Hello " + name\n\n'
                'print(greet("Student"))'
            )
        }
    }

    selected_lesson = lessons[lesson]

    st.info(selected_lesson["explanation"])

    st.code(
        selected_lesson["code"],
        language="python"
    )

    st.subheader("Mini Practice")

    answer = st.text_input(
        "What keyword is used to create a function in Python?"
    )

    if st.button("Check Coding Answer"):

        if answer.strip().lower() == "def":
            st.success("Correct! 🎉")
        else:
            st.error("Incorrect. The answer is: def")


# ==========================================================
# APTITUDE PRACTICE
# ==========================================================

def show_aptitude_practice():

    st.title("🧮 Aptitude Practice")

    with st.form("aptitude_form"):

        q1 = st.radio(
            "1. What is 25% of 200?",
            ["25", "50", "75", "100"]
        )

        q2 = st.radio(
            "2. If a book costs ₹120 after a ₹30 discount, "
            "what was its original price?",
            ["₹90", "₹120", "₹150", "₹180"]
        )

        q3 = st.radio(
            "3. Find the next number: 2, 4, 8, 16, ?",
            ["18", "24", "30", "32"]
        )

        q4 = st.radio(
            "4. A train travels 60 km in one hour. "
            "How far will it travel in 3 hours?",
            ["120 km", "150 km", "180 km", "240 km"]
        )

        submit = st.form_submit_button(
            "Submit Aptitude Test",
            use_container_width=True
        )

    if submit:

        score = 0

        if q1 == "50":
            score += 1

        if q2 == "₹150":
            score += 1

        if q3 == "32":
            score += 1

        if q4 == "180 km":
            score += 1

        st.metric("Aptitude Score", f"{score}/4")

        if score == 4:
            st.success("Excellent performance!")
        elif score >= 2:
            st.info("Good attempt. Keep practising.")
        else:
            st.warning("Practice percentages, patterns and speed problems.")


# ==========================================================
# COMMUNICATION SKILLS
# ==========================================================

def show_communication_skills():

    st.title("🗣️ Communication Skills")

    activity = st.selectbox(
        "Choose an activity",
        [
            "Self Introduction",
            "Story Writing",
            "Email Writing",
            "Public Speaking"
        ]
    )

    prompts = {
        "Self Introduction": (
            "Write a short self-introduction including your name, "
            "class, school, hobbies, strengths and career goal."
        ),
        "Story Writing": (
            "Write a short story using the words: school, robot, "
            "friend and future."
        ),
        "Email Writing": (
            "Write a polite email to your teacher requesting permission "
            "to participate in a coding competition."
        ),
        "Public Speaking": (
            "Prepare a one-minute speech on: "
            "'How technology helps students'."
        )
    }

    st.info(prompts[activity])

    response = st.text_area(
        "Write your response",
        height=220
    )

    if st.button("Evaluate My Response"):

        word_count = len(response.split())

        if word_count == 0:
            st.error("Write your response first.")

        else:

            st.write(f"**Word count:** {word_count}")

            if word_count >= 100:
                st.success(
                    "Good detailed response. Review grammar and clarity."
                )
            elif word_count >= 50:
                st.info(
                    "Good start. Add more examples and details."
                )
            else:
                st.warning(
                    "Your response is short. Try writing at least 50 words."
                )


# ==========================================================
# GOAL TRACKER
# ==========================================================

def show_goal_tracker():

    st.title("🎯 Goal Tracker")

    with st.form("goal_form"):

        goal_title = st.text_input(
            "Goal title",
            placeholder="Example: Score 90% in Mathematics"
        )

        target_date = st.date_input(
            "Target date",
            min_value=date.today()
        )

        priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High"]
        )

        add_goal = st.form_submit_button(
            "Add Goal",
            use_container_width=True
        )

    if add_goal:

        if goal_title.strip():

            st.session_state.student_goals.append({
                "title": goal_title.strip(),
                "target_date": str(target_date),
                "priority": priority,
                "progress": 0
            })

            st.success("Goal added successfully.")
            st.rerun()

        else:
            st.error("Enter a goal title.")

    if not st.session_state.student_goals:

        st.info("No goals added yet.")
        return

    for index, goal in enumerate(st.session_state.student_goals):

        with st.container(border=True):

            st.subheader(goal["title"])

            st.write(
                f"**Target date:** {goal['target_date']}"
            )

            st.write(
                f"**Priority:** {goal['priority']}"
            )

            progress = st.slider(
                "Progress",
                0,
                100,
                goal["progress"],
                key=f"goal_progress_{index}"
            )

            st.session_state.student_goals[index][
                "progress"
            ] = progress

            st.progress(progress / 100)

            if st.button(
                "Delete Goal",
                key=f"delete_goal_{index}"
            ):

                st.session_state.student_goals.pop(index)
                st.rerun()


# ==========================================================
# AI MENTOR CHATBOT
# ==========================================================

def generate_mentor_response(message):

    text = message.lower()

    if "career" in text:
        return (
            "Start by identifying your favourite subjects, interests "
            "and strengths. Complete the Career Quiz and Interest "
            "Assessment to receive suitable recommendations."
        )

    if "coding" in text or "python" in text:
        return (
            "Begin with Python basics: variables, input/output, "
            "conditions, loops and functions. Practise for at least "
            "20 minutes every day."
        )

    if "exam" in text or "study" in text:
        return (
            "Create a daily timetable, divide topics into small parts, "
            "practise previous questions and revise regularly."
        )

    if "communication" in text or "english" in text:
        return (
            "Read English daily, speak for ten minutes, learn five new "
            "words and practise writing short paragraphs."
        )

    if "goal" in text:
        return (
            "Create a specific goal with a target date. Divide it into "
            "weekly tasks and update your progress regularly."
        )

    return (
        "I can help you with careers, coding, studies, communication, "
        "examinations and goal planning. Ask me a specific question."
    )


def show_ai_mentor():

    st.title("🤖 AI Mentor Chatbot")
    st.write("Ask questions about careers, learning and personal growth.")

    for message in st.session_state.mentor_messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input(
        "Ask your AI mentor..."
    )

    if prompt:

        st.session_state.mentor_messages.append({
            "role": "user",
            "content": prompt
        })

        response = generate_mentor_response(prompt)

        st.session_state.mentor_messages.append({
            "role": "assistant",
            "content": response
        })

        st.rerun()


# ==========================================================
# SCHOOL STUDENT DASHBOARD HOME
# ==========================================================

def show_student_dashboard_home():

    profile = st.session_state.get("school_profile", {})

    student_name = profile.get(
        "full_name",
        "School Student"
    )

    st.markdown(
        f"""
        <div style="
            padding:30px;
            border-radius:20px;
            background:linear-gradient(135deg,#2563EB,#7C3AED);
            color:white;
            margin-bottom:25px;
        ">
            <h1 style="color:white;">👋 Welcome, {student_name}</h1>
            <p style="color:white;">
                Explore careers, improve your skills and achieve your goals.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Daily Tasks",
        len(st.session_state.daily_tasks)
    )

    col2.metric(
        "Goals",
        len(st.session_state.student_goals)
    )

    col3.metric(
        "Profile",
        "Completed" if profile else "Pending"
    )

    col4.metric(
        "Career Quiz",
        st.session_state.career_quiz_result or "Pending"
    )

    st.subheader("🚀 Quick Actions")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info(
            """
            ### 🔍 Discover Careers

            Explore career options based on your favourite subjects.
            """
        )

    with c2:
        st.success(
            """
            ### 📚 Improve Skills

            Learn coding, aptitude and communication skills.
            """
        )

    with c3:
        st.warning(
            """
            ### 🎯 Track Goals

            Add academic and career goals and monitor your progress.
            """
        )


# ==========================================================
# MAIN STUDENT DASHBOARD
# ==========================================================

def show_school_student_dashboard():

    initialize_student_session()

    st.sidebar.markdown("---")
    st.sidebar.subheader("👨‍🎓 School Student")

    student_menu = st.sidebar.radio(
        "Student Features",
        [
            "🏠 Student Dashboard",
            "👤 My Profile",
            "🔍 Career Explorer",
            "🧠 AI Career Quiz",
            "📊 Interest Assessment",
            "🛣️ Future Skills Roadmap",
            "✅ Daily Learning Tasks",
            "💻 Coding Basics",
            "🧮 Aptitude Practice",
            "🗣️ Communication Skills",
            "🎯 Goal Tracker",
            "🤖 AI Mentor Chatbot"
        ],
        key="school_student_menu"
    )

    if student_menu == "🏠 Student Dashboard":
        show_student_dashboard_home()

    elif student_menu == "👤 My Profile":
        show_student_profile()

    elif student_menu == "🔍 Career Explorer":
        show_career_explorer()

    elif student_menu == "🧠 AI Career Quiz":
        show_career_quiz()

    elif student_menu == "📊 Interest Assessment":
        show_interest_assessment()

    elif student_menu == "🛣️ Future Skills Roadmap":
        show_future_skills_roadmap()

    elif student_menu == "✅ Daily Learning Tasks":
        show_daily_learning_tasks()

    elif student_menu == "💻 Coding Basics":
        show_coding_basics()

    elif student_menu == "🧮 Aptitude Practice":
        show_aptitude_practice()

    elif student_menu == "🗣️ Communication Skills":
        show_communication_skills()

    elif student_menu == "🎯 Goal Tracker":
        show_goal_tracker()

    elif student_menu == "🤖 AI Mentor Chatbot":
        show_ai_mentor()