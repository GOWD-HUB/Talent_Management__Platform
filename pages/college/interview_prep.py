import random
import streamlit as st

from styles.college.theme import apply_college_theme


INTERVIEW_QUESTIONS = [
    {
        "category": "HR Interview",
        "topic": "Introduction",
        "difficulty": "Easy",
        "question": "Tell me about yourself.",
        "answer": """Use this structure:

1. Introduce yourself and your current education.
2. Mention your branch or specialization.
3. Mention your technical skills.
4. Mention one or two major projects or internships.
5. Mention your strengths.
6. Finish with your career goal.

Keep the answer around 60–90 seconds.""",
        "tip": "Do not repeat your entire resume. Give a short professional introduction."
    },
    {
        "category": "HR Interview",
        "topic": "Company Fit",
        "difficulty": "Easy",
        "question": "Why should we hire you?",
        "answer": """Mention your relevant technical skills, learning ability, problem solving, teamwork, communication, projects or internships, and willingness to contribute.""",
        "tip": "Connect your skills directly to the role."
    },
    {
        "category": "HR Interview",
        "topic": "Strengths",
        "difficulty": "Easy",
        "question": "What are your strengths?",
        "answer": """Choose two or three genuine strengths such as adaptability, problem solving, quick learning, communication, teamwork, leadership or time management. Give a short example.""",
        "tip": "Support your strengths with evidence."
    },
    {
        "category": "HR Interview",
        "topic": "Self Awareness",
        "difficulty": "Medium",
        "question": "What is your biggest weakness?",
        "answer": """Choose a real but manageable weakness. Explain what it is, how you identified it, what you are doing to improve, and what progress you have made.""",
        "tip": "Always explain your improvement action."
    },
    {
        "category": "HR Interview",
        "topic": "Career",
        "difficulty": "Easy",
        "question": "Where do you see yourself in five years?",
        "answer": """Discuss developing technical expertise, taking ownership of larger projects, learning continuously, contributing to business goals, and gradually taking leadership responsibilities.""",
        "tip": "Keep the answer ambitious but realistic."
    },
    {
        "category": "HR Interview",
        "topic": "Motivation",
        "difficulty": "Easy",
        "question": "Why do you want to join our company?",
        "answer": """Discuss the company's products, technology, innovation, learning opportunities, work culture, growth, and how the role matches your skills.""",
        "tip": "Research the company before the interview."
    },
    {
        "category": "HR Interview",
        "topic": "Achievement",
        "difficulty": "Medium",
        "question": "What is your greatest achievement?",
        "answer": """Use STAR: Situation, Task, Action, Result.""",
        "tip": "Projects, internships, competitions and hackathons are good examples."
    },
    {
        "category": "HR Interview",
        "topic": "Failure",
        "difficulty": "Medium",
        "question": "Tell me about a time you failed.",
        "answer": """Explain what happened, why it happened, what responsibility you took, what you learned and what you changed afterwards.""",
        "tip": "Focus on learning and improvement."
    },
    {
        "category": "HR Interview",
        "topic": "Pressure",
        "difficulty": "Medium",
        "question": "How do you handle pressure and deadlines?",
        "answer": """Mention prioritizing tasks, breaking work into smaller tasks, planning deadlines, communicating blockers early and focusing on high-priority work.""",
        "tip": "Use a real example from college or a project."
    },
    {
        "category": "HR Interview",
        "topic": "Teamwork",
        "difficulty": "Medium",
        "question": "Do you prefer working independently or in a team?",
        "answer": """A strong answer explains that you are comfortable with both. Independent work helps with ownership and focus; teamwork helps with collaboration and knowledge sharing.""",
        "tip": "Do not say you can work only in one environment."
    },
    {
        "category": "HR Interview",
        "topic": "Relocation",
        "difficulty": "Easy",
        "question": "Are you willing to relocate?",
        "answer": """Answer honestly. If yes, explain that relocation can provide new learning, teams and professional growth.""",
        "tip": "Be truthful because relocation may become a real requirement."
    },
    {
        "category": "HR Interview",
        "topic": "Salary",
        "difficulty": "Medium",
        "question": "What are your salary expectations?",
        "answer": """For a fresher: I am primarily looking for a role where I can learn, contribute and grow professionally. I am comfortable with the compensation structure offered for this position.""",
        "tip": "For campus placements, avoid unnecessarily demanding a specific package."
    },
    {
        "category": "HR Interview",
        "topic": "Leadership",
        "difficulty": "Medium",
        "question": "Describe a situation where you demonstrated leadership.",
        "answer": """Use STAR and explain how you coordinated people, assigned responsibilities, solved conflicts and completed the objective.""",
        "tip": "Leadership does not require an official title."
    },
    {
        "category": "HR Interview",
        "topic": "Learning",
        "difficulty": "Easy",
        "question": "How do you learn a new technology?",
        "answer": """Understand fundamentals, read documentation, follow structured tutorials, build a small project, practice independently and then apply it to a larger project.""",
        "tip": "Mention a technology you recently learned."
    },
    {
        "category": "HR Interview",
        "topic": "Closing",
        "difficulty": "Easy",
        "question": "Do you have any questions for us?",
        "answer": """Ask about technologies used by the team, success expectations for freshers, learning opportunities, or the projects you would initially work on.""",
        "tip": "Prepare at least two questions."
    },

    {
        "category": "Technical",
        "topic": "OOP",
        "difficulty": "Easy",
        "question": "What is Object-Oriented Programming?",
        "answer": """OOP organizes software around objects. The four principles are Encapsulation, Abstraction, Inheritance and Polymorphism.""",
        "tip": "Be ready to explain all four principles with examples."
    },
    {
        "category": "Technical",
        "topic": "OOP",
        "difficulty": "Medium",
        "question": "What is the difference between abstraction and encapsulation?",
        "answer": """Abstraction hides implementation complexity and exposes essential behavior. Encapsulation combines data and methods inside a class and controls access to internal data.""",
        "tip": "Give a real-world example."
    },
    {
        "category": "Technical",
        "topic": "DBMS",
        "difficulty": "Easy",
        "question": "What is DBMS?",
        "answer": """DBMS stands for Database Management System. It stores, retrieves, updates and manages data. Examples include MySQL, PostgreSQL and Oracle.""",
        "tip": "Also prepare DBMS vs RDBMS."
    },
    {
        "category": "Technical",
        "topic": "DBMS",
        "difficulty": "Medium",
        "question": "What is normalization?",
        "answer": """Normalization reduces redundancy and improves integrity. Common forms: 1NF atomic values, 2NF removes partial dependency, 3NF removes transitive dependency, BCNF is stronger than 3NF.""",
        "tip": "Practice normalization using a sample table."
    },
    {
        "category": "Technical",
        "topic": "SQL",
        "difficulty": "Medium",
        "question": "Explain different types of SQL JOINs.",
        "answer": """INNER JOIN returns matches, LEFT JOIN returns all left rows plus matches, RIGHT JOIN returns all right rows plus matches, FULL OUTER JOIN returns matching and non-matching rows from both sides.""",
        "tip": "Practice writing JOIN queries."
    },
    {
        "category": "Technical",
        "topic": "Operating Systems",
        "difficulty": "Medium",
        "question": "What is the difference between a process and a thread?",
        "answer": """A process is an independent program in execution. A thread is a lightweight execution unit inside a process. Processes usually have separate memory spaces while threads share process resources.""",
        "tip": "Mention that thread switching is usually cheaper."
    },
    {
        "category": "Technical",
        "topic": "Operating Systems",
        "difficulty": "Medium",
        "question": "What is deadlock?",
        "answer": """Deadlock occurs when processes wait indefinitely for resources held by one another. Conditions: Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait.""",
        "tip": "Remember all four conditions."
    },
    {
        "category": "Technical",
        "topic": "Networking",
        "difficulty": "Medium",
        "question": "What is the difference between HTTP and HTTPS?",
        "answer": """HTTP transfers web data. HTTPS is HTTP protected with TLS and provides confidentiality, integrity and authentication. Common ports are 80 and 443.""",
        "tip": "Explain TLS, not just 'HTTPS is secure'."
    },
    {
        "category": "Technical",
        "topic": "API",
        "difficulty": "Medium",
        "question": "What is a REST API?",
        "answer": """REST is an architectural style for web APIs. Common methods: GET, POST, PUT, PATCH and DELETE. REST APIs commonly exchange JSON.""",
        "tip": "Explain one REST API from your project."
    },
    {
        "category": "Technical",
        "topic": "Authentication",
        "difficulty": "Medium",
        "question": "What is JWT authentication?",
        "answer": """JWT stands for JSON Web Token. Flow: login, validate credentials, generate token, client stores token, client sends token with protected requests, server verifies token. JWT contains header, payload and signature.""",
        "tip": "JWT payload is encoded, not automatically encrypted."
    },
    {
        "category": "Technical",
        "topic": "Git",
        "difficulty": "Easy",
        "question": "What is the difference between Git and GitHub?",
        "answer": """Git is a distributed version control system. GitHub is a platform for hosting Git repositories and collaborating with developers.""",
        "tip": "Know add, commit, push, pull, branch and merge."
    },
    {
        "category": "Technical",
        "topic": "Data Structures",
        "difficulty": "Easy",
        "question": "What is the difference between stack and queue?",
        "answer": """Stack follows LIFO. Queue follows FIFO.""",
        "tip": "Give examples such as undo history and printer queue."
    },
    {
        "category": "Technical",
        "topic": "DSA",
        "difficulty": "Medium",
        "question": "What is time complexity?",
        "answer": """Time complexity describes how algorithm execution time grows with input size. Common complexities: O(1), O(log n), O(n), O(n log n), O(n²), O(2^n).""",
        "tip": "Know complexities of common searching and sorting algorithms."
    },
    {
        "category": "Technical",
        "topic": "DSA",
        "difficulty": "Medium",
        "question": "What is the difference between an array and a linked list?",
        "answer": """Arrays usually use contiguous memory and support O(1) indexed access. Linked lists use connected nodes and sequential access, with flexible insertion/deletion.""",
        "tip": "Explain when you would choose each."
    },
    {
        "category": "Technical",
        "topic": "Frontend",
        "difficulty": "Easy",
        "question": "What is the difference between frontend and backend?",
        "answer": """Frontend is the user-facing layer, such as HTML, CSS, JavaScript and React. Backend handles APIs, business logic, authentication and databases.""",
        "tip": "Explain the flow of one of your projects."
    },
    {
        "category": "Technical",
        "topic": "Database",
        "difficulty": "Medium",
        "question": "What is the difference between SQL and NoSQL?",
        "answer": """SQL databases usually store relational data in tables. NoSQL databases may use document, graph, key-value or other models. The choice depends on requirements.""",
        "tip": "Do not say NoSQL is always faster."
    },
    {
        "category": "Technical",
        "topic": "Web",
        "difficulty": "Medium",
        "question": "What happens when you enter a URL in a browser?",
        "answer": """Browser parses URL, DNS resolves domain, connection is established, TLS is negotiated for HTTPS, HTTP request is sent, server responds, browser renders the page.""",
        "tip": "This tests networking and web fundamentals together."
    },
    {
        "category": "Technical",
        "topic": "Software Engineering",
        "difficulty": "Easy",
        "question": "What is SDLC?",
        "answer": """SDLC phases: Requirement Analysis, Planning, Design, Development, Testing, Deployment and Maintenance.""",
        "tip": "Also prepare Agile concepts."
    },

    {
        "category": "Coding",
        "topic": "Strings",
        "difficulty": "Easy",
        "question": "Write a program to reverse a string.",
        "answer": """Python:

text = input()
print(text[::-1])

Time Complexity: O(n)""",
        "tip": "Also know the two-pointer approach."
    },
    {
        "category": "Coding",
        "topic": "Strings",
        "difficulty": "Easy",
        "question": "Check whether a string is a palindrome.",
        "answer": """Python:

text = input().lower()

if text == text[::-1]:
    print("Palindrome")
else:
    print("Not Palindrome")""",
        "tip": "Ask whether spaces and punctuation should be ignored."
    },
    {
        "category": "Coding",
        "topic": "Arrays",
        "difficulty": "Medium",
        "question": "Find the second largest element in an array.",
        "answer": """A simple solution uses sorted(set(arr))[-2]. For interviews, also know how to find largest and second largest in one traversal.""",
        "tip": "The one-traversal solution is stronger."
    },
    {
        "category": "Coding",
        "topic": "Arrays",
        "difficulty": "Medium",
        "question": "Find duplicate elements in an array.",
        "answer": """Use a set of seen values and another set for duplicates. This gives O(n) average time.""",
        "tip": "Explain the hash-set approach."
    },
    {
        "category": "Coding",
        "topic": "Hashing",
        "difficulty": "Medium",
        "question": "Count the frequency of each array element.",
        "answer": """Use a dictionary:

frequency = {}
for value in arr:
    frequency[value] = frequency.get(value, 0) + 1""",
        "tip": "Hash maps are very common in interviews."
    },
    {
        "category": "Coding",
        "topic": "Strings",
        "difficulty": "Medium",
        "question": "Check whether two strings are anagrams.",
        "answer": """Compare sorted strings or use character-frequency maps.""",
        "tip": "Frequency maps can achieve O(n) time."
    },
    {
        "category": "Coding",
        "topic": "Numbers",
        "difficulty": "Easy",
        "question": "Generate the Fibonacci sequence.",
        "answer": """Use two variables a and b, print a, then update a, b = b, a + b.""",
        "tip": "Know iterative and recursive approaches."
    },
    {
        "category": "Coding",
        "topic": "Numbers",
        "difficulty": "Easy",
        "question": "Check whether a number is prime.",
        "answer": """Test divisors only up to sqrt(n). If any divisor divides n exactly, it is not prime.""",
        "tip": "You only need to check divisors up to √n."
    },
    {
        "category": "Coding",
        "topic": "Searching",
        "difficulty": "Medium",
        "question": "Implement binary search.",
        "answer": """Use left, right and mid pointers on sorted data. If arr[mid] is target return mid; otherwise move left or right. Complexity O(log n).""",
        "tip": "Binary search requires sorted data."
    },
    {
        "category": "Coding",
        "topic": "Arrays",
        "difficulty": "Medium",
        "question": "Solve the Two Sum problem.",
        "answer": """Use a hash map of seen values. For each number, check whether target - number already exists. Average complexity O(n).""",
        "tip": "Explain why hashing improves brute force."
    },
    {
        "category": "Coding",
        "topic": "Arrays",
        "difficulty": "Medium",
        "question": "Find the missing number from 1 to n.",
        "answer": """Use expected_sum = n*(n+1)//2 and subtract sum(arr), or use XOR.""",
        "tip": "Know both sum and XOR approaches."
    },
    {
        "category": "Coding",
        "topic": "Stack",
        "difficulty": "Medium",
        "question": "Check whether parentheses are balanced.",
        "answer": """Use a stack. Push opening brackets. For closing brackets, check whether the top matches the expected opening bracket.""",
        "tip": "This is a classic stack problem."
    },
    {
        "category": "Coding",
        "topic": "Linked List",
        "difficulty": "Medium",
        "question": "How do you reverse a linked list?",
        "answer": """Use previous, current and next pointers. Reverse current.next each iteration. Complexity O(n), space O(1).""",
        "tip": "Be able to draw the pointer changes."
    },
    {
        "category": "Coding",
        "topic": "Sorting",
        "difficulty": "Easy",
        "question": "Implement Bubble Sort.",
        "answer": """Repeatedly compare adjacent values and swap if out of order. Worst-case complexity O(n²).""",
        "tip": "Know when the optimized version can stop early."
    },
    {
        "category": "Coding",
        "topic": "Dynamic Programming",
        "difficulty": "Hard",
        "question": "Find the maximum sum contiguous subarray.",
        "answer": """Use Kadane's algorithm: current = max(num, current + num), best = max(best, current). Complexity O(n).""",
        "tip": "Know why Kadane's algorithm beats brute force."
    },

    {
        "category": "Project",
        "topic": "Overview",
        "difficulty": "Easy",
        "question": "Explain your project.",
        "answer": """Structure: project name, problem statement, proposed solution, technologies, architecture, your contribution, features, challenges and result.""",
        "tip": "Prepare both 60-second and 3-minute explanations."
    },
    {
        "category": "Project",
        "topic": "Architecture",
        "difficulty": "Medium",
        "question": "Explain the architecture of your project.",
        "answer": """Explain the flow: User → Frontend → Backend/API → Business Logic → Database/AI Layer → Response → Frontend.""",
        "tip": "Draw the architecture if possible."
    },
    {
        "category": "Project",
        "topic": "Technology",
        "difficulty": "Medium",
        "question": "Why did you choose your technology stack?",
        "answer": """For each technology explain the requirement it solves, why it fits, advantages, alternatives considered and why you selected it.""",
        "tip": "Do not say you chose it only because it was easy."
    },
    {
        "category": "Project",
        "topic": "Contribution",
        "difficulty": "Medium",
        "question": "What was your individual contribution to the project?",
        "answer": """Explain exactly what you built: features, APIs, database work, UI modules, testing, deployment or integration.""",
        "tip": "Be precise about your own contribution."
    },
    {
        "category": "Project",
        "topic": "Challenges",
        "difficulty": "Medium",
        "question": "What was the biggest technical challenge in your project?",
        "answer": """Explain Problem → Root Cause → Solutions Considered → Solution Selected → Implementation → Result → Learning.""",
        "tip": "Choose a real technical challenge."
    },
    {
        "category": "Project",
        "topic": "Database",
        "difficulty": "Medium",
        "question": "How did you design your project's database?",
        "answer": """Discuss main entities, relationships, primary keys, foreign keys, data types, validation, indexing and why SQL or NoSQL was selected.""",
        "tip": "Know your project database schema."
    },
    {
        "category": "Project",
        "topic": "API",
        "difficulty": "Medium",
        "question": "How does your frontend communicate with your backend?",
        "answer": """Frontend sends HTTP requests. Backend validates input, runs business logic, communicates with the database and returns JSON. Frontend updates the UI from the response.""",
        "tip": "Mention actual endpoints from your project."
    },
    {
        "category": "Project",
        "topic": "Security",
        "difficulty": "Hard",
        "question": "How did you secure your application?",
        "answer": """Possible measures: password hashing, authentication, authorization, input validation, protected APIs, environment variables, HTTPS and database access controls.""",
        "tip": "Only mention security features you actually implemented."
    },
    {
        "category": "Project",
        "topic": "Testing",
        "difficulty": "Medium",
        "question": "How did you test your project?",
        "answer": """Discuss manual testing, unit testing, integration testing, API testing, validation testing, edge cases and error handling.""",
        "tip": "Mention tools such as Postman when relevant."
    },
    {
        "category": "Project",
        "topic": "Improvement",
        "difficulty": "Medium",
        "question": "If you had more time, what would you improve in your project?",
        "answer": """Possible improvements: scalability, UI/UX, testing, cloud deployment, security, performance, new features and monitoring.""",
        "tip": "Show that you understand your project's limitations."
    },

    {
        "category": "Behavioral",
        "topic": "Conflict",
        "difficulty": "Medium",
        "question": "Tell me about a conflict you had with a teammate.",
        "answer": """Use STAR and focus on understanding both viewpoints, professional communication, common ground, solving the problem and maintaining the relationship.""",
        "tip": "Never attack your teammate."
    },
    {
        "category": "Behavioral",
        "topic": "Deadline",
        "difficulty": "Medium",
        "question": "What would you do if you could not meet a deadline?",
        "answer": """Evaluate remaining work, prioritize important tasks, identify blockers, communicate early, ask for support and agree on a recovery plan.""",
        "tip": "Communicate before the deadline."
    },
    {
        "category": "Behavioral",
        "topic": "Teamwork",
        "difficulty": "Medium",
        "question": "How would you handle a teammate who is not contributing?",
        "answer": """Speak privately, understand technical or personal blockers, offer help, clarify expectations, and escalate professionally only if needed.""",
        "tip": "Show empathy and accountability."
    },
    {
        "category": "Behavioral",
        "topic": "Learning",
        "difficulty": "Medium",
        "question": "Your manager gives you a technology you have never used. What would you do?",
        "answer": """Understand the requirement, learn fundamentals, read documentation, build a proof of concept, ask focused questions when blocked, then apply it to the real task.""",
        "tip": "Companies value independent learning."
    },
    {
        "category": "Behavioral",
        "topic": "Feedback",
        "difficulty": "Medium",
        "question": "How do you handle criticism?",
        "answer": """Listen carefully, avoid defensiveness, ask questions, identify improvements, implement feedback and review progress.""",
        "tip": "Give an example where feedback improved your work."
    },
    {
        "category": "Behavioral",
        "topic": "Prioritization",
        "difficulty": "Medium",
        "question": "How do you prioritize multiple tasks?",
        "answer": """Consider importance, deadline, dependencies, effort and risk, then create a prioritized task list.""",
        "tip": "Mention how you track your tasks."
    },
    {
        "category": "Behavioral",
        "topic": "Initiative",
        "difficulty": "Medium",
        "question": "Tell me about a time you took initiative.",
        "answer": """Use STAR. Examples include learning a technology, fixing a recurring problem, improving a project or helping organize a team.""",
        "tip": "Highlight the result."
    },
    {
        "category": "Behavioral",
        "topic": "Mistakes",
        "difficulty": "Medium",
        "question": "What would you do if you made a mistake that affected the project?",
        "answer": """Acknowledge it, determine impact, inform relevant people, fix the issue, find the root cause and prevent recurrence.""",
        "tip": "Ownership is better than hiding mistakes."
    },
    {
        "category": "Behavioral",
        "topic": "Requirements",
        "difficulty": "Hard",
        "question": "What would you do if project requirements were unclear?",
        "answer": """Identify ambiguities, prepare specific questions, discuss with stakeholders, confirm behavior, document decisions, prototype if needed and validate before implementation.""",
        "tip": "Do not guess critical requirements."
    },
    {
        "category": "Behavioral",
        "topic": "Leadership",
        "difficulty": "Hard",
        "question": "Your team disagrees on two technical solutions. How would you decide?",
        "answer": """Compare requirements, performance, complexity, development time, maintainability, security, scalability and team expertise. Build a proof of concept if needed.""",
        "tip": "Engineering decisions should be evidence-based."
    },
]


def initialize_state():
    defaults = {
        "interview_completed": [],
        "interview_bookmarked": [],
        "random_interview_question": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_question_id(question):
    return (
        question["category"]
        + "::"
        + question["topic"]
        + "::"
        + question["question"]
    )


def difficulty_icon(level):
    return {
        "Easy": "🟢",
        "Medium": "🟡",
        "Hard": "🔴",
    }.get(level, "⚪")


def render_question_card(index, question, status_text):
    st.html(
        f"""<div style="
            background:#ffffff;
            border:1px solid #e2e8f0;
            border-radius:20px;
            padding:24px;
            margin-top:18px;
            margin-bottom:8px;
            box-shadow:0 8px 24px rgba(15,23,42,0.05);
        ">
            <div style="
                color:#4f46e5;
                font-size:11px;
                font-weight:900;
                letter-spacing:1px;
                margin-bottom:10px;
            ">
                QUESTION {index:02d}
            </div>

            <div style="
                color:#0f172a;
                font-size:18px;
                font-weight:800;
                line-height:1.5;
                margin-bottom:12px;
            ">
                {question["question"]}
            </div>

            <div style="
                color:#64748b;
                font-size:12px;
                line-height:1.7;
            ">
                {difficulty_icon(question["difficulty"])}
                {question["category"]}
                &nbsp;&nbsp;•&nbsp;&nbsp;
                {question["topic"]}
                &nbsp;&nbsp;•&nbsp;&nbsp;
                {question["difficulty"]}
                &nbsp;&nbsp;•&nbsp;&nbsp;
                {status_text}
            </div>
        </div>"""
    )


def render():
    apply_college_theme()
    initialize_state()

    total = len(INTERVIEW_QUESTIONS)
    completed_count = len(st.session_state.interview_completed)
    bookmarked_count = len(st.session_state.interview_bookmarked)

    progress = (
        round(completed_count / total * 100)
        if total
        else 0
    )

    st.html(
        """<div class="college-hero">
            <div class="college-hero-badge">
                🎤 COLLEGE INTERVIEW PREPARATION
            </div>
            <div class="college-hero-title">
                Interview Preparation
            </div>
            <div class="college-hero-description">
                Prepare HR, technical, coding, project and behavioral
                interview questions with structured answer guides,
                interview tips, bookmarks and preparation tracking.
            </div>
        </div>"""
    )

    st.html(
        f"""<div class="college-metric-grid">
            <div class="college-metric-card">
                <div class="college-metric-icon">🎤</div>
                <div class="college-metric-label">Question Bank</div>
                <div class="college-metric-value">{total}</div>
                <div class="college-metric-caption">Placement interview questions</div>
            </div>

            <div class="college-metric-card">
                <div class="college-metric-icon">✅</div>
                <div class="college-metric-label">Prepared</div>
                <div class="college-metric-value">{completed_count}</div>
                <div class="college-metric-caption">Questions completed</div>
            </div>

            <div class="college-metric-card">
                <div class="college-metric-icon">🔖</div>
                <div class="college-metric-label">Bookmarked</div>
                <div class="college-metric-value">{bookmarked_count}</div>
                <div class="college-metric-caption">Saved for revision</div>
            </div>

            <div class="college-metric-card">
                <div class="college-metric-icon">📈</div>
                <div class="college-metric-label">Progress</div>
                <div class="college-metric-value">{progress}%</div>
                <div class="college-metric-caption">Interview preparation</div>
            </div>
        </div>"""
    )

    st.progress(progress / 100)

    st.html(
        """<div class="college-section-header">
            <div>
                <div class="college-section-title">📚 Interview Areas</div>
                <div class="college-section-subtitle">
                    Prepare across every major placement interview area.
                </div>
            </div>
            <div class="college-section-tag">Placement Preparation</div>
        </div>"""
    )

    categories_info = [
        ("👔", "HR Interview"),
        ("💻", "Technical"),
        ("🧑‍💻", "Coding"),
        ("🚀", "Project"),
        ("🧠", "Behavioral"),
    ]

    area_columns = st.columns(5)

    for column, (icon, category_name) in zip(area_columns, categories_info):
        count = sum(
            1
            for question in INTERVIEW_QUESTIONS
            if question["category"] == category_name
        )

        with column:
            st.html(
                f"""<div style="
                    background:#ffffff;
                    border:1px solid #e2e8f0;
                    border-radius:18px;
                    padding:20px;
                    min-height:135px;
                    box-shadow:0 8px 24px rgba(15,23,42,.04);
                ">
                    <div style="font-size:25px;">{icon}</div>
                    <div style="
                        color:#0f172a;
                        font-size:14px;
                        font-weight:800;
                        margin-top:10px;
                    ">{category_name}</div>
                    <div style="
                        color:#64748b;
                        font-size:12px;
                        margin-top:7px;
                    ">{count} questions</div>
                </div>"""
            )

    st.html(
        """<div class="college-section-header">
            <div>
                <div class="college-section-title">⚡ Quick Practice</div>
                <div class="college-section-subtitle">
                    Pick a random question for instant interview practice.
                </div>
            </div>
        </div>"""
    )

    if st.button(
        "🎲 Give Me a Random Interview Question",
        key="interview_random_button",
        use_container_width=True,
    ):
        st.session_state.random_interview_question = random.choice(
            INTERVIEW_QUESTIONS
        )

    if st.session_state.random_interview_question:
        question = st.session_state.random_interview_question

        st.info(
            f"""{difficulty_icon(question["difficulty"])}
**{question["category"]} • {question["difficulty"]}**

### {question["question"]}"""
        )

    st.html(
        """<div class="college-section-header">
            <div>
                <div class="college-section-title">🔍 Question Bank</div>
                <div class="college-section-subtitle">
                    Search and filter your interview questions.
                </div>
            </div>
        </div>"""
    )

    filter1, filter2, filter3 = st.columns(3)

    with filter1:
        selected_category = st.selectbox(
            "Category",
            ["All", "HR Interview", "Technical", "Coding", "Project", "Behavioral"],
            key="interview_category_filter",
        )

    with filter2:
        selected_difficulty = st.selectbox(
            "Difficulty",
            ["All", "Easy", "Medium", "Hard"],
            key="interview_difficulty_filter",
        )

    topics = sorted({question["topic"] for question in INTERVIEW_QUESTIONS})

    with filter3:
        selected_topic = st.selectbox(
            "Topic",
            ["All", *topics],
            key="interview_topic_filter",
        )

    search_text = st.text_input(
        "Search questions",
        placeholder="Search OOP, SQL, project, API, arrays, HR...",
        key="interview_search",
    )

    filtered_questions = []

    for question in INTERVIEW_QUESTIONS:

        if (
            selected_category != "All"
            and question["category"] != selected_category
        ):
            continue

        if (
            selected_difficulty != "All"
            and question["difficulty"] != selected_difficulty
        ):
            continue

        if (
            selected_topic != "All"
            and question["topic"] != selected_topic
        ):
            continue

        if search_text.strip():
            keyword = search_text.strip().lower()

            searchable = (
                question["question"]
                + " "
                + question["category"]
                + " "
                + question["topic"]
            ).lower()

            if keyword not in searchable:
                continue

        filtered_questions.append(question)

    st.html(
        f"""<div class="college-section-header">
            <div>
                <div class="college-section-title">🎯 Interview Questions</div>
                <div class="college-section-subtitle">
                    Showing {len(filtered_questions)} of {total} questions.
                </div>
            </div>
        </div>"""
    )

    if not filtered_questions:
        st.warning("No interview questions match the selected filters.")
        return

    for index, question in enumerate(filtered_questions, start=1):

        qid = get_question_id(question)

        is_completed = (
            qid in st.session_state.interview_completed
        )

        is_bookmarked = (
            qid in st.session_state.interview_bookmarked
        )

        status_text = (
            "✅ Prepared"
            if is_completed
            else "⏳ Not Prepared"
        )

        render_question_card(
            index,
            question,
            status_text,
        )

        with st.expander(
            "💡 Show Answer Guide",
            expanded=False,
        ):

            st.markdown("### ✅ Answer Guide")
            st.markdown(question["answer"])

            st.html(
                f"""<div style="
                    background:#fff7ed;
                    border:1px solid #fed7aa;
                    border-radius:14px;
                    padding:15px 17px;
                    margin-top:14px;
                    margin-bottom:8px;
                ">
                    <div style="
                        color:#9a3412;
                        font-size:13px;
                        font-weight:800;
                    ">💡 Interview Tip</div>

                    <div style="
                        color:#7c2d12;
                        font-size:13px;
                        line-height:1.6;
                        margin-top:6px;
                    ">{question["tip"]}</div>
                </div>"""
            )

            action1, action2 = st.columns(2)

            with action1:

                if not is_completed:

                    if st.button(
                        "✅ Mark as Prepared",
                        key=f"complete_{index}_{abs(hash(qid))}",
                        use_container_width=True,
                    ):

                        st.session_state.interview_completed.append(qid)
                        st.rerun()

                else:

                    if st.button(
                        "↩ Mark as Not Prepared",
                        key=f"uncomplete_{index}_{abs(hash(qid))}",
                        use_container_width=True,
                    ):

                        st.session_state.interview_completed.remove(qid)
                        st.rerun()

            with action2:

                if not is_bookmarked:

                    if st.button(
                        "🔖 Save for Revision",
                        key=f"bookmark_{index}_{abs(hash(qid))}",
                        use_container_width=True,
                    ):

                        st.session_state.interview_bookmarked.append(qid)
                        st.rerun()

                else:

                    if st.button(
                        "❌ Remove Bookmark",
                        key=f"unbookmark_{index}_{abs(hash(qid))}",
                        use_container_width=True,
                    ):

                        st.session_state.interview_bookmarked.remove(qid)
                        st.rerun()

    if st.session_state.interview_bookmarked:

        st.html(
            """<div class="college-section-header">
                <div>
                    <div class="college-section-title">🔖 Saved for Revision</div>
                    <div class="college-section-subtitle">
                        Quickly revise your bookmarked questions.
                    </div>
                </div>
            </div>"""
        )

        for question in INTERVIEW_QUESTIONS:

            qid = get_question_id(question)

            if qid not in st.session_state.interview_bookmarked:
                continue

            with st.expander(f'🔖 {question["question"]}'):

                st.caption(
                    f'{question["category"]} • '
                    f'{question["topic"]} • '
                    f'{question["difficulty"]}'
                )

                st.markdown(question["answer"])
                st.info("💡 " + question["tip"])

    st.html(
        """<div class="college-section-header">
            <div>
                <div class="college-section-title">
                    🗓️ Interview Preparation Strategy
                </div>
                <div class="college-section-subtitle">
                    Follow this sequence before placement interviews.
                </div>
            </div>
        </div>"""
    )

    s1, s2, s3 = st.columns(3)

    with s1:
        st.html(
            """<div style="
                background:#eef2ff;
                border:1px solid #e0e7ff;
                border-radius:20px;
                padding:22px;
                min-height:185px;
            ">
                <div style="font-size:25px;">📘</div>
                <div style="
                    color:#0f172a;
                    font-size:17px;
                    font-weight:800;
                    margin-top:12px;
                ">1. Revise Fundamentals</div>
                <div style="
                    color:#64748b;
                    font-size:12px;
                    line-height:1.7;
                    margin-top:9px;
                ">
                    Prepare OOP, DBMS, SQL, OS, networks,
                    APIs, DSA and programming fundamentals.
                </div>
            </div>"""
        )

    with s2:
        st.html(
            """<div style="
                background:#ecfdf5;
                border:1px solid #d1fae5;
                border-radius:20px;
                padding:22px;
                min-height:185px;
            ">
                <div style="font-size:25px;">💻</div>
                <div style="
                    color:#0f172a;
                    font-size:17px;
                    font-weight:800;
                    margin-top:12px;
                ">2. Practice Coding</div>
                <div style="
                    color:#64748b;
                    font-size:12px;
                    line-height:1.7;
                    margin-top:9px;
                ">
                    Practice arrays, strings, hashing, searching,
                    sorting, stacks and linked lists.
                </div>
            </div>"""
        )

    with s3:
        st.html(
            """<div style="
                background:#fff7ed;
                border:1px solid #ffedd5;
                border-radius:20px;
                padding:22px;
                min-height:185px;
            ">
                <div style="font-size:25px;">🎤</div>
                <div style="
                    color:#0f172a;
                    font-size:17px;
                    font-weight:800;
                    margin-top:12px;
                ">3. Take Mock Interviews</div>
                <div style="
                    color:#64748b;
                    font-size:12px;
                    line-height:1.7;
                    margin-top:9px;
                ">
                    Practice speaking answers clearly,
                    explain your projects and improve confidence.
                </div>
            </div>"""
        )


if __name__ == "__main__":
    render()
