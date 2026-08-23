import random
import streamlit as st

from styles.college.theme import apply_college_theme


# ==========================================================
# INTERVIEW QUESTION BANK
# ==========================================================

INTERVIEW_QUESTIONS = [

    # ======================================================
    # HR INTERVIEW
    # ======================================================

    {
        "category": "HR Interview",
        "topic": "Introduction",
        "difficulty": "Easy",
        "question": "Tell me about yourself.",
        "answer": """
Use this structure:

1. Introduce yourself and your current education.
2. Mention your branch or specialization.
3. Mention your important technical skills.
4. Mention one or two major projects or internships.
5. Mention your strengths.
6. Finish with your career goal.

Keep the answer around 60–90 seconds.
""",
        "tip": "Do not repeat your entire resume. Give a short professional introduction."
    },

    {
        "category": "HR Interview",
        "topic": "Company Fit",
        "difficulty": "Easy",
        "question": "Why should we hire you?",
        "answer": """
Mention:

• Your relevant technical skills.
• Your ability to learn quickly.
• Problem-solving ability.
• Teamwork and communication.
• Projects or internships that demonstrate practical experience.
• Your willingness to contribute to the organization.
""",
        "tip": "Connect your skills directly to the job role."
    },

    {
        "category": "HR Interview",
        "topic": "Strengths",
        "difficulty": "Easy",
        "question": "What are your strengths?",
        "answer": """
Choose two or three genuine strengths.

Examples:

• Adaptability
• Problem solving
• Quick learning
• Communication
• Teamwork
• Leadership
• Time management

Give a short example for at least one strength.
""",
        "tip": "Do not only list strengths. Support them with an example."
    },

    {
        "category": "HR Interview",
        "topic": "Self Awareness",
        "difficulty": "Medium",
        "question": "What is your biggest weakness?",
        "answer": """
Choose a real but manageable weakness.

Explain:

1. What the weakness is.
2. How you identified it.
3. What you are doing to improve.
4. What progress you have made.

Avoid weaknesses that make you completely unsuitable for the role.
""",
        "tip": "Always explain the improvement action."
    },

    {
        "category": "HR Interview",
        "topic": "Career",
        "difficulty": "Easy",
        "question": "Where do you see yourself in five years?",
        "answer": """
A strong answer can include:

• Developing strong technical expertise.
• Taking ownership of larger projects.
• Learning continuously.
• Contributing to business goals.
• Gradually taking leadership responsibilities.
""",
        "tip": "Keep the answer ambitious but realistic."
    },

    {
        "category": "HR Interview",
        "topic": "Motivation",
        "difficulty": "Easy",
        "question": "Why do you want to join our company?",
        "answer": """
Discuss:

• Company's products or services.
• Technology and innovation.
• Learning opportunities.
• Work culture.
• Career growth.
• How the role matches your skills.
""",
        "tip": "Research the company before the interview."
    },

    {
        "category": "HR Interview",
        "topic": "Achievement",
        "difficulty": "Medium",
        "question": "What is your greatest achievement?",
        "answer": """
Use STAR:

Situation – Explain the background.

Task – Explain your responsibility.

Action – Explain what you did.

Result – Explain the final outcome.
""",
        "tip": "Projects, internships, competitions and hackathons are good examples."
    },

    {
        "category": "HR Interview",
        "topic": "Failure",
        "difficulty": "Medium",
        "question": "Tell me about a time you failed.",
        "answer": """
Explain:

• What happened.
• Why it happened.
• What responsibility you took.
• What you learned.
• What you changed after the experience.
""",
        "tip": "Focus on learning and improvement."
    },

    {
        "category": "HR Interview",
        "topic": "Pressure",
        "difficulty": "Medium",
        "question": "How do you handle pressure and deadlines?",
        "answer": """
Mention:

• Prioritizing tasks.
• Breaking large work into smaller tasks.
• Planning deadlines.
• Communicating blockers early.
• Focusing on high-priority work.
""",
        "tip": "Use a real example from college or a project."
    },

    {
        "category": "HR Interview",
        "topic": "Teamwork",
        "difficulty": "Medium",
        "question": "Do you prefer working independently or in a team?",
        "answer": """
A strong answer should explain that you are comfortable with both.

Independent work helps with:

• Ownership
• Focus
• Individual responsibility

Teamwork helps with:

• Collaboration
• Knowledge sharing
• Complex projects
• Faster problem solving
""",
        "tip": "Do not say you can work only in one environment."
    },

    {
        "category": "HR Interview",
        "topic": "Relocation",
        "difficulty": "Easy",
        "question": "Are you willing to relocate?",
        "answer": """
If you are comfortable relocating:

'I am open to relocation because it gives me an opportunity
to work with different teams, learn new things and grow professionally.'

Answer according to your real situation.
""",
        "tip": "Be truthful because relocation may become a real requirement."
    },

    {
        "category": "HR Interview",
        "topic": "Salary",
        "difficulty": "Medium",
        "question": "What are your salary expectations?",
        "answer": """
For a fresher:

'I am primarily looking for a role where I can learn,
contribute and grow professionally. I am comfortable
with the compensation structure offered by the company
for this position.'
""",
        "tip": "For campus placements, avoid unnecessarily demanding a specific package."
    },

    {
        "category": "HR Interview",
        "topic": "Leadership",
        "difficulty": "Medium",
        "question": "Describe a situation where you demonstrated leadership.",
        "answer": """
Use STAR:

Situation
Task
Action
Result

Mention how you:

• Coordinated people.
• Assigned responsibilities.
• Solved conflicts.
• Completed the objective.
""",
        "tip": "Leadership does not require an official title."
    },

    {
        "category": "HR Interview",
        "topic": "Learning",
        "difficulty": "Easy",
        "question": "How do you learn a new technology?",
        "answer": """
A useful process:

1. Understand fundamentals.
2. Read documentation.
3. Follow structured tutorials.
4. Build a small project.
5. Practice independently.
6. Apply the technology to a larger project.
""",
        "tip": "Mention a technology you recently learned."
    },

    {
        "category": "HR Interview",
        "topic": "Closing",
        "difficulty": "Easy",
        "question": "Do you have any questions for us?",
        "answer": """
Good questions include:

• What technologies does the team use?
• What does success look like for a fresher in this role?
• What learning opportunities are available?
• What kind of projects would I initially work on?
""",
        "tip": "Prepare at least two questions."
    },


    # ======================================================
    # TECHNICAL
    # ======================================================

    {
        "category": "Technical",
        "topic": "OOP",
        "difficulty": "Easy",
        "question": "What is Object-Oriented Programming?",
        "answer": """
OOP organizes software around objects.

The four major principles are:

1. Encapsulation
2. Abstraction
3. Inheritance
4. Polymorphism

Objects contain data and methods that operate on that data.
""",
        "tip": "Be ready to explain all four principles with examples."
    },

    {
        "category": "Technical",
        "topic": "OOP",
        "difficulty": "Medium",
        "question": "What is the difference between abstraction and encapsulation?",
        "answer": """
Abstraction hides implementation complexity and exposes only essential behavior.

Encapsulation combines data and methods inside a class and controls
access to internal data.
""",
        "tip": "Give a real-world example."
    },

    {
        "category": "Technical",
        "topic": "DBMS",
        "difficulty": "Easy",
        "question": "What is DBMS?",
        "answer": """
DBMS stands for Database Management System.

It is used to:

• Store data
• Retrieve data
• Update data
• Manage relationships
• Maintain security and consistency

Examples:
MySQL, PostgreSQL, Oracle.
""",
        "tip": "Also prepare the difference between DBMS and RDBMS."
    },

    {
        "category": "Technical",
        "topic": "DBMS",
        "difficulty": "Medium",
        "question": "What is normalization?",
        "answer": """
Normalization reduces data redundancy and improves integrity.

Common normal forms:

1NF – Atomic values

2NF – Removes partial dependency

3NF – Removes transitive dependency

BCNF – Stronger version of 3NF
""",
        "tip": "Practice normalization using a sample table."
    },

    {
        "category": "Technical",
        "topic": "SQL",
        "difficulty": "Medium",
        "question": "Explain different types of SQL JOINs.",
        "answer": """
INNER JOIN:
Returns matching rows.

LEFT JOIN:
Returns all rows from the left table and matching rows from the right.

RIGHT JOIN:
Returns all rows from the right table and matching rows from the left.

FULL OUTER JOIN:
Returns matching and non-matching rows from both tables.
""",
        "tip": "Practice writing JOIN queries."
    },

    {
        "category": "Technical",
        "topic": "Operating Systems",
        "difficulty": "Medium",
        "question": "What is the difference between a process and a thread?",
        "answer": """
Process:
An independent program in execution.

Thread:
A lightweight execution unit inside a process.

Processes generally have separate memory spaces.

Threads inside the same process share resources.
""",
        "tip": "Mention that thread switching is usually cheaper."
    },

    {
        "category": "Technical",
        "topic": "Operating Systems",
        "difficulty": "Medium",
        "question": "What is deadlock?",
        "answer": """
Deadlock occurs when processes wait indefinitely for resources
held by one another.

Four necessary conditions:

1. Mutual Exclusion
2. Hold and Wait
3. No Preemption
4. Circular Wait
""",
        "tip": "Remember all four conditions."
    },

    {
        "category": "Technical",
        "topic": "Networking",
        "difficulty": "Medium",
        "question": "What is the difference between HTTP and HTTPS?",
        "answer": """
HTTP transfers web data.

HTTPS is HTTP protected using TLS.

HTTPS provides:

• Confidentiality
• Integrity
• Authentication

Common ports:

HTTP – 80

HTTPS – 443
""",
        "tip": "Explain TLS, not just 'HTTPS is secure'."
    },

    {
        "category": "Technical",
        "topic": "API",
        "difficulty": "Medium",
        "question": "What is a REST API?",
        "answer": """
REST is an architectural style for web APIs.

Common methods:

GET – Read

POST – Create

PUT – Replace

PATCH – Partially update

DELETE – Delete

REST APIs commonly exchange JSON.
""",
        "tip": "Explain one REST API from your project."
    },

    {
        "category": "Technical",
        "topic": "Authentication",
        "difficulty": "Medium",
        "question": "What is JWT authentication?",
        "answer": """
JWT stands for JSON Web Token.

Flow:

1. User logs in.
2. Server validates credentials.
3. Server generates a signed JWT.
4. Client stores the token.
5. Client sends the token with protected requests.
6. Server verifies the token.

JWT contains:

Header
Payload
Signature
""",
        "tip": "JWT payload is encoded, not automatically encrypted."
    },

    {
        "category": "Technical",
        "topic": "Git",
        "difficulty": "Easy",
        "question": "What is the difference between Git and GitHub?",
        "answer": """
Git:
A distributed version control system.

GitHub:
A platform for hosting Git repositories and collaborating with developers.
""",
        "tip": "Know add, commit, push, pull, branch and merge."
    },

    {
        "category": "Technical",
        "topic": "Data Structures",
        "difficulty": "Easy",
        "question": "What is the difference between stack and queue?",
        "answer": """
Stack:
LIFO – Last In, First Out.

Queue:
FIFO – First In, First Out.
""",
        "tip": "Give examples such as undo history and printer queue."
    },

    {
        "category": "Technical",
        "topic": "DSA",
        "difficulty": "Medium",
        "question": "What is time complexity?",
        "answer": """
Time complexity describes how algorithm execution time grows with input size.

Common complexities:

O(1)

O(log n)

O(n)

O(n log n)

O(n²)

O(2^n)
""",
        "tip": "Know complexities of common searching and sorting algorithms."
    },

    {
        "category": "Technical",
        "topic": "DSA",
        "difficulty": "Medium",
        "question": "What is the difference between an array and a linked list?",
        "answer": """
Array:

• Usually contiguous memory
• Fast indexed access
• O(1) random access

Linked List:

• Nodes are connected using links
• Sequential access
• Flexible insertion and deletion
""",
        "tip": "Explain when you would choose each one."
    },

    {
        "category": "Technical",
        "topic": "Frontend",
        "difficulty": "Easy",
        "question": "What is the difference between frontend and backend?",
        "answer": """
Frontend:
The user-facing part of an application.

Examples:
HTML, CSS, JavaScript, React.

Backend:
Handles APIs, business logic, authentication and databases.

Examples:
Node.js, Django, FastAPI.
""",
        "tip": "Explain the frontend/backend flow of one of your projects."
    },

    {
        "category": "Technical",
        "topic": "Database",
        "difficulty": "Medium",
        "question": "What is the difference between SQL and NoSQL?",
        "answer": """
SQL databases usually store relational data in tables.

Examples:
MySQL
PostgreSQL

NoSQL databases can use document, graph, key-value or other models.

Example:
MongoDB

The choice depends on requirements.
""",
        "tip": "Do not say NoSQL is always faster."
    },

    {
        "category": "Technical",
        "topic": "Web",
        "difficulty": "Medium",
        "question": "What happens when you enter a URL in a browser?",
        "answer": """
Simplified flow:

1. Browser parses the URL.
2. DNS resolves the domain.
3. Connection is established.
4. TLS is negotiated for HTTPS.
5. Browser sends an HTTP request.
6. Server processes the request.
7. Server sends a response.
8. Browser renders the page.
""",
        "tip": "This tests networking and web fundamentals together."
    },

    {
        "category": "Technical",
        "topic": "Software Engineering",
        "difficulty": "Easy",
        "question": "What is SDLC?",
        "answer": """
SDLC stands for Software Development Life Cycle.

Typical phases:

1. Requirement Analysis
2. Planning
3. Design
4. Development
5. Testing
6. Deployment
7. Maintenance
""",
        "tip": "Also prepare Agile concepts."
    },


    # ======================================================
    # CODING
    # ======================================================

    {
        "category": "Coding",
        "topic": "Strings",
        "difficulty": "Easy",
        "question": "Write a program to reverse a string.",
        "answer": """
Python:

text = input()
print(text[::-1])

Time Complexity: O(n)
""",
        "tip": "Also know the two-pointer approach."
    },

    {
        "category": "Coding",
        "topic": "Strings",
        "difficulty": "Easy",
        "question": "Check whether a string is a palindrome.",
        "answer": """
Python:

text = input().lower()

if text == text[::-1]:
    print("Palindrome")
else:
    print("Not Palindrome")
""",
        "tip": "Ask whether spaces and punctuation should be ignored."
    },

    {
        "category": "Coding",
        "topic": "Arrays",
        "difficulty": "Medium",
        "question": "Find the second largest element in an array.",
        "answer": """
A simple approach:

arr = [10, 20, 4, 45, 99]

unique = list(set(arr))
unique.sort()

print(unique[-2])

For interviews, try solving it in one traversal.
""",
        "tip": "The one-traversal solution is more impressive."
    },

    {
        "category": "Coding",
        "topic": "Arrays",
        "difficulty": "Medium",
        "question": "Find duplicate elements in an array.",
        "answer": """
arr = [1, 2, 3, 2, 4, 1]

seen = set()
duplicates = set()

for value in arr:

    if value in seen:
        duplicates.add(value)

    else:
        seen.add(value)

print(duplicates)
""",
        "tip": "Hash-set approach is O(n) average time."
    },

    {
        "category": "Coding",
        "topic": "Hashing",
        "difficulty": "Medium",
        "question": "Count the frequency of each array element.",
        "answer": """
arr = [1, 2, 2, 3, 3, 3]

frequency = {}

for value in arr:

    frequency[value] = frequency.get(value, 0) + 1

print(frequency)
""",
        "tip": "Hash maps are very common in interviews."
    },

    {
        "category": "Coding",
        "topic": "Searching",
        "difficulty": "Medium",
        "question": "Implement binary search.",
        "answer": """
def binary_search(arr, target):

    left = 0
    right = len(arr) - 1

    while left <= right:

        mid = (left + right) // 2

        if arr[mid] == target:
            return mid

        if arr[mid] < target:
            left = mid + 1

        else:
            right = mid - 1

    return -1

Time Complexity: O(log n)
""",
        "tip": "Binary search requires sorted data."
    },

    {
        "category": "Coding",
        "topic": "Arrays",
        "difficulty": "Medium",
        "question": "Solve the Two Sum problem.",
        "answer": """
def two_sum(nums, target):

    seen = {}

    for index, value in enumerate(nums):

        required = target - value

        if required in seen:
            return [seen[required], index]

        seen[value] = index

    return []

Average Time Complexity: O(n)
""",
        "tip": "Explain why a hash map improves the brute-force solution."
    },

    {
        "category": "Coding",
        "topic": "Stack",
        "difficulty": "Medium",
        "question": "Check whether parentheses are balanced.",
        "answer": """
def balanced(text):

    stack = []

    pairs = {
        ')': '(',
        ']': '[',
        '}': '{'
    }

    for character in text:

        if character in "([{":
            stack.append(character)

        elif character in pairs:

            if not stack or stack[-1] != pairs[character]:
                return False

            stack.pop()

    return len(stack) == 0
""",
        "tip": "This is a classic stack problem."
    },

    {
        "category": "Coding",
        "topic": "Dynamic Programming",
        "difficulty": "Hard",
        "question": "Find the maximum sum contiguous subarray.",
        "answer": """
Use Kadane's Algorithm:

def max_subarray(nums):

    current = nums[0]
    best = nums[0]

    for num in nums[1:]:

        current = max(
            num,
            current + num
        )

        best = max(
            best,
            current
        )

    return best

Time Complexity: O(n)
""",
        "tip": "Know why Kadane's algorithm is better than brute force."
    },


    # ======================================================
    # PROJECT
    # ======================================================

    {
        "category": "Project",
        "topic": "Overview",
        "difficulty": "Easy",
        "question": "Explain your project.",
        "answer": """
Structure:

1. Project name.
2. Problem statement.
3. Proposed solution.
4. Technologies used.
5. Architecture.
6. Your contribution.
7. Features.
8. Challenges.
9. Result.
""",
        "tip": "Prepare a 60-second and a 3-minute project explanation."
    },

    {
        "category": "Project",
        "topic": "Architecture",
        "difficulty": "Medium",
        "question": "Explain the architecture of your project.",
        "answer": """
Example flow:

User
↓
Frontend
↓
Backend/API
↓
Business Logic
↓
Database or AI Layer
↓
Response
↓
Frontend

Explain how each component communicates.
""",
        "tip": "Draw the architecture if possible."
    },

    {
        "category": "Project",
        "topic": "Technology",
        "difficulty": "Medium",
        "question": "Why did you choose your technology stack?",
        "answer": """
For each technology explain:

• What requirement it solves.
• Why it was appropriate.
• Advantages.
• Alternatives considered.
• Why you selected it.
""",
        "tip": "Do not say you chose it only because it was easy."
    },

    {
        "category": "Project",
        "topic": "Contribution",
        "difficulty": "Medium",
        "question": "What was your individual contribution to the project?",
        "answer": """
Explain exactly what you developed:

• Features
• APIs
• Database work
• UI modules
• Testing
• Deployment
• Integration
""",
        "tip": "Be precise about your own contribution."
    },

    {
        "category": "Project",
        "topic": "Challenges",
        "difficulty": "Medium",
        "question": "What was the biggest technical challenge in your project?",
        "answer": """
Explain:

Problem
↓
Root Cause
↓
Solutions Considered
↓
Solution Selected
↓
Implementation
↓
Result
↓
Learning
""",
        "tip": "Choose a real technical challenge."
    },

    {
        "category": "Project",
        "topic": "Database",
        "difficulty": "Medium",
        "question": "How did you design your project's database?",
        "answer": """
Discuss:

• Main entities
• Relationships
• Primary keys
• Foreign keys
• Data types
• Validation
• Indexing
• Why SQL or NoSQL was selected
""",
        "tip": "Know your project database schema."
    },

    {
        "category": "Project",
        "topic": "API",
        "difficulty": "Medium",
        "question": "How does your frontend communicate with your backend?",
        "answer": """
Frontend sends an HTTP request.

Backend:

• Receives request
• Validates input
• Runs business logic
• Communicates with database
• Returns JSON response

Frontend processes the response and updates the UI.
""",
        "tip": "Mention actual endpoints from your project."
    },

    {
        "category": "Project",
        "topic": "Security",
        "difficulty": "Hard",
        "question": "How did you secure your application?",
        "answer": """
Possible measures:

• Password hashing
• Authentication
• Authorization
• Input validation
• Protected APIs
• Environment variables
• HTTPS
• Database access controls
""",
        "tip": "Only mention security features you actually implemented."
    },

    {
        "category": "Project",
        "topic": "Testing",
        "difficulty": "Medium",
        "question": "How did you test your project?",
        "answer": """
Discuss:

• Manual testing
• Unit testing
• Integration testing
• API testing
• Validation testing
• Edge cases
• Error handling
""",
        "tip": "Mention tools such as Postman when relevant."
    },

    {
        "category": "Project",
        "topic": "Improvement",
        "difficulty": "Medium",
        "question": "If you had more time, what would you improve in your project?",
        "answer": """
Possible improvements:

• Better scalability
• Improved UI/UX
• More testing
• Cloud deployment
• Better security
• Performance optimization
• New features
• Monitoring
""",
        "tip": "This shows that you understand the limitations of your project."
    },


    # ======================================================
    # BEHAVIORAL
    # ======================================================

    {
        "category": "Behavioral",
        "topic": "Conflict",
        "difficulty": "Medium",
        "question": "Tell me about a conflict you had with a teammate.",
        "answer": """
Use STAR.

Focus on:

• Understanding both viewpoints.
• Professional communication.
• Finding common ground.
• Solving the problem.
• Maintaining a positive relationship.
""",
        "tip": "Never attack your teammate."
    },

    {
        "category": "Behavioral",
        "topic": "Deadline",
        "difficulty": "Medium",
        "question": "What would you do if you could not meet a deadline?",
        "answer": """
1. Evaluate remaining work.
2. Prioritize important tasks.
3. Identify blockers.
4. Communicate early.
5. Ask for support.
6. Agree on a recovery plan.
""",
        "tip": "Communicate before the deadline."
    },

    {
        "category": "Behavioral",
        "topic": "Teamwork",
        "difficulty": "Medium",
        "question": "How would you handle a teammate who is not contributing?",
        "answer": """
First speak privately with the teammate.

Understand whether there are:

• Technical difficulties
• Unclear responsibilities
• Personal constraints

Offer support and clarify expectations.

Escalate professionally only if necessary.
""",
        "tip": "Show empathy and accountability."
    },

    {
        "category": "Behavioral",
        "topic": "Learning",
        "difficulty": "Medium",
        "question": "Your manager gives you a technology you have never used. What would you do?",
        "answer": """
1. Understand the requirement.
2. Learn fundamentals.
3. Read documentation.
4. Build a small proof of concept.
5. Ask focused questions when blocked.
6. Apply learning to the real task.
""",
        "tip": "Companies value independent learning."
    },

    {
        "category": "Behavioral",
        "topic": "Feedback",
        "difficulty": "Medium",
        "question": "How do you handle criticism?",
        "answer": """
I treat constructive criticism as feedback.

I would:

• Listen carefully.
• Avoid becoming defensive.
• Ask questions.
• Identify improvements.
• Implement feedback.
• Review progress.
""",
        "tip": "Give an example where feedback improved your work."
    },

    {
        "category": "Behavioral",
        "topic": "Prioritization",
        "difficulty": "Medium",
        "question": "How do you prioritize multiple tasks?",
        "answer": """
Consider:

• Importance
• Deadline
• Dependencies
• Effort
• Risk

Then create a prioritized task list.
""",
        "tip": "Mention how you track your tasks."
    },

    {
        "category": "Behavioral",
        "topic": "Initiative",
        "difficulty": "Medium",
        "question": "Tell me about a time you took initiative.",
        "answer": """
Use STAR.

Examples:

• Learning a technology without being asked.
• Fixing a recurring problem.
• Improving a project.
• Helping organize a team.
""",
        "tip": "Highlight the result."
    },

    {
        "category": "Behavioral",
        "topic": "Mistakes",
        "difficulty": "Medium",
        "question": "What would you do if you made a mistake that affected the project?",
        "answer": """
1. Acknowledge the mistake.
2. Determine the impact.
3. Inform relevant people.
4. Fix the issue.
5. Find the root cause.
6. Prevent recurrence.
""",
        "tip": "Ownership is better than hiding mistakes."
    },

    {
        "category": "Behavioral",
        "topic": "Requirements",
        "difficulty": "Hard",
        "question": "What would you do if project requirements were unclear?",
        "answer": """
I would:

• Identify ambiguous requirements.
• Prepare specific questions.
• Discuss them with stakeholders.
• Confirm expected behavior.
• Document decisions.
• Build a small prototype if needed.
• Validate before completing implementation.
""",
        "tip": "Do not guess critical requirements."
    },

    {
        "category": "Behavioral",
        "topic": "Leadership",
        "difficulty": "Hard",
        "question": "Your team disagrees on two technical solutions. How would you decide?",
        "answer": """
Compare solutions using:

• Requirements
• Performance
• Complexity
• Development time
• Maintainability
• Security
• Scalability
• Team expertise

If necessary, build a small proof of concept.
""",
        "tip": "Engineering decisions should be evidence-based."
    },
]


# ==========================================================
# INITIALIZE
# ==========================================================

def initialize_state():

    if "interview_completed" not in st.session_state:
        st.session_state.interview_completed = []

    if "interview_bookmarked" not in st.session_state:
        st.session_state.interview_bookmarked = []

    if "random_interview_question" not in st.session_state:
        st.session_state.random_interview_question = None


# ==========================================================
# QUESTION ID
# ==========================================================

def get_question_id(question):

    return (
        question["category"]
        + "::"
        + question["topic"]
        + "::"
        + question["question"]
    )


# ==========================================================
# DIFFICULTY
# ==========================================================

def difficulty_icon(level):

    return {
        "Easy": "🟢",
        "Medium": "🟡",
        "Hard": "🔴",
    }.get(level, "⚪")


# ==========================================================
# RENDER
# ==========================================================

def render():

    apply_college_theme()

    initialize_state()


    # ======================================================
    # HERO
    # ======================================================

    st.html(
        """
<div class="college-hero">

    <div class="college-hero-badge">
        🎤 COLLEGE INTERVIEW PREPARATION
    </div>

    <div class="college-hero-title">
        Interview Preparation
    </div>

    <div class="college-hero-description">
        Prepare HR, technical, coding, project and behavioral
        questions with structured answer guides and interview tips.
    </div>

</div>
"""
    )


    # ======================================================
    # METRICS
    # ======================================================

    total = len(INTERVIEW_QUESTIONS)

    completed_count = len(
        st.session_state.interview_completed
    )

    bookmarked_count = len(
        st.session_state.interview_bookmarked
    )

    progress = (
        round(
            completed_count
            / total
            * 100
        )
        if total
        else 0
    )


    st.html(
        f"""
<div class="college-metric-grid">

    <div class="college-metric-card">

        <div class="college-metric-icon">
            🎤
        </div>

        <div class="college-metric-label">
            Question Bank
        </div>

        <div class="college-metric-value">
            {total}
        </div>

        <div class="college-metric-caption">
            Placement interview questions
        </div>

    </div>


    <div class="college-metric-card">

        <div class="college-metric-icon">
            ✅
        </div>

        <div class="college-metric-label">
            Prepared
        </div>

        <div class="college-metric-value">
            {completed_count}
        </div>

        <div class="college-metric-caption">
            Questions completed
        </div>

    </div>


    <div class="college-metric-card">

        <div class="college-metric-icon">
            🔖
        </div>

        <div class="college-metric-label">
            Bookmarked
        </div>

        <div class="college-metric-value">
            {bookmarked_count}
        </div>

        <div class="college-metric-caption">
            Saved for revision
        </div>

    </div>


    <div class="college-metric-card">

        <div class="college-metric-icon">
            📈
        </div>

        <div class="college-metric-label">
            Progress
        </div>

        <div class="college-metric-value">
            {progress}%
        </div>

        <div class="college-metric-caption">
            Interview preparation
        </div>

    </div>

</div>
"""
    )


    st.progress(
        progress / 100
    )


    # ======================================================
    # CATEGORY SUMMARY
    # ======================================================

    st.html(
        """
<div class="college-section-header">

    <div>

        <div class="college-section-title">
            📚 Interview Areas
        </div>

        <div class="college-section-subtitle">
            Prepare across every major placement interview area.
        </div>

    </div>

    <div class="college-section-tag">
        Placement Preparation
    </div>

</div>
"""
    )


    category_names = [
        ("👔", "HR Interview"),
        ("💻", "Technical"),
        ("🧑‍💻", "Coding"),
        ("🚀", "Project"),
        ("🧠", "Behavioral"),
    ]


    category_columns = st.columns(5)


    for column, (
        icon,
        category_name,
    ) in zip(
        category_columns,
        category_names,
    ):

        category_count = sum(
            1
            for question
            in INTERVIEW_QUESTIONS
            if question["category"] == category_name
        )


        with column:

            st.markdown(
                f"""
<div style="
    background:#ffffff;
    border:1px solid #e2e8f0;
    border-radius:18px;
    padding:20px;
    min-height:130px;
    box-shadow:0 8px 24px rgba(15,23,42,.04);
">

    <div style="
        font-size:25px;
        margin-bottom:10px;
    ">
        {icon}
    </div>

    <div style="
        color:#0f172a;
        font-size:14px;
        font-weight:800;
    ">
        {category_name}
    </div>

    <div style="
        color:#64748b;
        font-size:12px;
        margin-top:7px;
    ">
        {category_count} questions
    </div>

</div>
""",
                unsafe_allow_html=True,
            )


    # ======================================================
    # RANDOM PRACTICE
    # ======================================================

    st.html(
        """
<div class="college-section-header">

    <div>

        <div class="college-section-title">
            ⚡ Quick Practice
        </div>

        <div class="college-section-subtitle">
            Pick a random interview question for instant practice.
        </div>

    </div>

</div>
"""
    )


    if st.button(
        "🎲 Give Me a Random Question",
        use_container_width=True,
        key="random_interview_question_button",
    ):

        st.session_state.random_interview_question = (
            random.choice(
                INTERVIEW_QUESTIONS
            )
        )


    random_question = (
        st.session_state.random_interview_question
    )


    if random_question:

        st.info(
            (
                f'{difficulty_icon(random_question["difficulty"])} '
                f'**{random_question["category"]} • '
                f'{random_question["difficulty"]}**\n\n'
                f'### {random_question["question"]}'
            )
        )


    # ======================================================
    # FILTERS
    # ======================================================

    st.html(
        """
<div class="college-section-header">

    <div>

        <div class="college-section-title">
            🔍 Question Bank
        </div>

        <div class="college-section-subtitle">
            Search and filter your interview preparation questions.
        </div>

    </div>

</div>
"""
    )


    filter1, filter2, filter3 = st.columns(3)


    categories = [
        "All",
        "HR Interview",
        "Technical",
        "Coding",
        "Project",
        "Behavioral",
    ]


    difficulties = [
        "All",
        "Easy",
        "Medium",
        "Hard",
    ]


    topics = sorted(
        {
            question["topic"]
            for question in INTERVIEW_QUESTIONS
        }
    )


    with filter1:

        selected_category = st.selectbox(
            "Category",
            categories,
            key="interview_filter_category",
        )


    with filter2:

        selected_difficulty = st.selectbox(
            "Difficulty",
            difficulties,
            key="interview_filter_difficulty",
        )


    with filter3:

        selected_topic = st.selectbox(
            "Topic",
            [
                "All",
                *topics,
            ],
            key="interview_filter_topic",
        )


    search_text = st.text_input(
        "Search",
        placeholder=(
            "Search OOP, SQL, API, HR, project, arrays..."
        ),
        key="interview_search_box",
    )


    # ======================================================
    # FILTER QUESTIONS
    # ======================================================

    filtered_questions = []


    for question in INTERVIEW_QUESTIONS:

        if (
            selected_category != "All"
            and
            question["category"]
            != selected_category
        ):
            continue


        if (
            selected_difficulty != "All"
            and
            question["difficulty"]
            != selected_difficulty
        ):
            continue


        if (
            selected_topic != "All"
            and
            question["topic"]
            != selected_topic
        ):
            continue


        if search_text.strip():

            keyword = search_text.strip().lower()

            searchable_text = (
                question["question"]
                + " "
                + question["category"]
                + " "
                + question["topic"]
            ).lower()

            if keyword not in searchable_text:
                continue


        filtered_questions.append(
            question
        )


    # ======================================================
    # SHOW COUNT
    # ======================================================

    st.caption(
        (
            f"Showing {len(filtered_questions)} "
            f"of {total} interview questions"
        )
    )


    # ======================================================
    # QUESTION CARDS
    # ======================================================

    for index, question in enumerate(
        filtered_questions,
        start=1,
    ):

        question_key = get_question_id(
            question
        )


        is_completed = (
            question_key
            in st.session_state.interview_completed
        )


        is_bookmarked = (
            question_key
            in st.session_state.interview_bookmarked
        )


        status_text = (
            "✅ Prepared"
            if is_completed
            else "⏳ Not Prepared"
        )


        # IMPORTANT:
        # unsafe_allow_html=True prevents the HTML from
        # displaying as raw source code.

        st.markdown(
            f"""
<div style="
    background:#ffffff;
    border:1px solid #e2e8f0;
    border-radius:20px;
    padding:22px 24px;
    margin-top:16px;
    box-shadow:0 8px 24px rgba(15,23,42,.04);
">

    <div style="
        color:#4f46e5;
        font-size:11px;
        font-weight:900;
        letter-spacing:1px;
    ">
        QUESTION {index:02d}
    </div>

    <div style="
        color:#0f172a;
        font-size:18px;
        line-height:1.5;
        font-weight:800;
        margin-top:9px;
    ">
        {question["question"]}
    </div>

    <div style="
        color:#64748b;
        font-size:12px;
        line-height:1.7;
        margin-top:10px;
    ">

        {difficulty_icon(question["difficulty"])}
        {question["category"]}

        &nbsp; • &nbsp;

        {question["topic"]}

        &nbsp; • &nbsp;

        {question["difficulty"]}

        &nbsp; • &nbsp;

        {status_text}

    </div>

</div>
""",
            unsafe_allow_html=True,
        )


        # ==================================================
        # ANSWER GUIDE
        # ==================================================

        with st.expander(
            "💡 Show Answer Guide",
            expanded=False,
        ):

            st.markdown(
                "### ✅ Answer Guide"
            )

            st.markdown(
                question["answer"]
            )


            st.markdown(
                f"""
<div style="
    background:#fff7ed;
    border:1px solid #fed7aa;
    border-radius:14px;
    padding:15px 17px;
    margin-top:14px;
">

    <div style="
        color:#9a3412;
        font-size:13px;
        font-weight:800;
    ">
        💡 Interview Tip
    </div>

    <div style="
        color:#7c2d12;
        font-size:13px;
        line-height:1.6;
        margin-top:6px;
    ">
        {question["tip"]}
    </div>

</div>
""",
                unsafe_allow_html=True,
            )


            st.write("")


            action1, action2 = st.columns(2)


            # ==============================================
            # COMPLETE
            # ==============================================

            with action1:

                if not is_completed:

                    if st.button(
                        "✅ Mark as Prepared",
                        key=(
                            f"interview_complete_"
                            f"{index}_"
                            f"{abs(hash(question_key))}"
                        ),
                        use_container_width=True,
                    ):

                        st.session_state.interview_completed.append(
                            question_key
                        )

                        st.rerun()


                else:

                    if st.button(
                        "↩ Mark as Not Prepared",
                        key=(
                            f"interview_uncomplete_"
                            f"{index}_"
                            f"{abs(hash(question_key))}"
                        ),
                        use_container_width=True,
                    ):

                        st.session_state.interview_completed.remove(
                            question_key
                        )

                        st.rerun()


            # ==============================================
            # BOOKMARK
            # ==============================================

            with action2:

                if not is_bookmarked:

                    if st.button(
                        "🔖 Save for Revision",
                        key=(
                            f"interview_bookmark_"
                            f"{index}_"
                            f"{abs(hash(question_key))}"
                        ),
                        use_container_width=True,
                    ):

                        st.session_state.interview_bookmarked.append(
                            question_key
                        )

                        st.rerun()


                else:

                    if st.button(
                        "❌ Remove Bookmark",
                        key=(
                            f"interview_unbookmark_"
                            f"{index}_"
                            f"{abs(hash(question_key))}"
                        ),
                        use_container_width=True,
                    ):

                        st.session_state.interview_bookmarked.remove(
                            question_key
                        )

                        st.rerun()


    # ======================================================
    # NO RESULTS
    # ======================================================

    if not filtered_questions:

        st.warning(
            "No interview questions match the selected filters."
        )


    # ======================================================
    # BOOKMARKED QUESTIONS
    # ======================================================

    if st.session_state.interview_bookmarked:

        st.html(
            """
<div class="college-section-header">

    <div>

        <div class="college-section-title">
            🔖 Saved for Revision
        </div>

        <div class="college-section-subtitle">
            Quickly revise your bookmarked interview questions.
        </div>

    </div>

</div>
"""
        )


        for question in INTERVIEW_QUESTIONS:

            question_key = get_question_id(
                question
            )


            if (
                question_key
                not in st.session_state.interview_bookmarked
            ):
                continue


            with st.expander(
                f'🔖 {question["question"]}'
            ):

                st.caption(
                    (
                        f'{question["category"]} • '
                        f'{question["topic"]} • '
                        f'{question["difficulty"]}'
                    )
                )

                st.markdown(
                    question["answer"]
                )

                st.info(
                    "💡 " + question["tip"]
                )


    # ======================================================
    # STRATEGY
    # ======================================================

    st.html(
        """
<div class="college-section-header">

    <div>

        <div class="college-section-title">
            🗓️ Preparation Strategy
        </div>

        <div class="college-section-subtitle">
            Follow this sequence before your placement interviews.
        </div>

    </div>

</div>
"""
    )


    strategy1, strategy2, strategy3 = st.columns(3)


    with strategy1:

        st.markdown(
            """
<div style="
    background:#eef2ff;
    border:1px solid #e0e7ff;
    border-radius:20px;
    padding:22px;
    min-height:180px;
">

    <div style="font-size:25px;">
        📘
    </div>

    <div style="
        color:#0f172a;
        font-size:17px;
        font-weight:800;
        margin-top:12px;
    ">
        1. Revise Fundamentals
    </div>

    <div style="
        color:#64748b;
        font-size:12px;
        line-height:1.7;
        margin-top:9px;
    ">
        Prepare OOP, DBMS, SQL, OS, Networks,
        DSA, APIs and your programming language.
    </div>

</div>
""",
            unsafe_allow_html=True,
        )


    with strategy2:

        st.markdown(
            """
<div style="
    background:#ecfdf5;
    border:1px solid #d1fae5;
    border-radius:20px;
    padding:22px;
    min-height:180px;
">

    <div style="font-size:25px;">
        💻
    </div>

    <div style="
        color:#0f172a;
        font-size:17px;
        font-weight:800;
        margin-top:12px;
    ">
        2. Practice Coding
    </div>

    <div style="
        color:#64748b;
        font-size:12px;
        line-height:1.7;
        margin-top:9px;
    ">
        Practice arrays, strings, searching,
        sorting, hashing, stacks and linked lists.
    </div>

</div>
""",
            unsafe_allow_html=True,
        )


    with strategy3:

        st.markdown(
            """
<div style="
    background:#fff7ed;
    border:1px solid #ffedd5;
    border-radius:20px;
    padding:22px;
    min-height:180px;
">

    <div style="font-size:25px;">
        🎤
    </div>

    <div style="
        color:#0f172a;
        font-size:17px;
        font-weight:800;
        margin-top:12px;
    ">
        3. Take Mock Interviews
    </div>

    <div style="
        color:#64748b;
        font-size:12px;
        line-height:1.7;
        margin-top:9px;
    ">
        Practice speaking answers clearly,
        explain your projects and improve confidence.
    </div>

</div>
""",
            unsafe_allow_html=True,
        )