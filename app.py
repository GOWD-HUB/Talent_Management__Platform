import streamlit as st
import plotly.express as px
import pandas as pd
import sqlite3
import hashlib
import json
import random
import re
import base64
import urllib.error
import urllib.parse
import urllib.request
from io import BytesIO
from pathlib import Path
from datetime import date, datetime, timezone

try:
    from pypdf import PdfReader
except ImportError:
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        PdfReader = None


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="TalentSphere Elevate",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_NAME = DATABASE_DIR / "talentsphere.db"

UPLOADS_DIR = BASE_DIR / "uploads"
LINKEDIN_PDF_DIR = UPLOADS_DIR / "linkedin_profiles"
LINKEDIN_PDF_DIR.mkdir(parents=True, exist_ok=True)


def get_connection():
    connection = sqlite3.connect(
        str(DATABASE_NAME),
        check_same_thread=False
    )
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def migrate_old_users_table(cursor):
    """Convert the older users schema to the current schema automatically."""

    cursor.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type='table' AND name='users'"
    )

    if cursor.fetchone() is None:
        return

    cursor.execute("PRAGMA table_info(users)")
    columns = {
        row[1]
        for row in cursor.fetchall()
    }

    required_columns = {
        "id",
        "fullname",
        "email",
        "password",
        "role",
        "created_at"
    }

    if required_columns.issubset(columns):
        return

    fullname_column = (
        "fullname"
        if "fullname" in columns
        else "full_name"
        if "full_name" in columns
        else None
    )

    role_column = (
        "role"
        if "role" in columns
        else "category"
        if "category" in columns
        else None
    )

    if not fullname_column or not role_column:
        cursor.execute("DROP TABLE users")
        return

    cursor.execute("ALTER TABLE users RENAME TO users_old")

    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    old_columns = {
        row[1]
        for row in cursor.execute(
            "PRAGMA table_info(users_old)"
        ).fetchall()
    }

    created_expression = (
        "created_at"
        if "created_at" in old_columns
        else "datetime('now')"
    )

    cursor.execute(f"""
        INSERT OR IGNORE INTO users (
            id,
            fullname,
            email,
            password,
            role,
            created_at
        )
        SELECT
            id,
            {fullname_column},
            email,
            password,
            {role_column},
            {created_expression}
        FROM users_old
    """)

    cursor.execute("DROP TABLE users_old")


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    migrate_old_users_table(cursor)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS school_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            school_name TEXT,
            current_class TEXT,
            board TEXT,
            city TEXT,
            parent_name TEXT,
            phone TEXT,
            favourite_subjects TEXT,
            interests TEXT,
            skills TEXT,
            dream_career TEXT,
            academic_goal TEXT,
            achievements TEXT,
            updated_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS college_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            college_name TEXT,
            degree TEXT,
            branch TEXT,
            current_year TEXT,
            semester TEXT,
            university TEXT,
            city TEXT,
            phone TEXT,
            cgpa REAL,
            backlogs INTEGER DEFAULT 0,
            technical_skills TEXT,
            programming_languages TEXT,
            tools TEXT,
            certifications TEXT,
            projects TEXT,
            internships TEXT,
            career_goal TEXT,
            preferred_role TEXT,
            preferred_location TEXT,
            linkedin_url TEXT,
            linkedin_pdf_path TEXT,
            github_url TEXT,
            portfolio_url TEXT,
            resume_path TEXT,
            placement_status TEXT,
            updated_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Add LinkedIn PDF support to databases created by older versions.
    cursor.execute("PRAGMA table_info(college_profiles)")
    college_profile_columns = {
        row[1]
        for row in cursor.fetchall()
    }

    if "linkedin_pdf_path" not in college_profile_columns:
        cursor.execute(
            "ALTER TABLE college_profiles "
            "ADD COLUMN linkedin_pdf_path TEXT"
        )

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professional_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            current_company TEXT,
            current_role TEXT,
            department TEXT,
            total_experience REAL DEFAULT 0,
            employment_type TEXT,
            current_location TEXT,
            work_mode TEXT,
            phone TEXT,
            highest_qualification TEXT,
            technical_skills TEXT,
            programming_languages TEXT,
            frameworks TEXT,
            databases TEXT,
            cloud_platforms TEXT,
            devops_tools TEXT,
            certifications TEXT,
            leadership_experience TEXT,
            team_size INTEGER DEFAULT 0,
            projects_led INTEGER DEFAULT 0,
            mentoring_experience TEXT,
            communication_level TEXT,
            career_goal TEXT,
            preferred_roles TEXT,
            target_company TEXT,
            preferred_location TEXT,
            current_salary REAL DEFAULT 0,
            expected_salary REAL DEFAULT 0,
            notice_period TEXT,
            linkedin_url TEXT,
            github_url TEXT,
            portfolio_url TEXT,
            updated_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            target_date TEXT,
            priority TEXT,
            progress INTEGER DEFAULT 0,
            created_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            quiz_type TEXT NOT NULL,
            result TEXT,
            score INTEGER,
            completed_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coding_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            topic TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            score INTEGER NOT NULL,
            completed_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS placement_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            application_date TEXT,
            status TEXT,
            next_round TEXT,
            notes TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mock_interview_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            interview_type TEXT NOT NULL,
            score INTEGER NOT NULL,
            feedback TEXT,
            completed_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_match_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            match_score INTEGER NOT NULL,
            reasons TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professional_skill_assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            target_role TEXT,
            backend_score INTEGER NOT NULL,
            system_design_score INTEGER NOT NULL,
            cloud_score INTEGER NOT NULL,
            devops_score INTEGER NOT NULL,
            leadership_score INTEGER NOT NULL,
            communication_score INTEGER NOT NULL,
            overall_score INTEGER NOT NULL,
            readiness_level TEXT NOT NULL,
            answers_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    connection.commit()
    connection.close()


create_tables()


# ==========================================================
# LINKEDIN PDF FILE FUNCTIONS
# ==========================================================

def safe_pdf_filename(filename):
    """Return a filesystem-safe PDF filename."""
    original_name = Path(filename or "linkedin_profile.pdf").name
    stem = re.sub(r"[^A-Za-z0-9_-]+", "_", Path(original_name).stem)
    stem = stem.strip("_") or "linkedin_profile"
    return f"{stem}.pdf"


def save_linkedin_pdf(uploaded_file, user_id):
    """Save a student's LinkedIn profile PDF and return its relative path."""
    if uploaded_file is None:
        return ""

    if uploaded_file.type != "application/pdf":
        raise ValueError("Only PDF files are supported.")

    safe_name = safe_pdf_filename(uploaded_file.name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stored_name = f"user_{user_id}_{timestamp}_{safe_name}"
    destination = LINKEDIN_PDF_DIR / stored_name

    destination.write_bytes(uploaded_file.getvalue())

    return str(destination.relative_to(BASE_DIR))


def get_existing_pdf_bytes(relative_path):
    """Read a previously saved LinkedIn PDF when it still exists."""
    if not relative_path:
        return None

    file_path = BASE_DIR / relative_path

    if not file_path.exists() or not file_path.is_file():
        return None

    return file_path.read_bytes()


def extract_pdf_text(pdf_bytes):
    """Extract text from a PDF and return text, page count and an error."""
    if PdfReader is None:
        return "", 0, (
            "PDF reader library is missing. Install it with: pip install pypdf"
        )

    try:
        reader = PdfReader(BytesIO(pdf_bytes))
        page_text = []

        for page in reader.pages:
            page_text.append(page.extract_text() or "")

        return "\n".join(page_text).strip(), len(reader.pages), None

    except Exception as error:
        return "", 0, f"Unable to read this PDF: {error}"


def find_any(text, keywords):
    """Return True when one or more keywords occur in the extracted text."""
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def analyze_linkedin_pdf(pdf_bytes):
    """Evaluate an exported LinkedIn profile PDF using its extracted text."""
    text, page_count, error = extract_pdf_text(pdf_bytes)

    if error:
        return None, error

    clean_text = re.sub(r"\s+", " ", text).strip()
    lowered = clean_text.lower()
    word_count = len(clean_text.split())

    checks = []

    def add_check(name, passed, points, feedback):
        checks.append({
            "Section": name,
            "Status": "Found" if passed else "Missing / Weak",
            "Points": points if passed else 0,
            "Maximum": points,
            "Feedback": feedback
        })

    # LinkedIn PDF exports commonly contain these visible section labels.
    add_check(
        "Headline / Role Focus",
        find_any(
            clean_text,
            [
                "software developer",
                "software engineer",
                "data analyst",
                "data scientist",
                "machine learning",
                "artificial intelligence",
                "full stack",
                "web developer",
                "student at",
                "aspiring"
            ]
        ),
        12,
        "Use a clear target-role headline near your name."
    )

    add_check(
        "About / Summary",
        find_any(clean_text, ["about", "summary", "profile"]),
        12,
        "Add an About section with skills, interests and career direction."
    )

    add_check(
        "Education",
        find_any(
            clean_text,
            [
                "education",
                "b.tech",
                "btech",
                "bachelor",
                "university",
                "college",
                "engineering"
            ]
        ),
        12,
        "Include college, degree, branch, dates and CGPA when appropriate."
    )

    add_check(
        "Skills",
        find_any(
            clean_text,
            [
                "skills",
                "python",
                "java",
                "c++",
                "sql",
                "javascript",
                "react",
                "node.js",
                "machine learning"
            ]
        ),
        12,
        "Add relevant technical and professional skills."
    )

    add_check(
        "Projects",
        find_any(
            clean_text,
            [
                "projects",
                "project",
                "github",
                "developed",
                "built",
                "implemented"
            ]
        ),
        12,
        "Add two or more projects with technologies, contribution and outcome."
    )

    add_check(
        "Experience / Internship",
        find_any(
            clean_text,
            [
                "experience",
                "internship",
                "intern",
                "employment",
                "trainee"
            ]
        ),
        10,
        "Add internships, training or practical experience."
    )

    add_check(
        "Certifications",
        find_any(
            clean_text,
            [
                "licenses & certifications",
                "certifications",
                "certificate",
                "certified",
                "nptel",
                "coursera",
                "udemy",
                "infosys springboard"
            ]
        ),
        8,
        "Add relevant certifications with issuer and completion date."
    )

    add_check(
        "Contact Information",
        bool(
            re.search(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", clean_text, re.I)
            or re.search(r"(?:\+?91[-\s]?)?[6-9]\d{9}", clean_text)
        ),
        8,
        "Include a professional email and reachable phone number."
    )

    quantified = bool(
        re.search(
            r"\b\d+(?:\.\d+)?\s*(?:%|users?|projects?|months?|years?|"
            r"hours?|students?|clients?|records?|accuracy|downloads?)\b",
            lowered
        )
    )

    add_check(
        "Measurable Achievements",
        quantified,
        8,
        "Use numbers to show impact, such as accuracy, users, time saved or results."
    )

    add_check(
        "Profile Detail",
        word_count >= 250,
        6,
        "The exported profile is brief. Add more meaningful detail to key sections."
    )

    score = sum(item["Points"] for item in checks)
    maximum = sum(item["Maximum"] for item in checks)
    score = round(score / maximum * 100) if maximum else 0

    strengths = [
        item["Section"]
        for item in checks
        if item["Status"] == "Found"
    ]

    improvements = [
        item["Feedback"]
        for item in checks
        if item["Status"] != "Found"
    ]

    if word_count < 80:
        improvements.insert(
            0,
            "Very little text was extracted. Export the complete LinkedIn profile "
            "using Print → Save as PDF and upload it again."
        )

    return {
        "score": score,
        "text": clean_text,
        "page_count": page_count,
        "word_count": word_count,
        "checks": checks,
        "strengths": strengths,
        "improvements": improvements
    }, None



# ==========================================================
# AUTOMATIC GITHUB PORTFOLIO ANALYSER
# ==========================================================

GITHUB_API_BASE = "https://api.github.com"


def normalise_github_username(value):
    """Return a username from either a username or GitHub profile URL."""
    value = (value or "").strip().rstrip("/")

    if not value:
        return ""

    if "github.com/" in value.lower():
        parsed = urllib.parse.urlparse(
            value if "://" in value else f"https://{value}"
        )
        parts = [part for part in parsed.path.split("/") if part]
        return parts[0] if parts else ""

    return value.lstrip("@")


def github_api_get(endpoint):
    """Read public GitHub API data without requiring an access token."""
    request = urllib.request.Request(
        f"{GITHUB_API_BASE}{endpoint}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "TalentSphere-Elevate",
            "X-GitHub-Api-Version": "2022-11-28"
        }
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return json.loads(response.read().decode("utf-8")), None

    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None, "GitHub profile was not found."

        if error.code == 403:
            return None, (
                "GitHub API limit reached. Wait for some time and try again."
            )

        return None, f"GitHub API returned error {error.code}."

    except urllib.error.URLError:
        return None, (
            "Unable to connect to GitHub. Check your internet connection."
        )

    except Exception as error:
        return None, f"Unable to analyse the profile: {error}"


def github_readme_text(owner, repository):
    """Return decoded README content for a public repository."""
    payload, error = github_api_get(
        f"/repos/{owner}/{repository}/readme"
    )

    if error or not payload or not payload.get("content"):
        return ""

    try:
        return base64.b64decode(
            payload["content"]
        ).decode("utf-8", errors="ignore")
    except Exception:
        return ""


def github_days_since(timestamp):
    """Calculate days since a GitHub ISO timestamp."""
    if not timestamp:
        return None

    try:
        parsed = datetime.fromisoformat(
            timestamp.replace("Z", "+00:00")
        )
        return max(
            (datetime.now(timezone.utc) - parsed).days,
            0
        )
    except (TypeError, ValueError):
        return None


def analyse_github_portfolio(username):
    """Automatically score a public GitHub profile and its repositories."""
    encoded_username = urllib.parse.quote(username)

    profile, profile_error = github_api_get(
        f"/users/{encoded_username}"
    )

    if profile_error:
        return None, profile_error

    repositories, repository_error = github_api_get(
        f"/users/{encoded_username}/repos"
        "?per_page=100&sort=updated&type=owner"
    )

    if repository_error:
        return None, repository_error

    repositories = [
        repository
        for repository in (repositories or [])
        if not repository.get("fork")
    ]

    analysed = repositories[:12]
    rows = []
    languages = {}
    readmes = 0
    detailed_readmes = 0
    recent_projects = 0
    descriptions = 0
    live_links = 0
    topics_count = 0
    stars = 0
    strongest = None
    strongest_score = -1

    for repository in analysed:
        name = repository.get("name", "")
        language = repository.get("language") or "Not specified"
        description = (repository.get("description") or "").strip()
        homepage = (repository.get("homepage") or "").strip()
        topics = repository.get("topics") or []
        repository_stars = int(
            repository.get("stargazers_count") or 0
        )
        days = github_days_since(
            repository.get("pushed_at")
            or repository.get("updated_at")
        )

        readme = github_readme_text(username, name)
        readme_words = len(readme.split())
        has_readme = bool(readme.strip())

        if language != "Not specified":
            languages[language] = languages.get(language, 0) + 1

        if has_readme:
            readmes += 1

        if readme_words >= 80:
            detailed_readmes += 1

        if description:
            descriptions += 1

        if homepage:
            live_links += 1

        if topics:
            topics_count += 1

        if days is not None and days <= 90:
            recent_projects += 1

        stars += repository_stars

        quality = (
            (20 if description else 0)
            + (20 if has_readme else 0)
            + (15 if readme_words >= 80 else 0)
            + (15 if homepage else 0)
            + (10 if topics else 0)
            + (10 if language != "Not specified" else 0)
            + (10 if days is not None and days <= 90 else 0)
        )

        if quality > strongest_score:
            strongest_score = quality
            strongest = repository

        rows.append({
            "Repository": name,
            "Language": language,
            "README": (
                "Detailed"
                if readme_words >= 80
                else "Present"
                if has_readme
                else "Missing"
            ),
            "Description": "Yes" if description else "No",
            "Live Demo": "Yes" if homepage else "No",
            "Stars": repository_stars,
            "Updated": (
                f"{days} day(s) ago"
                if days is not None
                else "Unknown"
            ),
            "URL": repository.get("html_url", "")
        })

    repository_count = len(repositories)
    analysed_count = len(analysed)
    score = 0
    strengths = []
    suggestions = []

    # Profile completeness: 20 points.
    if profile.get("name"):
        score += 4
        strengths.append("Professional display name is present.")
    else:
        suggestions.append("Add your full professional name.")

    if profile.get("bio"):
        score += 6
        strengths.append("Profile contains a professional bio.")
    else:
        suggestions.append(
            "Add a short bio with your role, skills and career goal."
        )

    if profile.get("location"):
        score += 3
    else:
        suggestions.append("Add your location.")

    if profile.get("blog"):
        score += 4
        strengths.append("Portfolio or professional link is available.")
    else:
        suggestions.append(
            "Add a portfolio, LinkedIn or deployed project link."
        )

    if profile.get("avatar_url"):
        score += 3

    # Repository strength: 20 points.
    if repository_count >= 6:
        score += 20
        strengths.append(
            f"Profile contains {repository_count} original repositories."
        )
    elif repository_count >= 3:
        score += 15
        strengths.append(
            f"Profile contains {repository_count} original repositories."
        )
    elif repository_count >= 1:
        score += 8
        suggestions.append(
            "Upload at least three strong projects."
        )
    else:
        suggestions.append(
            "Create repositories for your best coding projects."
        )

    # Documentation: 20 points.
    readme_ratio = (
        readmes / analysed_count
        if analysed_count
        else 0
    )
    detailed_ratio = (
        detailed_readmes / analysed_count
        if analysed_count
        else 0
    )

    if readme_ratio >= 0.8:
        score += 12
        strengths.append("Most projects contain README files.")
    elif readme_ratio >= 0.5:
        score += 8
        suggestions.append(
            "Add README files to the remaining projects."
        )
    elif readme_ratio > 0:
        score += 4
        suggestions.append(
            "Add clear README files to every important project."
        )
    else:
        suggestions.append(
            "Create README files with features, setup and screenshots."
        )

    if detailed_ratio >= 0.5:
        score += 8
        strengths.append("Several README files are detailed.")
    elif readmes:
        score += 3
        suggestions.append(
            "Improve README files with screenshots and installation steps."
        )

    # Activity: 15 points.
    if recent_projects >= 3:
        score += 15
        strengths.append("Portfolio shows recent project activity.")
    elif recent_projects >= 1:
        score += 9
        suggestions.append("Maintain more regular commit activity.")
    else:
        suggestions.append("Update and contribute to projects regularly.")

    # Professional repository presentation: 15 points.
    description_ratio = (
        descriptions / analysed_count
        if analysed_count
        else 0
    )
    live_ratio = (
        live_links / analysed_count
        if analysed_count
        else 0
    )
    topic_ratio = (
        topics_count / analysed_count
        if analysed_count
        else 0
    )

    if description_ratio >= 0.8:
        score += 6
        strengths.append("Most repositories have clear descriptions.")
    elif description_ratio >= 0.4:
        score += 3
        suggestions.append(
            "Add descriptions to all repositories."
        )
    else:
        suggestions.append(
            "Add one-line descriptions explaining every project."
        )

    if live_ratio >= 0.3:
        score += 5
        strengths.append("Some projects contain live demo links.")
    elif repository_count:
        suggestions.append(
            "Deploy web projects and add live demo links."
        )

    if topic_ratio >= 0.5:
        score += 4
    elif repository_count:
        suggestions.append(
            "Add topics such as python, react, machine-learning or mern."
        )

    # Technology variety and engagement: 10 points.
    if len(languages) >= 3:
        score += 7
        strengths.append(
            "Portfolio demonstrates multiple technologies."
        )
    elif len(languages) >= 1:
        score += 4
        suggestions.append(
            "Add projects demonstrating broader technical skills."
        )
    else:
        suggestions.append(
            "Upload complete source-code projects."
        )

    if stars >= 3:
        score += 3
        strengths.append("Repositories show external engagement.")

    score = min(score, 100)

    if score >= 85:
        readiness = "Excellent"
        summary = (
            "This portfolio is professional and recruiter-ready."
        )
    elif score >= 70:
        readiness = "Good"
        summary = (
            "This is a good student portfolio. Improve documentation, "
            "deployment links and consistency to make it stronger."
        )
    elif score >= 50:
        readiness = "Developing"
        summary = (
            "The profile has a useful foundation but needs stronger "
            "projects, README files and recent activity."
        )
    else:
        readiness = "Needs Improvement"
        summary = (
            "The portfolio is incomplete for recruiter review. Add at "
            "least three complete projects with documentation."
        )

    return {
        "profile": profile,
        "repositories": rows,
        "repository_count": repository_count,
        "analysed_count": analysed_count,
        "languages": sorted(
            languages.items(),
            key=lambda item: item[1],
            reverse=True
        ),
        "readmes": readmes,
        "detailed_readmes": detailed_readmes,
        "recent_projects": recent_projects,
        "live_links": live_links,
        "stars": stars,
        "strongest": strongest,
        "score": score,
        "readiness": readiness,
        "summary": summary,
        "strengths": strengths,
        "suggestions": suggestions
    }, None


# ==========================================================
# PASSWORD FUNCTIONS
# ==========================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(fullname, email, password, role):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO users (
                fullname,
                email,
                password,
                role,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            fullname,
            email.lower(),
            hash_password(password),
            role,
            datetime.now().isoformat()
        ))

        connection.commit()
        return True, "Registration successful."

    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."

    finally:
        connection.close()


def authenticate_user(email, password):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, fullname, email, role
        FROM users
        WHERE email = ? AND password = ?
    """, (
        email.lower(),
        hash_password(password)
    ))

    user = cursor.fetchone()
    connection.close()

    return user


# ==========================================================
# SESSION STATE
# ==========================================================

session_defaults = {
    "logged_in": False,
    "user_id": None,
    "user_name": "",
    "user_email": "",
    "user_role": None,
    "daily_tasks": [
        {
            "task": "Mathematics: revise one topic (30 minutes)",
            "completed": False
        },
        {
            "task": "Science: read one lesson and note key points",
            "completed": False
        },
        {
            "task": "English: grammar or vocabulary practice (20 minutes)",
            "completed": False
        },
        {
            "task": "Complete today's school homework",
            "completed": False
        }
    ],
    "mentor_messages": [],
    "subject_quiz_result": None,
    "interest_result": None,
    "subject_quiz_questions": [],
    "subject_quiz_subject": "",
    "subject_quiz_difficulty": "",
    "college_coding_questions": [],
    "college_coding_result": None,
    "mock_interview_questions": [],
    "mock_interview_result": None,
    "daily_coding_challenge": None,
    "resume_preview": "",
    "professional_navigation": "🏢 Professional Dashboard",
    "professional_learning_track": "Backend Development",
    "professional_learning_quiz_result": None
}

for key, value in session_defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap'
);

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: #F4F7FC;
}

/* Main content typography */
[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3,
[data-testid="stMain"] h4,
[data-testid="stMain"] h5,
[data-testid="stMain"] h6,
[data-testid="stMain"] p,
[data-testid="stMain"] label,
[data-testid="stMain"] .stMarkdown,
[data-testid="stMain"] [data-testid="stWidgetLabel"] {
    color: #111827 !important;
}

/* Streamlit page titles */
[data-testid="stMain"] [data-testid="stHeadingWithActionElements"] h1,
[data-testid="stMain"] [data-testid="stHeadingWithActionElements"] h2,
[data-testid="stMain"] [data-testid="stHeadingWithActionElements"] h3 {
    color: #111827 !important;
}

/* Input text, placeholder text and disabled values */
[data-testid="stMain"] input,
[data-testid="stMain"] textarea {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

[data-testid="stMain"] input::placeholder,
[data-testid="stMain"] textarea::placeholder {
    color: #9CA3AF !important;
    opacity: 1 !important;
}

[data-testid="stMain"] input:disabled,
[data-testid="stMain"] textarea:disabled {
    color: #374151 !important;
    -webkit-text-fill-color: #374151 !important;
    opacity: 1 !important;
}

/* Select boxes and multiselect values */
[data-testid="stMain"] div[data-baseweb="select"] > div,
[data-testid="stMain"] div[data-baseweb="select"] span {
    color: #F9FAFB !important;
}

[data-testid="stMain"] div[data-baseweb="tag"] span {
    color: #111827 !important;
}

section[data-testid="stSidebar"] {
    background: #111827;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.hero {
    background: linear-gradient(135deg, #2563EB, #7C3AED);
    padding: 40px;
    border-radius: 25px;
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, .15);
}

.hero h1 {
    color: white !important;
    font-size: 48px;
    font-weight: 700;
}

.hero p {
    color: white !important;
    font-size: 20px;
}

.card {
    background: white;
    padding: 24px;
    border-radius: 20px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, .08);
    min-height: 220px;
}

.card h2, .card h3 {
    color: #2563EB !important;
}

.metric-card {
    background: white;
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 5px 15px rgba(0, 0, 0, .08);
}

.metric-card h2 {
    color: #2563EB !important;
    font-size: 36px;
    margin-bottom: 0;
}

.metric-card p {
    color: #6B7280 !important;
}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background: white !important;
    color: #111827 !important;
    border-radius: 10px;
}

.stButton button {
    background: #2563EB;
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 600;
}

.stButton button:hover {
    background: #1D4ED8;
    color: white;
}

.stDownloadButton button {
    background: #16A34A;
    color: white;
    border-radius: 12px;
}

.profile-box {
    background: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, .08);
}

.page-title {
    color: #111827 !important;
    font-size: 2.5rem;
    font-weight: 700;
    line-height: 1.2;
    margin: 0 0 1.25rem 0;
}


/* ==========================================================
   QUIZ / RADIO OPTION VISIBILITY
   ========================================================== */

/* Keep quiz question text clearly visible */
[data-testid="stMain"] .stRadio > label,
[data-testid="stMain"] .stRadio [data-testid="stWidgetLabel"] {
    color: #111827 !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
}

/* Turn every radio option into a light card */
[data-testid="stMain"] .stRadio div[role="radiogroup"] > label {
    display: flex !important;
    align-items: center !important;
    gap: 0.65rem !important;
    background: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 12px !important;
    padding: 10px 14px !important;
    margin: 5px 0 !important;
    color: #111827 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}

/* Make all text inside quiz options dark and readable */
[data-testid="stMain"] .stRadio div[role="radiogroup"] > label *,
[data-testid="stMain"] .stRadio div[role="radiogroup"] > label p,
[data-testid="stMain"] .stRadio div[role="radiogroup"] > label span {
    color: #111827 !important;
}

/* Hover effect */
[data-testid="stMain"] .stRadio div[role="radiogroup"] > label:hover {
    background: #EFF6FF !important;
    border-color: #3B82F6 !important;
    box-shadow: 0 3px 10px rgba(37, 99, 235, 0.12) !important;
}

/* Selected option card */
[data-testid="stMain"] .stRadio div[role="radiogroup"] > label:has(input:checked) {
    background: #DBEAFE !important;
    border-color: #2563EB !important;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.12) !important;
}

/* Native radio accent */
[data-testid="stMain"] .stRadio input[type="radio"] {
    accent-color: #2563EB !important;
}

/* Streamlit's custom radio circle */
[data-testid="stMain"] .stRadio [role="radio"] {
    border-color: #64748B !important;
    background: #FFFFFF !important;
}

[data-testid="stMain"] .stRadio [role="radio"][aria-checked="true"] {
    border-color: #2563EB !important;
    background: #2563EB !important;
}

/* Select boxes: lighter and readable */
[data-testid="stMain"] div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    color: #111827 !important;
}

[data-testid="stMain"] div[data-baseweb="select"] span,
[data-testid="stMain"] div[data-baseweb="select"] input {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

/* Dropdown icon */
[data-testid="stMain"] div[data-baseweb="select"] svg {
    fill: #334155 !important;
}

/* General primary buttons: bright blue with white text */
[data-testid="stMain"] .stButton button,
[data-testid="stMain"] .stFormSubmitButton button {
    background: linear-gradient(135deg, #3B82F6, #2563EB) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.22) !important;
}

[data-testid="stMain"] .stButton button:hover,
[data-testid="stMain"] .stFormSubmitButton button:hover {
    background: linear-gradient(135deg, #60A5FA, #1D4ED8) !important;
    color: #FFFFFF !important;
    transform: translateY(-1px) !important;
}

/* Ensure button labels and icons stay white */
[data-testid="stMain"] .stButton button *,
[data-testid="stMain"] .stFormSubmitButton button * {
    color: #FFFFFF !important;
}

/* Checkbox options also remain readable */
[data-testid="stMain"] .stCheckbox label,
[data-testid="stMain"] .stCheckbox label * {
    color: #111827 !important;
}


/* ==========================================================
   FORM AND LOGIN PAGE FIXES
   ========================================================== */

/* Main form container */
[data-testid="stMain"] [data-testid="stForm"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 20px !important;
    padding: 1.5rem 1.5rem 1.25rem !important;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08) !important;
}

/* Entire BaseWeb text-input wrapper, including password fields */
[data-testid="stMain"] .stTextInput div[data-baseweb="input"],
[data-testid="stMain"] .stNumberInput div[data-baseweb="input"],
[data-testid="stMain"] div[data-baseweb="base-input"] {
    background: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 12px !important;
    box-shadow: none !important;
}

/* Text/password input itself */
[data-testid="stMain"] .stTextInput div[data-baseweb="input"] input,
[data-testid="stMain"] .stNumberInput div[data-baseweb="input"] input,
[data-testid="stMain"] input[type="text"],
[data-testid="stMain"] input[type="password"],
[data-testid="stMain"] input[type="email"] {
    background: #FFFFFF !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    caret-color: #2563EB !important;
    border: none !important;
}

/* Password visibility icon */
[data-testid="stMain"] .stTextInput div[data-baseweb="input"] button,
[data-testid="stMain"] .stTextInput div[data-baseweb="input"] svg {
    color: #475569 !important;
    fill: #475569 !important;
    background: transparent !important;
}

/* Input focus */
[data-testid="stMain"] .stTextInput div[data-baseweb="input"]:focus-within,
[data-testid="stMain"] .stNumberInput div[data-baseweb="input"]:focus-within {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.13) !important;
}

/* Labels above inputs */
[data-testid="stMain"] .stTextInput label,
[data-testid="stMain"] .stNumberInput label,
[data-testid="stMain"] .stSelectbox label,
[data-testid="stMain"] .stTextArea label {
    color: #334155 !important;
    font-weight: 600 !important;
}

/* Login card */
.login-card {
    max-width: 760px;
    margin: 1.25rem auto 0 auto;
    padding: 2rem 2.25rem 1.5rem;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 24px;
    box-shadow: 0 14px 40px rgba(15, 23, 42, 0.09);
}

.login-heading {
    color: #0F172A !important;
    font-size: 2.65rem;
    font-weight: 700;
    line-height: 1.15;
    margin: 0;
}

.login-subtitle {
    color: #64748B !important;
    font-size: 1rem;
    margin: 0.65rem 0 1.4rem;
}

/* Keep footer separated from forms */
.app-footer {
    text-align: center;
    color: #64748B !important;
    padding: 2rem 1rem 1rem;
    margin-top: 2rem;
}

/* Remove accidental empty paragraph height near the footer */
[data-testid="stMain"] .element-container:has(> .stMarkdown:empty) {
    display: none !important;
}


/* ==========================================================
   PROFESSIONAL LOGIN AND FORM THEME
   ========================================================== */

:root {
    --ts-primary: #2563EB;
    --ts-primary-dark: #1D4ED8;
    --ts-secondary: #7C3AED;
    --ts-navy: #0F172A;
    --ts-slate: #475569;
    --ts-muted: #64748B;
    --ts-border: #DDE5F0;
    --ts-surface: #FFFFFF;
    --ts-background: #F4F7FC;
}

[data-testid="stMain"] .block-container {
    max-width: 1240px;
    padding-top: 2.4rem;
    padding-bottom: 2rem;
}

/* Professional page header */
.auth-page-header {
    margin-bottom: 1.15rem;
}

.auth-page-header h1 {
    color: var(--ts-navy) !important;
    font-size: clamp(2rem, 4vw, 3rem);
    line-height: 1.08;
    margin: 0;
    font-weight: 750;
    letter-spacing: -0.035em;
}

.auth-page-header p {
    color: var(--ts-muted) !important;
    margin: 0.65rem 0 0;
    font-size: 1rem;
    line-height: 1.65;
}

/* Left brand panel */
.auth-brand-panel {
    min-height: 510px;
    padding: 3rem;
    border-radius: 28px;
    background:
        radial-gradient(
            circle at 85% 12%,
            rgba(255, 255, 255, 0.22),
            transparent 28%
        ),
        linear-gradient(145deg, #1D4ED8 0%, #4F46E5 48%, #7C3AED 100%);
    box-shadow: 0 24px 55px rgba(37, 99, 235, 0.23);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
    position: relative;
}

.auth-brand-panel::after {
    content: "";
    position: absolute;
    right: -85px;
    bottom: -95px;
    width: 245px;
    height: 245px;
    border: 42px solid rgba(255, 255, 255, 0.10);
    border-radius: 50%;
}

.auth-brand-logo {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 66px;
    height: 66px;
    border-radius: 19px;
    background: rgba(255, 255, 255, 0.18);
    border: 1px solid rgba(255, 255, 255, 0.28);
    backdrop-filter: blur(10px);
    font-size: 2rem;
    margin-bottom: 2rem;
}

.auth-brand-panel h2 {
    color: #FFFFFF !important;
    margin: 0;
    font-size: clamp(2rem, 4vw, 3.15rem);
    line-height: 1.08;
    letter-spacing: -0.04em;
}

.auth-brand-panel > div > p,
.auth-brand-panel p {
    color: rgba(255, 255, 255, 0.86) !important;
    font-size: 1rem;
    line-height: 1.7;
    max-width: 34rem;
}

.auth-feature-list {
    display: grid;
    gap: 0.85rem;
    margin-top: 2rem;
}

.auth-feature {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: #FFFFFF;
    font-size: 0.95rem;
    font-weight: 500;
}

.auth-feature-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 30px;
    height: 30px;
    border-radius: 9px;
    background: rgba(255, 255, 255, 0.18);
}

.auth-brand-footer {
    color: rgba(255, 255, 255, 0.70) !important;
    font-size: 0.82rem !important;
    margin: 2rem 0 0 !important;
}

/* Right login card */
.auth-form-shell {
    min-height: 510px;
    padding: 2.3rem 2.4rem;
    border-radius: 28px;
    background: var(--ts-surface);
    border: 1px solid rgba(203, 213, 225, 0.74);
    box-shadow: 0 22px 55px rgba(15, 23, 42, 0.10);
}

.auth-form-shell h1 {
    color: var(--ts-navy) !important;
}

.auth-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    color: var(--ts-primary) !important;
    background: #EFF6FF;
    border: 1px solid #DBEAFE;
    border-radius: 999px;
    padding: 0.45rem 0.75rem;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.035em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.auth-helper {
    color: var(--ts-muted) !important;
    font-size: 0.9rem;
    line-height: 1.55;
    margin: 0.6rem 0 1.45rem;
}

/* Avoid a second heavy card inside the professional form shell */
[data-testid="stMain"] [data-testid="stForm"] {
    background: transparent !important;
    border: 0 !important;
    border-radius: 0 !important;
    padding: 0 !important;
    box-shadow: none !important;
}

/* Inputs */
[data-testid="stMain"] .stTextInput {
    margin-bottom: 0.35rem;
}

[data-testid="stMain"] .stTextInput label p,
[data-testid="stMain"] .stSelectbox label p,
[data-testid="stMain"] .stTextArea label p {
    color: #334155 !important;
    font-size: 0.9rem !important;
    font-weight: 650 !important;
}

[data-testid="stMain"] .stTextInput div[data-baseweb="input"],
[data-testid="stMain"] .stNumberInput div[data-baseweb="input"],
[data-testid="stMain"] div[data-baseweb="select"] > div {
    min-height: 50px !important;
    background: #F8FAFC !important;
    border: 1px solid var(--ts-border) !important;
    border-radius: 13px !important;
    box-shadow: none !important;
    transition: border-color 0.18s ease, box-shadow 0.18s ease,
                background 0.18s ease;
}

[data-testid="stMain"] .stTextInput div[data-baseweb="input"]:focus-within,
[data-testid="stMain"] .stNumberInput div[data-baseweb="input"]:focus-within,
[data-testid="stMain"] div[data-baseweb="select"] > div:focus-within {
    background: #FFFFFF !important;
    border-color: var(--ts-primary) !important;
    box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.11) !important;
}

[data-testid="stMain"] input[type="text"],
[data-testid="stMain"] input[type="password"],
[data-testid="stMain"] input[type="email"] {
    background: transparent !important;
    color: var(--ts-navy) !important;
    -webkit-text-fill-color: var(--ts-navy) !important;
    font-size: 0.95rem !important;
}

[data-testid="stMain"] input::placeholder {
    color: #94A3B8 !important;
    -webkit-text-fill-color: #94A3B8 !important;
}

[data-testid="stMain"] .stTextInput div[data-baseweb="input"] button {
    box-shadow: none !important;
    transform: none !important;
}

[data-testid="stMain"] .stTextInput div[data-baseweb="input"] button svg {
    fill: #64748B !important;
    color: #64748B !important;
}

/* Login button */
[data-testid="stMain"] .stFormSubmitButton button {
    min-height: 50px !important;
    margin-top: 0.75rem !important;
    border-radius: 13px !important;
    background: linear-gradient(
        135deg,
        var(--ts-primary),
        #4F46E5
    ) !important;
    border: 0 !important;
    color: #FFFFFF !important;
    font-size: 0.96rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.01em;
    box-shadow: 0 10px 22px rgba(37, 99, 235, 0.25) !important;
    transition: transform 0.18s ease, box-shadow 0.18s ease !important;
}

[data-testid="stMain"] .stFormSubmitButton button:hover {
    background: linear-gradient(
        135deg,
        var(--ts-primary-dark),
        #4338CA
    ) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 13px 28px rgba(37, 99, 235, 0.30) !important;
}

.auth-security-note {
    margin-top: 1.15rem;
    padding: 0.85rem 1rem;
    border-radius: 12px;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    color: #64748B !important;
    font-size: 0.82rem;
    line-height: 1.5;
}

.auth-security-note strong {
    color: #334155;
}

/* Sidebar refinement */
section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #0F172A 0%, #111827 100%) !important;
    border-right: 1px solid rgba(148, 163, 184, 0.10);
}

section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
    padding-top: 1rem;
}

section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
    border-radius: 10px !important;
    padding: 0.35rem 0.45rem !important;
    transition: background 0.18s ease !important;
}

section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
    background: rgba(255, 255, 255, 0.07) !important;
}

/* Footer */
.app-footer {
    margin-top: 2.5rem !important;
    border-top: 1px solid #E2E8F0;
    color: #64748B !important;
    font-size: 0.85rem;
}

/* Mobile */
@media (max-width: 900px) {
    .auth-brand-panel {
        min-height: auto;
        padding: 2rem;
        margin-bottom: 1rem;
    }

    .auth-form-shell {
        min-height: auto;
        padding: 1.65rem;
    }
}


/* Final login rendering correction */
.auth-form-heading {
    background: #FFFFFF;
    border: 1px solid rgba(203, 213, 225, 0.74);
    border-bottom: 0;
    border-radius: 26px 26px 0 0;
    padding: 2.2rem 2.3rem 0.35rem;
    box-shadow: 0 18px 45px rgba(15, 23, 42, 0.09);
}

[data-testid="stMain"] [data-testid="stForm"] {
    background: #FFFFFF !important;
    border: 1px solid rgba(203, 213, 225, 0.74) !important;
    border-top: 0 !important;
    border-radius: 0 0 26px 26px !important;
    padding: 0.75rem 2.3rem 2.2rem !important;
    box-shadow: 0 18px 45px rgba(15, 23, 42, 0.09) !important;
}

.auth-security-note {
    margin-top: 1rem;
}

.auth-brand-panel code,
.auth-form-heading code {
    display: none !important;
}


/* ==========================================================
   FINAL CONTROL-ONLY LIGHT THEME
   Only buttons, inputs, selects, textareas, radio options,
   checkboxes and date fields are changed.
   ========================================================== */

/* Text, email, password and number inputs */
[data-testid="stMain"] .stTextInput div[data-baseweb="input"],
[data-testid="stMain"] .stNumberInput div[data-baseweb="input"],
[data-testid="stMain"] div[data-baseweb="base-input"] {
    background: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 12px !important;
    box-shadow: none !important;
}

[data-testid="stMain"] .stTextInput input,
[data-testid="stMain"] .stNumberInput input,
[data-testid="stMain"] input[type="text"],
[data-testid="stMain"] input[type="password"],
[data-testid="stMain"] input[type="email"],
[data-testid="stMain"] input[type="number"] {
    background: #FFFFFF !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

[data-testid="stMain"] .stTextInput div[data-baseweb="input"]:focus-within,
[data-testid="stMain"] .stNumberInput div[data-baseweb="input"]:focus-within {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12) !important;
}

/* Placeholder and disabled text */
[data-testid="stMain"] input::placeholder,
[data-testid="stMain"] textarea::placeholder {
    color: #94A3B8 !important;
    -webkit-text-fill-color: #94A3B8 !important;
}

[data-testid="stMain"] input:disabled,
[data-testid="stMain"] textarea:disabled {
    background: #F1F5F9 !important;
    color: #475569 !important;
    -webkit-text-fill-color: #475569 !important;
    opacity: 1 !important;
}

/* Password eye icon */
[data-testid="stMain"] .stTextInput button,
[data-testid="stMain"] .stTextInput button:hover {
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
}

[data-testid="stMain"] .stTextInput button svg {
    fill: #64748B !important;
    color: #64748B !important;
}

/* Textareas */
[data-testid="stMain"] .stTextArea textarea {
    background: #FFFFFF !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 12px !important;
}

[data-testid="stMain"] .stTextArea textarea:focus {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12) !important;
}

/* Selectbox and multiselect */
[data-testid="stMain"] div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: #111827 !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 12px !important;
    box-shadow: none !important;
}

[data-testid="stMain"] div[data-baseweb="select"] span,
[data-testid="stMain"] div[data-baseweb="select"] input,
[data-testid="stMain"] div[data-baseweb="select"] div {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

[data-testid="stMain"] div[data-baseweb="select"] svg {
    fill: #475569 !important;
    color: #475569 !important;
}

/* Open dropdown menu */
div[role="listbox"],
div[role="option"],
div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] li {
    background: #FFFFFF !important;
    color: #111827 !important;
}

div[role="option"]:hover,
div[role="option"][aria-selected="true"] {
    background: #EFF6FF !important;
    color: #1D4ED8 !important;
}

/* Multiselect chips */
[data-testid="stMain"] div[data-baseweb="tag"] {
    background: #DBEAFE !important;
    border: 1px solid #BFDBFE !important;
}

[data-testid="stMain"] div[data-baseweb="tag"] span,
[data-testid="stMain"] div[data-baseweb="tag"] svg {
    color: #1E3A8A !important;
    fill: #1E3A8A !important;
}

/* Date input */
[data-testid="stMain"] .stDateInput div[data-baseweb="input"],
[data-testid="stMain"] .stDateInput input {
    background: #FFFFFF !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    border-color: #CBD5E1 !important;
}

/* Radio / quiz options */
[data-testid="stMain"] .stRadio div[role="radiogroup"] > label {
    background: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 11px !important;
    padding: 10px 13px !important;
    margin: 5px 0 !important;
    color: #111827 !important;
}

[data-testid="stMain"] .stRadio div[role="radiogroup"] > label *,
[data-testid="stMain"] .stRadio div[role="radiogroup"] > label p,
[data-testid="stMain"] .stRadio div[role="radiogroup"] > label span {
    color: #111827 !important;
}

[data-testid="stMain"] .stRadio div[role="radiogroup"] > label:hover {
    background: #EFF6FF !important;
    border-color: #60A5FA !important;
}

[data-testid="stMain"] .stRadio div[role="radiogroup"] > label:has(input:checked),
[data-testid="stMain"] .stRadio div[role="radiogroup"] > label:has([aria-checked="true"]) {
    background: #DBEAFE !important;
    border-color: #2563EB !important;
}

/* Checkboxes */
[data-testid="stMain"] .stCheckbox label,
[data-testid="stMain"] .stCheckbox label * {
    color: #111827 !important;
}

/* Buttons only */
[data-testid="stMain"] .stButton button,
[data-testid="stMain"] .stFormSubmitButton button,
[data-testid="stMain"] .stDownloadButton button {
    background: linear-gradient(135deg, #60A5FA, #2563EB) !important;
    color: #FFFFFF !important;
    border: 0 !important;
    border-radius: 12px !important;
    font-weight: 650 !important;
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.20) !important;
}

[data-testid="stMain"] .stButton button:hover,
[data-testid="stMain"] .stFormSubmitButton button:hover,
[data-testid="stMain"] .stDownloadButton button:hover {
    background: linear-gradient(135deg, #3B82F6, #1D4ED8) !important;
    color: #FFFFFF !important;
    transform: translateY(-1px) !important;
}

[data-testid="stMain"] .stButton button *,
[data-testid="stMain"] .stFormSubmitButton button *,
[data-testid="stMain"] .stDownloadButton button * {
    color: #FFFFFF !important;
}

/* Do not modify page background, cards, titles, normal text, or sidebar. */


/* ==========================================================
   AI STUDY MENTOR CHAT VISIBILITY
   ========================================================== */

[data-testid="stMain"] [data-testid="stChatMessage"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06) !important;
}

[data-testid="stMain"] [data-testid="stChatMessage"] p,
[data-testid="stMain"] [data-testid="stChatMessage"] span,
[data-testid="stMain"] [data-testid="stChatMessage"] div {
    color: #111827 !important;
}

[data-testid="stMain"] [data-testid="stChatInput"] {
    background: #FFFFFF !important;
    border-top: 1px solid #E2E8F0 !important;
}

[data-testid="stMain"] [data-testid="stChatInput"] textarea {
    background: #FFFFFF !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    border: 1px solid #CBD5E1 !important;
}

[data-testid="stMain"] [data-testid="stChatInput"] textarea::placeholder {
    color: #94A3B8 !important;
    -webkit-text-fill-color: #94A3B8 !important;
}

[data-testid="stMain"] [data-testid="stChatInput"] button {
    background: #2563EB !important;
    color: #FFFFFF !important;
}

[data-testid="stMain"] [data-testid="stChatInput"] button svg {
    fill: #FFFFFF !important;
    color: #FFFFFF !important;
}


/* ==========================================================
   LOGIN INPUT VISIBILITY FIX
   ========================================================== */

[data-testid="stMain"] .stTextInput div[data-baseweb="input"] {
    background: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 12px !important;
}

[data-testid="stMain"] .stTextInput input,
[data-testid="stMain"] input[type="email"],
[data-testid="stMain"] input[type="password"] {
    background: #FFFFFF !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    caret-color: #2563EB !important;
}

[data-testid="stMain"] .stTextInput input::placeholder,
[data-testid="stMain"] input[type="email"]::placeholder,
[data-testid="stMain"] input[type="password"]::placeholder {
    color: #94A3B8 !important;
    -webkit-text-fill-color: #94A3B8 !important;
    opacity: 1 !important;
}

[data-testid="stMain"] .stTextInput div[data-baseweb="input"]:focus-within {
    background: #FFFFFF !important;
    border-color: #2563EB !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12) !important;
}

[data-testid="stMain"] .stTextInput button,
[data-testid="stMain"] .stTextInput button:hover {
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
}

[data-testid="stMain"] .stTextInput button svg {
    color: #64748B !important;
    fill: #64748B !important;
}


/* ==========================================================
   COLLEGE STUDENT DASHBOARD — PROFESSIONAL UI
   ========================================================== */

.studio-hero {
    position: relative;
    overflow: hidden;
    padding: 34px 36px;
    border-radius: 26px;
    background:
        radial-gradient(circle at 90% 15%, rgba(255,255,255,.22), transparent 27%),
        linear-gradient(135deg, #1D4ED8 0%, #4F46E5 52%, #7C3AED 100%);
    box-shadow: 0 18px 45px rgba(37, 99, 235, .22);
    margin-bottom: 24px;
}

.studio-hero::after {
    content: "";
    position: absolute;
    right: -70px;
    bottom: -105px;
    width: 260px;
    height: 260px;
    border: 42px solid rgba(255,255,255,.08);
    border-radius: 50%;
}

.studio-badge {
    display: inline-block;
    padding: 7px 12px;
    border-radius: 999px;
    background: rgba(255,255,255,.16);
    border: 1px solid rgba(255,255,255,.25);
    color: #FFFFFF !important;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: .06em;
    text-transform: uppercase;
    margin-bottom: 15px;
}

.studio-hero h1 {
    color: #FFFFFF !important;
    font-size: clamp(32px, 5vw, 50px);
    line-height: 1.08;
    margin: 0 0 10px;
    letter-spacing: -.035em;
}

.studio-hero p {
    color: rgba(255,255,255,.88) !important;
    font-size: 16px;
    max-width: 790px;
    line-height: 1.7;
    margin: 0;
}

.studio-section-title {
    color: #0F172A !important;
    font-size: 25px;
    font-weight: 750;
    margin: 8px 0 16px;
    letter-spacing: -.025em;
}

.studio-kpi {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 19px 20px;
    min-height: 134px;
    box-shadow: 0 7px 24px rgba(15, 23, 42, .06);
    transition: transform .18s ease, box-shadow .18s ease;
}

.studio-kpi:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 30px rgba(15, 23, 42, .10);
}

.studio-kpi-icon {
    width: 38px;
    height: 38px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 11px;
    background: #EFF6FF;
    font-size: 19px;
    margin-bottom: 12px;
}

.studio-kpi-label {
    color: #64748B !important;
    font-size: 12px;
    font-weight: 650;
    letter-spacing: .035em;
    text-transform: uppercase;
    margin-bottom: 5px;
}

.studio-kpi-value {
    color: #0F172A !important;
    font-size: 28px;
    line-height: 1.1;
    font-weight: 800;
    margin: 0;
}

.studio-kpi-sub {
    color: #64748B !important;
    font-size: 12px;
    margin-top: 7px;
}

.studio-panel {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 20px;
    padding: 22px;
    box-shadow: 0 8px 25px rgba(15, 23, 42, .06);
    height: 100%;
}

.studio-panel h3 {
    color: #0F172A !important;
    margin-top: 0;
    font-size: 19px;
    letter-spacing: -.02em;
}

.studio-role-card {
    background: linear-gradient(145deg, #F8FAFC, #FFFFFF);
    border: 1px solid #DBEAFE;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 12px;
}

.studio-role-title {
    color: #1D4ED8 !important;
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 4px;
}

.studio-match {
    color: #059669 !important;
    font-weight: 750;
    font-size: 15px;
}

.studio-chip {
    display: inline-block;
    padding: 6px 10px;
    margin: 4px 5px 4px 0;
    border-radius: 999px;
    background: #EEF2FF;
    border: 1px solid #E0E7FF;
    color: #3730A3 !important;
    font-size: 12px;
    font-weight: 650;
}

.studio-action {
    padding: 14px 15px;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #2563EB;
    border-radius: 12px;
    margin-bottom: 10px;
}

.studio-action strong {
    color: #0F172A;
}

.studio-action span {
    color: #64748B;
    font-size: 13px;
}

.studio-module-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 17px;
    padding: 18px;
    min-height: 172px;
    box-shadow: 0 6px 19px rgba(15,23,42,.05);
}

.studio-module-card h4 {
    color: #0F172A !important;
    margin: 8px 0 7px;
    font-size: 17px;
}

.studio-module-card p {
    color: #64748B !important;
    font-size: 13px;
    line-height: 1.55;
}

.studio-status-good {
    color: #047857 !important;
    background: #ECFDF5;
    border: 1px solid #A7F3D0;
    border-radius: 999px;
    padding: 5px 9px;
    font-size: 11px;
    font-weight: 700;
}

.studio-status-progress {
    color: #B45309 !important;
    background: #FFFBEB;
    border: 1px solid #FDE68A;
    border-radius: 999px;
    padding: 5px 9px;
    font-size: 11px;
    font-weight: 700;
}

/* College profile heading and form polish */
.college-profile-header {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 22px;
    padding: 24px 26px;
    box-shadow: 0 8px 26px rgba(15,23,42,.06);
    margin-bottom: 18px;
}

.college-profile-header h1 {
    color: #0F172A !important;
    margin: 0 0 7px;
    letter-spacing: -.03em;
}

.college-profile-header p {
    color: #64748B !important;
    margin: 0;
}

/* Improve charts and tables inside the studio */
[data-testid="stMain"] [data-testid="stDataFrame"] {
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    overflow: hidden;
}

@media (max-width: 850px) {
    .studio-hero {
        padding: 26px 22px;
    }

    .studio-kpi {
        min-height: 118px;
    }
}


/* ==========================================================
   MODERN COLLEGE SIDEBAR NAVIGATION
   ========================================================== */

section[data-testid="stSidebar"] {
    padding-top: 0.5rem;
}

section[data-testid="stSidebar"] .college-user-card {
    background: linear-gradient(
        135deg,
        rgba(37, 99, 235, 0.24),
        rgba(124, 58, 237, 0.20)
    );
    border: 1px solid rgba(148, 163, 184, 0.20);
    border-radius: 16px;
    padding: 15px 16px;
    margin: 8px 0 16px;
}

section[data-testid="stSidebar"] .college-user-card .user-label {
    color: #94A3B8 !important;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 5px;
}

section[data-testid="stSidebar"] .college-user-card .user-name {
    color: #FFFFFF !important;
    font-size: 16px;
    font-weight: 750;
    line-height: 1.3;
}

section[data-testid="stSidebar"] .college-user-card .user-role {
    color: #CBD5E1 !important;
    font-size: 12px;
    margin-top: 4px;
}

section[data-testid="stSidebar"] .nav-section-label {
    color: #94A3B8 !important;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.11em;
    text-transform: uppercase;
    margin: 17px 4px 8px;
}

section[data-testid="stSidebar"] .stButton {
    margin-bottom: 3px;
}

section[data-testid="stSidebar"] .stButton button {
    width: 100% !important;
    min-height: 42px !important;
    justify-content: flex-start !important;
    text-align: left !important;
    padding: 9px 12px !important;
    border-radius: 11px !important;
    border: 1px solid transparent !important;
    background: transparent !important;
    color: #CBD5E1 !important;
    font-size: 13px !important;
    font-weight: 550 !important;
    box-shadow: none !important;
    transition: all 0.18s ease !important;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(255, 255, 255, 0.075) !important;
    border-color: rgba(148, 163, 184, 0.16) !important;
    color: #FFFFFF !important;
    transform: translateX(2px) !important;
}

section[data-testid="stSidebar"] .stButton button[kind="primary"] {
    background: linear-gradient(
        135deg,
        rgba(37, 99, 235, 0.96),
        rgba(79, 70, 229, 0.96)
    ) !important;
    color: #FFFFFF !important;
    border-color: rgba(147, 197, 253, 0.22) !important;
    box-shadow: 0 8px 18px rgba(37, 99, 235, 0.24) !important;
    font-weight: 700 !important;
}

section[data-testid="stSidebar"] .stButton button p,
section[data-testid="stSidebar"] .stButton button span,
section[data-testid="stSidebar"] .stButton button div {
    color: inherit !important;
}

section[data-testid="stSidebar"] .nav-divider {
    height: 1px;
    background: rgba(148, 163, 184, 0.14);
    margin: 14px 2px;
}

section[data-testid="stSidebar"] .sidebar-footer-card {
    margin-top: 16px;
    padding: 11px 13px;
    border-radius: 12px;
    background: rgba(15, 23, 42, 0.55);
    border: 1px solid rgba(148, 163, 184, 0.12);
}

section[data-testid="stSidebar"] .sidebar-footer-card p {
    margin: 0;
    color: #94A3B8 !important;
    font-size: 10px;
    line-height: 1.55;
}

/* Hide the old radio-style circles if any remain in the sidebar */
section[data-testid="stSidebar"] .stRadio [role="radio"] {
    display: none !important;
}


/* Career Intelligence visibility fallback */
[data-testid="stMain"] .studio-section-title,
[data-testid="stMain"] div.studio-section-title {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    color: #0F172A !important;
    background: #FFFFFF !important;
    border: 1px solid #DCE6F3 !important;
    border-left: 6px solid #2563EB !important;
    border-radius: 15px !important;
    padding: 16px 20px !important;
    margin: 14px 0 20px !important;
    font-size: 25px !important;
    font-weight: 800 !important;
    line-height: 1.2 !important;
    box-shadow: 0 7px 22px rgba(15, 23, 42, 0.07) !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# COLLEGE STUDENT REPORT HELPERS
# ==========================================================

def report_display_value(value, fallback="-"):
    """Return clean text for report display."""
    if value is None:
        return fallback

    value = str(value).strip()
    return value if value else fallback


def report_list_value(value):
    """Convert JSON-list database values to readable text."""
    if not value:
        return "-"

    try:
        parsed = json.loads(value)

        if isinstance(parsed, list):
            cleaned = [
                str(item).strip()
                for item in parsed
                if str(item).strip()
            ]
            return ", ".join(cleaned) if cleaned else "-"

    except (json.JSONDecodeError, TypeError):
        pass

    return report_display_value(value)


def calculate_college_report_scores(
    profile,
    coding_average,
    interview_average
):
    """Calculate placement-readiness scores from saved profile data."""
    skill_items = []

    for field_name in [
        "technical_skills",
        "programming_languages",
        "tools"
    ]:
        readable = report_list_value(profile.get(field_name))

        if readable != "-":
            skill_items.extend(
                item.strip()
                for item in readable.split(",")
                if item.strip()
            )

    resume_score = min(
        100,
        25
        + len(skill_items) * 4
        + (20 if profile.get("projects") else 0)
        + (12 if profile.get("internships") else 0)
        + (8 if profile.get("certifications") else 0)
    )

    project_score = (
        min(
            100,
            20 + len(
                str(profile.get("projects") or "").split()
            ) * 2
        )
        if profile.get("projects")
        else 20
    )

    experience_score = (
        85
        if profile.get("internships")
        else 30
    )

    coding_score = round(coding_average or 0)
    interview_score = round(interview_average or 0)

    overall_score = round(
        resume_score * 0.25
        + coding_score * 0.30
        + project_score * 0.20
        + interview_score * 0.15
        + experience_score * 0.10
    )

    return {
        "Resume": resume_score,
        "Coding": coding_score,
        "Projects": project_score,
        "Interview": interview_score,
        "Experience": experience_score,
        "Placement Readiness": overall_score
    }


def create_college_report_recommendations(
    profile,
    scores,
    coding_count,
    interview_count,
    application_count
):
    """Create personalised report recommendations."""
    recommendations = []

    if not profile.get("college_name"):
        recommendations.append(
            "Complete your College Profile with academic and career information."
        )

    if scores["Resume"] < 70:
        recommendations.append(
            "Improve your resume by adding technical skills, certifications, "
            "projects and measurable achievements."
        )

    if scores["Coding"] < 70:
        recommendations.append(
            "Practise Data Structures, Algorithms, aptitude and coding regularly."
        )

    if coding_count < 5:
        recommendations.append(
            "Complete at least five coding assessments for a reliable coding score."
        )

    if scores["Projects"] < 70:
        recommendations.append(
            "Add two or three strong projects with technologies, role and outcomes."
        )

    if not profile.get("internships"):
        recommendations.append(
            "Apply for internships or practical training to improve experience."
        )

    if scores["Interview"] < 70:
        recommendations.append(
            "Practise technical, HR and communication interview questions."
        )

    if interview_count < 3:
        recommendations.append(
            "Complete at least three mock interviews and review the feedback."
        )

    if application_count == 0:
        recommendations.append(
            "Start tracking internship and placement applications."
        )

    if not profile.get("github_url"):
        recommendations.append(
            "Add your GitHub profile and maintain at least three documented projects."
        )

    if not profile.get("linkedin_pdf_path"):
        recommendations.append(
            "Upload and review your LinkedIn profile PDF."
        )

    if not recommendations:
        recommendations.append(
            "Your preparation is progressing well. Continue regular coding, "
            "mock interviews and targeted applications."
        )

    return recommendations[:8]


def build_college_report_text(report_data):
    """Create a downloadable plain-text College Student report."""
    profile = report_data["profile"]
    scores = report_data["scores"]

    lines = [
        "TALENTSPHERE ELEVATE",
        "COLLEGE STUDENT PLACEMENT REPORT",
        "=" * 48,
        f"Student Name: {report_data['student_name']}",
        f"Email: {report_data['student_email']}",
        f"Generated On: {report_data['generated_at']}",
        "",
        "ACADEMIC PROFILE",
        "-" * 48,
        f"College: {report_display_value(profile.get('college_name'))}",
        f"Degree: {report_display_value(profile.get('degree'))}",
        f"Branch: {report_display_value(profile.get('branch'))}",
        f"Current Year: {report_display_value(profile.get('current_year'))}",
        f"Semester: {report_display_value(profile.get('semester'))}",
        f"University: {report_display_value(profile.get('university'))}",
        f"City: {report_display_value(profile.get('city'))}",
        f"CGPA: {report_display_value(profile.get('cgpa'), '0')}",
        f"Backlogs: {report_display_value(profile.get('backlogs'), '0')}",
        "",
        "CAREER PROFILE",
        "-" * 48,
        f"Career Goal: {report_display_value(profile.get('career_goal'))}",
        f"Preferred Role: {report_display_value(profile.get('preferred_role'))}",
        f"Preferred Location: {report_display_value(profile.get('preferred_location'))}",
        f"Placement Status: {report_display_value(profile.get('placement_status'))}",
        "",
        "SKILLS AND EXPERIENCE",
        "-" * 48,
        f"Technical Skills: {report_list_value(profile.get('technical_skills'))}",
        f"Programming Languages: {report_list_value(profile.get('programming_languages'))}",
        f"Tools: {report_list_value(profile.get('tools'))}",
        f"Certifications: {report_display_value(profile.get('certifications'))}",
        f"Projects: {report_display_value(profile.get('projects'))}",
        f"Internships: {report_display_value(profile.get('internships'))}",
        "",
        "PLACEMENT READINESS",
        "-" * 48
    ]

    for component in [
        "Resume",
        "Coding",
        "Projects",
        "Interview",
        "Experience",
        "Placement Readiness"
    ]:
        lines.append(
            f"{component}: {scores[component]}/100"
        )

    lines.extend([
        "",
        "ACTIVITY SUMMARY",
        "-" * 48,
        f"Coding Assessments: {report_data['coding_count']}",
        f"Mock Interviews: {report_data['interview_count']}",
        f"Placement Applications: {report_data['application_count']}",
        f"Job Matches Generated: {report_data['job_match_count']}",
        "",
        "PERSONALISED RECOMMENDATIONS",
        "-" * 48
    ])

    for number, recommendation in enumerate(
        report_data["recommendations"],
        start=1
    ):
        lines.append(f"{number}. {recommendation}")

    if report_data["applications"]:
        lines.extend([
            "",
            "RECENT PLACEMENT APPLICATIONS",
            "-" * 48
        ])

        for application in report_data["applications"][:10]:
            lines.append(
                f"{application[0]} | {application[1]} | "
                f"{application[2]} | Next: {application[3] or '-'}"
            )

    lines.extend([
        "",
        "This report is generated from the details and activities "
        "stored in TalentSphere Elevate."
    ])

    return "\n".join(lines)


# ==========================================================
# COLLEGE NAVIGATION HELPERS
# ==========================================================

def set_college_navigation(page_name):
    """Update the selected College Student page."""
    st.session_state.college_navigation = page_name


def college_nav_button(label, page_name, key):
    """Render one modern sidebar navigation button."""
    is_active = (
        st.session_state.get("college_navigation")
        == page_name
    )

    st.sidebar.button(
        label,
        key=key,
        width="stretch",
        type="primary" if is_active else "secondary",
        on_click=set_college_navigation,
        args=(page_name,)
    )


def set_school_navigation(page_name):
    """Update the selected School Student page."""
    st.session_state.school_navigation = page_name


def school_nav_button(label, page_name, key):
    """Render one modern School Student sidebar navigation button."""
    is_active = (
        st.session_state.get("school_navigation")
        == page_name
    )

    st.sidebar.button(
        label,
        key=key,
        width="stretch",
        type="primary" if is_active else "secondary",
        on_click=set_school_navigation,
        args=(page_name,)
    )


# ==========================================================
# WORKING PROFESSIONAL HELPERS
# ==========================================================

def set_professional_navigation(page_name):
    """Update the selected Working Professional page."""
    st.session_state.professional_navigation = page_name


def professional_nav_button(label, page_name, key):
    """Render one modern Working Professional navigation button."""
    is_active = st.session_state.get("professional_navigation") == page_name
    st.sidebar.button(
        label,
        key=key,
        width="stretch",
        type="primary" if is_active else "secondary",
        on_click=set_professional_navigation,
        args=(page_name,)
    )


def csv_list(value):
    """Convert comma-separated profile text into a clean list."""
    return [item.strip() for item in (value or "").split(",") if item.strip()]


def get_professional_profile(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM professional_profiles WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    columns = [item[0] for item in cursor.description] if cursor.description else []
    connection.close()
    return dict(zip(columns, row)) if row else {}


def professional_metrics(profile):
    skills = set(item.lower() for item in csv_list(profile.get("technical_skills")))
    skills.update(item.lower() for item in csv_list(profile.get("programming_languages")))
    skills.update(item.lower() for item in csv_list(profile.get("frameworks")))
    skills.update(item.lower() for item in csv_list(profile.get("cloud_platforms")))
    skills.update(item.lower() for item in csv_list(profile.get("devops_tools")))
    experience = float(profile.get("total_experience") or 0)
    team_size = int(profile.get("team_size") or 0)
    projects_led = int(profile.get("projects_led") or 0)
    leadership_text = (profile.get("leadership_experience") or "").lower()
    communication = profile.get("communication_level") or "Beginner"
    comm_score = {"Beginner": 45, "Intermediate": 65, "Advanced": 82, "Expert": 92}.get(communication, 60)

    backend_terms = {"python", "django", "flask", "fastapi", "java", "spring", "spring boot", "node", "node.js", "rest api", "sql"}
    cloud_terms = {"aws", "azure", "gcp", "google cloud", "cloud computing"}
    devops_terms = {"docker", "kubernetes", "jenkins", "terraform", "devops", "ci/cd"}
    system_terms = {"system design", "microservices", "distributed systems", "architecture"}

    backend = min(95, 50 + 5 * len(skills & backend_terms) + int(experience * 3))
    cloud = min(95, 40 + 10 * len(skills & cloud_terms) + 5 * len(skills & devops_terms))
    devops = min(95, 38 + 10 * len(skills & devops_terms))
    system_design = min(95, 42 + 10 * len(skills & system_terms) + int(experience * 4))
    leadership = min(95, 45 + int(experience * 3) + min(team_size, 10) * 2 + projects_led * 3 + (8 if leadership_text else 0))
    technical = round((backend + cloud + devops + system_design) / 4)
    promotion = min(96, round(technical * .48 + leadership * .27 + comm_score * .25))

    profile_fields = [
        "current_company", "current_role", "total_experience", "technical_skills",
        "certifications", "career_goal", "preferred_roles", "current_salary",
        "expected_salary", "leadership_experience", "linkedin_url", "phone"
    ]
    completion = round(sum(bool(profile.get(field)) for field in profile_fields) / len(profile_fields) * 100)
    current_salary = float(profile.get("current_salary") or 0)
    expected_salary = float(profile.get("expected_salary") or 0)
    salary_growth = round(((expected_salary-current_salary)/current_salary)*100) if current_salary and expected_salary else 0

    return {
        "Backend Development": backend,
        "System Design": system_design,
        "Cloud Computing": cloud,
        "DevOps": devops,
        "Leadership": leadership,
        "Communication": comm_score,
        "Technical Readiness": technical,
        "Promotion Readiness": promotion,
        "Profile Completion": completion,
        "Salary Growth": salary_growth
    }


def professional_role_matches(profile, metrics):
    current_role = profile.get("current_role") or "Software Professional"
    preferred = csv_list(profile.get("preferred_roles"))
    defaults = ["Senior Backend Engineer", "Backend Architect", "Cloud Engineer", "Engineering Lead"]
    roles = (preferred + defaults)[:4]
    base = metrics["Technical Readiness"]
    scores = []
    for index, role in enumerate(roles):
        role_lower = role.lower()
        score = base + 8 - index * 5
        if "lead" in role_lower or "manager" in role_lower:
            score = round((metrics["Leadership"] + metrics["Communication"]) / 2)
        elif "cloud" in role_lower:
            score = metrics["Cloud Computing"] + 10
        elif "architect" in role_lower or "system" in role_lower:
            score = metrics["System Design"] + 8
        elif "backend" in role_lower:
            score = metrics["Backend Development"] + 7
        scores.append((role, max(45, min(96, score))))
    return scores


# ==========================================================
# FINAL STREAMLIT FRAME / TOP-BAR PROFESSIONAL UI FIX
# ==========================================================

st.markdown("""
<style>

/* Light, compact Streamlit top bar instead of the large black strip */
[data-testid="stHeader"] {
    background: rgba(244, 247, 252, 0.98) !important;
    border-bottom: 1px solid #E5EAF2 !important;
    box-shadow: none !important;
    height: 52px !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

[data-testid="stToolbar"] {
    background: transparent !important;
}

[data-testid="stToolbar"] button,
[data-testid="stToolbar"] a,
[data-testid="stToolbar"] span {
    color: #475569 !important;
}

[data-testid="stToolbar"] svg,
[data-testid="stMainMenu"] svg {
    color: #475569 !important;
    fill: #475569 !important;
}

[data-testid="stMainMenu"] button {
    background: transparent !important;
    color: #475569 !important;
    box-shadow: none !important;
}

/* Main workspace */
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: #F4F7FC !important;
}

[data-testid="stMain"] .block-container {
    max-width: 1160px !important;
    padding-top: 1.05rem !important;
    padding-left: 1.4rem !important;
    padding-right: 1.4rem !important;
    padding-bottom: 2.25rem !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Slightly more compact professional hero */
.studio-hero,
.learn-hero {
    margin-top: 0 !important;
    padding: 28px 32px !important;
    border-radius: 23px !important;
}

.studio-hero h1,
.learn-hero h1 {
    font-size: clamp(30px, 3.2vw, 42px) !important;
    line-height: 1.08 !important;
}

.studio-hero p,
.learn-hero p {
    font-size: 14px !important;
    line-height: 1.6 !important;
    max-width: 840px !important;
}

/* Make the KPI row look like a professional dashboard */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #E5EAF2 !important;
    border-radius: 16px !important;
    padding: 14px 16px !important;
    min-height: 100px !important;
    box-shadow: 0 7px 20px rgba(15, 23, 42, 0.045) !important;
}

[data-testid="stMetricLabel"] {
    color: #64748B !important;
    font-weight: 650 !important;
}

[data-testid="stMetricValue"] {
    color: #0F172A !important;
    font-weight: 800 !important;
    font-size: clamp(1.65rem, 2.3vw, 2.45rem) !important;
}

/* Cleaner cards */
.studio-panel,
.studio-kpi,
.learn-card,
.learn-stat,
.learn-project,
.learn-road {
    border-color: #E5EAF2 !important;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05) !important;
}

/* Professional sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #101828 100%) !important;
    border-right: 1px solid rgba(148, 163, 184, 0.12) !important;
}

section[data-testid="stSidebar"] > div {
    padding-top: 0.55rem !important;
}

/* Reduce unnecessary vertical gaps */
[data-testid="stVerticalBlock"] {
    gap: 0.82rem !important;
}

/* Laptop fit */
@media (max-width: 1400px) {
    [data-testid="stMain"] .block-container {
        max-width: 1080px !important;
        padding-left: 1.15rem !important;
        padding-right: 1.15rem !important;
    }

    .studio-hero,
    .learn-hero {
        padding: 25px 28px !important;
    }
}

/* Mobile/tablet */
@media (max-width: 900px) {
    [data-testid="stHeader"] {
        height: 48px !important;
    }

    [data-testid="stMain"] .block-container {
        padding: 0.85rem 0.85rem 2rem !important;
    }

    .studio-hero,
    .learn-hero {
        padding: 22px 20px !important;
        border-radius: 18px !important;
    }
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# SIDEBAR HEADER
# ==========================================================

st.sidebar.image(
    "https://img.icons8.com/color/96/artificial-intelligence.png",
    width=90
)

st.sidebar.title("TalentSphere")
st.sidebar.caption("AI Career Development Platform")


# ==========================================================
# SIDEBAR NAVIGATION
# ==========================================================

if (
    st.session_state.logged_in
    and st.session_state.user_role == "School Student"
):

    if "school_navigation" not in st.session_state:
        st.session_state.school_navigation = "🏠 Student Home"

    st.sidebar.markdown(
        f"""<div class="college-user-card">
<div class="user-label">Student Workspace</div>
<div class="user-name">{st.session_state.user_name}</div>
<div class="user-role">School Student · Learning & Career Discovery</div>
</div>""",
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        '<div class="nav-section-label">Overview</div>',
        unsafe_allow_html=True
    )
    school_nav_button("🏠  Student Home", "🏠 Student Home", "school_nav_home")
    school_nav_button("👤  My Profile", "👤 My Profile", "school_nav_profile")

    st.sidebar.markdown(
        '<div class="nav-section-label">Career Discovery</div>',
        unsafe_allow_html=True
    )
    school_nav_button("🔍  Career Explorer", "🔍 Career Explorer", "school_nav_career")
    school_nav_button("📊  Interest Assessment", "📊 Interest Assessment", "school_nav_interest")
    school_nav_button("🛣️  Future Skills Roadmap", "🛣️ Future Skills Roadmap", "school_nav_roadmap")

    st.sidebar.markdown(
        '<div class="nav-section-label">Learning & Practice</div>',
        unsafe_allow_html=True
    )
    school_nav_button("📝  Subject Quiz", "📝 Subject Quiz", "school_nav_quiz")
    school_nav_button("📅  Daily Study Planner", "📅 Daily Study Planner", "school_nav_planner")
    school_nav_button("📚  School Subjects", "📚 School Subjects", "school_nav_subjects")
    school_nav_button("🧮  Aptitude Practice", "🧮 Aptitude Practice", "school_nav_aptitude")
    school_nav_button("🗣️  Communication Skills", "🗣️ Communication Skills", "school_nav_communication")

    st.sidebar.markdown(
        '<div class="nav-section-label">Goals & Guidance</div>',
        unsafe_allow_html=True
    )
    school_nav_button("🎯  Goal Tracker", "🎯 Goal Tracker", "school_nav_goals")
    school_nav_button("🤖  AI Study Mentor", "🤖 AI Study Mentor", "school_nav_mentor")
    school_nav_button("📄  My Report", "📄 My Report", "school_nav_report")

    st.sidebar.markdown(
        '<div class="nav-divider"></div>',
        unsafe_allow_html=True
    )
    school_nav_button("🚪  Logout", "🚪 Logout", "school_nav_logout")

    menu = st.session_state.school_navigation

elif (
    st.session_state.logged_in
    and st.session_state.user_role == "College Student"
):

    if "college_navigation" not in st.session_state:
        st.session_state.college_navigation = "🏠 College Dashboard"

    st.sidebar.markdown(
        f"""<div class="college-user-card">
<div class="user-label">Student Workspace</div>
<div class="user-name">{st.session_state.user_name}</div>
<div class="user-role">College Student · Placement Preparation</div>
</div>""",
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        '<div class="nav-section-label">Overview</div>',
        unsafe_allow_html=True
    )

    college_nav_button(
        "🏠  Dashboard",
        "🏠 College Dashboard",
        "college_nav_dashboard"
    )
    college_nav_button(
        "👤  College Profile",
        "👤 College Profile",
        "college_nav_profile"
    )

    st.sidebar.markdown(
        '<div class="nav-section-label">Skill Development</div>',
        unsafe_allow_html=True
    )

    college_nav_button(
        "💻  Coding Practice",
        "💻 Coding Practice",
        "college_nav_coding"
    )
    college_nav_button(
        "🔥  Daily Challenge",
        "🔥 Daily Coding Challenge",
        "college_nav_daily"
    )
    college_nav_button(
        "🎤  Interview Preparation",
        "🎤 Interview Preparation",
        "college_nav_interview"
    )
    college_nav_button(
        "🧑‍💼  Mock Interviews",
        "🧑‍💼 Mock Interviews",
        "college_nav_mock"
    )
    college_nav_button(
        "📊  Skill Gap Analysis",
        "📊 Skill Gap Analysis",
        "college_nav_skill_gap"
    )

    st.sidebar.markdown(
        '<div class="nav-section-label">Career Documents</div>',
        unsafe_allow_html=True
    )

    college_nav_button(
        "📄  Resume Builder",
        "📄 Resume Builder",
        "college_nav_resume"
    )
    college_nav_button(
        "✅  ATS Resume Checker",
        "✅ ATS Resume Checker",
        "college_nav_ats"
    )
    college_nav_button(
        "📄  LinkedIn PDF Review",
        "📄 LinkedIn PDF Review",
        "college_nav_linkedin"
    )

    st.sidebar.markdown(
        '<div class="nav-section-label">Career Opportunities</div>',
        unsafe_allow_html=True
    )

    college_nav_button(
        "🧭  Internship Recommendations",
        "🧭 Internship Recommendations",
        "college_nav_internships"
    )
    college_nav_button(
        "🧠  Job Matching Engine",
        "🧠 Job Matching Engine",
        "college_nav_jobs"
    )
    college_nav_button(
        "🎯  Placement Tracker",
        "🎯 Placement Tracker",
        "college_nav_placement"
    )
    college_nav_button(
        "🏆  Hackathon Updates",
        "🏆 Hackathon Updates",
        "college_nav_hackathons"
    )

    st.sidebar.markdown(
        '<div class="nav-section-label">Technical Portfolio</div>',
        unsafe_allow_html=True
    )

    college_nav_button(
        "🐙  GitHub Portfolio Review",
        "🐙 GitHub Portfolio Review",
        "college_nav_github"
    )

    st.sidebar.markdown(
        '<div class="nav-section-label">Progress Report</div>',
        unsafe_allow_html=True
    )

    college_nav_button(
        "📑  College Student Report",
        "📑 College Student Report",
        "college_nav_report"
    )

    st.sidebar.markdown(
        '<div class="nav-divider"></div>',
        unsafe_allow_html=True
    )

    college_nav_button(
        "🚪  Logout",
        "🚪 Logout",
        "college_nav_logout"
    )

    menu = st.session_state.college_navigation

elif (
    st.session_state.logged_in
    and st.session_state.user_role == "Professional"
):

    if "professional_navigation" not in st.session_state:
        st.session_state.professional_navigation = "🏢 Professional Dashboard"

    st.sidebar.markdown(
        f"""<div class="college-user-card">
<div class="user-label">Professional Workspace</div>
<div class="user-name">{st.session_state.user_name}</div>
<div class="user-role">Working Professional · Career Growth</div>
</div>""",
        unsafe_allow_html=True
    )

    st.sidebar.markdown('<div class="nav-section-label">Overview</div>', unsafe_allow_html=True)
    professional_nav_button("🏢  Dashboard", "🏢 Professional Dashboard", "pro_nav_dashboard")
    professional_nav_button("👨‍💼  Professional Profile", "👨‍💼 Professional Profile", "pro_nav_profile")

    st.sidebar.markdown('<div class="nav-section-label">Career Intelligence</div>', unsafe_allow_html=True)
    professional_nav_button("📚  Learning & Skills", "📚 Professional Learning & Skill Development", "pro_nav_skills")
    professional_nav_button("🚀  Career Transition", "🚀 Career Transition Suggestions", "pro_nav_transition")
    professional_nav_button("📈  Promotion Readiness", "📈 Promotion Readiness", "pro_nav_promotion")
    professional_nav_button("💰  Career & Salary Insights", "💰 Career & Salary Insights", "pro_nav_salary")

    st.sidebar.markdown('<div class="nav-section-label">Growth & Opportunities</div>', unsafe_allow_html=True)
    professional_nav_button("🔥  Industry Trends", "🔥 Industry Trends", "pro_nav_trends")
    professional_nav_button("🎓  Certifications", "🎓 Certification Suggestions", "pro_nav_certifications")
    professional_nav_button("🧭  Leadership Evaluation", "🧭 Leadership Evaluation", "pro_nav_leadership")
    professional_nav_button("🎯  Advanced Job Matching", "🎯 Advanced Job Matching", "pro_nav_jobs")
    professional_nav_button("🤖  AI Growth Report", "🤖 AI Growth Report", "pro_nav_report")

    st.sidebar.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)
    professional_nav_button("🚪  Logout", "🚪 Logout", "pro_nav_logout")
    menu = st.session_state.professional_navigation

elif st.session_state.logged_in:

    st.sidebar.success(
        f"Welcome, {st.session_state.user_name}"
    )

    menu = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "👤 Profile",
            "🚪 Logout"
        ]
    )

else:

    menu = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Home",
            "🔐 Login",
            "📝 Register",
            "ℹ About"
        ]
    )

st.sidebar.markdown(
    """<div class="sidebar-footer-card">
<p><strong>TalentSphere Elevate</strong><br>
AI-powered placement and career development platform · v2.0</p>
</div>""",
    unsafe_allow_html=True
)


# ==========================================================
# COLLEGE DASHBOARD NAVIGATION
# ==========================================================

def open_college_page(page_name):
    """Open a College Student module from a dashboard button."""
    set_college_navigation(page_name)


# ==========================================================
# PUBLIC HOME PAGE
# ==========================================================

if menu == "🏠 Home":

    st.markdown("""
        <div class="hero">
            <h1>🎯 TalentSphere Elevate</h1>
            <p>AI-Powered Career Development Platform</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown("""
            <div class="metric-card">
                <h2>12K+</h2>
                <p>Students</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
            <div class="metric-card">
                <h2>540+</h2>
                <p>Courses</p>
            </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown("""
            <div class="metric-card">
                <h2>125</h2>
                <p>Career Paths</p>
            </div>
        """, unsafe_allow_html=True)

    with col4:

        st.markdown("""
            <div class="metric-card">
                <h2>96%</h2>
                <p>Success Rate</p>
            </div>
        """, unsafe_allow_html=True)

    st.write("")

    growth_data = pd.DataFrame({
        "Month": [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June"
        ],
        "Users": [
            500,
            1200,
            2500,
            4500,
            7600,
            12000
        ]
    })

    left, right = st.columns([2, 1])

    with left:

        growth_chart = px.area(
            growth_data,
            x="Month",
            y="Users",
            title="Platform Growth"
        )

        growth_chart.update_layout(height=400)

        st.plotly_chart(
            growth_chart,
            width="stretch"
        )

    with right:

        st.info("""
### 🤖 Platform Capabilities

✅ Career Explorer

✅ Subject-wise Quiz

✅ Interest Assessment

✅ Skills Roadmap

✅ School Subjects

✅ Aptitude Practice

✅ Goal Tracking

✅ AI Study Mentor
        """)

    st.subheader("🚀 Platform Features")

    feature1, feature2, feature3 = st.columns(3)

    with feature1:

        st.markdown("""
            <div class="card">
                <h3>👨‍🎓 School Students</h3>
                <p>Career Explorer</p>
                <p>Interest Assessment</p>
                <p>Daily Study Planner</p>
                <p>Goal Tracking</p>
                <p>AI Study Mentor</p>
            </div>
        """, unsafe_allow_html=True)

    with feature2:

        st.markdown("""
            <div class="card">
                <h3>🏠 College Dashboard</h3>
                <p>Coding Practice</p>
                <p>Resume Builder</p>
                <p>Mock Interviews</p>
                <p>Placement Tracking</p>
                <p>Skill Gap Analysis</p>
            </div>
        """, unsafe_allow_html=True)

    with feature3:

        st.markdown("""
            <div class="card">
                <h3>👨‍💼 Professionals</h3>
                <p>Career Growth</p>
                <p>Promotion Readiness</p>
                <p>Industry Skills</p>
                <p>AI Coaching</p>
                <p>Certifications</p>
            </div>
        """, unsafe_allow_html=True)


# ==========================================================
# REGISTER PAGE
# ==========================================================

elif menu == "📝 Register":

    st.title("📝 Create an Account")

    st.write(
        "Register to access personalised career development features."
    )

    with st.form("registration_form"):

        fullname = st.text_input(
            "Full Name *"
        )

        email = st.text_input(
            "Email Address *"
        )

        password = st.text_input(
            "Password *",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password *",
            type="password"
        )

        role = st.selectbox(
            "Select Category *",
            [
                "School Student",
                "College Student",
                "Professional"
            ]
        )

        register_button = st.form_submit_button(
            "Create Account",
            width="stretch"
        )

    if register_button:

        if not fullname.strip():

            st.error("Full name is required.")

        elif not email.strip():

            st.error("Email address is required.")

        elif "@" not in email or "." not in email:

            st.error("Enter a valid email address.")

        elif len(password) < 6:

            st.error(
                "Password must contain at least six characters."
            )

        elif password != confirm_password:

            st.error("Passwords do not match.")

        else:

            success, message = register_user(
                fullname.strip(),
                email.strip(),
                password,
                role
            )

            if success:

                st.success(
                    "Registration successful. You can now log in."
                )

            else:

                st.error(message)


# ==========================================================
# LOGIN PAGE
# ==========================================================

elif menu == "🔐 Login":

    brand_column, form_column = st.columns(
        [1.08, 0.92],
        gap="large"
    )

    with brand_column:

        st.markdown(
            """<div class="auth-brand-panel">
<div>
<div class="auth-brand-logo">🎯</div>
<h2>Shape your future with confidence.</h2>
<p>
TalentSphere Elevate helps students understand their interests,
strengthen school subjects and build a clear roadmap toward their
future career.
</p>

<div class="auth-feature-list">
<div class="auth-feature">
<span class="auth-feature-icon">✓</span>
Personalised career exploration
</div>

<div class="auth-feature">
<span class="auth-feature-icon">✓</span>
Subject-wise dynamic assessments
</div>

<div class="auth-feature">
<span class="auth-feature-icon">✓</span>
Study planning and progress tracking
</div>

<div class="auth-feature">
<span class="auth-feature-icon">✓</span>
AI-powered academic guidance
</div>
</div>
</div>

<p class="auth-brand-footer">
Learn better · Plan smarter · Grow confidently
</p>
</div>""",
            unsafe_allow_html=True
        )

    with form_column:

        st.markdown(
            """<div class="auth-form-heading">
<div class="auth-eyebrow">Secure student access</div>
<div class="auth-page-header">
<h1>Welcome back</h1>
<p>
Sign in to continue your personalised learning and career journey.
</p>
</div>
</div>""",
            unsafe_allow_html=True
        )

        with st.form(
            "login_form",
            clear_on_submit=False
        ):

            email = st.text_input(
                "Email address",
                placeholder="name@example.com",
                autocomplete="email"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                autocomplete="current-password"
            )

            login_button = st.form_submit_button(
                "Sign in to TalentSphere",
                width="stretch"
            )

        st.markdown(
            """<div class="auth-security-note">
<strong>🔒 Secure login:</strong>
Your password is verified using a stored password hash.
TalentSphere does not display your password.
</div>""",
            unsafe_allow_html=True
        )

        if login_button:

            clean_email = email.strip().lower()

            if not clean_email or not password:

                st.error(
                    "Please enter both your email address and password."
                )

            else:

                user = authenticate_user(
                    clean_email,
                    password
                )

                if user:

                    st.session_state.logged_in = True
                    st.session_state.user_id = user[0]
                    st.session_state.user_name = user[1]
                    st.session_state.user_email = user[2]
                    st.session_state.user_role = user[3]

                    st.success("Login successful.")
                    st.rerun()

                else:

                    st.error(
                        "The email address or password is incorrect."
                    )



# ==========================================================
# COLLEGE STUDENT DASHBOARD
# ==========================================================

elif menu == "🏠 College Dashboard":

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            college_name,
            degree,
            branch,
            current_year,
            cgpa,
            technical_skills,
            programming_languages,
            tools,
            projects,
            internships,
            preferred_role,
            preferred_location,
            placement_status
        FROM college_profiles
        WHERE user_id = ?
        """,
        (st.session_state.user_id,)
    )

    profile = cursor.fetchone()

    cursor.execute(
        """
        SELECT AVG(score), COUNT(*)
        FROM coding_results
        WHERE user_id = ?
        """,
        (st.session_state.user_id,)
    )

    coding_row = cursor.fetchone()
    coding_score = round(coding_row[0] or 0)
    coding_tests = int(coding_row[1] or 0)

    cursor.execute(
        """
        SELECT AVG(score), COUNT(*)
        FROM mock_interview_results
        WHERE user_id = ?
        """,
        (st.session_state.user_id,)
    )

    interview_row = cursor.fetchone()
    interview_score = round(interview_row[0] or 0)
    mock_count = int(interview_row[1] or 0)

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM placement_applications
        WHERE user_id = ?
        """,
        (st.session_state.user_id,)
    )

    application_count = cursor.fetchone()[0]

    connection.close()

    def studio_load_list(value):
        try:
            return json.loads(value) if value else []
        except (json.JSONDecodeError, TypeError):
            return []

    if profile:
        college_name = profile[0] or "College not added"
        degree = profile[1] or "-"
        branch = profile[2] or "-"
        current_year = profile[3] or "-"
        cgpa = float(profile[4] or 0)
        technical_skills = studio_load_list(profile[5])
        programming_languages = studio_load_list(profile[6])
        tools = studio_load_list(profile[7])
        projects_text = profile[8] or ""
        internships_text = profile[9] or ""
        preferred_role = profile[10] or "Software Developer"
        preferred_location = profile[11] or "Any Location"
        placement_status = profile[12] or "Not Started"
        profile_complete = True
    else:
        college_name = "Complete your college profile"
        degree = "-"
        branch = "-"
        current_year = "-"
        cgpa = 0
        technical_skills = []
        programming_languages = []
        tools = []
        projects_text = ""
        internships_text = ""
        preferred_role = "Software Developer"
        preferred_location = "Any Location"
        placement_status = "Not Started"
        profile_complete = False

    all_skills = (
        technical_skills
        + programming_languages
        + tools
    )

    project_word_count = len(projects_text.split())

    resume_score = min(
        100,
        25
        + len(all_skills) * 4
        + (22 if projects_text.strip() else 0)
        + (12 if internships_text.strip() else 0)
    )

    project_score = min(
        100,
        20 + project_word_count * 2
    ) if projects_text.strip() else 18

    experience_score = (
        82 if internships_text.strip() else 28
    )

    communication_score = interview_score

    placement_score = round(
        resume_score * 0.25
        + coding_score * 0.30
        + project_score * 0.20
        + communication_score * 0.15
        + experience_score * 0.10
    )

    role_skills = {
        "Software Developer": {
            "Python",
            "Java",
            "C++",
            "SQL",
            "Data Structures & Algorithms",
            "Git"
        },
        "Backend Developer": {
            "Python",
            "Java",
            "Node.js",
            "SQL",
            "Database Management",
            "REST APIs"
        },
        "Data Analyst": {
            "Python",
            "SQL",
            "Pandas",
            "Power BI",
            "Statistics"
        },
        "AI Engineer": {
            "Python",
            "Machine Learning",
            "Deep Learning",
            "TensorFlow",
            "PyTorch"
        },
        "QA Engineer": {
            "Java",
            "Python",
            "SQL",
            "Testing",
            "Git"
        }
    }

    current_skill_set = set(all_skills)

    job_matches = []

    for role_name, required_skills in role_skills.items():

        skill_component = (
            len(current_skill_set & required_skills)
            / len(required_skills)
            * 55
        )

        cgpa_component = min(
            cgpa / 10 * 15,
            15
        )

        resume_component = resume_score * 0.15
        coding_component = coding_score * 0.15

        match_score = round(
            skill_component
            + cgpa_component
            + resume_component
            + coding_component
        )

        job_matches.append({
            "Job Role": role_name,
            "Match %": min(match_score, 100)
        })

    job_matches = sorted(
        job_matches,
        key=lambda item: item["Match %"],
        reverse=True
    )

    top_role = job_matches[0]
    missing_skills = sorted(
        role_skills[top_role["Job Role"]]
        - current_skill_set
    )

    st.markdown(
        f"""<div class="studio-hero">
<span class="studio-badge">TalentSphere College Dashboard</span>
<h1>Your complete placement preparation dashboard.</h1>
<p>
Welcome, {st.session_state.user_name}. Your dashboard brings together
resume quality, coding performance, interview preparation, projects,
internships and job matching in one professional workspace.
</p>
</div>""",
        unsafe_allow_html=True
    )

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.markdown(
            f"""<div class="studio-kpi">
<div class="studio-kpi-icon">🎯</div>
<div class="studio-kpi-label">Placement Readiness</div>
<p class="studio-kpi-value">{placement_score}/100</p>
<div class="studio-kpi-sub">Weighted career readiness score</div>
</div>""",
            unsafe_allow_html=True
        )

    with kpi2:
        st.markdown(
            f"""<div class="studio-kpi">
<div class="studio-kpi-icon">📄</div>
<div class="studio-kpi-label">Resume Strength</div>
<p class="studio-kpi-value">{resume_score}%</p>
<div class="studio-kpi-sub">ATS and profile completeness</div>
</div>""",
            unsafe_allow_html=True
        )

    with kpi3:
        st.markdown(
            f"""<div class="studio-kpi">
<div class="studio-kpi-icon">💻</div>
<div class="studio-kpi-label">Coding Performance</div>
<p class="studio-kpi-value">{coding_score}%</p>
<div class="studio-kpi-sub">{coding_tests} practice test(s) completed</div>
</div>""",
            unsafe_allow_html=True
        )

    with kpi4:
        st.markdown(
            f"""<div class="studio-kpi">
<div class="studio-kpi-icon">🧠</div>
<div class="studio-kpi-label">Top Job Match</div>
<p class="studio-kpi-value">{top_role['Match %']}%</p>
<div class="studio-kpi-sub">{top_role['Job Role']}</div>
</div>""",
            unsafe_allow_html=True
        )

    st.write("")
    st.markdown(
        """
        <div style="
            display:flex;
            align-items:center;
            gap:12px;
            background:#FFFFFF;
            border:1px solid #DCE6F3;
            border-left:6px solid #2563EB;
            border-radius:16px;
            padding:17px 20px;
            margin:14px 0 20px 0;
            box-shadow:0 7px 22px rgba(15,23,42,0.07);
        ">
            <div style="
                width:42px;
                height:42px;
                border-radius:12px;
                background:#EFF6FF;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:22px;
            ">🧠</div>
            <div>
                <div style="
                    color:#0F172A !important;
                    font-size:25px;
                    line-height:1.15;
                    font-weight:800;
                    letter-spacing:-0.02em;
                ">Career Intelligence</div>
                <div style="
                    color:#64748B !important;
                    font-size:13px;
                    margin-top:4px;
                ">
                    AI-based analysis of your placement readiness and career direction
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    intelligence_left, intelligence_right = st.columns(
        [1.32, 1],
        gap="large"
    )

    with intelligence_left:

        progress_df = pd.DataFrame({
            "Readiness Area": [
                "Resume",
                "Coding",
                "Projects",
                "Interview",
                "Experience"
            ],
            "Score": [
                resume_score,
                coding_score,
                project_score,
                communication_score,
                experience_score
            ]
        })

        progress_chart = px.bar(
            progress_df,
            x="Score",
            y="Readiness Area",
            orientation="h",
            text="Score",
            range_x=[0, 100],
            title="Readiness Breakdown"
        )

        progress_chart.update_layout(
            height=405,
            margin=dict(l=15, r=20, t=55, b=20),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            font=dict(
                color="#0F172A",
                size=13
            ),
            title_font=dict(
                color="#0F172A",
                size=19
            ),
            xaxis=dict(
                title_font=dict(color="#334155"),
                tickfont=dict(color="#475569"),
                gridcolor="#E2E8F0",
                zerolinecolor="#CBD5E1"
            ),
            yaxis=dict(
                title_font=dict(color="#334155"),
                tickfont=dict(color="#334155")
            )
        )

        progress_chart.update_traces(
            textfont=dict(color="#0F172A"),
            marker_line_width=0
        )

        st.plotly_chart(
            progress_chart,
            width="stretch"
        )

    with intelligence_right:

        skill_chips = "".join(
            f'<span class="studio-chip">{skill}</span>'
            for skill in sorted(current_skill_set)[:8]
        )

        st.markdown(
            f"""<div class="studio-panel">
<h3>⭐ Recommended Career Direction</h3>
<div class="studio-role-card">
<div class="studio-role-title">{top_role['Job Role']}</div>
<div class="studio-match">{top_role['Match %']}% profile match</div>
</div>
<p><strong>Preferred role:</strong> {preferred_role}</p>
<p><strong>Preferred location:</strong> {preferred_location}</p>
<p><strong>Current status:</strong> {placement_status}</p>
<div>{skill_chips if skill_chips else '<span class="studio-chip">Add skills in profile</span>'}</div>
</div>""",
            unsafe_allow_html=True
        )

    st.write("")
    overview_left, overview_right = st.columns(
        [1, 1],
        gap="large"
    )

    with overview_left:

        status_class = (
            "studio-status-good"
            if profile_complete
            else "studio-status-progress"
        )

        status_text = (
            "Profile Complete"
            if profile_complete
            else "Action Required"
        )

        st.markdown(
            f"""<div class="studio-panel">
<h3>👤 Academic & Placement Profile</h3>
<p><span class="{status_class}">{status_text}</span></p>
<p><strong>College:</strong> {college_name}</p>
<p><strong>Programme:</strong> {degree} — {branch}</p>
<p><strong>Year:</strong> {current_year}</p>
<p><strong>CGPA:</strong> {cgpa:.2f}</p>
<p><strong>Applications tracked:</strong> {application_count}</p>
<p><strong>Mock interviews:</strong> {mock_count}</p>
</div>""",
            unsafe_allow_html=True
        )

    with overview_right:

        action_items = []

        if not profile_complete:
            action_items.append(
                ("Complete profile", "Add education, skills, links and career goals.")
            )

        if coding_score < 70:
            action_items.append(
                ("Improve coding score", "Complete Python, DSA and DBMS practice tests.")
            )

        if not projects_text.strip():
            action_items.append(
                ("Add a strong project", "Build and document one complete CRUD or AI project.")
            )

        if interview_score < 70:
            action_items.append(
                ("Practise interviews", "Complete one technical and one HR mock interview.")
            )

        if missing_skills:
            action_items.append(
                (
                    f"Learn {missing_skills[0]}",
                    "This is a missing skill for your highest-matching role."
                )
            )

        action_html = "".join(
            f"""<div class="studio-action">
<strong>{title}</strong><br>
<span>{description}</span>
</div>"""
            for title, description in action_items[:5]
        )

        if not action_html:
            action_html = """<div class="studio-action">
<strong>Maintain momentum</strong><br>
<span>Continue applications, coding practice and portfolio updates.</span>
</div>"""

        st.markdown(
            f"""<div class="studio-panel">
<h3>📌 Priority Actions</h3>
{action_html}
</div>""",
            unsafe_allow_html=True
        )

        priority_button1, priority_button2 = st.columns(2)

        with priority_button1:
            st.button(
                "Update Profile",
                key="priority_profile_button",
                use_container_width=True,
                on_click=open_college_page,
                args=("👤 College Profile",)
            )

        with priority_button2:
            st.button(
                "Open Skill Analysis",
                key="priority_skill_button",
                use_container_width=True,
                on_click=open_college_page,
                args=("📊 Skill Gap Analysis",)
            )

    st.write("")
    st.markdown(
        '<div class="studio-section-title">Placement Tools</div>',
        unsafe_allow_html=True
    )

    module1, module2, module3, module4 = st.columns(4)

    with module1:
        st.markdown(
            """<div class="studio-module-card">
<div style="font-size:25px;">📄</div>
<h4>Resume Builder</h4>
<p>Create an ATS-friendly resume and improve keywords, summary and project impact.</p>
<span class="studio-status-good">Ready</span>
</div>""",
            unsafe_allow_html=True
        )
        st.button(
            "Open Resume Builder",
            key="dashboard_resume_builder",
            use_container_width=True,
            on_click=open_college_page,
            args=("📄 Resume Builder",)
        )

    with module2:
        st.markdown(
            """<div class="studio-module-card">
<div style="font-size:25px;">💻</div>
<h4>Coding Practice</h4>
<p>Complete Python, Data Structures and DBMS assessments and improve your score.</p>
<span class="studio-status-good">Ready</span>
</div>""",
            unsafe_allow_html=True
        )
        st.button(
            "Start Coding Practice",
            key="dashboard_coding_practice",
            use_container_width=True,
            on_click=open_college_page,
            args=("💻 Coding Practice",)
        )

    with module3:
        st.markdown(
            """<div class="studio-module-card">
<div style="font-size:25px;">🎤</div>
<h4>Mock Interview</h4>
<p>Practise HR, technical and behavioural questions with scoring and feedback.</p>
<span class="studio-status-progress">Practice</span>
</div>""",
            unsafe_allow_html=True
        )
        st.button(
            "Start Mock Interview",
            key="dashboard_mock_interview",
            use_container_width=True,
            on_click=open_college_page,
            args=("🧑‍💼 Mock Interviews",)
        )

    with module4:
        st.markdown(
            """<div class="studio-module-card">
<div style="font-size:25px;">🧠</div>
<h4>Job Matching</h4>
<p>Compare your profile with suitable roles using skills, CGPA and performance.</p>
<span class="studio-status-good">Available</span>
</div>""",
            unsafe_allow_html=True
        )
        st.button(
            "View Job Matches",
            key="dashboard_job_matching",
            use_container_width=True,
            on_click=open_college_page,
            args=("🧠 Job Matching Engine",)
        )

    st.write("")
    quick1, quick2, quick3, quick4 = st.columns(4)

    with quick1:
        st.button(
            "👤 Complete Profile",
            key="dashboard_profile",
            use_container_width=True,
            on_click=open_college_page,
            args=("👤 College Profile",)
        )

    with quick2:
        st.button(
            "✅ Review Resume",
            key="dashboard_ats",
            use_container_width=True,
            on_click=open_college_page,
            args=("✅ ATS Resume Checker",)
        )

    with quick3:
        st.button(
            "📊 Analyse Skill Gap",
            key="dashboard_skill_gap",
            use_container_width=True,
            on_click=open_college_page,
            args=("📊 Skill Gap Analysis",)
        )

    with quick4:
        st.button(
            "🎯 Track Placements",
            key="dashboard_placement",
            use_container_width=True,
            on_click=open_college_page,
            args=("🎯 Placement Tracker",)
        )

    st.write("")
    match_col, plan_col = st.columns(
        [1, 1],
        gap="large"
    )

    with match_col:

        st.subheader("💼 Job Match Ranking")

        st.dataframe(
            pd.DataFrame(job_matches),
            width="stretch",
            hide_index=True
        )

        st.button(
            "Open Full Job Matching Engine",
            key="dashboard_full_job_match",
            use_container_width=True,
            on_click=open_college_page,
            args=("🧠 Job Matching Engine",)
        )

    with plan_col:

        st.subheader("📅 Personal 30-Day Plan")

        plan_rows = [
            {
                "Week": "Week 1",
                "Focus": (
                    f"Learn {missing_skills[0]}"
                    if missing_skills
                    else "Improve resume keywords"
                )
            },
            {
                "Week": "Week 2",
                "Focus": (
                    f"Practise {missing_skills[1]}"
                    if len(missing_skills) > 1
                    else "Complete 3 coding tests"
                )
            },
            {
                "Week": "Week 3",
                "Focus": "Build and publish one portfolio project"
            },
            {
                "Week": "Week 4",
                "Focus": "Mock interview and targeted applications"
            }
        ]

        st.dataframe(
            pd.DataFrame(plan_rows),
            width="stretch",
            hide_index=True
        )

        st.button(
            "Start Daily Coding Challenge",
            key="dashboard_daily_challenge",
            use_container_width=True,
            on_click=open_college_page,
            args=("🔥 Daily Coding Challenge",)
        )




# ==========================================================
# COLLEGE STUDENT PROFILE
# ==========================================================

elif menu == "👤 College Profile":

    st.markdown(
        """<div class="college-profile-header">
<h1>👤 College Career Profile</h1>
<p>
Create a complete academic and placement profile for personalised
resume, coding, internship and job recommendations.
</p>
</div>""",
        unsafe_allow_html=True
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            college_name,
            degree,
            branch,
            current_year,
            semester,
            university,
            city,
            phone,
            cgpa,
            backlogs,
            technical_skills,
            programming_languages,
            tools,
            certifications,
            projects,
            internships,
            career_goal,
            preferred_role,
            preferred_location,
            linkedin_pdf_path,
            github_url,
            portfolio_url,
            placement_status
        FROM college_profiles
        WHERE user_id = ?
        """,
        (st.session_state.user_id,)
    )

    profile = cursor.fetchone()
    connection.close()

    def safe_json_list(value):
        try:
            return json.loads(value) if value else []
        except (json.JSONDecodeError, TypeError):
            return []

    if profile:

        saved_profile = {
            "college_name": profile[0] or "",
            "degree": profile[1] or "B.Tech",
            "branch": profile[2] or "CSE (AI & ML)",
            "current_year": profile[3] or "3rd Year",
            "semester": profile[4] or "6th Semester",
            "university": profile[5] or "",
            "city": profile[6] or "",
            "phone": profile[7] or "",
            "cgpa": float(profile[8] or 0.0),
            "backlogs": int(profile[9] or 0),
            "technical_skills": safe_json_list(profile[10]),
            "programming_languages": safe_json_list(profile[11]),
            "tools": safe_json_list(profile[12]),
            "certifications": profile[13] or "",
            "projects": profile[14] or "",
            "internships": profile[15] or "",
            "career_goal": profile[16] or "",
            "preferred_role": profile[17] or "",
            "preferred_location": profile[18] or "",
            "linkedin_pdf_path": profile[19] or "",
            "github_url": profile[20] or "",
            "portfolio_url": profile[21] or "",
            "placement_status": profile[22] or "Not Started"
        }

    else:

        saved_profile = {
            "college_name": "",
            "degree": "B.Tech",
            "branch": "CSE (AI & ML)",
            "current_year": "3rd Year",
            "semester": "6th Semester",
            "university": "",
            "city": "",
            "phone": "",
            "cgpa": 0.0,
            "backlogs": 0,
            "technical_skills": [],
            "programming_languages": [],
            "tools": [],
            "certifications": "",
            "projects": "",
            "internships": "",
            "career_goal": "",
            "preferred_role": "",
            "preferred_location": "",
            "linkedin_pdf_path": "",
            "github_url": "",
            "portfolio_url": "",
            "placement_status": "Not Started"
        }

    with st.form("college_profile_form"):

        st.subheader("🎓 Academic Information")

        academic_col1, academic_col2 = st.columns(2)

        with academic_col1:

            st.text_input(
                "Full Name",
                value=st.session_state.user_name,
                disabled=True
            )

            st.text_input(
                "Email Address",
                value=st.session_state.user_email,
                disabled=True
            )

            college_name = st.text_input(
                "College Name *",
                value=saved_profile["college_name"]
            )

            degree_options = [
                "B.Tech",
                "B.E",
                "B.Sc",
                "BCA",
                "B.Com",
                "BBA",
                "M.Tech",
                "MCA",
                "MBA",
                "Other"
            ]

            degree_index = (
                degree_options.index(saved_profile["degree"])
                if saved_profile["degree"] in degree_options
                else 0
            )

            degree = st.selectbox(
                "Degree *",
                degree_options,
                index=degree_index
            )

            branch = st.text_input(
                "Branch / Specialisation *",
                value=saved_profile["branch"],
                placeholder="Example: CSE (AI & ML)"
            )

            university = st.text_input(
                "University",
                value=saved_profile["university"]
            )

        with academic_col2:

            year_options = [
                "1st Year",
                "2nd Year",
                "3rd Year",
                "4th Year",
                "5th Year",
                "Completed"
            ]

            year_index = (
                year_options.index(saved_profile["current_year"])
                if saved_profile["current_year"] in year_options
                else 2
            )

            current_year = st.selectbox(
                "Current Year *",
                year_options,
                index=year_index
            )

            semester_options = [
                "1st Semester",
                "2nd Semester",
                "3rd Semester",
                "4th Semester",
                "5th Semester",
                "6th Semester",
                "7th Semester",
                "8th Semester",
                "Completed"
            ]

            semester_index = (
                semester_options.index(saved_profile["semester"])
                if saved_profile["semester"] in semester_options
                else 5
            )

            semester = st.selectbox(
                "Current Semester",
                semester_options,
                index=semester_index
            )

            cgpa = st.number_input(
                "CGPA",
                min_value=0.0,
                max_value=10.0,
                value=saved_profile["cgpa"],
                step=0.01
            )

            backlogs = st.number_input(
                "Active Backlogs",
                min_value=0,
                max_value=50,
                value=saved_profile["backlogs"],
                step=1
            )

            city = st.text_input(
                "City",
                value=saved_profile["city"]
            )

            phone = st.text_input(
                "Phone Number",
                value=saved_profile["phone"]
            )

        st.subheader("💻 Technical Profile")

        technical_skills = st.multiselect(
            "Technical Skills",
            [
                "Data Structures & Algorithms",
                "Object-Oriented Programming",
                "Database Management",
                "Operating Systems",
                "Computer Networks",
                "Machine Learning",
                "Deep Learning",
                "Data Science",
                "Web Development",
                "Cloud Computing",
                "Cybersecurity",
                "DevOps",
                "Mobile Development",
                "UI/UX Design"
            ],
            default=saved_profile["technical_skills"]
        )

        programming_languages = st.multiselect(
            "Programming Languages",
            [
                "Python",
                "C",
                "C++",
                "Java",
                "JavaScript",
                "TypeScript",
                "SQL",
                "R",
                "Go",
                "C#",
                "Kotlin",
                "Swift"
            ],
            default=saved_profile["programming_languages"]
        )

        tools = st.multiselect(
            "Tools and Platforms",
            [
                "Git",
                "GitHub",
                "VS Code",
                "Jupyter Notebook",
                "Postman",
                "MongoDB",
                "MySQL",
                "Docker",
                "Kubernetes",
                "AWS",
                "Azure",
                "Google Cloud",
                "Linux",
                "Figma",
                "Power BI",
                "Tableau"
            ],
            default=saved_profile["tools"]
        )

        certifications = st.text_area(
            "Certifications",
            value=saved_profile["certifications"],
            placeholder=(
                "Example: NPTEL Python, AWS Cloud Practitioner, "
                "Infosys Springboard certification"
            )
        )

        projects = st.text_area(
            "Projects",
            value=saved_profile["projects"],
            placeholder=(
                "Mention project name, technologies used and your contribution."
            )
        )

        internships = st.text_area(
            "Internships / Training",
            value=saved_profile["internships"],
            placeholder=(
                "Mention company, role, duration and major work completed."
            )
        )

        st.subheader("🎯 Career and Placement Preferences")

        placement_col1, placement_col2 = st.columns(2)

        with placement_col1:

            career_goal = st.text_area(
                "Career Goal",
                value=saved_profile["career_goal"],
                placeholder=(
                    "Example: Become a full-stack developer and secure "
                    "a product-based company role."
                )
            )

            preferred_role = st.text_input(
                "Preferred Job Role",
                value=saved_profile["preferred_role"],
                placeholder="Example: Software Engineer"
            )

            preferred_location = st.text_input(
                "Preferred Job Location",
                value=saved_profile["preferred_location"],
                placeholder="Example: Bengaluru, Hyderabad or Remote"
            )

        with placement_col2:

            status_options = [
                "Not Started",
                "Preparing",
                "Applied",
                "Assessment Cleared",
                "Interview Stage",
                "Offer Received"
            ]

            status_index = (
                status_options.index(saved_profile["placement_status"])
                if saved_profile["placement_status"] in status_options
                else 0
            )

            placement_status = st.selectbox(
                "Placement Status",
                status_options,
                index=status_index
            )

            st.markdown("#### 📄 LinkedIn Profile PDF")

            linkedin_pdf = st.file_uploader(
                "Upload LinkedIn Profile PDF",
                type=["pdf"],
                help=(
                    "Open your LinkedIn profile, choose Print, and save it "
                    "as a PDF before uploading it here."
                ),
                key="college_linkedin_pdf"
            )

            if saved_profile["linkedin_pdf_path"]:
                st.caption(
                    "A LinkedIn profile PDF is already saved. "
                    "Upload another PDF only when you want to replace it."
                )

            github_url = st.text_input(
                "GitHub Profile URL",
                value=saved_profile["github_url"],
                placeholder="https://github.com/username"
            )

            portfolio_url = st.text_input(
                "Portfolio URL",
                value=saved_profile["portfolio_url"],
                placeholder="https://yourportfolio.com"
            )

        save_profile = st.form_submit_button(
            "💾 Save College Profile",
            width="stretch"
        )

    if save_profile:

        if not college_name.strip():

            st.error("College name is required.")

        elif not branch.strip():

            st.error("Branch or specialisation is required.")

        elif not programming_languages:

            st.error(
                "Select at least one programming language."
            )

        else:

            linkedin_pdf_path = saved_profile["linkedin_pdf_path"]

            if linkedin_pdf is not None:
                try:
                    linkedin_pdf_path = save_linkedin_pdf(
                        linkedin_pdf,
                        st.session_state.user_id
                    )
                except (OSError, ValueError) as error:
                    st.error(f"Unable to save LinkedIn PDF: {error}")
                    st.stop()

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO college_profiles (
                    user_id,
                    college_name,
                    degree,
                    branch,
                    current_year,
                    semester,
                    university,
                    city,
                    phone,
                    cgpa,
                    backlogs,
                    technical_skills,
                    programming_languages,
                    tools,
                    certifications,
                    projects,
                    internships,
                    career_goal,
                    preferred_role,
                    preferred_location,
                    linkedin_pdf_path,
                    github_url,
                    portfolio_url,
                    placement_status,
                    updated_at
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                ON CONFLICT(user_id)
                DO UPDATE SET
                    college_name = excluded.college_name,
                    degree = excluded.degree,
                    branch = excluded.branch,
                    current_year = excluded.current_year,
                    semester = excluded.semester,
                    university = excluded.university,
                    city = excluded.city,
                    phone = excluded.phone,
                    cgpa = excluded.cgpa,
                    backlogs = excluded.backlogs,
                    technical_skills = excluded.technical_skills,
                    programming_languages = excluded.programming_languages,
                    tools = excluded.tools,
                    certifications = excluded.certifications,
                    projects = excluded.projects,
                    internships = excluded.internships,
                    career_goal = excluded.career_goal,
                    preferred_role = excluded.preferred_role,
                    preferred_location = excluded.preferred_location,
                    linkedin_pdf_path = excluded.linkedin_pdf_path,
                    github_url = excluded.github_url,
                    portfolio_url = excluded.portfolio_url,
                    placement_status = excluded.placement_status,
                    updated_at = excluded.updated_at
                """,
                (
                    st.session_state.user_id,
                    college_name.strip(),
                    degree,
                    branch.strip(),
                    current_year,
                    semester,
                    university.strip(),
                    city.strip(),
                    phone.strip(),
                    float(cgpa),
                    int(backlogs),
                    json.dumps(technical_skills),
                    json.dumps(programming_languages),
                    json.dumps(tools),
                    certifications.strip(),
                    projects.strip(),
                    internships.strip(),
                    career_goal.strip(),
                    preferred_role.strip(),
                    preferred_location.strip(),
                    linkedin_pdf_path,
                    github_url.strip(),
                    portfolio_url.strip(),
                    placement_status,
                    datetime.now().isoformat()
                )
            )

            connection.commit()
            connection.close()

            st.success(
                "College student profile saved successfully."
            )
            st.rerun()

    if profile:

        st.divider()
        st.subheader("📋 Placement Profile Summary")

        summary1, summary2, summary3 = st.columns(3)

        with summary1:
            st.write(
                f"**College:** {saved_profile['college_name']}"
            )
            st.write(
                f"**Degree:** {saved_profile['degree']}"
            )
            st.write(
                f"**Branch:** {saved_profile['branch']}"
            )

        with summary2:
            st.write(
                f"**Year:** {saved_profile['current_year']}"
            )
            st.write(
                f"**CGPA:** {saved_profile['cgpa']:.2f}"
            )
            st.write(
                f"**Backlogs:** {saved_profile['backlogs']}"
            )

        with summary3:
            st.write(
                f"**Preferred Role:** "
                f"{saved_profile['preferred_role'] or '-'}"
            )
            st.write(
                f"**Placement Status:** "
                f"{saved_profile['placement_status']}"
            )
            st.write(
                f"**GitHub:** {saved_profile['github_url'] or '-'}"
            )

        saved_linkedin_pdf = get_existing_pdf_bytes(
            saved_profile["linkedin_pdf_path"]
        )

        if saved_linkedin_pdf:
            st.download_button(
                "📥 Download Saved LinkedIn Profile PDF",
                data=saved_linkedin_pdf,
                file_name=Path(
                    saved_profile["linkedin_pdf_path"]
                ).name,
                mime="application/pdf",
                width="stretch"
            )
        elif saved_profile["linkedin_pdf_path"]:
            st.warning(
                "The saved LinkedIn PDF file could not be found. "
                "Please upload it again."
            )


# ==========================================================
# CODING PRACTICE
# ==========================================================

elif menu == "💻 Coding Practice":

    st.title("💻 Coding Practice")
    st.write(
        "Practice placement-oriented programming, DSA and core CS questions."
    )

    coding_bank = {
        "Python": {
            "Easy": [
                {
                    "question": "What is the output of len({1, 1, 2, 3})?",
                    "options": ["3", "4", "2", "Error"],
                    "answer": "3",
                    "explanation": "A set stores only unique values."
                },
                {
                    "question": "Which keyword creates a function in Python?",
                    "options": ["function", "define", "def", "fun"],
                    "answer": "def",
                    "explanation": "Python functions are declared using def."
                },
                {
                    "question": "Which data type is immutable?",
                    "options": ["List", "Dictionary", "Set", "Tuple"],
                    "answer": "Tuple",
                    "explanation": "Tuple elements cannot be changed after creation."
                },
                {
                    "question": "What does range(3) generate?",
                    "options": ["1,2,3", "0,1,2", "0,1,2,3", "3 only"],
                    "answer": "0,1,2",
                    "explanation": "The stop value is excluded."
                },
                {
                    "question": "Which operator checks equality?",
                    "options": ["=", "==", "!=", "is not"],
                    "answer": "==",
                    "explanation": "== compares values for equality."
                }
            ],
            "Medium": [
                {
                    "question": "What is the output of [x*x for x in range(4)]?",
                    "options": [
                        "[0, 1, 4, 9]",
                        "[1, 4, 9, 16]",
                        "[0, 1, 2, 3]",
                        "Error"
                    ],
                    "answer": "[0, 1, 4, 9]",
                    "explanation": "Each number from 0 to 3 is squared."
                },
                {
                    "question": "Which statement about shallow copy is correct?",
                    "options": [
                        "It recursively copies all nested objects",
                        "It creates a new outer object but shares nested objects",
                        "It returns the same reference",
                        "It works only for tuples"
                    ],
                    "answer": "It creates a new outer object but shares nested objects",
                    "explanation": "Nested references are shared in a shallow copy."
                },
                {
                    "question": "Which method safely retrieves a dictionary value?",
                    "options": ["fetch()", "get()", "read()", "value()"],
                    "answer": "get()",
                    "explanation": "get() can return a default instead of raising KeyError."
                },
                {
                    "question": "What is a generator mainly useful for?",
                    "options": [
                        "Storing all values immediately",
                        "Lazy iteration with low memory usage",
                        "Creating database tables",
                        "Compiling Python"
                    ],
                    "answer": "Lazy iteration with low memory usage",
                    "explanation": "Generators produce values on demand."
                },
                {
                    "question": "Which block always executes in exception handling?",
                    "options": ["try", "except", "else", "finally"],
                    "answer": "finally",
                    "explanation": "finally executes whether or not an exception occurs."
                }
            ],
            "Hard": [
                {
                    "question": "What is the time complexity of dictionary average lookup?",
                    "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
                    "answer": "O(1)",
                    "explanation": "Python dictionaries use hash tables."
                },
                {
                    "question": "Which mechanism controls access to Python object attributes?",
                    "options": [
                        "Descriptor protocol",
                        "Garbage collector",
                        "Bytecode cache",
                        "Virtual environment"
                    ],
                    "answer": "Descriptor protocol",
                    "explanation": "Descriptors implement __get__, __set__ or __delete__."
                },
                {
                    "question": "What does the GIL primarily affect?",
                    "options": [
                        "File reading",
                        "Parallel execution of Python bytecode in threads",
                        "SQL queries",
                        "Package installation"
                    ],
                    "answer": "Parallel execution of Python bytecode in threads",
                    "explanation": "Only one thread executes Python bytecode at a time in CPython."
                },
                {
                    "question": "What is monkey patching?",
                    "options": [
                        "Changing code behaviour at runtime",
                        "Installing packages",
                        "Encrypting source files",
                        "Converting Python to C"
                    ],
                    "answer": "Changing code behaviour at runtime",
                    "explanation": "Objects or modules are modified dynamically."
                },
                {
                    "question": "Which special method supports context managers?",
                    "options": [
                        "__enter__ and __exit__",
                        "__start__ and __stop__",
                        "__open__ and __close__",
                        "__begin__ and __end__"
                    ],
                    "answer": "__enter__ and __exit__",
                    "explanation": "They are used by the with statement."
                }
            ]
        },
        "Data Structures": {
            "Easy": [
                {
                    "question": "Which data structure follows LIFO?",
                    "options": ["Queue", "Stack", "Tree", "Graph"],
                    "answer": "Stack",
                    "explanation": "LIFO means last in, first out."
                },
                {
                    "question": "Binary search requires the array to be:",
                    "options": ["Random", "Sorted", "Reversed", "Unique"],
                    "answer": "Sorted",
                    "explanation": "Binary search repeatedly halves a sorted search range."
                },
                {
                    "question": "Which structure follows FIFO?",
                    "options": ["Stack", "Queue", "Heap", "BST"],
                    "answer": "Queue",
                    "explanation": "FIFO means first in, first out."
                },
                {
                    "question": "A linked-list node stores:",
                    "options": [
                        "Only data",
                        "Data and link/reference",
                        "Only index",
                        "Only address"
                    ],
                    "answer": "Data and link/reference",
                    "explanation": "The reference connects nodes."
                },
                {
                    "question": "The top element of a stack is removed using:",
                    "options": ["push", "pop", "enqueue", "insert"],
                    "answer": "pop",
                    "explanation": "pop removes the most recently added item."
                }
            ],
            "Medium": [
                {
                    "question": "Average search time in a balanced BST is:",
                    "options": ["O(1)", "O(log n)", "O(n)", "O(n²)"],
                    "answer": "O(log n)",
                    "explanation": "A balanced tree reduces the search space by levels."
                },
                {
                    "question": "Which traversal of a BST gives sorted order?",
                    "options": ["Preorder", "Inorder", "Postorder", "Level order"],
                    "answer": "Inorder",
                    "explanation": "Left-root-right visits keys in sorted order."
                },
                {
                    "question": "A priority queue is commonly implemented using:",
                    "options": ["Heap", "Stack", "Array only", "Linked list only"],
                    "answer": "Heap",
                    "explanation": "A heap supports efficient priority removal."
                },
                {
                    "question": "The worst-case search time in a hash table can be:",
                    "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
                    "answer": "O(n)",
                    "explanation": "Heavy collisions can degrade lookup to linear time."
                },
                {
                    "question": "Which algorithm finds the shortest path in an unweighted graph?",
                    "options": ["DFS", "BFS", "Prim", "Kruskal"],
                    "answer": "BFS",
                    "explanation": "BFS explores nodes by distance layers."
                }
            ],
            "Hard": [
                {
                    "question": "Amortised time for appending to a dynamic array is:",
                    "options": ["O(1)", "O(log n)", "O(n)", "O(n²)"],
                    "answer": "O(1)",
                    "explanation": "Occasional resizing is spread across many appends."
                },
                {
                    "question": "Which structure efficiently supports range-sum queries and updates?",
                    "options": ["Stack", "Segment tree", "Queue", "Hash set"],
                    "answer": "Segment tree",
                    "explanation": "Segment trees support both operations in O(log n)."
                },
                {
                    "question": "A topological ordering exists only for:",
                    "options": [
                        "Undirected graphs",
                        "Directed acyclic graphs",
                        "Complete graphs",
                        "Weighted trees"
                    ],
                    "answer": "Directed acyclic graphs",
                    "explanation": "Cycles prevent a valid dependency ordering."
                },
                {
                    "question": "Path compression is used in:",
                    "options": ["Trie", "Disjoint Set Union", "Heap", "AVL tree"],
                    "answer": "Disjoint Set Union",
                    "explanation": "It speeds up future find operations."
                },
                {
                    "question": "The maximum number of nodes at level k in a binary tree is:",
                    "options": ["k", "2k", "2^k", "k²"],
                    "answer": "2^k",
                    "explanation": "Each level can double the number of nodes."
                }
            ]
        },
        "DBMS": {
            "Easy": [
                {
                    "question": "Which command retrieves rows from a table?",
                    "options": ["SELECT", "UPDATE", "DELETE", "DROP"],
                    "answer": "SELECT",
                    "explanation": "SELECT reads data."
                },
                {
                    "question": "A primary key must be:",
                    "options": ["Nullable", "Unique and non-null", "Repeated", "Text only"],
                    "answer": "Unique and non-null",
                    "explanation": "It uniquely identifies each row."
                },
                {
                    "question": "Which clause filters rows?",
                    "options": ["WHERE", "GROUP", "ORDER", "JOIN"],
                    "answer": "WHERE",
                    "explanation": "WHERE applies row conditions."
                },
                {
                    "question": "Which normal form removes partial dependency?",
                    "options": ["1NF", "2NF", "3NF", "BCNF only"],
                    "answer": "2NF",
                    "explanation": "2NF removes dependency on part of a composite key."
                },
                {
                    "question": "COMMIT is used to:",
                    "options": [
                        "Save transaction changes",
                        "Delete a database",
                        "Create an index",
                        "Undo changes"
                    ],
                    "answer": "Save transaction changes",
                    "explanation": "COMMIT permanently records the transaction."
                }
            ],
            "Medium": [
                {
                    "question": "Which JOIN returns only matching rows?",
                    "options": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN"],
                    "answer": "INNER JOIN",
                    "explanation": "INNER JOIN keeps rows with matches on both sides."
                },
                {
                    "question": "Atomicity means:",
                    "options": [
                        "All operations happen or none happen",
                        "Transactions run faster",
                        "Data is always duplicated",
                        "Queries are encrypted"
                    ],
                    "answer": "All operations happen or none happen",
                    "explanation": "Atomicity prevents partial transaction completion."
                },
                {
                    "question": "Which index structure is common in relational databases?",
                    "options": ["B+ tree", "Stack", "Queue", "Linked list"],
                    "answer": "B+ tree",
                    "explanation": "B+ trees support efficient ordered access."
                },
                {
                    "question": "A foreign key maintains:",
                    "options": [
                        "Referential integrity",
                        "File permissions",
                        "Sorting order",
                        "Password security"
                    ],
                    "answer": "Referential integrity",
                    "explanation": "It links values to an existing parent key."
                },
                {
                    "question": "Which command removes all rows but keeps the table?",
                    "options": ["DROP", "TRUNCATE", "ALTER", "RENAME"],
                    "answer": "TRUNCATE",
                    "explanation": "TRUNCATE removes table data while preserving structure."
                }
            ],
            "Hard": [
                {
                    "question": "A dirty read occurs when a transaction reads:",
                    "options": [
                        "Uncommitted data",
                        "Duplicate data",
                        "Encrypted data",
                        "Indexed data"
                    ],
                    "answer": "Uncommitted data",
                    "explanation": "The source transaction may later roll back."
                },
                {
                    "question": "Which isolation level prevents dirty reads but may allow non-repeatable reads?",
                    "options": [
                        "Read Uncommitted",
                        "Read Committed",
                        "Repeatable Read",
                        "Serializable"
                    ],
                    "answer": "Read Committed",
                    "explanation": "Only committed data is visible."
                },
                {
                    "question": "Two-phase locking is used for:",
                    "options": [
                        "Concurrency control",
                        "Data compression",
                        "Schema design",
                        "Backup scheduling"
                    ],
                    "answer": "Concurrency control",
                    "explanation": "It provides conflict serialisability."
                },
                {
                    "question": "BCNF is stricter than 3NF because:",
                    "options": [
                        "Every determinant must be a candidate key",
                        "It allows more redundancy",
                        "It removes all foreign keys",
                        "It forbids composite keys"
                    ],
                    "answer": "Every determinant must be a candidate key",
                    "explanation": "That is the defining BCNF condition."
                },
                {
                    "question": "A clustered index determines:",
                    "options": [
                        "Physical row order",
                        "User permissions",
                        "Transaction size",
                        "Number of columns"
                    ],
                    "answer": "Physical row order",
                    "explanation": "Rows are stored according to the clustered index order."
                }
            ]
        }
    }

    c1, c2, c3 = st.columns(3)

    with c1:
        coding_topic = st.selectbox(
            "Topic",
            list(coding_bank.keys())
        )

    with c2:
        coding_difficulty = st.selectbox(
            "Difficulty",
            ["Easy", "Medium", "Hard"]
        )

    with c3:
        coding_count = st.selectbox(
            "Questions",
            [3, 5],
            index=1
        )

    if st.button("Generate Coding Test", width="stretch"):

        selected = random.sample(
            coding_bank[coding_topic][coding_difficulty],
            k=min(
                coding_count,
                len(coding_bank[coding_topic][coding_difficulty])
            )
        )

        st.session_state.college_coding_questions = selected
        st.session_state.college_coding_result = None
        st.rerun()

    coding_questions = st.session_state.college_coding_questions

    if coding_questions:

        with st.form("college_coding_form"):

            coding_answers = []

            for index, item in enumerate(coding_questions, start=1):

                answer = st.radio(
                    f"{index}. {item['question']}",
                    item["options"],
                    index=None,
                    key=f"college_coding_{index}"
                )

                coding_answers.append(answer)

            coding_submit = st.form_submit_button(
                "Submit Coding Test",
                width="stretch"
            )

        if coding_submit:

            if any(answer is None for answer in coding_answers):

                st.error("Answer every question before submitting.")

            else:

                score = sum(
                    answer == item["answer"]
                    for answer, item in zip(
                        coding_answers,
                        coding_questions
                    )
                )

                percentage = round(
                    score / len(coding_questions) * 100
                )

                st.session_state.college_coding_result = {
                    "score": score,
                    "total": len(coding_questions),
                    "percentage": percentage
                }

                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute(
                    """
                    INSERT INTO coding_results (
                        user_id,
                        topic,
                        difficulty,
                        score,
                        completed_at
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        st.session_state.user_id,
                        coding_topic,
                        coding_difficulty,
                        percentage,
                        datetime.now().isoformat()
                    )
                )

                connection.commit()
                connection.close()

        if st.session_state.college_coding_result:

            result = st.session_state.college_coding_result

            st.success(
                f"Score: {result['score']}/{result['total']} "
                f"({result['percentage']}%)"
            )

            for index, item in enumerate(coding_questions, start=1):
                with st.expander(
                    f"Question {index}: Answer and explanation"
                ):
                    st.write(f"**Correct answer:** {item['answer']}")
                    st.write(item["explanation"])


# ==========================================================
# RESUME BUILDER
# ==========================================================

elif menu == "📄 Resume Builder":

    st.title("📄 Resume Builder")
    st.write(
        "Create a clean placement resume using your academic and technical details."
    )

    with st.form("resume_builder_form"):

        resume_name = st.text_input(
            "Full Name",
            value=st.session_state.user_name
        )

        resume_headline = st.text_input(
            "Professional Headline",
            placeholder="Example: Aspiring Full Stack Developer"
        )

        resume_phone = st.text_input("Phone Number")
        resume_location = st.text_input("Location")
        resume_summary = st.text_area(
            "Professional Summary",
            placeholder=(
                "Write 3–4 lines about your skills, interests and career objective."
            )
        )

        resume_education = st.text_area(
            "Education",
            placeholder=(
                "B.Tech CSE (AI & ML), College Name, CGPA, Graduation Year"
            )
        )

        resume_skills = st.text_area(
            "Skills",
            placeholder="Python, Java, React, SQL, Git, Machine Learning"
        )

        resume_projects = st.text_area(
            "Projects",
            placeholder=(
                "Project name | Technologies | What you built | Result"
            )
        )

        resume_experience = st.text_area(
            "Internships / Experience",
            placeholder="Organisation | Role | Duration | Contributions"
        )

        resume_certifications = st.text_area(
            "Certifications and Achievements"
        )

        resume_links = st.text_area(
            "Profile Links",
            placeholder="LinkedIn, GitHub and portfolio URLs"
        )

        build_resume = st.form_submit_button(
            "Build Resume",
            width="stretch"
        )

    if build_resume:

        resume_text = f"""# {resume_name}
**{resume_headline}**

{resume_phone} | {resume_location}

## Professional Summary
{resume_summary}

## Education
{resume_education}

## Technical Skills
{resume_skills}

## Projects
{resume_projects}

## Internships / Experience
{resume_experience}

## Certifications & Achievements
{resume_certifications}

## Links
{resume_links}
"""

        st.session_state.resume_preview = resume_text

    if st.session_state.resume_preview:

        st.subheader("Resume Preview")
        st.markdown(st.session_state.resume_preview)

        st.subheader("🤖 AI Resume Suggestions")
        resume_lower = st.session_state.resume_preview.lower()
        if not any(x in resume_lower for x in ["%", "improved", "reduced", "increased", "users", "accuracy"]):
            st.write("• Add measurable project outcomes.")
        if "sql" not in resume_lower:
            st.write("• Add SQL when it is relevant to your target role.")
        if "data structures" not in resume_lower:
            st.write("• Add Data Structures and Algorithms for software roles.")
        st.write("• Keep the resume concise and remove unnecessary information.")

        st.download_button(
            "⬇ Download Resume",
            data=st.session_state.resume_preview,
            file_name="TalentSphere_Resume.md",
            mime="text/markdown",
            width="stretch"
        )


# ==========================================================
# AI RESUME REVIEW / ATS CHECKER
# ==========================================================

elif menu == "✅ ATS Resume Checker":

    st.title("✅ AI Resume Review")
    st.write("Paste your resume and target job description to receive ATS scores and AI-style feedback.")

    c1, c2 = st.columns(2)
    with c1:
        resume_text = st.text_area("Resume Text", height=360)
    with c2:
        job_text = st.text_area("Target Job Description", height=360)

    if st.button("Run AI Resume Review", width="stretch"):
        if not resume_text.strip() or not job_text.strip():
            st.error("Provide both resume text and job description.")
        else:
            stop = {"the","and","or","a","an","to","of","in","for","with","on","is","are","be","as","at","by","from"}
            def words(text):
                return {w for w in re.findall(r"[A-Za-z][A-Za-z0-9+#.-]{1,}", text.lower()) if w not in stop and len(w)>2}
            rwords, jwords = words(resume_text), words(job_text)
            matched = sorted(rwords & jwords)
            missing = sorted(jwords-rwords)
            ats_score = round(len(matched)/max(len(jwords),1)*100)
            keyword_score = min(100, round(ats_score*1.1))
            project_score = 45 + (20 if "project" in resume_text.lower() else 0) + (20 if any(x in resume_text.lower() for x in ["%","improved","reduced","increased","users","accuracy"]) else 0) + (15 if "github" in resume_text.lower() else 0)
            project_score=min(project_score,100)
            formatting=50+sum(x in resume_text.lower() for x in ["summary","education","skills","projects","experience"])*10
            formatting=min(formatting,100)
            overall=round(ats_score*.35+keyword_score*.25+project_score*.20+formatting*.20)
            table=pd.DataFrame({"Criteria":["ATS Compatibility","Keyword Optimization","Project Quality","Formatting","Overall Resume Score"],"Score":[f"{ats_score}%",f"{keyword_score}%",f"{project_score}%",f"{formatting}%",f"{overall}%"]})
            st.dataframe(table,width="stretch",hide_index=True)
            st.metric("Overall Resume Score",f"{overall}/100")
            st.progress(overall/100)
            st.subheader("🤖 AI Feedback")
            if missing: st.write("• Add relevant missing keywords: "+", ".join(missing[:8]))
            if project_score<75: st.write("• Add measurable project outcomes and GitHub links.")
            if formatting<80: st.write("• Use clear headings for summary, education, skills, projects and experience.")
            if ats_score>=75: st.write("• Your resume is ATS-friendly for this role.")



# ==========================================================
# INTERVIEW PREPARATION
# ==========================================================

elif menu == "🎤 Interview Preparation":

    st.title("🎤 Interview Preparation")

    interview_category = st.selectbox(
        "Choose Interview Category",
        [
            "HR Interview",
            "Technical Interview",
            "Behavioural Interview",
            "Project Discussion",
            "Company Preparation"
        ]
    )

    preparation_data = {
        "HR Interview": [
            ("Tell me about yourself.", "Use present–past–future structure."),
            ("Why should we hire you?", "Connect skills with the role."),
            ("What are your strengths?", "Give proof using one example."),
            ("What is your weakness?", "Mention improvement actions."),
            ("Where do you see yourself in five years?", "Show realistic growth.")
        ],
        "Technical Interview": [
            ("Explain OOP principles.", "Cover encapsulation, inheritance, polymorphism and abstraction."),
            ("What is time complexity?", "Explain growth of algorithm running time."),
            ("Difference between process and thread?", "Compare memory and execution."),
            ("What is database normalisation?", "Explain redundancy reduction."),
            ("Explain REST API.", "Discuss resources, HTTP methods and statelessness.")
        ],
        "Behavioural Interview": [
            ("Describe a team conflict.", "Use STAR: Situation, Task, Action, Result."),
            ("Tell me about a failure.", "Focus on learning and correction."),
            ("How do you handle pressure?", "Describe planning and prioritisation."),
            ("Give an example of leadership.", "Show initiative and outcome."),
            ("Describe a difficult deadline.", "Explain execution and result.")
        ],
        "Project Discussion": [
            ("Explain your project architecture.", "Start from problem, modules and data flow."),
            ("What was your contribution?", "Be specific about files and features."),
            ("What challenges did you face?", "Mention issue, diagnosis and solution."),
            ("How did you test the project?", "Explain functional and API testing."),
            ("What would you improve?", "Discuss scalability and security.")
        ],
        "Company Preparation": [
            ("Research the company.", "Know products, values and recent work."),
            ("Understand the job description.", "Map requirements to your skills."),
            ("Prepare company-specific questions.", "Ask about team and role."),
            ("Review commonly asked topics.", "Focus on role-relevant subjects."),
            ("Practise timed answers.", "Keep responses clear and structured.")
        ]
    }

    for question, tip in preparation_data[interview_category]:
        with st.expander(question):
            st.write(f"**Preparation tip:** {tip}")

    st.info(
        "Practise answers aloud, keep each answer between 60 and 120 seconds, "
        "and include examples from projects or internships."
    )


# ==========================================================
# MOCK INTERVIEWS
# ==========================================================

elif menu == "🧑‍💼 Mock Interviews":

    st.title("🧑‍💼 Mock Interviews")

    mock_type = st.selectbox(
        "Interview Type",
        ["HR", "Technical", "Behavioural"]
    )

    mock_bank = {
        "HR": [
            "Introduce yourself in 90 seconds.",
            "Why do you want this role?",
            "What is your biggest strength?",
            "Describe one weakness and how you are improving it.",
            "Why should we hire you?"
        ],
        "Technical": [
            "Explain one project end to end.",
            "What is the difference between stack and queue?",
            "Explain SQL JOIN types.",
            "What is REST and why is it stateless?",
            "How would you improve application performance?"
        ],
        "Behavioural": [
            "Tell me about a conflict in a team.",
            "Describe a failure and what you learnt.",
            "Give an example of leadership.",
            "How did you handle a tight deadline?",
            "Describe a time you learnt a new skill quickly."
        ]
    }

    if st.button("Start Mock Interview", width="stretch"):

        st.session_state.mock_interview_questions = random.sample(
            mock_bank[mock_type],
            k=5
        )
        st.session_state.mock_interview_result = None
        st.rerun()

    if st.session_state.mock_interview_questions:

        with st.form("mock_interview_form"):

            answer_scores = []

            for index, question in enumerate(
                st.session_state.mock_interview_questions,
                start=1
            ):

                st.write(f"### Question {index}")
                st.write(question)

                answer = st.text_area(
                    "Your Answer",
                    key=f"mock_answer_{index}"
                )

                answer_scores.append(answer)

            submit_mock = st.form_submit_button(
                "Complete Mock Interview",
                width="stretch"
            )

        if submit_mock:

            score = 0
            feedback = []

            for answer in answer_scores:

                word_count = len(answer.split())

                if word_count >= 60:
                    score += 20
                elif word_count >= 30:
                    score += 14
                elif word_count >= 10:
                    score += 8
                else:
                    score += 2

            if score >= 80:
                feedback_text = "Strong answers with good detail."
            elif score >= 60:
                feedback_text = "Good attempt. Add clearer examples and outcomes."
            else:
                feedback_text = "Answers are brief. Use the STAR method and add evidence."

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO mock_interview_results (
                    user_id,
                    interview_type,
                    score,
                    feedback,
                    completed_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    st.session_state.user_id,
                    mock_type,
                    score,
                    feedback_text,
                    datetime.now().isoformat()
                )
            )

            connection.commit()
            connection.close()

            st.session_state.mock_interview_result = {
                "score": score,
                "feedback": feedback_text
            }

        if st.session_state.mock_interview_result:

            result = st.session_state.mock_interview_result
            st.metric("Mock Interview Score", f"{result['score']}/100")
            st.info(result["feedback"])


# ==========================================================
# SKILL GAP ANALYSIS
# ==========================================================

elif menu == "📊 Skill Gap Analysis":

    st.title("📊 Skill Gap Analysis")

    role_skills = {
        "Software Engineer": {
            "Python", "Java", "C++", "Data Structures & Algorithms",
            "Object-Oriented Programming", "SQL", "Git", "System Design"
        },
        "Full Stack Developer": {
            "HTML", "CSS", "JavaScript", "React", "Node.js",
            "MongoDB", "SQL", "Git", "REST APIs"
        },
        "Data Scientist": {
            "Python", "SQL", "Statistics", "Machine Learning",
            "Pandas", "NumPy", "Data Visualisation", "Git"
        },
        "AI Engineer": {
            "Python", "Machine Learning", "Deep Learning",
            "TensorFlow", "PyTorch", "NLP", "Computer Vision", "Git"
        },
        "Cloud Engineer": {
            "Linux", "Networking", "AWS", "Docker",
            "Kubernetes", "Terraform", "CI/CD", "Monitoring"
        }
    }

    target_role = st.selectbox(
        "Target Role",
        list(role_skills.keys())
    )

    available_skills = sorted(
        set().union(*role_skills.values())
    )

    current_skills = st.multiselect(
        "Select Your Current Skills",
        available_skills
    )

    if st.button("Analyse Skill Gap", width="stretch"):

        required = role_skills[target_role]
        current = set(current_skills)

        matched = sorted(required & current)
        missing = sorted(required - current)

        readiness = round(
            len(matched) / len(required) * 100
        )

        st.metric("Role Readiness", f"{readiness}%")
        st.progress(readiness / 100)

        st.write("### Skills You Already Have")
        st.write(", ".join(matched) or "None selected.")

        st.write("### Skills to Learn Next")
        st.write(", ".join(missing) or "No major skill gap.")

        if missing:
            st.info(
                "Recommended plan: learn one missing skill every 2–4 weeks, "
                "build a small project and add it to GitHub."
            )


# ==========================================================
# PLACEMENT TRACKER
# ==========================================================

elif menu == "🎯 Placement Tracker":

    st.title("🎯 Placement Tracker")

    with st.form("placement_application_form"):

        p1, p2 = st.columns(2)

        with p1:
            company = st.text_input("Company *")
            role = st.text_input("Role *")
            application_date = st.date_input(
                "Application Date",
                value=date.today()
            )

        with p2:
            status = st.selectbox(
                "Status",
                [
                    "Applied",
                    "Online Assessment",
                    "Technical Interview",
                    "HR Interview",
                    "Rejected",
                    "Offer Received"
                ]
            )

            next_round = st.text_input(
                "Next Round / Date",
                placeholder="Example: Technical interview on 20 July"
            )

            notes = st.text_area("Notes")

        add_application = st.form_submit_button(
            "Add Application",
            width="stretch"
        )

    if add_application:

        if not company.strip() or not role.strip():

            st.error("Company and role are required.")

        else:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO placement_applications (
                    user_id,
                    company,
                    role,
                    application_date,
                    status,
                    next_round,
                    notes,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    st.session_state.user_id,
                    company.strip(),
                    role.strip(),
                    application_date.isoformat(),
                    status,
                    next_round.strip(),
                    notes.strip(),
                    datetime.now().isoformat()
                )
            )

            connection.commit()
            connection.close()

            st.success("Application added.")
            st.rerun()

    connection = get_connection()

    applications = pd.read_sql_query(
        """
        SELECT
            id,
            company,
            role,
            application_date,
            status,
            next_round,
            notes
        FROM placement_applications
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        connection,
        params=(st.session_state.user_id,)
    )

    connection.close()

    if applications.empty:

        st.info("No placement applications added yet.")

    else:

        st.dataframe(
            applications.drop(columns=["id"]),
            width="stretch",
            hide_index=True
        )

        delete_id = st.selectbox(
            "Select Application to Delete",
            applications["id"].tolist(),
            format_func=lambda app_id: (
                f"{applications.loc[applications['id'] == app_id, 'company'].iloc[0]}"
                f" – {applications.loc[applications['id'] == app_id, 'role'].iloc[0]}"
            )
        )

        if st.button("Delete Selected Application"):

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM placement_applications
                WHERE id = ? AND user_id = ?
                """,
                (
                    int(delete_id),
                    st.session_state.user_id
                )
            )

            connection.commit()
            connection.close()

            st.success("Application deleted.")
            st.rerun()


# ==========================================================
# INTERNSHIP RECOMMENDATIONS
# ==========================================================

elif menu == "🧭 Internship Recommendations":

    st.title("🧭 AI Internship Recommendations")

    interest_area = st.selectbox(
        "Area of Interest",
        [
            "Web Development",
            "Data Science",
            "Machine Learning",
            "Cloud Computing",
            "Cybersecurity",
            "Mobile Development"
        ]
    )

    skill_level = st.selectbox(
        "Current Skill Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    recommendations = {
        "Web Development": [
            "Frontend Intern",
            "MERN Stack Intern",
            "Backend API Intern"
        ],
        "Data Science": [
            "Data Analyst Intern",
            "Business Intelligence Intern",
            "Junior Data Science Intern"
        ],
        "Machine Learning": [
            "ML Research Intern",
            "Computer Vision Intern",
            "NLP Intern"
        ],
        "Cloud Computing": [
            "Cloud Support Intern",
            "DevOps Intern",
            "Infrastructure Intern"
        ],
        "Cybersecurity": [
            "SOC Analyst Intern",
            "Security Testing Intern",
            "Network Security Intern"
        ],
        "Mobile Development": [
            "Android Intern",
            "Flutter Intern",
            "iOS Intern"
        ]
    }

    if st.button("Show Recommendations", width="stretch"):

        st.success(
            f"Recommended {skill_level.lower()} opportunities"
        )

        for item in recommendations[interest_area]:

            with st.container(border=True):
                st.subheader(item)
                st.write(
                    f"Build one {interest_area} project, update your resume "
                    "and prepare role-specific interview questions."
                )


# ==========================================================
# JOB MATCHING ENGINE
# ==========================================================

elif menu == "🧠 Job Matching Engine":

    st.title("🧠 AI Job Matching Engine")
    st.write("Match skills, CGPA, projects, resume quality, coding score and location preference with suitable roles.")

    target_location = st.text_input("Preferred Location", placeholder="Bengaluru, Hyderabad or Remote")
    selected_skills = st.multiselect("Current Skills", ["Python","Java","C++","SQL","Data Structures & Algorithms","Git","React","Node.js","MongoDB","Pandas","Power BI","Machine Learning","Testing","REST APIs"])
    cgpa = st.number_input("CGPA",0.0,10.0,7.0,0.1)
    project_count = st.number_input("Strong Projects",0,20,2)
    resume_score = st.slider("Resume Score",0,100,70)
    coding_score = st.slider("Coding Score",0,100,60)

    if st.button("Generate Job Matches",width="stretch"):
        roles={
            "Software Developer":{"Python","Java","C++","SQL","Data Structures & Algorithms","Git"},
            "Backend Developer":{"Python","Java","Node.js","SQL","MongoDB","REST APIs"},
            "Data Analyst":{"Python","SQL","Pandas","Power BI"},
            "QA Engineer":{"Java","Python","SQL","Testing","Git"}
        }
        rows=[]
        current=set(selected_skills)
        for role,required in roles.items():
            skill=len(current & required)/len(required)*45
            score=round(skill+cgpa/10*15+min(project_count*5,15)+resume_score*.15+coding_score*.10+(5 if target_location.strip() else 0))
            rows.append({"Job Role":role,"Match %":min(score,100)})
        rows=sorted(rows,key=lambda x:x["Match %"],reverse=True)
        st.dataframe(pd.DataFrame(rows),width="stretch",hide_index=True)
        st.success(f"Top Recommendation: **{rows[0]['Job Role']}** ({rows[0]['Match %']}% Match)")
        st.write("**Suggested Companies:** Infosys, TCS, Wipro and Zoho")

# ==========================================================
# HACKATHON UPDATES
# ==========================================================

elif menu == "🏆 Hackathon Updates":

    st.title("🏆 Hackathon Updates")
    st.warning(
        "Demo opportunity board. Verify event dates on the official organiser website."
    )

    hackathons = pd.DataFrame({
        "Hackathon": [
            "AI Innovation Challenge",
            "Smart India Hackathon Practice",
            "Web3 Campus Challenge",
            "Green Technology Hackathon",
            "Open Source Sprint"
        ],
        "Theme": [
            "Artificial Intelligence",
            "National Problem Statements",
            "Blockchain",
            "Sustainability",
            "Open Source"
        ],
        "Team Size": ["2–4", "4–6", "2–5", "2–4", "Individual/Team"],
        "Preparation": [
            "ML prototype and pitch",
            "Problem research and full-stack prototype",
            "Smart contract demo",
            "Impact-focused solution",
            "GitHub contribution"
        ]
    })

    st.dataframe(
        hackathons,
        width="stretch",
        hide_index=True
    )

    st.info(
        "Use this module as a planning board. Live event search can be added "
        "later using official hackathon APIs or verified web sources."
    )


# ==========================================================
# GITHUB PORTFOLIO REVIEW
# ==========================================================

elif menu == "🐙 GitHub Portfolio Review":

    st.title("🐙 Automatic GitHub Portfolio Review")
    st.write(
        "Enter only your GitHub username or profile URL. "
        "TalentSphere automatically checks your public repositories, "
        "README files, languages, project activity and portfolio quality."
    )

    st.info(
        "Example: thimmegowd or https://github.com/thimmegowd"
    )

    github_input = st.text_input(
        "GitHub Username or Profile URL",
        placeholder="Enter username or GitHub profile URL",
        key="github_auto_review_username"
    )

    if st.button(
        "🔍 Analyse GitHub Portfolio",
        width="stretch"
    ):
        username = normalise_github_username(github_input)

        if not username:
            st.error("Enter your GitHub username or profile URL.")

        elif not re.fullmatch(
            r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?",
            username
        ):
            st.error("Enter a valid GitHub username.")

        else:
            with st.spinner(
                "Connecting to GitHub and analysing your portfolio..."
            ):
                review, error = analyse_github_portfolio(username)

            if error:
                st.error(error)
                st.caption(
                    "Only public GitHub information can be analysed."
                )

            else:
                profile = review["profile"]
                score = review["score"]

                profile_column, score_column = st.columns(
                    [1, 3],
                    gap="large"
                )

                with profile_column:
                    st.image(
                        profile.get("avatar_url"),
                        width=150
                    )
                    st.subheader(
                        profile.get("name")
                        or profile.get("login")
                    )

                    if profile.get("bio"):
                        st.write(profile.get("bio"))

                    if profile.get("location"):
                        st.caption(
                            f"📍 {profile.get('location')}"
                        )

                    st.markdown(
                        f"[Open GitHub Profile]"
                        f"({profile.get('html_url')})"
                    )

                with score_column:
                    m1, m2, m3, m4 = st.columns(4)

                    with m1:
                        st.metric(
                            "Portfolio Score",
                            f"{score}/100"
                        )

                    with m2:
                        st.metric(
                            "Repositories",
                            review["repository_count"]
                        )

                    with m3:
                        st.metric(
                            "Followers",
                            profile.get("followers", 0)
                        )

                    with m4:
                        st.metric(
                            "Recent Projects",
                            review["recent_projects"]
                        )

                    st.progress(score / 100)

                    if score >= 85:
                        st.success(
                            f"Recruiter Readiness: {review['readiness']}"
                        )
                    elif score >= 70:
                        st.info(
                            f"Recruiter Readiness: {review['readiness']}"
                        )
                    elif score >= 50:
                        st.warning(
                            f"Recruiter Readiness: {review['readiness']}"
                        )
                    else:
                        st.error(
                            f"Recruiter Readiness: {review['readiness']}"
                        )

                    st.write(review["summary"])

                st.divider()

                stat1, stat2, stat3, stat4 = st.columns(4)

                with stat1:
                    st.metric(
                        "README Files",
                        f"{review['readmes']}/{review['analysed_count']}"
                    )

                with stat2:
                    st.metric(
                        "Detailed READMEs",
                        review["detailed_readmes"]
                    )

                with stat3:
                    st.metric(
                        "Total Stars",
                        review["stars"]
                    )

                with stat4:
                    st.metric(
                        "Live Demo Links",
                        review["live_links"]
                    )

                strengths_col, suggestions_col = st.columns(
                    2,
                    gap="large"
                )

                with strengths_col:
                    st.subheader("✅ Portfolio Strengths")

                    if review["strengths"]:
                        for strength in review["strengths"]:
                            st.write(f"• {strength}")
                    else:
                        st.write(
                            "No strong portfolio signals were found yet."
                        )

                with suggestions_col:
                    st.subheader("🚀 Improvement Suggestions")

                    for suggestion in review["suggestions"]:
                        st.write(f"• {suggestion}")

                st.subheader("💻 Technologies Detected")

                if review["languages"]:
                    language_data = pd.DataFrame(
                        review["languages"],
                        columns=["Language", "Repositories"]
                    )

                    language_chart = px.bar(
                        language_data,
                        x="Language",
                        y="Repositories",
                        text="Repositories",
                        title="Languages Across Analysed Repositories"
                    )

                    language_chart.update_layout(
                        height=380,
                        plot_bgcolor="#FFFFFF",
                        paper_bgcolor="#FFFFFF",
                        font=dict(color="#111827")
                    )

                    st.plotly_chart(
                        language_chart,
                        width="stretch"
                    )
                else:
                    st.warning(
                        "No programming languages were detected."
                    )

                st.subheader("📂 Repository Analysis")

                if review["repositories"]:
                    repository_data = pd.DataFrame(
                        review["repositories"]
                    )

                    st.dataframe(
                        repository_data[
                            [
                                "Repository",
                                "Language",
                                "README",
                                "Description",
                                "Live Demo",
                                "Stars",
                                "Updated"
                            ]
                        ],
                        width="stretch",
                        hide_index=True
                    )

                    selected_repository = st.selectbox(
                        "Open a repository",
                        [
                            row["Repository"]
                            for row in review["repositories"]
                        ]
                    )

                    selected_data = next(
                        (
                            row
                            for row in review["repositories"]
                            if row["Repository"] == selected_repository
                        ),
                        None
                    )

                    if selected_data:
                        st.markdown(
                            f"[Open {selected_repository}]"
                            f"({selected_data['URL']})"
                        )
                else:
                    st.warning(
                        "No original public repositories were found."
                    )

                if review["strongest"]:
                    st.subheader("🏆 Strongest Repository")
                    st.write(
                        f"**{review['strongest'].get('name')}**"
                    )
                    st.write(
                        review["strongest"].get("description")
                        or "No description is available."
                    )
                    st.markdown(
                        f"[Open strongest repository]"
                        f"({review['strongest'].get('html_url')})"
                    )

                report = [
                    "TalentSphere Automatic GitHub Portfolio Review",
                    "=" * 47,
                    f"Username: {profile.get('login')}",
                    f"Profile: {profile.get('html_url')}",
                    f"Portfolio Score: {score}/100",
                    f"Recruiter Readiness: {review['readiness']}",
                    f"Repositories: {review['repository_count']}",
                    f"README Files: {review['readmes']}",
                    f"Detailed README Files: "
                    f"{review['detailed_readmes']}",
                    f"Recent Projects: {review['recent_projects']}",
                    f"Total Stars: {review['stars']}",
                    "",
                    "Overall Review",
                    review["summary"],
                    "",
                    "Strengths"
                ]

                report.extend(
                    f"- {item}"
                    for item in (
                        review["strengths"]
                        or ["No strong signals identified."]
                    )
                )

                report.extend([
                    "",
                    "Recommended Improvements"
                ])

                report.extend(
                    f"- {item}"
                    for item in review["suggestions"]
                )

                if review["languages"]:
                    report.extend([
                        "",
                        "Technologies Detected"
                    ])
                    report.extend(
                        f"- {language}: {count} repositories"
                        for language, count in review["languages"]
                    )

                st.download_button(
                    "📥 Download GitHub Portfolio Review",
                    data="\n".join(report),
                    file_name=(
                        f"{profile.get('login')}_github_review.txt"
                    ),
                    mime="text/plain",
                    width="stretch"
                )


# ==========================================================
# LINKEDIN PDF REVIEW
# ==========================================================

elif menu == "📄 LinkedIn PDF Review":

    st.title("📄 Automatic LinkedIn PDF Review")
    st.write(
        "Upload the PDF version of your LinkedIn profile. "
        "TalentSphere will extract the text and automatically evaluate "
        "its important career sections."
    )

    st.info(
        "To create the PDF: open your LinkedIn profile, press Ctrl + P, "
        "select Save as PDF, save all pages, and upload the file below."
    )

    linkedin_pdf_review = st.file_uploader(
        "Upload LinkedIn Profile PDF",
        type=["pdf"],
        key="linkedin_pdf_review_upload",
        help="Only PDF files exported from LinkedIn are supported."
    )

    if linkedin_pdf_review is not None:

        pdf_bytes = linkedin_pdf_review.getvalue()
        file_size_mb = len(pdf_bytes) / (1024 * 1024)

        file_col1, file_col2 = st.columns(2)

        with file_col1:
            st.metric("File", linkedin_pdf_review.name)

        with file_col2:
            st.metric("Size", f"{file_size_mb:.2f} MB")

        if file_size_mb > 10:
            st.error("The PDF is larger than 10 MB. Upload a smaller file.")
        else:
            with st.spinner("Reading and evaluating your LinkedIn PDF..."):
                review, review_error = analyze_linkedin_pdf(pdf_bytes)

            if review_error:
                st.error(review_error)
            else:
                score = review["score"]

                score_col, pages_col, words_col = st.columns(3)

                with score_col:
                    st.metric("LinkedIn Profile Score", f"{score}/100")

                with pages_col:
                    st.metric("PDF Pages", review["page_count"])

                with words_col:
                    st.metric("Extracted Words", review["word_count"])

                st.progress(score / 100)

                if score >= 85:
                    st.success(
                        "Excellent profile. It is detailed and placement-ready."
                    )
                elif score >= 70:
                    st.success(
                        "Good profile. A few improvements can make it stronger."
                    )
                elif score >= 50:
                    st.warning(
                        "Your profile has useful content, but important sections "
                        "need improvement."
                    )
                else:
                    st.error(
                        "Your profile is incomplete or the PDF did not contain "
                        "enough readable text."
                    )

                st.subheader("📊 Section Evaluation")

                evaluation_table = pd.DataFrame(review["checks"])
                st.dataframe(
                    evaluation_table,
                    width="stretch",
                    hide_index=True
                )

                left_review, right_review = st.columns(2)

                with left_review:
                    st.subheader("✅ Strengths")

                    if review["strengths"]:
                        for strength in review["strengths"]:
                            st.write(f"• {strength}")
                    else:
                        st.write(
                            "No strong section could be confidently identified."
                        )

                with right_review:
                    st.subheader("🚀 Recommended Improvements")

                    if review["improvements"]:
                        for improvement in review["improvements"]:
                            st.write(f"• {improvement}")
                    else:
                        st.success(
                            "All major text-based profile sections were found."
                        )

                st.subheader("📝 Overall Review")

                if score >= 85:
                    overall_review = (
                        "Your LinkedIn profile presents a strong professional "
                        "identity. Keep the headline role-focused, update your "
                        "projects regularly and continue adding measurable outcomes."
                    )
                elif score >= 70:
                    overall_review = (
                        "Your LinkedIn profile has a solid foundation. Strengthen "
                        "the missing sections, use measurable achievements and make "
                        "your target role more visible."
                    )
                elif score >= 50:
                    overall_review = (
                        "Your profile includes some useful information, but it needs "
                        "more complete project, skill, experience and summary details "
                        "before placement use."
                    )
                else:
                    overall_review = (
                        "Your profile needs significant improvement, or the uploaded "
                        "PDF may not be a complete LinkedIn export. Add the missing "
                        "sections and upload a fresh complete PDF."
                    )

                st.write(overall_review)

                with st.expander("View extracted PDF text"):
                    st.text_area(
                        "Extracted content",
                        value=review["text"],
                        height=300,
                        disabled=True
                    )

                report_lines = [
                    "TalentSphere LinkedIn PDF Review",
                    "=" * 38,
                    f"File: {linkedin_pdf_review.name}",
                    f"Score: {score}/100",
                    f"Pages: {review['page_count']}",
                    f"Extracted words: {review['word_count']}",
                    "",
                    "Section Evaluation"
                ]

                for item in review["checks"]:
                    report_lines.append(
                        f"- {item['Section']}: {item['Status']} "
                        f"({item['Points']}/{item['Maximum']})"
                    )

                report_lines.extend([
                    "",
                    "Recommended Improvements"
                ])

                if review["improvements"]:
                    report_lines.extend(
                        f"- {item}"
                        for item in review["improvements"]
                    )
                else:
                    report_lines.append(
                        "- All major text-based profile sections were found."
                    )

                report_lines.extend([
                    "",
                    "Overall Review",
                    overall_review
                ])

                review_report = "\n".join(report_lines)

                st.download_button(
                    "📥 Download LinkedIn Review Report",
                    data=review_report,
                    file_name="linkedin_profile_review.txt",
                    mime="text/plain",
                    width="stretch"
                )

# ==========================================================
# DAILY CODING CHALLENGE
# ==========================================================

elif menu == "🔥 Daily Coding Challenge":

    st.title("🔥 Daily Coding Challenge")

    challenges = [
        {
            "title": "Two Sum",
            "difficulty": "Easy",
            "problem": (
                "Given an integer array and a target, return the indices of "
                "two numbers whose sum equals the target."
            ),
            "hint": "Use a hash map to store previously seen values.",
            "complexity": "O(n) time and O(n) space"
        },
        {
            "title": "Longest Substring Without Repeating Characters",
            "difficulty": "Medium",
            "problem": (
                "Find the length of the longest substring without repeating characters."
            ),
            "hint": "Use a sliding window and a set or dictionary.",
            "complexity": "O(n) time"
        },
        {
            "title": "Merge Intervals",
            "difficulty": "Medium",
            "problem": (
                "Merge all overlapping intervals from a list of intervals."
            ),
            "hint": "Sort intervals by start time before scanning.",
            "complexity": "O(n log n) time"
        },
        {
            "title": "Detect Cycle in Linked List",
            "difficulty": "Medium",
            "problem": (
                "Determine whether a singly linked list contains a cycle."
            ),
            "hint": "Use slow and fast pointers.",
            "complexity": "O(n) time and O(1) space"
        },
        {
            "title": "Maximum Subarray",
            "difficulty": "Medium",
            "problem": (
                "Find the contiguous subarray with the largest sum."
            ),
            "hint": "Use Kadane's algorithm.",
            "complexity": "O(n) time"
        }
    ]

    if (
        st.session_state.daily_coding_challenge is None
        or st.button("Generate New Challenge")
    ):
        st.session_state.daily_coding_challenge = random.choice(challenges)

    challenge = st.session_state.daily_coding_challenge

    with st.container(border=True):

        st.subheader(challenge["title"])
        st.write(f"**Difficulty:** {challenge['difficulty']}")
        st.write(challenge["problem"])

        with st.expander("Show Hint"):
            st.write(challenge["hint"])

        with st.expander("Expected Complexity"):
            st.write(challenge["complexity"])

    solution = st.text_area(
        "Write your approach or code",
        height=300
    )

    if st.button("Submit Daily Challenge", width="stretch"):

        if len(solution.strip()) < 40:
            st.warning(
                "Add a clearer explanation or more complete code."
            )
        else:
            st.success(
                "Challenge submitted. Review complexity and test edge cases."
            )




# ==========================================================
# SCHOOL STUDENT HOME — PROFESSIONAL UI
# ==========================================================

elif menu == "🏠 Student Home":

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            school_name,
            current_class,
            board,
            city,
            favourite_subjects,
            interests,
            skills,
            dream_career,
            academic_goal,
            achievements
        FROM school_profiles
        WHERE user_id = ?
        """,
        (st.session_state.user_id,)
    )

    school_profile = cursor.fetchone()

    cursor.execute(
        "SELECT COUNT(*) FROM student_goals WHERE user_id = ?",
        (st.session_state.user_id,)
    )
    goal_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM quiz_results WHERE user_id = ?",
        (st.session_state.user_id,)
    )
    quiz_count = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT AVG(score)
        FROM quiz_results
        WHERE user_id = ? AND score IS NOT NULL
        """,
        (st.session_state.user_id,)
    )
    average_quiz_score = round(cursor.fetchone()[0] or 0)

    cursor.execute(
        """
        SELECT title, target_date, priority, progress
        FROM student_goals
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 4
        """,
        (st.session_state.user_id,)
    )
    recent_goals = cursor.fetchall()

    connection.close()

    def school_dashboard_list(value):
        try:
            return json.loads(value) if value else []
        except (json.JSONDecodeError, TypeError):
            return []

    if school_profile:
        school_name = school_profile[0] or "School not added"
        current_class = school_profile[1] or "Class not added"
        board = school_profile[2] or "Board not added"
        city = school_profile[3] or "City not added"
        favourite_subjects = school_dashboard_list(school_profile[4])
        interests = school_dashboard_list(school_profile[5])
        skills = school_dashboard_list(school_profile[6])
        dream_career = school_profile[7] or "Explore career options"
        academic_goal = school_profile[8] or "Set your academic goal"
        achievements = school_profile[9] or ""
        profile_exists = True
    else:
        school_name = "Complete your school profile"
        current_class = "Class not added"
        board = "Board not added"
        city = "City not added"
        favourite_subjects = []
        interests = []
        skills = []
        dream_career = "Explore career options"
        academic_goal = "Set your academic goal"
        achievements = ""
        profile_exists = False

    profile_fields = [
        school_name if profile_exists else "",
        current_class if profile_exists else "",
        board if profile_exists else "",
        city if profile_exists else "",
        favourite_subjects,
        interests,
        skills,
        dream_career if profile_exists else "",
        academic_goal if profile_exists else "",
        achievements
    ]

    completed_profile_fields = sum(bool(value) for value in profile_fields)
    profile_completion = round(
        completed_profile_fields / len(profile_fields) * 100
    )

    completed_tasks = sum(
        task["completed"]
        for task in st.session_state.daily_tasks
    )
    total_tasks = len(st.session_state.daily_tasks)
    task_completion = round(
        completed_tasks / total_tasks * 100
    ) if total_tasks else 0

    goal_progress = round(
        sum(int(goal[3] or 0) for goal in recent_goals) / len(recent_goals)
    ) if recent_goals else 0

    learning_score = round(
        profile_completion * 0.30
        + min(quiz_count * 12, 100) * 0.20
        + average_quiz_score * 0.20
        + task_completion * 0.20
        + min(goal_count * 20, 100) * 0.10
    )

    if learning_score >= 80:
        readiness_label = "Excellent Progress"
    elif learning_score >= 60:
        readiness_label = "Good Progress"
    elif learning_score >= 40:
        readiness_label = "Developing"
    else:
        readiness_label = "Getting Started"

    st.markdown(
        f"""<div class="studio-hero">
<span class="studio-badge">TalentSphere School Dashboard</span>
<h1>Your complete learning and career discovery dashboard.</h1>
<p>
Welcome, {st.session_state.user_name}. Your dashboard brings together
academic profile, quizzes, daily learning tasks, personal goals, skills
and career exploration in one professional workspace.
</p>
</div>""",
        unsafe_allow_html=True
    )

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.markdown(
            f"""<div class="studio-kpi">
<div class="studio-kpi-icon">🎯</div>
<div class="studio-kpi-label">Learning Readiness</div>
<p class="studio-kpi-value">{learning_score}/100</p>
<div class="studio-kpi-sub">{readiness_label}</div>
</div>""",
            unsafe_allow_html=True
        )

    with kpi2:
        st.markdown(
            f"""<div class="studio-kpi">
<div class="studio-kpi-icon">👤</div>
<div class="studio-kpi-label">Profile Strength</div>
<p class="studio-kpi-value">{profile_completion}%</p>
<div class="studio-kpi-sub">Academic and career profile</div>
</div>""",
            unsafe_allow_html=True
        )

    with kpi3:
        st.markdown(
            f"""<div class="studio-kpi">
<div class="studio-kpi-icon">📝</div>
<div class="studio-kpi-label">Quiz Performance</div>
<p class="studio-kpi-value">{average_quiz_score}%</p>
<div class="studio-kpi-sub">{quiz_count} quiz attempt(s) completed</div>
</div>""",
            unsafe_allow_html=True
        )

    with kpi4:
        st.markdown(
            f"""<div class="studio-kpi">
<div class="studio-kpi-icon">✅</div>
<div class="studio-kpi-label">Daily Tasks</div>
<p class="studio-kpi-value">{completed_tasks}/{total_tasks}</p>
<div class="studio-kpi-sub">Today's learning checklist</div>
</div>""",
            unsafe_allow_html=True
        )

    st.write("")

    st.markdown(
        """
        <div style="
            display:flex;
            align-items:center;
            gap:12px;
            background:#FFFFFF;
            border:1px solid #DCE6F3;
            border-left:6px solid #2563EB;
            border-radius:16px;
            padding:17px 20px;
            margin:14px 0 20px 0;
            box-shadow:0 7px 22px rgba(15,23,42,0.07);
        ">
            <div style="
                width:42px;
                height:42px;
                border-radius:12px;
                background:#EFF6FF;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:22px;
            ">🧠</div>
            <div>
                <div style="
                    color:#0F172A !important;
                    font-size:25px;
                    line-height:1.15;
                    font-weight:800;
                    letter-spacing:-0.02em;
                ">Learning Intelligence</div>
                <div style="
                    color:#64748B !important;
                    font-size:13px;
                    margin-top:4px;
                ">
                    Personalised analysis of your academic progress and career direction
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    intelligence_left, intelligence_right = st.columns([1.45, 1])

    with intelligence_left:
        st.markdown(
            """<div class="studio-panel">
<h3>📊 Readiness Breakdown</h3>
<p style="color:#64748B !important;font-size:13px;">
Your score combines profile completion, quiz performance, daily tasks
and goal activity.
</p>
</div>""",
            unsafe_allow_html=True
        )

        breakdown_df = pd.DataFrame({
            "Area": [
                "Profile",
                "Quiz Activity",
                "Quiz Score",
                "Daily Tasks",
                "Goals"
            ],
            "Score": [
                profile_completion,
                min(quiz_count * 12, 100),
                average_quiz_score,
                task_completion,
                min(goal_count * 20, 100)
            ]
        })

        breakdown_chart = px.bar(
            breakdown_df,
            x="Score",
            y="Area",
            orientation="h",
            text="Score",
            range_x=[0, 100]
        )
        breakdown_chart.update_traces(texttemplate="%{text}%", textposition="outside")
        breakdown_chart.update_layout(
            height=310,
            margin=dict(l=10, r=25, t=20, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#0F172A"),
            xaxis_title="",
            yaxis_title="",
            showlegend=False
        )
        st.plotly_chart(breakdown_chart, width="stretch")

    with intelligence_right:
        st.markdown(
            f"""<div class="studio-panel">
<h3>🎓 Student Snapshot</h3>
<div class="studio-role-card">
<div class="studio-role-title">{current_class}</div>
<div class="studio-match">{school_name}</div>
<p style="color:#64748B !important;margin:10px 0 0;">
{board} · {city}
</p>
</div>
<p style="color:#64748B !important;font-size:13px;margin-bottom:6px;">
<strong style="color:#0F172A;">Dream career:</strong> {dream_career}
</p>
<p style="color:#64748B !important;font-size:13px;">
<strong style="color:#0F172A;">Academic goal:</strong> {academic_goal}
</p>
</div>""",
            unsafe_allow_html=True
        )

        if favourite_subjects or skills:
            chips = favourite_subjects[:3] + skills[:3]
            chip_html = "".join(
                f'<span class="studio-chip">{item}</span>'
                for item in chips
            )
            st.markdown(chip_html, unsafe_allow_html=True)
        else:
            st.info("Complete your profile to display subjects and skills.")

    st.write("")
    st.markdown(
        '<div class="studio-section-title">🚀 Your Learning Areas</div>',
        unsafe_allow_html=True
    )

    area1, area2, area3 = st.columns(3)

    with area1:
        st.markdown(
            """<div class="studio-module-card">
<div style="font-size:28px;">🔍</div>
<h4>Career Discovery</h4>
<p>Explore suitable careers based on your favourite subjects, interests and strengths.</p>
<span class="studio-status-good">Personalised</span>
</div>""",
            unsafe_allow_html=True
        )

    with area2:
        st.markdown(
            """<div class="studio-module-card">
<div style="font-size:28px;">📚</div>
<h4>Skill Development</h4>
<p>Improve academic knowledge, aptitude, communication and beginner technical skills.</p>
<span class="studio-status-progress">In Progress</span>
</div>""",
            unsafe_allow_html=True
        )

    with area3:
        st.markdown(
            """<div class="studio-module-card">
<div style="font-size:28px;">🎯</div>
<h4>Goal Planning</h4>
<p>Create academic and career goals, define target dates and monitor your progress.</p>
<span class="studio-status-progress">Track Goals</span>
</div>""",
            unsafe_allow_html=True
        )

    st.write("")
    focus_left, focus_right = st.columns([1.15, 1])

    with focus_left:
        st.markdown(
            '<div class="studio-section-title">📌 Recommended Next Actions</div>',
            unsafe_allow_html=True
        )

        recommended_actions = []

        if profile_completion < 80:
            recommended_actions.append(
                ("Complete your student profile", "Add subjects, interests, skills and your dream career.")
            )
        if quiz_count < 3:
            recommended_actions.append(
                ("Complete a career or subject quiz", "Quiz results help TalentSphere personalise recommendations.")
            )
        if completed_tasks < total_tasks:
            recommended_actions.append(
                ("Finish today's learning tasks", "Complete the remaining items in your daily checklist.")
            )
        if goal_count == 0:
            recommended_actions.append(
                ("Create your first goal", "Set one academic target with a realistic target date.")
            )
        if not recommended_actions:
            recommended_actions.append(
                ("Continue your learning streak", "Review your progress and set a stronger weekly target.")
            )

        for title, description in recommended_actions[:4]:
            st.markdown(
                f"""<div class="studio-action">
<strong>{title}</strong><br>
<span>{description}</span>
</div>""",
                unsafe_allow_html=True
            )

    with focus_right:
        st.markdown(
            '<div class="studio-section-title">🎯 Goal Progress</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""<div class="studio-panel">
<h3>Current Goal Activity</h3>
<div class="studio-role-card">
<div class="studio-role-title">{goal_progress}%</div>
<div class="studio-match">Average progress</div>
<p style="color:#64748B !important;margin:10px 0 0;">
{goal_count} goal(s) created in your workspace.
</p>
</div>
</div>""",
            unsafe_allow_html=True
        )

        if recent_goals:
            for goal_title, target_date, priority, progress in recent_goals:
                st.progress(int(progress or 0) / 100)
                st.caption(
                    f"{goal_title} · {int(progress or 0)}% · "
                    f"{priority or 'Normal priority'}"
                )
        else:
            st.info("No goals created yet. Open Goal Setting to add one.")


# ==========================================================
# SCHOOL STUDENT PROFILE
# ==========================================================

elif menu == "👤 My Profile":

    st.markdown(
        """<div class="college-profile-header">
<h1>👤 School Student Profile</h1>
<p>
Create a complete academic and career-interest profile to receive
personalised subject, skills, study-plan and career recommendations.
</p>
</div>""",
        unsafe_allow_html=True
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            school_name,
            current_class,
            board,
            city,
            parent_name,
            phone,
            favourite_subjects,
            interests,
            skills,
            dream_career,
            academic_goal,
            achievements
        FROM school_profiles
        WHERE user_id = ?
    """, (st.session_state.user_id,))

    profile = cursor.fetchone()
    connection.close()

    def safe_school_json_list(value):
        try:
            return json.loads(value) if value else []
        except (json.JSONDecodeError, TypeError):
            return []

    if profile:

        saved_profile = {
            "school_name": profile[0] or "",
            "current_class": profile[1] or "10th Class",
            "board": profile[2] or "State Board",
            "city": profile[3] or "",
            "parent_name": profile[4] or "",
            "phone": profile[5] or "",
            "favourite_subjects": safe_school_json_list(profile[6]),
            "interests": safe_school_json_list(profile[7]),
            "skills": safe_school_json_list(profile[8]),
            "dream_career": profile[9] or "",
            "academic_goal": profile[10] or "",
            "achievements": profile[11] or ""
        }

    else:

        saved_profile = {
            "school_name": "",
            "current_class": "10th Class",
            "board": "State Board",
            "city": "",
            "parent_name": "",
            "phone": "",
            "favourite_subjects": [],
            "interests": [],
            "skills": [],
            "dream_career": "",
            "academic_goal": "",
            "achievements": ""
        }

    with st.form("school_profile_form"):

        st.subheader("🏫 Academic Information")

        academic_col1, academic_col2 = st.columns(2)

        with academic_col1:

            st.text_input(
                "Full Name",
                value=st.session_state.user_name,
                disabled=True
            )

            st.text_input(
                "Email Address",
                value=st.session_state.user_email,
                disabled=True
            )

            school_name = st.text_input(
                "School Name *",
                value=saved_profile["school_name"],
                placeholder="Enter your school name"
            )

            city = st.text_input(
                "City",
                value=saved_profile["city"],
                placeholder="Enter your city"
            )

        with academic_col2:

            class_options = [
                "6th Class",
                "7th Class",
                "8th Class",
                "9th Class",
                "10th Class",
                "11th Class",
                "12th Class"
            ]

            saved_class = saved_profile["current_class"]

            class_index = (
                class_options.index(saved_class)
                if saved_class in class_options
                else 4
            )

            current_class = st.selectbox(
                "Current Class *",
                class_options,
                index=class_index
            )

            board_options = [
                "State Board",
                "CBSE",
                "ICSE",
                "IB",
                "Other"
            ]

            saved_board = saved_profile["board"]

            board_index = (
                board_options.index(saved_board)
                if saved_board in board_options
                else 0
            )

            board = st.selectbox(
                "Education Board",
                board_options,
                index=board_index
            )

            parent_name = st.text_input(
                "Parent or Guardian Name",
                value=saved_profile["parent_name"],
                placeholder="Enter parent or guardian name"
            )

            phone = st.text_input(
                "Phone Number",
                value=saved_profile["phone"],
                placeholder="Enter contact number"
            )

        st.subheader("📚 Subjects, Interests and Skills")

        learning_col1, learning_col2 = st.columns(2)

        with learning_col1:

            favourite_subjects = st.multiselect(
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
                default=saved_profile["favourite_subjects"]
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
                default=saved_profile["interests"]
            )

        with learning_col2:

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
                default=saved_profile["skills"]
            )

            dream_career = st.text_input(
                "Dream Career",
                value=saved_profile["dream_career"],
                placeholder="Example: Doctor or Software Engineer"
            )

        st.subheader("🎯 Goals and Achievements")

        goal_col1, goal_col2 = st.columns(2)

        with goal_col1:

            academic_goal = st.text_area(
                "Academic Goal",
                value=saved_profile["academic_goal"],
                placeholder="Example: Score above 90% in Mathematics",
                height=140
            )

        with goal_col2:

            achievements = st.text_area(
                "Achievements",
                value=saved_profile["achievements"],
                placeholder="Mention awards, certificates or competitions",
                height=140
            )

        save_profile = st.form_submit_button(
            "💾 Save School Profile",
            width="stretch"
        )

    if save_profile:

        if not school_name.strip():

            st.error("School name is required.")

        elif not favourite_subjects:

            st.error(
                "Select at least one favourite subject."
            )

        else:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO school_profiles (
                    user_id,
                    school_name,
                    current_class,
                    board,
                    city,
                    parent_name,
                    phone,
                    favourite_subjects,
                    interests,
                    skills,
                    dream_career,
                    academic_goal,
                    achievements,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id)
                DO UPDATE SET
                    school_name = excluded.school_name,
                    current_class = excluded.current_class,
                    board = excluded.board,
                    city = excluded.city,
                    parent_name = excluded.parent_name,
                    phone = excluded.phone,
                    favourite_subjects = excluded.favourite_subjects,
                    interests = excluded.interests,
                    skills = excluded.skills,
                    dream_career = excluded.dream_career,
                    academic_goal = excluded.academic_goal,
                    achievements = excluded.achievements,
                    updated_at = excluded.updated_at
            """, (
                st.session_state.user_id,
                school_name.strip(),
                current_class,
                board,
                city.strip(),
                parent_name.strip(),
                phone.strip(),
                json.dumps(favourite_subjects),
                json.dumps(interests),
                json.dumps(skills),
                dream_career.strip(),
                academic_goal.strip(),
                achievements.strip(),
                datetime.now().isoformat()
            ))

            connection.commit()
            connection.close()

            st.success(
                "School student profile saved successfully."
            )
            st.rerun()

    if profile:

        st.write("")
        st.markdown(
            '<div class="studio-section-title">📋 Profile Summary</div>',
            unsafe_allow_html=True
        )

        summary1, summary2, summary3 = st.columns(3)

        with summary1:

            st.markdown(
                f"""<div class="studio-module-card">
<div class="studio-kpi-icon">🏫</div>
<h4>Academic Profile</h4>
<p><strong>Name:</strong> {st.session_state.user_name}</p>
<p><strong>School:</strong> {saved_profile['school_name']}</p>
<p><strong>Class:</strong> {saved_profile['current_class']}</p>
</div>""",
                unsafe_allow_html=True
            )

        with summary2:

            st.markdown(
                f"""<div class="studio-module-card">
<div class="studio-kpi-icon">🎯</div>
<h4>Career Direction</h4>
<p><strong>Board:</strong> {saved_profile['board']}</p>
<p><strong>City:</strong> {saved_profile['city'] or '-'}</p>
<p><strong>Dream Career:</strong> {saved_profile['dream_career'] or '-'}</p>
</div>""",
                unsafe_allow_html=True
            )

        with summary3:

            subject_text = (
                ", ".join(saved_profile["favourite_subjects"])
                if saved_profile["favourite_subjects"]
                else "-"
            )
            skill_text = (
                ", ".join(saved_profile["skills"])
                if saved_profile["skills"]
                else "-"
            )

            st.markdown(
                f"""<div class="studio-module-card">
<div class="studio-kpi-icon">💡</div>
<h4>Learning Profile</h4>
<p><strong>Subjects:</strong> {subject_text}</p>
<p><strong>Skills:</strong> {skill_text}</p>
</div>""",
                unsafe_allow_html=True
            )


# ==========================================================
# CAREER EXPLORER
# ==========================================================

elif menu == "🔍 Career Explorer":

    st.title("🔍 Career Explorer")

    st.write(
        "Select your favourite subject to discover suitable careers."
    )

    career_data = {
        "Mathematics": [
            {
                "career": "Data Scientist",
                "description": (
                    "Uses mathematics and data to solve real-world problems."
                ),
                "skills": "Python, Statistics, Analytics"
            },
            {
                "career": "Engineer",
                "description": (
                    "Designs machines, structures and useful systems."
                ),
                "skills": "Mathematics, Physics, Problem Solving"
            },
            {
                "career": "Actuary",
                "description": (
                    "Uses mathematics to calculate financial risks."
                ),
                "skills": "Statistics, Finance, Logical Thinking"
            }
        ],

        "Computer Science": [
            {
                "career": "Software Engineer",
                "description": (
                    "Develops applications, websites and software systems."
                ),
                "skills": "Programming, DSA, Databases"
            },
            {
                "career": "AI Engineer",
                "description": (
                    "Builds intelligent systems using machine learning."
                ),
                "skills": "Python, Mathematics, Machine Learning"
            },
            {
                "career": "Cybersecurity Analyst",
                "description": (
                    "Protects computers, networks and information."
                ),
                "skills": "Networking, Linux, Security"
            }
        ],

        "Biology": [
            {
                "career": "Doctor",
                "description": (
                    "Diagnoses and treats medical conditions."
                ),
                "skills": "Biology, Communication, Decision Making"
            },
            {
                "career": "Biotechnologist",
                "description": (
                    "Uses biological systems to create useful products."
                ),
                "skills": "Biology, Chemistry, Research"
            },
            {
                "career": "Pharmacist",
                "description": (
                    "Works with medicines and patient healthcare."
                ),
                "skills": "Chemistry, Biology, Accuracy"
            }
        ],

        "Commerce": [
            {
                "career": "Chartered Accountant",
                "description": (
                    "Works in accounting, taxation and auditing."
                ),
                "skills": "Accounting, Finance, Mathematics"
            },
            {
                "career": "Business Analyst",
                "description": (
                    "Helps organisations improve their performance."
                ),
                "skills": "Analytics, Business, Communication"
            },
            {
                "career": "Entrepreneur",
                "description": (
                    "Creates and manages a new business."
                ),
                "skills": "Leadership, Finance, Creativity"
            }
        ],

        "Arts": [
            {
                "career": "Graphic Designer",
                "description": (
                    "Creates visual content for companies and media."
                ),
                "skills": "Creativity, Design, Communication"
            },
            {
                "career": "Animator",
                "description": (
                    "Creates animated characters and visual stories."
                ),
                "skills": "Drawing, Animation, Storytelling"
            },
            {
                "career": "Content Creator",
                "description": (
                    "Creates educational and entertaining content."
                ),
                "skills": "Writing, Video Editing, Creativity"
            }
        ],

        "Social Studies": [
            {
                "career": "Civil Services Officer",
                "description": (
                    "Works in government administration and public service."
                ),
                "skills": "Leadership, General Knowledge, Communication"
            },
            {
                "career": "Lawyer",
                "description": (
                    "Provides legal advice and represents clients."
                ),
                "skills": "Reasoning, Communication, Law"
            },
            {
                "career": "Journalist",
                "description": (
                    "Researches and reports important information."
                ),
                "skills": "Writing, Communication, Investigation"
            }
        ]
    }

    selected_subject = st.selectbox(
        "Choose your favourite subject",
        list(career_data.keys())
    )

    if st.button(
        "Explore Careers",
        width="stretch"
    ):

        st.success(
            f"Career suggestions for {selected_subject}"
        )

        for career in career_data[selected_subject]:

            with st.container(border=True):

                st.subheader(career["career"])
                st.write(career["description"])
                st.write(
                    f"**Important skills:** {career['skills']}"
                )


# ==========================================================
# SUBJECT-WISE DYNAMIC QUIZ
# ==========================================================

elif menu == "📝 Subject Quiz":

    st.title("📝 Subject-wise Dynamic Quiz")
    st.write(
        "High-school-level quiz for Classes 9 to 12. "
        "Select a subject, class level and difficulty. "
        "The application dynamically creates a fresh quiz each time."
    )

    question_bank = {
        "Mathematics": {
            "Easy": [
                {
                    "question": "Solve: 2x + 7 = 19.",
                    "options": ["4", "5", "6", "7"],
                    "answer": "6",
                    "explanation": "2x = 12, so x = 6."
                },
                {
                    "question": "What is the value of √225?",
                    "options": ["12", "13", "15", "25"],
                    "answer": "15",
                    "explanation": "15 × 15 = 225."
                },
                {
                    "question": "The sum of the interior angles of a quadrilateral is:",
                    "options": ["180°", "270°", "360°", "540°"],
                    "answer": "360°",
                    "explanation": "A quadrilateral can be divided into two triangles."
                },
                {
                    "question": "If f(x) = 3x - 2, find f(4).",
                    "options": ["8", "10", "12", "14"],
                    "answer": "10",
                    "explanation": "f(4) = 3(4) - 2 = 10."
                },
                {
                    "question": "The slope of the line y = 5x + 3 is:",
                    "options": ["3", "5", "8", "-5"],
                    "answer": "5",
                    "explanation": "In y = mx + c, the coefficient of x is the slope."
                },
                {
                    "question": "Factorise x² - 9.",
                    "options": [
                        "(x - 9)(x + 1)",
                        "(x - 3)(x + 3)",
                        "(x - 3)²",
                        "(x + 9)(x - 1)"
                    ],
                    "answer": "(x - 3)(x + 3)",
                    "explanation": "x² - 9 is a difference of squares."
                },
                {
                    "question": "The probability of getting a head in one fair coin toss is:",
                    "options": ["0", "1/4", "1/2", "1"],
                    "answer": "1/2",
                    "explanation": "There is one favourable outcome out of two equally likely outcomes."
                },
                {
                    "question": "What is 15% of 640?",
                    "options": ["86", "92", "96", "102"],
                    "answer": "96",
                    "explanation": "0.15 × 640 = 96."
                }
            ],
            "Medium": [
                {
                    "question": "Solve the quadratic equation x² - 7x + 12 = 0.",
                    "options": ["x = 2, 6", "x = 3, 4", "x = -3, -4", "x = 1, 12"],
                    "answer": "x = 3, 4",
                    "explanation": "(x - 3)(x - 4) = 0."
                },
                {
                    "question": "If sin θ = 3/5 for an acute angle, then cos θ is:",
                    "options": ["2/5", "3/4", "4/5", "5/4"],
                    "answer": "4/5",
                    "explanation": "Using the 3-4-5 right triangle, cos θ = 4/5."
                },
                {
                    "question": "The 10th term of the arithmetic sequence 4, 7, 10, ... is:",
                    "options": ["28", "30", "31", "34"],
                    "answer": "31",
                    "explanation": "a₁₀ = 4 + 9(3) = 31."
                },
                {
                    "question": "Find the distance between (2, 3) and (8, 11).",
                    "options": ["8", "10", "12", "14"],
                    "answer": "10",
                    "explanation": "Distance = √[(6)² + (8)²] = 10."
                },
                {
                    "question": "If log₁₀ 1000 = x, then x equals:",
                    "options": ["2", "3", "10", "100"],
                    "answer": "3",
                    "explanation": "10³ = 1000."
                },
                {
                    "question": "The mean of 6, 8, 10, 12 and 14 is:",
                    "options": ["8", "9", "10", "11"],
                    "answer": "10",
                    "explanation": "The total is 50 and 50 ÷ 5 = 10."
                },
                {
                    "question": "The area of a sector of angle 90° in a circle of radius 14 cm is:",
                    "options": ["77 cm²", "154 cm²", "308 cm²", "616 cm²"],
                    "answer": "154 cm²",
                    "explanation": "Area = 90/360 × 22/7 × 14² = 154 cm²."
                },
                {
                    "question": "If 2ˣ = 32, the value of x is:",
                    "options": ["4", "5", "6", "8"],
                    "answer": "5",
                    "explanation": "2⁵ = 32."
                }
            ],
            "Hard": [
                {
                    "question": "The roots of 2x² - 5x - 3 = 0 are:",
                    "options": [
                        "3 and -1/2",
                        "-3 and 1/2",
                        "1 and -3",
                        "3/2 and -1"
                    ],
                    "answer": "3 and -1/2",
                    "explanation": "(2x + 1)(x - 3) = 0."
                },
                {
                    "question": "If tan θ = 1 and 0° < θ < 90°, then θ is:",
                    "options": ["30°", "45°", "60°", "90°"],
                    "answer": "45°",
                    "explanation": "tan 45° = 1."
                },
                {
                    "question": "The sum of the first 20 natural numbers is:",
                    "options": ["190", "200", "210", "220"],
                    "answer": "210",
                    "explanation": "n(n + 1)/2 = 20 × 21 / 2 = 210."
                },
                {
                    "question": "If the determinant |2  3; 4  5| is evaluated, the result is:",
                    "options": ["-2", "2", "10", "22"],
                    "answer": "-2",
                    "explanation": "2×5 - 3×4 = -2."
                },
                {
                    "question": "A bag contains 5 red, 4 blue and 3 green balls. The probability of drawing a blue ball is:",
                    "options": ["1/4", "1/3", "4/11", "4/12"],
                    "answer": "1/3",
                    "explanation": "There are 12 balls and 4 are blue: 4/12 = 1/3."
                },
                {
                    "question": "If the radius of a sphere is doubled, its volume becomes:",
                    "options": ["2 times", "4 times", "6 times", "8 times"],
                    "answer": "8 times",
                    "explanation": "Volume is proportional to r³."
                },
                {
                    "question": "The equation of a line with slope 2 passing through (1, 3) is:",
                    "options": ["y = 2x + 1", "y = 2x - 1", "y = x + 2", "y = 3x - 1"],
                    "answer": "y = 2x + 1",
                    "explanation": "Using y - 3 = 2(x - 1), we get y = 2x + 1."
                },
                {
                    "question": "If a geometric progression has first term 3 and common ratio 2, its 6th term is:",
                    "options": ["48", "64", "96", "192"],
                    "answer": "96",
                    "explanation": "a₆ = 3 × 2⁵ = 96."
                }
            ]
        },
        "Science": {
            "Easy": [
                {
                    "question": "The SI unit of electric current is:",
                    "options": ["Volt", "Ampere", "Ohm", "Watt"],
                    "answer": "Ampere",
                    "explanation": "Electric current is measured in amperes."
                },
                {
                    "question": "Which cell organelle is called the powerhouse of the cell?",
                    "options": ["Nucleus", "Mitochondrion", "Ribosome", "Golgi body"],
                    "answer": "Mitochondrion",
                    "explanation": "Mitochondria release energy through cellular respiration."
                },
                {
                    "question": "A substance with pH 9 is:",
                    "options": ["Acidic", "Basic", "Neutral", "Salt-free"],
                    "answer": "Basic",
                    "explanation": "pH values above 7 are basic."
                },
                {
                    "question": "The speed of light in vacuum is approximately:",
                    "options": ["3×10⁶ m/s", "3×10⁷ m/s", "3×10⁸ m/s", "3×10⁹ m/s"],
                    "answer": "3×10⁸ m/s",
                    "explanation": "The accepted value is about 3×10⁸ m/s."
                },
                {
                    "question": "Which gas is produced during photosynthesis?",
                    "options": ["Nitrogen", "Oxygen", "Carbon dioxide", "Hydrogen"],
                    "answer": "Oxygen",
                    "explanation": "Plants release oxygen during photosynthesis."
                },
                {
                    "question": "The chemical symbol for sodium is:",
                    "options": ["S", "So", "Na", "N"],
                    "answer": "Na",
                    "explanation": "Na comes from the Latin name natrium."
                },
                {
                    "question": "The functional unit of the kidney is:",
                    "options": ["Neuron", "Nephron", "Alveolus", "Villus"],
                    "answer": "Nephron",
                    "explanation": "Nephrons filter blood and form urine."
                },
                {
                    "question": "Newton's second law is expressed as:",
                    "options": ["F = ma", "V = IR", "P = VI", "E = mc²"],
                    "answer": "F = ma",
                    "explanation": "Force equals mass multiplied by acceleration."
                }
            ],
            "Medium": [
                {
                    "question": "A 10 Ω resistor carries 2 A current. The potential difference is:",
                    "options": ["5 V", "10 V", "20 V", "40 V"],
                    "answer": "20 V",
                    "explanation": "V = IR = 2 × 10 = 20 V."
                },
                {
                    "question": "Which process produces gametes?",
                    "options": ["Mitosis", "Meiosis", "Binary fission", "Budding"],
                    "answer": "Meiosis",
                    "explanation": "Meiosis produces haploid gametes."
                },
                {
                    "question": "The molar mass of water is:",
                    "options": ["16 g/mol", "18 g/mol", "20 g/mol", "22 g/mol"],
                    "answer": "18 g/mol",
                    "explanation": "2(1) + 16 = 18 g/mol."
                },
                {
                    "question": "A convex lens has focal length 20 cm. Its power is:",
                    "options": ["+2 D", "+5 D", "-2 D", "-5 D"],
                    "answer": "+5 D",
                    "explanation": "P = 1/f(m) = 1/0.20 = +5 D."
                },
                {
                    "question": "The hormone that regulates blood glucose is:",
                    "options": ["Thyroxine", "Insulin", "Adrenaline", "Estrogen"],
                    "answer": "Insulin",
                    "explanation": "Insulin lowers blood glucose levels."
                },
                {
                    "question": "Which metal is extracted from bauxite?",
                    "options": ["Iron", "Copper", "Aluminium", "Zinc"],
                    "answer": "Aluminium",
                    "explanation": "Bauxite is the principal ore of aluminium."
                },
                {
                    "question": "The unit of frequency is:",
                    "options": ["Joule", "Hertz", "Newton", "Pascal"],
                    "answer": "Hertz",
                    "explanation": "Frequency is measured in hertz."
                },
                {
                    "question": "DNA replication occurs during which phase of the cell cycle?",
                    "options": ["G₁ phase", "S phase", "G₂ phase", "M phase"],
                    "answer": "S phase",
                    "explanation": "DNA synthesis occurs during S phase."
                }
            ],
            "Hard": [
                {
                    "question": "Two resistors of 6 Ω and 3 Ω are connected in parallel. Their equivalent resistance is:",
                    "options": ["1 Ω", "2 Ω", "3 Ω", "9 Ω"],
                    "answer": "2 Ω",
                    "explanation": "1/R = 1/6 + 1/3 = 1/2, so R = 2 Ω."
                },
                {
                    "question": "The oxidation state of sulfur in H₂SO₄ is:",
                    "options": ["+4", "+5", "+6", "-2"],
                    "answer": "+6",
                    "explanation": "2(+1) + S + 4(-2) = 0, so S = +6."
                },
                {
                    "question": "Which enzyme unwinds DNA during replication?",
                    "options": ["Ligase", "Helicase", "Amylase", "Pepsin"],
                    "answer": "Helicase",
                    "explanation": "Helicase separates the two DNA strands."
                },
                {
                    "question": "The work done in moving a charge of 2 C through 12 V is:",
                    "options": ["6 J", "12 J", "24 J", "48 J"],
                    "answer": "24 J",
                    "explanation": "W = QV = 2 × 12 = 24 J."
                },
                {
                    "question": "A solution has [H⁺] = 10⁻³ mol/L. Its pH is:",
                    "options": ["2", "3", "7", "11"],
                    "answer": "3",
                    "explanation": "pH = -log[H⁺] = 3."
                },
                {
                    "question": "Crossing over occurs during:",
                    "options": ["Prophase I", "Metaphase I", "Anaphase II", "Telophase II"],
                    "answer": "Prophase I",
                    "explanation": "Homologous chromosomes exchange segments during prophase I."
                },
                {
                    "question": "The energy stored in a 2 F capacitor charged to 3 V is:",
                    "options": ["3 J", "6 J", "9 J", "18 J"],
                    "answer": "9 J",
                    "explanation": "E = 1/2 CV² = 1/2 × 2 × 9 = 9 J."
                },
                {
                    "question": "Which law relates pressure and volume at constant temperature?",
                    "options": ["Charles' law", "Boyle's law", "Ohm's law", "Hooke's law"],
                    "answer": "Boyle's law",
                    "explanation": "Boyle's law states PV = constant at constant temperature."
                }
            ]
        },
        "English": {
            "Easy": [
                {
                    "question": "Choose the correct sentence.",
                    "options": [
                        "She don't like music.",
                        "She doesn't likes music.",
                        "She doesn't like music.",
                        "She not like music."
                    ],
                    "answer": "She doesn't like music.",
                    "explanation": "After 'doesn't', use the base form of the verb."
                },
                {
                    "question": "Identify the figure of speech: 'The moon smiled at us.'",
                    "options": ["Simile", "Personification", "Metaphor", "Alliteration"],
                    "answer": "Personification",
                    "explanation": "The moon is given a human action."
                },
                {
                    "question": "The antonym of 'scarce' is:",
                    "options": ["Rare", "Limited", "Abundant", "Small"],
                    "answer": "Abundant",
                    "explanation": "Abundant means plentiful."
                },
                {
                    "question": "Choose the correct passive form: 'They completed the project.'",
                    "options": [
                        "The project was completed by them.",
                        "The project is completed by them.",
                        "The project completed them.",
                        "They were completed by the project."
                    ],
                    "answer": "The project was completed by them.",
                    "explanation": "Simple past passive uses was/were + past participle."
                },
                {
                    "question": "Which word is an adverb?",
                    "options": ["Careful", "Carefully", "Care", "Caring"],
                    "answer": "Carefully",
                    "explanation": "Carefully describes how an action is performed."
                },
                {
                    "question": "Choose the correctly spelt word.",
                    "options": ["Occassion", "Occasion", "Ocassion", "Ocasian"],
                    "answer": "Occasion",
                    "explanation": "The correct spelling is 'occasion'."
                },
                {
                    "question": "Complete: Neither the teacher nor the students ___ ready.",
                    "options": ["is", "are", "was", "has"],
                    "answer": "are",
                    "explanation": "The verb agrees with the nearer subject 'students'."
                },
                {
                    "question": "A word that imitates a sound is called:",
                    "options": ["Oxymoron", "Onomatopoeia", "Hyperbole", "Irony"],
                    "answer": "Onomatopoeia",
                    "explanation": "Examples include buzz, hiss and bang."
                }
            ],
            "Medium": [
                {
                    "question": "Choose the correct reported speech: Ravi said, 'I have finished my work.'",
                    "options": [
                        "Ravi said that he had finished his work.",
                        "Ravi said that I have finished my work.",
                        "Ravi says he finished his work.",
                        "Ravi told that he has finished."
                    ],
                    "answer": "Ravi said that he had finished his work.",
                    "explanation": "Present perfect changes to past perfect in reported speech."
                },
                {
                    "question": "Identify the clause: 'What she decided' surprised everyone.",
                    "options": ["Adjective clause", "Adverb clause", "Noun clause", "Relative clause"],
                    "answer": "Noun clause",
                    "explanation": "The clause functions as the subject of the sentence."
                },
                {
                    "question": "Choose the sentence with correct punctuation.",
                    "options": [
                        "However I decided to stay.",
                        "However, I decided to stay.",
                        "However I, decided to stay.",
                        "However; I decided, to stay."
                    ],
                    "answer": "However, I decided to stay.",
                    "explanation": "A comma follows the introductory transition word."
                },
                {
                    "question": "The phrase 'a blessing in disguise' means:",
                    "options": [
                        "A hidden danger",
                        "Something good that first seemed bad",
                        "A false promise",
                        "An obvious advantage"
                    ],
                    "answer": "Something good that first seemed bad",
                    "explanation": "The expression refers to an unexpected benefit."
                },
                {
                    "question": "Choose the correct conditional sentence.",
                    "options": [
                        "If I will study, I pass.",
                        "If I studied, I would pass.",
                        "If I study, I would passed.",
                        "If I had study, I pass."
                    ],
                    "answer": "If I studied, I would pass.",
                    "explanation": "This is the correct second conditional form."
                },
                {
                    "question": "Which sentence contains a dangling modifier?",
                    "options": [
                        "Walking to school, I saw a rainbow.",
                        "Walking to school, the rain began.",
                        "I saw a rainbow while walking to school.",
                        "While I walked, I saw a rainbow."
                    ],
                    "answer": "Walking to school, the rain began.",
                    "explanation": "The phrase incorrectly appears to modify 'the rain'."
                },
                {
                    "question": "The word 'meticulous' most nearly means:",
                    "options": ["Careless", "Very careful", "Fast", "Ordinary"],
                    "answer": "Very careful",
                    "explanation": "Meticulous means showing great attention to detail."
                },
                {
                    "question": "Identify the tone: 'The author strongly criticises the policy as unfair and harmful.'",
                    "options": ["Neutral", "Critical", "Humorous", "Optimistic"],
                    "answer": "Critical",
                    "explanation": "The wording expresses disapproval."
                }
            ],
            "Hard": [
                {
                    "question": "Choose the sentence with correct parallel structure.",
                    "options": [
                        "She likes reading, to swim and cycling.",
                        "She likes reading, swimming and cycling.",
                        "She likes to read, swimming and to cycle.",
                        "She likes read, swim and cycling."
                    ],
                    "answer": "She likes reading, swimming and cycling.",
                    "explanation": "All three items use the same grammatical form."
                },
                {
                    "question": "Identify the literary device: 'It was the best of times, it was the worst of times.'",
                    "options": ["Antithesis", "Simile", "Euphemism", "Pun"],
                    "answer": "Antithesis",
                    "explanation": "Contrasting ideas are placed in parallel structure."
                },
                {
                    "question": "Choose the most concise sentence.",
                    "options": [
                        "Due to the fact that it rained, the match was cancelled.",
                        "Because it rained, the match was cancelled.",
                        "The match was cancelled owing to the fact of rain.",
                        "Rain being the reason, cancellation happened."
                    ],
                    "answer": "Because it rained, the match was cancelled.",
                    "explanation": "It expresses the same idea clearly and directly."
                },
                {
                    "question": "Which sentence uses the subjunctive mood correctly?",
                    "options": [
                        "I wish I was taller.",
                        "I wish I were taller.",
                        "I wish I am taller.",
                        "I wish I be taller."
                    ],
                    "answer": "I wish I were taller.",
                    "explanation": "The subjunctive uses 'were' for unreal wishes."
                },
                {
                    "question": "The phrase 'the crown' used to mean 'the monarchy' is an example of:",
                    "options": ["Metonymy", "Simile", "Alliteration", "Hyperbole"],
                    "answer": "Metonymy",
                    "explanation": "A related term stands for the larger concept."
                },
                {
                    "question": "Choose the correctly revised sentence: 'Each of the players have submitted their form.'",
                    "options": [
                        "Each of the players has submitted his or her form.",
                        "Each players have submitted their form.",
                        "Each of players has submit form.",
                        "Each player have submitted forms."
                    ],
                    "answer": "Each of the players has submitted his or her form.",
                    "explanation": "'Each' is singular and takes 'has'."
                },
                {
                    "question": "Which sentence is an example of irony?",
                    "options": [
                        "A fire station burns down.",
                        "The stars danced.",
                        "He is as brave as a lion.",
                        "The wind whispered."
                    ],
                    "answer": "A fire station burns down.",
                    "explanation": "The outcome is opposite to what is expected."
                },
                {
                    "question": "The primary purpose of a thesis statement is to:",
                    "options": [
                        "List every source",
                        "State the central argument",
                        "Provide a concluding quotation",
                        "Introduce unrelated background"
                    ],
                    "answer": "State the central argument",
                    "explanation": "A thesis presents the main claim of an essay."
                }
            ]
        },
        "Social Studies": {
            "Easy": [
                {
                    "question": "The Indian Constitution came into force on:",
                    "options": ["15 August 1947", "26 January 1950", "26 November 1949", "2 October 1950"],
                    "answer": "26 January 1950",
                    "explanation": "India celebrates this date as Republic Day."
                },
                {
                    "question": "The Tropic of Cancer passes through:",
                    "options": ["India", "Sri Lanka", "Nepal only", "Maldives"],
                    "answer": "India",
                    "explanation": "The Tropic of Cancer crosses eight Indian states."
                },
                {
                    "question": "Who founded the Mauryan Empire?",
                    "options": ["Ashoka", "Chandragupta Maurya", "Harsha", "Samudragupta"],
                    "answer": "Chandragupta Maurya",
                    "explanation": "He founded the Mauryan Empire in the 4th century BCE."
                },
                {
                    "question": "The lower house of Parliament is:",
                    "options": ["Rajya Sabha", "Lok Sabha", "Vidhan Parishad", "Supreme Court"],
                    "answer": "Lok Sabha",
                    "explanation": "Lok Sabha is the House of the People."
                },
                {
                    "question": "Black soil is best suited for growing:",
                    "options": ["Tea", "Cotton", "Jute", "Coffee"],
                    "answer": "Cotton",
                    "explanation": "Black soil retains moisture and supports cotton cultivation."
                },
                {
                    "question": "The Green Revolution mainly increased the production of:",
                    "options": ["Milk", "Food grains", "Fish", "Oil"],
                    "answer": "Food grains",
                    "explanation": "It greatly increased wheat and rice production."
                },
                {
                    "question": "The Prime Meridian passes through:",
                    "options": ["Greenwich", "New Delhi", "Tokyo", "Cairo"],
                    "answer": "Greenwich",
                    "explanation": "0° longitude passes through Greenwich, England."
                },
                {
                    "question": "Fundamental Rights are found in which part of the Indian Constitution?",
                    "options": ["Part I", "Part II", "Part III", "Part IV"],
                    "answer": "Part III",
                    "explanation": "Part III contains the Fundamental Rights."
                }
            ],
            "Medium": [
                {
                    "question": "The 73rd Constitutional Amendment is related to:",
                    "options": ["Panchayati Raj", "Emergency powers", "Judicial review", "Fundamental Duties"],
                    "answer": "Panchayati Raj",
                    "explanation": "It strengthened rural local self-government."
                },
                {
                    "question": "The Permanent Settlement was introduced by:",
                    "options": ["Lord Curzon", "Lord Cornwallis", "Lord Dalhousie", "Lord Ripon"],
                    "answer": "Lord Cornwallis",
                    "explanation": "It was introduced in Bengal in 1793."
                },
                {
                    "question": "Orographic rainfall occurs when:",
                    "options": [
                        "Air rises over mountains",
                        "Two ocean currents meet",
                        "Desert air cools rapidly",
                        "Rivers overflow"
                    ],
                    "answer": "Air rises over mountains",
                    "explanation": "Mountains force moist air upward, causing cooling and rain."
                },
                {
                    "question": "Which institution formulates monetary policy in India?",
                    "options": ["SEBI", "RBI", "NITI Aayog", "Election Commission"],
                    "answer": "RBI",
                    "explanation": "The Reserve Bank of India manages monetary policy."
                },
                {
                    "question": "The Non-Cooperation Movement began in:",
                    "options": ["1905", "1919", "1920", "1930"],
                    "answer": "1920",
                    "explanation": "Mahatma Gandhi launched it in 1920."
                },
                {
                    "question": "The Human Development Index includes:",
                    "options": [
                        "Health, education and income",
                        "Only income",
                        "Only literacy",
                        "Population and rainfall"
                    ],
                    "answer": "Health, education and income",
                    "explanation": "HDI combines these three broad dimensions."
                },
                {
                    "question": "Which soil is formed by river deposits?",
                    "options": ["Black soil", "Alluvial soil", "Laterite soil", "Red soil"],
                    "answer": "Alluvial soil",
                    "explanation": "Rivers deposit fine sediments that form alluvial soil."
                },
                {
                    "question": "A federal system of government divides power between:",
                    "options": [
                        "Judiciary and media",
                        "Central and state governments",
                        "Only local governments",
                        "Citizens and courts"
                    ],
                    "answer": "Central and state governments",
                    "explanation": "Federalism distributes authority across levels of government."
                }
            ],
            "Hard": [
                {
                    "question": "Which Article of the Indian Constitution deals with the Right to Constitutional Remedies?",
                    "options": ["Article 14", "Article 19", "Article 21", "Article 32"],
                    "answer": "Article 32",
                    "explanation": "Dr. Ambedkar called Article 32 the heart and soul of the Constitution."
                },
                {
                    "question": "The Doctrine of Lapse is associated with:",
                    "options": ["Lord Wellesley", "Lord Dalhousie", "Lord Ripon", "Lord Curzon"],
                    "answer": "Lord Dalhousie",
                    "explanation": "Dalhousie used the doctrine to annex princely states."
                },
                {
                    "question": "A rain-shadow region is generally found on the:",
                    "options": ["Windward side", "Leeward side", "Coastal side", "River delta"],
                    "answer": "Leeward side",
                    "explanation": "Descending air on the leeward side is dry."
                },
                {
                    "question": "The policy of liberalisation in India began prominently in:",
                    "options": ["1947", "1969", "1991", "2005"],
                    "answer": "1991",
                    "explanation": "Major economic reforms were introduced in 1991."
                },
                {
                    "question": "Which schedule of the Constitution lists the recognised languages of India?",
                    "options": ["Fifth", "Sixth", "Eighth", "Tenth"],
                    "answer": "Eighth",
                    "explanation": "The Eighth Schedule lists constitutionally recognised languages."
                },
                {
                    "question": "The Battle of Plassey was fought in:",
                    "options": ["1757", "1764", "1857", "1905"],
                    "answer": "1757",
                    "explanation": "The British East India Company defeated Siraj-ud-Daulah in 1757."
                },
                {
                    "question": "Which type of unemployment is common in agriculture when more workers are employed than necessary?",
                    "options": ["Seasonal", "Disguised", "Structural", "Frictional"],
                    "answer": "Disguised",
                    "explanation": "Some workers add little or no additional output."
                },
                {
                    "question": "Judicial review allows courts to:",
                    "options": [
                        "Make tax laws",
                        "Examine the constitutionality of laws",
                        "Conduct elections",
                        "Control the media"
                    ],
                    "answer": "Examine the constitutionality of laws",
                    "explanation": "Courts may invalidate laws that violate the Constitution."
                }
            ]
        },
        "General Knowledge": {
            "Easy": [
                {
                    "question": "The headquarters of the United Nations is located in:",
                    "options": ["Geneva", "Paris", "New York", "London"],
                    "answer": "New York",
                    "explanation": "The UN headquarters is in New York City."
                },
                {
                    "question": "The currency of Japan is:",
                    "options": ["Won", "Yuan", "Yen", "Baht"],
                    "answer": "Yen",
                    "explanation": "Japan uses the yen."
                },
                {
                    "question": "Which planet is known as the Red Planet?",
                    "options": ["Venus", "Mars", "Jupiter", "Mercury"],
                    "answer": "Mars",
                    "explanation": "Iron oxide gives Mars its reddish appearance."
                },
                {
                    "question": "Who developed the theory of relativity?",
                    "options": ["Isaac Newton", "Albert Einstein", "Galileo", "Nikola Tesla"],
                    "answer": "Albert Einstein",
                    "explanation": "Einstein developed special and general relativity."
                },
                {
                    "question": "The largest ocean is:",
                    "options": ["Atlantic", "Indian", "Pacific", "Arctic"],
                    "answer": "Pacific",
                    "explanation": "The Pacific Ocean is the world's largest."
                },
                {
                    "question": "The national aquatic animal of India is:",
                    "options": ["Blue whale", "Ganges river dolphin", "Crocodile", "Sea turtle"],
                    "answer": "Ganges river dolphin",
                    "explanation": "It is India's national aquatic animal."
                },
                {
                    "question": "Which instrument measures atmospheric pressure?",
                    "options": ["Thermometer", "Barometer", "Hygrometer", "Seismograph"],
                    "answer": "Barometer",
                    "explanation": "A barometer measures air pressure."
                },
                {
                    "question": "The Nobel Prize is not traditionally awarded in:",
                    "options": ["Physics", "Chemistry", "Mathematics", "Literature"],
                    "answer": "Mathematics",
                    "explanation": "There is no original Nobel category for Mathematics."
                }
            ],
            "Medium": [
                {
                    "question": "The International Court of Justice is located in:",
                    "options": ["Geneva", "The Hague", "New York", "Vienna"],
                    "answer": "The Hague",
                    "explanation": "The ICJ is based in The Hague, Netherlands."
                },
                {
                    "question": "The ozone layer is mainly found in the:",
                    "options": ["Troposphere", "Stratosphere", "Mesosphere", "Thermosphere"],
                    "answer": "Stratosphere",
                    "explanation": "Most atmospheric ozone is concentrated in the stratosphere."
                },
                {
                    "question": "Which strait separates Asia from North America?",
                    "options": ["Bering Strait", "Palk Strait", "Malacca Strait", "Gibraltar Strait"],
                    "answer": "Bering Strait",
                    "explanation": "It lies between Russia and Alaska."
                },
                {
                    "question": "The longest river entirely within India is:",
                    "options": ["Ganga", "Godavari", "Narmada", "Krishna"],
                    "answer": "Godavari",
                    "explanation": "The Godavari is the longest river entirely within India."
                },
                {
                    "question": "The Blue Revolution relates to:",
                    "options": ["Milk", "Fisheries", "Oilseeds", "Space technology"],
                    "answer": "Fisheries",
                    "explanation": "It refers to growth in fish production."
                },
                {
                    "question": "Which country has the largest population in Africa?",
                    "options": ["Egypt", "Nigeria", "South Africa", "Kenya"],
                    "answer": "Nigeria",
                    "explanation": "Nigeria has Africa's largest population."
                },
                {
                    "question": "The device that converts chemical energy into electrical energy is:",
                    "options": ["Generator", "Battery", "Motor", "Transformer"],
                    "answer": "Battery",
                    "explanation": "A battery converts chemical energy into electrical energy."
                },
                {
                    "question": "The first artificial satellite was:",
                    "options": ["Apollo 11", "Sputnik 1", "Voyager 1", "Aryabhata"],
                    "answer": "Sputnik 1",
                    "explanation": "The Soviet Union launched Sputnik 1 in 1957."
                }
            ],
            "Hard": [
                {
                    "question": "The Bretton Woods institutions include:",
                    "options": [
                        "IMF and World Bank",
                        "WTO and WHO",
                        "UNESCO and UNICEF",
                        "NATO and EU"
                    ],
                    "answer": "IMF and World Bank",
                    "explanation": "Both institutions emerged from the Bretton Woods Conference."
                },
                {
                    "question": "Which element has atomic number 74?",
                    "options": ["Tungsten", "Platinum", "Mercury", "Uranium"],
                    "answer": "Tungsten",
                    "explanation": "Tungsten has atomic number 74."
                },
                {
                    "question": "The term 'biodiversity hotspot' refers to a region with:",
                    "options": [
                        "High species richness and high threat",
                        "Only high rainfall",
                        "Only desert vegetation",
                        "No human settlement"
                    ],
                    "answer": "High species richness and high threat",
                    "explanation": "Hotspots contain exceptional biodiversity under severe threat."
                },
                {
                    "question": "The Chandrasekhar limit is related to:",
                    "options": ["Black holes only", "White dwarf stars", "Planetary motion", "Ocean tides"],
                    "answer": "White dwarf stars",
                    "explanation": "It is the maximum stable mass of a white dwarf."
                },
                {
                    "question": "Which treaty established the European Union?",
                    "options": ["Treaty of Versailles", "Maastricht Treaty", "Treaty of Rome only", "Kyoto Protocol"],
                    "answer": "Maastricht Treaty",
                    "explanation": "The Maastricht Treaty formally established the EU."
                },
                {
                    "question": "The Richter scale measures:",
                    "options": ["Wind speed", "Earthquake magnitude", "Rainfall", "Humidity"],
                    "answer": "Earthquake magnitude",
                    "explanation": "It quantifies the magnitude of earthquakes."
                },
                {
                    "question": "The concept of 'survival of the fittest' is associated with:",
                    "options": ["Charles Darwin", "Gregor Mendel", "Louis Pasteur", "James Watt"],
                    "answer": "Charles Darwin",
                    "explanation": "The phrase is linked with evolutionary theory."
                },
                {
                    "question": "Which Indian mission was designed to study the Sun?",
                    "options": ["Chandrayaan-3", "Aditya-L1", "Mangalyaan", "Gaganyaan"],
                    "answer": "Aditya-L1",
                    "explanation": "Aditya-L1 is India's solar observation mission."
                }
            ]
        }
    }

    setup_col1, setup_col2, setup_col3, setup_col4 = st.columns(4)

    with setup_col1:
        quiz_subject = st.selectbox(
            "Subject",
            list(question_bank.keys()),
            key="subject_quiz_selector"
        )

    with setup_col2:
        quiz_class_level = st.selectbox(
            "Class Level",
            ["Class 9", "Class 10", "Class 11", "Class 12"],
            index=1,
            key="subject_quiz_class_selector"
        )

    with setup_col3:
        quiz_difficulty = st.selectbox(
            "Difficulty",
            ["Easy", "Medium", "Hard"],
            key="subject_quiz_difficulty_selector"
        )

    with setup_col4:
        number_of_questions = st.selectbox(
            "Number of Questions",
            [5, 10, 15, 20, 25, 30],
            index=1,
            help=(
                "Select the quiz length. When the selected number is "
                "greater than the available unique questions, the app "
                "adds randomly selected questions to reach the total."
            )
        )

    if st.button("🔄 Generate New Quiz", width="stretch"):
        available_questions = question_bank[
            quiz_subject
        ][quiz_difficulty]

        if number_of_questions <= len(available_questions):

            selected_questions = random.sample(
                available_questions,
                k=number_of_questions
            )

        else:

            # Include every available question once.
            selected_questions = available_questions.copy()

            # Add random questions until the requested total is reached.
            additional_count = (
                number_of_questions - len(available_questions)
            )

            selected_questions.extend(
                random.choices(
                    available_questions,
                    k=additional_count
                )
            )

            random.shuffle(selected_questions)

        # Create independent question copies and shuffle each answer list.
        generated_questions = []

        for question_number, item in enumerate(
            selected_questions,
            start=1
        ):

            generated_item = item.copy()
            generated_item["options"] = item["options"].copy()
            generated_item["instance_id"] = (
                f"{quiz_subject}_{quiz_difficulty}_"
                f"{question_number}_{random.randint(1000, 9999)}"
            )

            random.shuffle(generated_item["options"])
            generated_questions.append(generated_item)

        st.session_state.subject_quiz_questions = generated_questions
        st.session_state.subject_quiz_subject = quiz_subject
        st.session_state.subject_quiz_difficulty = quiz_difficulty
        st.session_state.subject_quiz_result = None
        st.rerun()

    questions = st.session_state.subject_quiz_questions

    if questions:

        st.info(
            f"Subject: **{st.session_state.subject_quiz_subject}** · "
            f"Class: **{quiz_class_level}** · "
            f"Difficulty: **{st.session_state.subject_quiz_difficulty}** · "
            f"Questions: **{len(questions)}**"
        )

        with st.form("dynamic_subject_quiz_form"):

            submitted_answers = []

            for question_index, question_item in enumerate(
                questions,
                start=1
            ):
                answer = st.radio(
                    f"{question_index}. {question_item['question']}",
                    question_item["options"],
                    index=None,
                    key=(
                        "dynamic_quiz_answer_"
                        f"{question_item.get('instance_id', question_index)}"
                    )
                )
                submitted_answers.append(answer)

            submit_subject_quiz = st.form_submit_button(
                "Submit Quiz",
                width="stretch"
            )

        if submit_subject_quiz:

            if any(answer is None for answer in submitted_answers):
                st.error("Please answer every question before submitting.")

            else:
                correct_count = 0
                review_items = []

                for question_item, submitted_answer in zip(
                    questions,
                    submitted_answers
                ):
                    is_correct = (
                        submitted_answer == question_item["answer"]
                    )

                    if is_correct:
                        correct_count += 1

                    review_items.append({
                        "question": question_item["question"],
                        "submitted": submitted_answer,
                        "correct": question_item["answer"],
                        "explanation": question_item["explanation"],
                        "is_correct": is_correct
                    })

                percentage = round(
                    correct_count / len(questions) * 100
                )

                if percentage >= 80:
                    performance = "Excellent"
                elif percentage >= 60:
                    performance = "Good"
                elif percentage >= 40:
                    performance = "Needs More Practice"
                else:
                    performance = "Revision Required"

                st.session_state.subject_quiz_result = {
                    "score": correct_count,
                    "total": len(questions),
                    "percentage": percentage,
                    "performance": performance,
                    "review": review_items
                }

                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute("""
                    INSERT INTO quiz_results (
                        user_id,
                        quiz_type,
                        result,
                        score,
                        completed_at
                    )
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    st.session_state.user_id,
                    f"{st.session_state.subject_quiz_subject} Quiz",
                    (
                        f"{st.session_state.subject_quiz_difficulty} - "
                        f"{performance}"
                    ),
                    percentage,
                    datetime.now().isoformat()
                ))

                connection.commit()
                connection.close()

        result = st.session_state.subject_quiz_result

        if result:

            metric1, metric2, metric3 = st.columns(3)

            metric1.metric(
                "Score",
                f"{result['score']}/{result['total']}"
            )
            metric2.metric(
                "Percentage",
                f"{result['percentage']}%"
            )
            metric3.metric(
                "Performance",
                result["performance"]
            )

            st.progress(result["percentage"] / 100)

            st.subheader("📋 Answer Review")

            for review_index, review in enumerate(
                result["review"],
                start=1
            ):
                if review["is_correct"]:
                    st.success(
                        f"{review_index}. Correct — "
                        f"{review['question']}"
                    )
                else:
                    st.error(
                        f"{review_index}. Incorrect — "
                        f"{review['question']}"
                    )

                st.write(
                    f"**Your answer:** {review['submitted']}"
                )
                st.write(
                    f"**Correct answer:** {review['correct']}"
                )
                st.caption(review["explanation"])
                st.divider()

    else:
        st.warning(
            "Choose the subject and difficulty, then click "
            "'Generate New Quiz'."
        )


# ==========================================================
# INTEREST ASSESSMENT
# ==========================================================

elif menu == "📊 Interest Assessment":

    st.title("📊 Interest Assessment")

    st.write(
        "Rate your interest in each area from 1 to 10."
    )

    mathematics = st.slider(
        "Mathematics",
        1,
        10,
        5
    )

    science = st.slider(
        "Science",
        1,
        10,
        5
    )

    technology = st.slider(
        "Technology",
        1,
        10,
        5
    )

    creativity = st.slider(
        "Creativity and Arts",
        1,
        10,
        5
    )

    communication = st.slider(
        "Communication",
        1,
        10,
        5
    )

    business = st.slider(
        "Business and Finance",
        1,
        10,
        5
    )

    social_service = st.slider(
        "Helping Society",
        1,
        10,
        5
    )

    if st.button(
        "Analyse My Interests",
        width="stretch"
    ):

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

        strongest_score = interest_scores[
            strongest_interest
        ]

        st.session_state.interest_result = strongest_interest

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO quiz_results (
                user_id,
                quiz_type,
                result,
                score,
                completed_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            st.session_state.user_id,
            "Interest Assessment",
            strongest_interest,
            strongest_score,
            datetime.now().isoformat()
        ))

        connection.commit()
        connection.close()

        st.success(
            f"Your strongest interest is: {strongest_interest}"
        )

        interest_data = pd.DataFrame({
            "Interest": list(interest_scores.keys()),
            "Score": list(interest_scores.values())
        })

        interest_chart = px.bar(
            interest_data,
            x="Interest",
            y="Score",
            text="Score",
            title="Interest Assessment Result"
        )

        interest_chart.update_yaxes(
            range=[0, 10]
        )

        st.plotly_chart(
            interest_chart,
            width="stretch"
        )


# ==========================================================
# FUTURE SKILLS ROADMAP
# ==========================================================

elif menu == "🛣️ Future Skills Roadmap":

    st.title("🛣️ Future Skills Roadmap")

    roadmaps = {
        "Software Engineer": [
            "Learn computer fundamentals",
            "Learn Python programming",
            "Practice logical problem solving",
            "Learn HTML, CSS and JavaScript",
            "Study data structures and algorithms",
            "Build small software projects",
            "Learn Git and GitHub",
            "Prepare for coding interviews"
        ],

        "Doctor": [
            "Build strong Biology fundamentals",
            "Improve Chemistry knowledge",
            "Develop communication skills",
            "Prepare for NEET",
            "Practise previous examination papers",
            "Learn basic healthcare concepts",
            "Develop empathy and decision-making skills"
        ],

        "Data Scientist": [
            "Strengthen Mathematics",
            "Learn Python programming",
            "Study Statistics",
            "Learn NumPy and Pandas",
            "Understand Machine Learning",
            "Learn data visualisation",
            "Build data analysis projects"
        ],

        "Civil Services Officer": [
            "Improve general knowledge",
            "Read newspapers daily",
            "Develop communication skills",
            "Study history and geography",
            "Improve writing skills",
            "Practise aptitude",
            "Develop leadership abilities"
        ],

        "Graphic Designer": [
            "Learn basic design principles",
            "Practise drawing",
            "Learn Canva",
            "Learn Adobe Photoshop",
            "Study typography and colour theory",
            "Create a design portfolio",
            "Learn UI and UX basics"
        ],

        "Chartered Accountant": [
            "Build accounting fundamentals",
            "Improve Mathematics",
            "Learn Economics",
            "Understand taxation basics",
            "Develop analytical abilities",
            "Practise financial calculations",
            "Prepare for CA Foundation"
        ]
    }

    selected_career = st.selectbox(
        "Select your future career",
        list(roadmaps.keys())
    )

    st.subheader(
        f"{selected_career} Roadmap"
    )

    roadmap_steps = roadmaps[selected_career]

    for index, roadmap_step in enumerate(
        roadmap_steps,
        start=1
    ):

        with st.container(border=True):

            st.write(
                f"### Step {index}"
            )

            st.write(roadmap_step)

            step_progress = int(
                index / len(roadmap_steps) * 100
            )

            st.progress(step_progress)


# ==========================================================
# DAILY STUDY PLANNER
# ==========================================================

elif menu == "📅 Daily Study Planner":

    st.title("📅 Daily Study Planner")
    st.write(
        "Plan today's academic work and mark each activity when completed."
    )

    completed_task_count = 0

    for index, task in enumerate(
        st.session_state.daily_tasks
    ):

        task_completed = st.checkbox(
            task["task"],
            value=task["completed"],
            key=f"daily_task_{index}"
        )

        st.session_state.daily_tasks[index][
            "completed"
        ] = task_completed

        if task_completed:
            completed_task_count += 1

    total_tasks = len(
        st.session_state.daily_tasks
    )

    progress_value = (
        completed_task_count / total_tasks
        if total_tasks > 0
        else 0
    )

    st.progress(progress_value)

    st.write(
        f"Completed {completed_task_count} "
        f"out of {total_tasks} study tasks"
    )

    planner_col1, planner_col2 = st.columns(2)

    with planner_col1:
        task_subject = st.selectbox(
            "Subject",
            [
                "Mathematics",
                "Science",
                "English",
                "Social Studies",
                "General Knowledge",
                "Homework",
                "Revision"
            ],
            key="planner_subject"
        )

    with planner_col2:
        task_duration = st.selectbox(
            "Study Duration",
            [
                "15 minutes",
                "30 minutes",
                "45 minutes",
                "1 hour",
                "2 hours"
            ],
            key="planner_duration"
        )

    task_description = st.text_input(
        "Study activity",
        placeholder="Example: Revise algebra chapter"
    )

    add_task_column, reset_task_column = st.columns(2)

    with add_task_column:

        if st.button(
            "Add Study Task",
            width="stretch"
        ):

            if task_description.strip():

                st.session_state.daily_tasks.append({
                    "task": (
                        f"{task_subject}: {task_description.strip()} "
                        f"({task_duration})"
                    ),
                    "completed": False
                })

                st.rerun()

            else:

                st.warning(
                    "Enter a study activity before adding it."
                )

    with reset_task_column:

        if st.button(
            "Reset Today's Tasks",
            width="stretch"
        ):

            for task in st.session_state.daily_tasks:
                task["completed"] = False

            st.rerun()


# ==========================================================
# SCHOOL SUBJECTS
# ==========================================================

elif menu == "📚 School Subjects":

    st.title("📚 School Subjects")
    st.write(
        "Choose a subject and topic to view simple notes, key points "
        "and a practice activity."
    )

    subject_content = {
        "Mathematics": {
            "Algebra": {
                "summary": (
                    "Algebra uses letters and symbols to represent numbers. "
                    "An equation shows that two expressions are equal."
                ),
                "key_points": [
                    "A variable represents an unknown value.",
                    "Perform the same operation on both sides of an equation.",
                    "Like terms have the same variables and powers."
                ],
                "example": "2x + 6 = 16 → 2x = 10 → x = 5",
                "practice": "Solve: 4x - 8 = 20",
                "answer": "7"
            },
            "Geometry": {
                "summary": (
                    "Geometry studies shapes, sizes, angles, areas "
                    "and spatial relationships."
                ),
                "key_points": [
                    "A triangle has three sides and three angles.",
                    "The angles of a triangle total 180°.",
                    "Area of a rectangle = length × breadth."
                ],
                "example": "Rectangle: length 8 cm, breadth 5 cm → area = 40 cm²",
                "practice": "Find the perimeter of a square with side 9 cm.",
                "answer": "36"
            },
            "Percentages": {
                "summary": (
                    "A percentage represents a value out of one hundred."
                ),
                "key_points": [
                    "50% means one-half.",
                    "25% means one-fourth.",
                    "Percentage = part ÷ whole × 100."
                ],
                "example": "20% of 150 = 20/100 × 150 = 30",
                "practice": "Find 10% of 450.",
                "answer": "45"
            }
        },
        "Science": {
            "Physics": {
                "summary": (
                    "Physics studies matter, motion, force, energy "
                    "and their interactions."
                ),
                "key_points": [
                    "Speed = distance ÷ time.",
                    "Force can change the motion of an object.",
                    "Energy cannot be created or destroyed."
                ],
                "example": "A car covers 120 km in 2 hours → speed = 60 km/h",
                "practice": "A cyclist covers 45 km in 3 hours. Find the speed.",
                "answer": "15"
            },
            "Chemistry": {
                "summary": (
                    "Chemistry studies substances, their properties "
                    "and how they change."
                ),
                "key_points": [
                    "An element contains one type of atom.",
                    "A compound contains chemically combined elements.",
                    "Acids have pH below 7 and bases have pH above 7."
                ],
                "example": "Water is a compound made of hydrogen and oxygen.",
                "practice": "Is a substance with pH 3 acidic or basic?",
                "answer": "acidic"
            },
            "Biology": {
                "summary": (
                    "Biology is the study of living organisms and life processes."
                ),
                "key_points": [
                    "The cell is the basic unit of life.",
                    "Photosynthesis helps plants prepare food.",
                    "The heart circulates blood in the body."
                ],
                "example": "Plants use sunlight, water and carbon dioxide to make food.",
                "practice": "Which organ pumps blood through the human body?",
                "answer": "heart"
            }
        },
        "English": {
            "Grammar": {
                "summary": (
                    "Grammar gives rules for creating clear and correct sentences."
                ),
                "key_points": [
                    "A noun names a person, place, animal or thing.",
                    "A verb expresses an action or state.",
                    "An adjective describes a noun."
                ],
                "example": "The clever student answered quickly.",
                "practice": "Identify the adjective: 'The blue car moved fast.'",
                "answer": "blue"
            },
            "Vocabulary": {
                "summary": (
                    "Vocabulary is the collection of words a person knows and uses."
                ),
                "key_points": [
                    "A synonym has a similar meaning.",
                    "An antonym has an opposite meaning.",
                    "Context helps determine a word's meaning."
                ],
                "example": "Happy → joyful; ancient → modern",
                "practice": "Write a synonym for 'brave'.",
                "answer": "courageous"
            },
            "Writing": {
                "summary": (
                    "Good writing is clear, organised and suitable for its audience."
                ),
                "key_points": [
                    "Start with a clear main idea.",
                    "Use paragraphs for different points.",
                    "Review spelling, punctuation and grammar."
                ],
                "example": "Introduction → supporting points → conclusion",
                "practice": "Write three sentences about your favourite subject.",
                "answer": "open response"
            }
        },
        "Social Studies": {
            "History": {
                "summary": (
                    "History studies past people, societies and important events."
                ),
                "key_points": [
                    "Sources include inscriptions, coins and manuscripts.",
                    "Timelines organise events chronologically.",
                    "Historical events have causes and consequences."
                ],
                "example": "India became independent on 15 August 1947.",
                "practice": "In which year did India become independent?",
                "answer": "1947"
            },
            "Geography": {
                "summary": (
                    "Geography studies Earth, places, environments and people."
                ),
                "key_points": [
                    "Latitude measures distance north or south.",
                    "Longitude measures distance east or west.",
                    "Climate is the long-term weather pattern of a place."
                ],
                "example": "The Equator is at 0° latitude.",
                "practice": "Which line divides Earth into northern and southern halves?",
                "answer": "equator"
            },
            "Civics": {
                "summary": (
                    "Civics explains government, citizenship, rights and duties."
                ),
                "key_points": [
                    "Democracy allows citizens to choose representatives.",
                    "The Constitution is the supreme law of India.",
                    "Citizens have both rights and responsibilities."
                ],
                "example": "Voting is an important democratic responsibility.",
                "practice": "What is the supreme law of India?",
                "answer": "constitution"
            }
        },
        "General Knowledge": {
            "India": {
                "summary": (
                    "Learn important facts about India's geography, culture "
                    "and national symbols."
                ),
                "key_points": [
                    "New Delhi is India's capital.",
                    "The peacock is the national bird.",
                    "The Indian rupee is the national currency."
                ],
                "example": "India celebrates Republic Day on 26 January.",
                "practice": "What is the capital of India?",
                "answer": "new delhi"
            },
            "World": {
                "summary": (
                    "World knowledge includes countries, organisations, "
                    "landmarks and global events."
                ),
                "key_points": [
                    "There are seven continents.",
                    "The United Nations headquarters is in New York.",
                    "The Pacific is the largest ocean."
                ],
                "example": "Mount Everest is the world's highest mountain above sea level.",
                "practice": "Which is the largest ocean?",
                "answer": "pacific"
            },
            "Environment": {
                "summary": (
                    "Environmental studies explains ecosystems, resources "
                    "and sustainable living."
                ),
                "key_points": [
                    "Reduce, reuse and recycle conserve resources.",
                    "Trees absorb carbon dioxide.",
                    "Renewable resources can be naturally replenished."
                ],
                "example": "Solar and wind energy are renewable.",
                "practice": "Name one renewable source of energy.",
                "answer": "solar"
            }
        }
    }

    subject_name = st.selectbox(
        "Choose Subject",
        list(subject_content.keys())
    )

    topic_name = st.selectbox(
        "Choose Topic",
        list(subject_content[subject_name].keys())
    )

    topic_data = subject_content[subject_name][topic_name]

    st.subheader(f"{subject_name} — {topic_name}")

    with st.container(border=True):
        st.write("### 📖 Lesson Summary")
        st.write(topic_data["summary"])

        st.write("### ⭐ Key Points")
        for key_point in topic_data["key_points"]:
            st.write(f"✅ {key_point}")

        st.write("### ✏️ Example")
        st.code(topic_data["example"], language=None)

    st.subheader("🧠 Quick Practice")

    st.info(topic_data["practice"])

    practice_answer = st.text_input(
        "Enter your answer",
        key=f"subject_practice_{subject_name}_{topic_name}"
    )

    if st.button("Check Answer", width="stretch"):

        expected_answer = topic_data["answer"].strip().lower()
        entered_answer = practice_answer.strip().lower()

        if expected_answer == "open response":
            if len(entered_answer.split()) >= 8:
                st.success(
                    "Good response. Review your spelling and sentence structure."
                )
            else:
                st.warning(
                    "Write at least three complete sentences."
                )

        elif entered_answer == expected_answer:
            st.success("Correct answer! 🎉")

        else:
            st.error(
                f"Not correct yet. Suggested answer: {topic_data['answer']}"
            )


# ==========================================================
# APTITUDE PRACTICE
# ==========================================================

elif menu == "🧮 Aptitude Practice":

    st.title("🧮 Aptitude Practice")

    with st.form("aptitude_practice_form"):

        aptitude1 = st.radio(
            "1. What is 25% of 200?",
            [
                "25",
                "50",
                "75",
                "100"
            ]
        )

        aptitude2 = st.radio(
            "2. A book costs ₹120 after a ₹30 discount. "
            "What was the original price?",
            [
                "₹90",
                "₹120",
                "₹150",
                "₹180"
            ]
        )

        aptitude3 = st.radio(
            "3. Find the next number: 2, 4, 8, 16, ?",
            [
                "18",
                "24",
                "30",
                "32"
            ]
        )

        aptitude4 = st.radio(
            "4. A vehicle travels 60 km in one hour. "
            "How far will it travel in three hours?",
            [
                "120 km",
                "150 km",
                "180 km",
                "240 km"
            ]
        )

        submit_aptitude = st.form_submit_button(
            "Submit Aptitude Test",
            width="stretch"
        )

    if submit_aptitude:

        aptitude_score = 0

        if aptitude1 == "50":
            aptitude_score += 1

        if aptitude2 == "₹150":
            aptitude_score += 1

        if aptitude3 == "32":
            aptitude_score += 1

        if aptitude4 == "180 km":
            aptitude_score += 1

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO quiz_results (
                user_id,
                quiz_type,
                result,
                score,
                completed_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            st.session_state.user_id,
            "Aptitude Practice",
            f"{aptitude_score}/4",
            aptitude_score,
            datetime.now().isoformat()
        ))

        connection.commit()
        connection.close()

        st.metric(
            "Aptitude Score",
            f"{aptitude_score}/4"
        )

        if aptitude_score == 4:

            st.success(
                "Excellent! All answers are correct."
            )

        elif aptitude_score >= 2:

            st.info(
                "Good attempt. Continue practising."
            )

        else:

            st.warning(
                "Practise percentages, patterns and speed problems."
            )


# ==========================================================
# COMMUNICATION SKILLS
# ==========================================================

elif menu == "🗣️ Communication Skills":

    st.title("🗣️ Communication Skills")

    communication_activity = st.selectbox(
        "Choose an activity",
        [
            "Self Introduction",
            "Story Writing",
            "Email Writing",
            "Public Speaking"
        ]
    )

    activity_prompts = {
        "Self Introduction": (
            "Write a self-introduction including your name, class, "
            "school, hobbies, strengths and career goal."
        ),

        "Story Writing": (
            "Write a short story using the words school, robot, "
            "friend and future."
        ),

        "Email Writing": (
            "Write a polite email to your teacher requesting "
            "permission to participate in a coding competition."
        ),

        "Public Speaking": (
            "Prepare a one-minute speech about how technology "
            "helps students."
        )
    }

    st.info(
        activity_prompts[communication_activity]
    )

    communication_response = st.text_area(
        "Write your response",
        height=220
    )

    if st.button(
        "Evaluate My Response",
        width="stretch"
    ):

        word_count = len(
            communication_response.split()
        )

        if word_count == 0:

            st.error(
                "Write your response before evaluating it."
            )

        else:

            st.metric(
                "Word Count",
                word_count
            )

            if word_count >= 100:

                st.success(
                    "Good detailed response. "
                    "Review grammar and clarity."
                )

            elif word_count >= 50:

                st.info(
                    "Good start. Add examples and more details."
                )

            else:

                st.warning(
                    "Your response is short. "
                    "Try writing at least 50 words."
                )


# ==========================================================
# GOAL TRACKER
# ==========================================================

elif menu == "🎯 Goal Tracker":

    st.title("🎯 Goal Tracker")

    with st.form("goal_creation_form"):

        goal_title = st.text_input(
            "Goal Title",
            placeholder="Example: Score 90% in Mathematics"
        )

        target_date = st.date_input(
            "Target Date",
            min_value=date.today()
        )

        priority = st.selectbox(
            "Priority",
            [
                "Low",
                "Medium",
                "High"
            ]
        )

        add_goal = st.form_submit_button(
            "Add Goal",
            width="stretch"
        )

    if add_goal:

        if not goal_title.strip():

            st.error(
                "Enter a goal title."
            )

        else:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO student_goals (
                    user_id,
                    title,
                    target_date,
                    priority,
                    progress,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                st.session_state.user_id,
                goal_title.strip(),
                str(target_date),
                priority,
                0,
                datetime.now().isoformat()
            ))

            connection.commit()
            connection.close()

            st.success("Goal added successfully.")
            st.rerun()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            target_date,
            priority,
            progress
        FROM student_goals
        WHERE user_id = ?
        ORDER BY id DESC
    """, (st.session_state.user_id,))

    goals = cursor.fetchall()
    connection.close()

    if not goals:

        st.info(
            "You have not added any goals yet."
        )

    for goal in goals:

        goal_id = goal[0]
        title = goal[1]
        target = goal[2]
        goal_priority = goal[3]
        saved_progress = goal[4]

        with st.container(border=True):

            st.subheader(title)
            st.write(f"**Target Date:** {target}")
            st.write(f"**Priority:** {goal_priority}")

            updated_progress = st.slider(
                "Progress",
                0,
                100,
                saved_progress,
                key=f"goal_progress_{goal_id}"
            )

            st.progress(
                updated_progress / 100
            )

            update_column, delete_column = st.columns(2)

            with update_column:

                if st.button(
                    "Update Progress",
                    key=f"update_goal_{goal_id}",
                    width="stretch"
                ):

                    connection = get_connection()
                    cursor = connection.cursor()

                    cursor.execute("""
                        UPDATE student_goals
                        SET progress = ?
                        WHERE id = ? AND user_id = ?
                    """, (
                        updated_progress,
                        goal_id,
                        st.session_state.user_id
                    ))

                    connection.commit()
                    connection.close()

                    st.success(
                        "Goal progress updated."
                    )

            with delete_column:

                if st.button(
                    "Delete Goal",
                    key=f"delete_goal_{goal_id}",
                    width="stretch"
                ):

                    connection = get_connection()
                    cursor = connection.cursor()

                    cursor.execute("""
                        DELETE FROM student_goals
                        WHERE id = ? AND user_id = ?
                    """, (
                        goal_id,
                        st.session_state.user_id
                    ))

                    connection.commit()
                    connection.close()

                    st.rerun()


# ==========================================================
# AI STUDY MENTOR
# ==========================================================

elif menu == "🤖 AI Study Mentor":

    st.title("🤖 AI Study Mentor")

    st.write(
        "Ask questions about Mathematics, Science, English, "
        "Social Studies, examinations, study plans, careers and goals."
    )

    with st.expander("💡 Example questions you can ask", expanded=False):
        st.write("• Explain photosynthesis in simple words")
        st.write("• How can I improve in Mathematics?")
        st.write("• Create a study plan for my exams")
        st.write("• What career can I choose after studying Biology?")
        st.write("• Explain Newton's third law")
        st.write("• How can I improve my English communication?")

    def generate_mentor_response(message):

        clean_message = message.strip()
        user_message = clean_message.lower()

        if not clean_message:
            return (
                "Please type a question. For example: "
                "'Explain photosynthesis' or "
                "'Create a study plan for Mathematics'."
            )

        greeting_words = {
            "hi",
            "hello",
            "hey",
            "hii",
            "hlo",
            "good morning",
            "good evening"
        }

        if user_message in greeting_words:
            return (
                "Hello! 👋 I am your AI Study Mentor. "
                "You can ask me about school subjects, examinations, "
                "study planning, career choices or academic goals."
            )

        if "photosynthesis" in user_message:
            return (
                "Photosynthesis is the process by which green plants prepare "
                "their food. Plants use sunlight, water and carbon dioxide. "
                "Chlorophyll in the leaves captures sunlight. The plant then "
                "produces glucose as food and releases oxygen. "
                "Simple formula: carbon dioxide + water + sunlight → "
                "glucose + oxygen."
            )

        if (
            "newton" in user_message
            and (
                "third" in user_message
                or "3rd" in user_message
                or "law" in user_message
            )
        ):
            return (
                "Newton's third law states: For every action, there is an "
                "equal and opposite reaction. Example: When you jump, your "
                "feet push the ground downward, and the ground pushes your "
                "body upward."
            )

        if (
            "math" in user_message
            or "mathematics" in user_message
            or "algebra" in user_message
            or "geometry" in user_message
            or "percentage" in user_message
        ):
            return (
                "To improve Mathematics: 1) understand the formula, "
                "2) study one solved example, 3) solve five similar problems, "
                "4) write mistakes in a correction notebook, and "
                "5) revise for 30 minutes every day. Start with basic questions "
                "and then move to medium and hard questions."
            )

        if (
            "science" in user_message
            or "physics" in user_message
            or "chemistry" in user_message
            or "biology" in user_message
        ):
            if "biology" in user_message and "career" in user_message:
                return (
                    "Students interested in Biology can explore careers such "
                    "as Doctor, Dentist, Pharmacist, Nurse, Biotechnologist, "
                    "Microbiologist, Nutritionist and Environmental Scientist. "
                    "Focus strongly on Biology and Chemistry and compare the "
                    "eligibility requirements for each career."
                )

            return (
                "For Science, first understand the concept, then draw a diagram "
                "or connect it with a real-life example. Learn important terms, "
                "write the process in steps and finish with practice questions. "
                "Avoid memorising without understanding."
            )

        if (
            "english" in user_message
            or "grammar" in user_message
            or "communication" in user_message
            or "speaking" in user_message
        ):
            return (
                "Improve English with this daily routine: read for 15 minutes, "
                "learn five words, write one paragraph, speak for two minutes "
                "on one topic and check one grammar rule. Record your voice "
                "once a week to observe improvement."
            )

        if (
            "social" in user_message
            or "history" in user_message
            or "geography" in user_message
            or "civics" in user_message
        ):
            return (
                "For Social Studies: use timelines for History, maps for "
                "Geography and short point-wise notes for Civics. After every "
                "chapter, write five important facts and answer one long "
                "question without looking at the textbook."
            )

        if (
            "exam" in user_message
            or "timetable" in user_message
            or "study plan" in user_message
            or "study schedule" in user_message
        ):
            return (
                "Simple exam study plan: Morning—revise difficult concepts for "
                "45 minutes. Afternoon—complete homework and notes. "
                "Evening—solve practice questions for 60 minutes. "
                "Night—revise formulas and key points for 20 minutes. "
                "Use 40-minute study sessions with 10-minute breaks."
            )

        if "quiz" in user_message:
            return (
                "Open Subject Quiz, choose the subject, difficulty and number "
                "of questions, then click Generate New Quiz. After submitting, "
                "review each correct answer and explanation. Retake the quiz "
                "after revising weak topics."
            )

        if (
            "career" in user_message
            or "future" in user_message
            or "job" in user_message
        ):
            return (
                "To choose a career, compare four things: favourite subjects, "
                "interests, current strengths and the type of work you enjoy. "
                "Complete the Interest Assessment and Career Explorer, then "
                "study the required education and skills for your top three "
                "career options."
            )

        if (
            "goal" in user_message
            or "target" in user_message
        ):
            return (
                "Create a SMART goal: Specific, Measurable, Achievable, "
                "Relevant and Time-bound. Example: 'I will score at least 85% "
                "in Mathematics by solving 10 questions daily for 30 days.' "
                "Add it to Goal Tracker and update the progress weekly."
            )

        if (
            "stress" in user_message
            or "afraid" in user_message
            or "anxiety" in user_message
            or "nervous" in user_message
        ):
            return (
                "Take a short break, breathe slowly and divide the work into "
                "small tasks. Complete one easy task first to build confidence. "
                "Talk to a parent, teacher or trusted adult when exam stress "
                "feels difficult to manage."
            )

        return (
            "I understood your question, but I need a little more detail. "
            "Please mention the subject or goal clearly. For example: "
            "'Explain photosynthesis', 'How do I improve Mathematics?', "
            "or 'Create an exam study plan'."
        )

    if not st.session_state.mentor_messages:

        st.session_state.mentor_messages.append({
            "role": "assistant",
            "content": (
                "Hello! 👋 I am your AI Study Mentor. "
                "Ask me a school subject or study-related question."
            )
        })

    for chat_message in st.session_state.mentor_messages:

        with st.chat_message(chat_message["role"]):

            st.markdown(
                chat_message["content"]
            )

    mentor_prompt = st.chat_input(
        "Ask your study mentor..."
    )

    if mentor_prompt:

        st.session_state.mentor_messages.append({
            "role": "user",
            "content": mentor_prompt
        })

        mentor_response = generate_mentor_response(
            mentor_prompt
        )

        st.session_state.mentor_messages.append({
            "role": "assistant",
            "content": mentor_response
        })

        st.rerun()

    if st.button(
        "🗑️ Clear Mentor Chat",
        key="clear_mentor_chat"
    ):

        st.session_state.mentor_messages = []
        st.rerun()



# ==========================================================
# COLLEGE STUDENT REPORT
# ==========================================================

elif menu == "📑 College Student Report":

    st.title("📑 College Student Placement Report")
    st.write(
        "View your academic profile, preparation activity, placement readiness "
        "and personalised improvement plan in one professional report."
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            college_name,
            degree,
            branch,
            current_year,
            semester,
            university,
            city,
            phone,
            cgpa,
            backlogs,
            technical_skills,
            programming_languages,
            tools,
            certifications,
            projects,
            internships,
            career_goal,
            preferred_role,
            preferred_location,
            linkedin_pdf_path,
            github_url,
            portfolio_url,
            resume_path,
            placement_status,
            updated_at
        FROM college_profiles
        WHERE user_id = ?
    """, (st.session_state.user_id,))

    profile_row = cursor.fetchone()

    profile_columns = [
        "college_name",
        "degree",
        "branch",
        "current_year",
        "semester",
        "university",
        "city",
        "phone",
        "cgpa",
        "backlogs",
        "technical_skills",
        "programming_languages",
        "tools",
        "certifications",
        "projects",
        "internships",
        "career_goal",
        "preferred_role",
        "preferred_location",
        "linkedin_pdf_path",
        "github_url",
        "portfolio_url",
        "resume_path",
        "placement_status",
        "updated_at"
    ]

    profile = (
        dict(zip(profile_columns, profile_row))
        if profile_row
        else {}
    )

    cursor.execute("""
        SELECT
            AVG(score),
            COUNT(*),
            MAX(score)
        FROM coding_results
        WHERE user_id = ?
    """, (st.session_state.user_id,))

    coding_average, coding_count, coding_best = cursor.fetchone()
    coding_average = round(coding_average or 0)
    coding_count = int(coding_count or 0)
    coding_best = int(coding_best or 0)

    cursor.execute("""
        SELECT
            topic,
            difficulty,
            score,
            completed_at
        FROM coding_results
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 10
    """, (st.session_state.user_id,))

    coding_rows = cursor.fetchall()

    cursor.execute("""
        SELECT
            AVG(score),
            COUNT(*),
            MAX(score)
        FROM mock_interview_results
        WHERE user_id = ?
    """, (st.session_state.user_id,))

    interview_average, interview_count, interview_best = cursor.fetchone()
    interview_average = round(interview_average or 0)
    interview_count = int(interview_count or 0)
    interview_best = int(interview_best or 0)

    cursor.execute("""
        SELECT
            interview_type,
            score,
            feedback,
            completed_at
        FROM mock_interview_results
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 10
    """, (st.session_state.user_id,))

    interview_rows = cursor.fetchall()

    cursor.execute("""
        SELECT
            company,
            role,
            status,
            next_round,
            application_date
        FROM placement_applications
        WHERE user_id = ?
        ORDER BY id DESC
    """, (st.session_state.user_id,))

    application_rows = cursor.fetchall()
    application_count = len(application_rows)

    cursor.execute("""
        SELECT
            role,
            match_score,
            reasons,
            created_at
        FROM job_match_results
        WHERE user_id = ?
        ORDER BY match_score DESC, id DESC
        LIMIT 10
    """, (st.session_state.user_id,))

    job_match_rows = cursor.fetchall()
    job_match_count = len(job_match_rows)

    connection.close()

    report_scores = calculate_college_report_scores(
        profile,
        coding_average,
        interview_average
    )

    recommendations = create_college_report_recommendations(
        profile,
        report_scores,
        coding_count,
        interview_count,
        application_count
    )

    readiness_score = report_scores["Placement Readiness"]

    report_data = {
        "student_name": st.session_state.user_name,
        "student_email": st.session_state.user_email,
        "generated_at": datetime.now().strftime(
            "%d %B %Y, %I:%M %p"
        ),
        "profile": profile,
        "scores": report_scores,
        "coding_count": coding_count,
        "interview_count": interview_count,
        "application_count": application_count,
        "job_match_count": job_match_count,
        "applications": application_rows,
        "recommendations": recommendations
    }

    if not profile:
        st.warning(
            "Your College Profile is incomplete. Complete the profile to "
            "generate a more accurate placement report."
        )

        if st.button(
            "👤 Open College Profile",
            width="stretch",
            key="college_report_open_profile"
        ):
            open_college_page("👤 College Profile")
            st.rerun()

    st.markdown(
        f"""<div class="studio-hero">
<span class="studio-badge">Placement Progress Report</span>
<h1>{st.session_state.user_name}'s career readiness report.</h1>
<p>
This report combines your academic information, skills, coding practice,
mock interviews, projects, experience and placement applications.
</p>
</div>""",
        unsafe_allow_html=True
    )

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        st.metric(
            "Placement Readiness",
            f"{readiness_score}/100"
        )

    with metric2:
        st.metric(
            "Coding Average",
            f"{coding_average}%",
            f"Best: {coding_best}%"
        )

    with metric3:
        st.metric(
            "Interview Average",
            f"{interview_average}%",
            f"Best: {interview_best}%"
        )

    with metric4:
        st.metric(
            "Applications",
            application_count
        )

    st.progress(readiness_score / 100)

    if readiness_score >= 80:
        st.success(
            "Placement readiness: Strong. Continue targeted applications "
            "and advanced preparation."
        )
    elif readiness_score >= 60:
        st.info(
            "Placement readiness: Developing well. Focus on the weaker sections."
        )
    elif readiness_score >= 40:
        st.warning(
            "Placement readiness: Early preparation. Follow the action plan below."
        )
    else:
        st.error(
            "Placement readiness: Needs attention. Complete your profile and "
            "core preparation activities."
        )

    st.subheader("📊 Career Readiness Components")

    score_dataframe = pd.DataFrame({
        "Component": [
            "Resume",
            "Coding",
            "Projects",
            "Interview",
            "Experience"
        ],
        "Score": [
            report_scores["Resume"],
            report_scores["Coding"],
            report_scores["Projects"],
            report_scores["Interview"],
            report_scores["Experience"]
        ]
    })

    score_chart = px.bar(
        score_dataframe,
        x="Component",
        y="Score",
        text="Score",
        range_y=[0, 100],
        title="Placement Readiness by Component"
    )

    score_chart.update_layout(
        height=410,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(color="#111827"),
        yaxis_title="Score out of 100"
    )

    st.plotly_chart(
        score_chart,
        width="stretch"
    )

    (
        profile_tab,
        activity_tab,
        application_tab,
        recommendation_tab
    ) = st.tabs([
        "👤 Profile Summary",
        "📈 Preparation Activity",
        "🎯 Applications",
        "🚀 Recommendations"
    ])

    with profile_tab:

        left_profile, right_profile = st.columns(2)

        with left_profile:
            st.subheader("Academic Information")
            st.write(
                f"**College:** "
                f"{report_display_value(profile.get('college_name'))}"
            )
            st.write(
                f"**Degree:** "
                f"{report_display_value(profile.get('degree'))}"
            )
            st.write(
                f"**Branch:** "
                f"{report_display_value(profile.get('branch'))}"
            )
            st.write(
                f"**Current Year:** "
                f"{report_display_value(profile.get('current_year'))}"
            )
            st.write(
                f"**Semester:** "
                f"{report_display_value(profile.get('semester'))}"
            )
            st.write(
                f"**CGPA:** "
                f"{report_display_value(profile.get('cgpa'), '0')}"
            )
            st.write(
                f"**Backlogs:** "
                f"{report_display_value(profile.get('backlogs'), '0')}"
            )

        with right_profile:
            st.subheader("Career Information")
            st.write(
                f"**Career Goal:** "
                f"{report_display_value(profile.get('career_goal'))}"
            )
            st.write(
                f"**Preferred Role:** "
                f"{report_display_value(profile.get('preferred_role'))}"
            )
            st.write(
                f"**Preferred Location:** "
                f"{report_display_value(profile.get('preferred_location'))}"
            )
            st.write(
                f"**Placement Status:** "
                f"{report_display_value(profile.get('placement_status'))}"
            )
            st.write(
                f"**GitHub:** "
                f"{'Added' if profile.get('github_url') else 'Not added'}"
            )
            st.write(
                f"**LinkedIn PDF:** "
                f"{'Uploaded' if profile.get('linkedin_pdf_path') else 'Not uploaded'}"
            )
            st.write(
                f"**Resume:** "
                f"{'Available' if profile.get('resume_path') else 'Not available'}"
            )

        st.subheader("Skills and Experience")

        profile_table = pd.DataFrame({
            "Category": [
                "Technical Skills",
                "Programming Languages",
                "Tools",
                "Certifications",
                "Projects",
                "Internships"
            ],
            "Details": [
                report_list_value(profile.get("technical_skills")),
                report_list_value(profile.get("programming_languages")),
                report_list_value(profile.get("tools")),
                report_display_value(profile.get("certifications")),
                report_display_value(profile.get("projects")),
                report_display_value(profile.get("internships"))
            ]
        })

        st.dataframe(
            profile_table,
            width="stretch",
            hide_index=True
        )

    with activity_tab:

        activity_metric1, activity_metric2 = st.columns(2)

        with activity_metric1:
            st.metric(
                "Coding Assessments",
                coding_count
            )

        with activity_metric2:
            st.metric(
                "Mock Interviews",
                interview_count
            )

        if coding_rows:
            st.subheader("Recent Coding Results")

            coding_dataframe = pd.DataFrame(
                coding_rows,
                columns=[
                    "Topic",
                    "Difficulty",
                    "Score",
                    "Completed At"
                ]
            )

            st.dataframe(
                coding_dataframe,
                width="stretch",
                hide_index=True
            )
        else:
            st.info(
                "No coding assessment results are available yet."
            )

        if interview_rows:
            st.subheader("Recent Mock Interview Results")

            interview_dataframe = pd.DataFrame(
                interview_rows,
                columns=[
                    "Interview Type",
                    "Score",
                    "Feedback",
                    "Completed At"
                ]
            )

            st.dataframe(
                interview_dataframe,
                width="stretch",
                hide_index=True
            )
        else:
            st.info(
                "No mock interview results are available yet."
            )

    with application_tab:

        application_metric1, application_metric2 = st.columns(2)

        with application_metric1:
            st.metric(
                "Placement Applications",
                application_count
            )

        with application_metric2:
            st.metric(
                "Job Matches Generated",
                job_match_count
            )

        if application_rows:
            st.subheader("Placement Application History")

            application_dataframe = pd.DataFrame(
                application_rows,
                columns=[
                    "Company",
                    "Role",
                    "Status",
                    "Next Round",
                    "Application Date"
                ]
            )

            st.dataframe(
                application_dataframe,
                width="stretch",
                hide_index=True
            )
        else:
            st.info(
                "No placement applications have been tracked yet."
            )

        if job_match_rows:
            st.subheader("Top Job Match Results")

            job_match_dataframe = pd.DataFrame(
                job_match_rows,
                columns=[
                    "Role",
                    "Match Score",
                    "Reasons",
                    "Generated At"
                ]
            )

            st.dataframe(
                job_match_dataframe,
                width="stretch",
                hide_index=True
            )

    with recommendation_tab:

        st.subheader("Your Personalised Action Plan")

        for number, recommendation in enumerate(
            recommendations,
            start=1
        ):
            st.markdown(
                f"""<div class="studio-action">
<strong>{number}. {recommendation}</strong>
</div>""",
                unsafe_allow_html=True
            )

        st.subheader("30-Day Placement Focus")

        plan_dataframe = pd.DataFrame({
            "Week": [
                "Week 1",
                "Week 2",
                "Week 3",
                "Week 4"
            ],
            "Focus": [
                "Complete profile, resume and LinkedIn PDF",
                "Daily DSA practice and one coding assessment",
                "Improve projects, GitHub and technical skills",
                "Mock interviews, job matching and applications"
            ]
        })

        st.dataframe(
            plan_dataframe,
            width="stretch",
            hide_index=True
        )

    st.divider()
    st.subheader("📥 Download Report")

    report_text = build_college_report_text(report_data)

    safe_student_name = re.sub(
        r"[^A-Za-z0-9_-]+",
        "_",
        st.session_state.user_name.strip()
    ).strip("_") or "college_student"

    st.download_button(
        "📥 Download College Student Report",
        data=report_text,
        file_name=f"{safe_student_name}_placement_report.txt",
        mime="text/plain",
        width="stretch"
    )


# ==========================================================
# STUDENT REPORT
# ==========================================================

elif menu == "📄 My Report":

    st.title("📄 School Student Report")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            quiz_type,
            result,
            score,
            completed_at
        FROM quiz_results
        WHERE user_id = ?
        ORDER BY id DESC
    """, (st.session_state.user_id,))

    report_rows = cursor.fetchall()

    cursor.execute("""
        SELECT
            title,
            target_date,
            priority,
            progress
        FROM student_goals
        WHERE user_id = ?
    """, (st.session_state.user_id,))

    goal_rows = cursor.fetchall()
    connection.close()

    st.subheader("Assessment Results")

    if report_rows:

        assessment_report = pd.DataFrame(
            report_rows,
            columns=[
                "Assessment",
                "Result",
                "Score",
                "Completed At"
            ]
        )

        st.dataframe(
            assessment_report,
            width="stretch"
        )

        score_report = assessment_report.dropna(
            subset=["Score"]
        )

        if not score_report.empty:

            report_chart = px.bar(
                score_report,
                x="Assessment",
                y="Score",
                text="Score",
                title="Assessment Performance"
            )

            st.plotly_chart(
                report_chart,
                width="stretch"
            )

        st.download_button(
            "⬇ Download Assessment Report",
            data=assessment_report.to_csv(
                index=False
            ),
            file_name="school_student_report.csv",
            mime="text/csv",
            width="stretch"
        )

    else:

        st.info(
            "Complete quizzes and assessments to generate your report."
        )

    st.subheader("Goal Progress")

    if goal_rows:

        goals_report = pd.DataFrame(
            goal_rows,
            columns=[
                "Goal",
                "Target Date",
                "Priority",
                "Progress"
            ]
        )

        st.dataframe(
            goals_report,
            width="stretch"
        )

        goals_chart = px.bar(
            goals_report,
            x="Goal",
            y="Progress",
            text="Progress",
            title="Goal Progress"
        )

        goals_chart.update_yaxes(
            range=[0, 100]
        )

        st.plotly_chart(
            goals_chart,
            width="stretch"
        )

    else:

        st.info(
            "Add goals in the Goal Tracker."
        )


# ==========================================================
# WORKING PROFESSIONAL MODULE
# ==========================================================

elif menu == "👨‍💼 Professional Profile":
    profile = get_professional_profile(st.session_state.user_id)
    metrics = professional_metrics(profile)

    st.markdown(f"""
    <div class="studio-hero">
        <span class="studio-badge">TalentSphere Professional Profile</span>
        <h1>Build your next career chapter.</h1>
        <p>Keep your experience, technical strengths, leadership exposure and career goals in one professional workspace. Profile completion: <strong>{metrics['Profile Completion']}%</strong>.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("professional_profile_form"):
        st.markdown('<div class="studio-section-title">🏢 Professional Information</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            current_company = st.text_input("Current Company", value=profile.get("current_company", ""))
            current_role = st.text_input("Current Role", value=profile.get("current_role", ""))
            department = st.text_input("Department", value=profile.get("department", ""))
            total_experience = st.number_input("Total Experience (Years)", min_value=0.0, max_value=50.0, step=0.5, value=float(profile.get("total_experience") or 0))
            employment_type = st.selectbox("Employment Type", ["Full-time", "Part-time", "Contract", "Freelance", "Consultant", "Other"], index=["Full-time", "Part-time", "Contract", "Freelance", "Consultant", "Other"].index(profile.get("employment_type")) if profile.get("employment_type") in ["Full-time", "Part-time", "Contract", "Freelance", "Consultant", "Other"] else 0)
        with c2:
            current_location = st.text_input("Current Location", value=profile.get("current_location", ""))
            work_mode = st.selectbox("Work Mode", ["On-site", "Hybrid", "Remote"], index=["On-site", "Hybrid", "Remote"].index(profile.get("work_mode")) if profile.get("work_mode") in ["On-site", "Hybrid", "Remote"] else 1)
            phone = st.text_input("Phone Number", value=profile.get("phone", ""))
            highest_qualification = st.text_input("Highest Qualification", value=profile.get("highest_qualification", ""))
            notice_period = st.selectbox("Notice Period", ["Immediate", "15 Days", "30 Days", "60 Days", "90 Days", "More than 90 Days"], index=["Immediate", "15 Days", "30 Days", "60 Days", "90 Days", "More than 90 Days"].index(profile.get("notice_period")) if profile.get("notice_period") in ["Immediate", "15 Days", "30 Days", "60 Days", "90 Days", "More than 90 Days"] else 2)

        st.markdown('<div class="studio-section-title">💻 Technical Profile</div>', unsafe_allow_html=True)
        t1, t2 = st.columns(2)
        with t1:
            technical_skills = st.text_area("Technical Skills (comma separated)", value=profile.get("technical_skills", ""), height=100)
            programming_languages = st.text_input("Programming Languages", value=profile.get("programming_languages", ""))
            frameworks = st.text_input("Frameworks", value=profile.get("frameworks", ""))
            databases = st.text_input("Databases", value=profile.get("databases", ""))
        with t2:
            cloud_platforms = st.text_input("Cloud Platforms", value=profile.get("cloud_platforms", ""))
            devops_tools = st.text_input("DevOps Tools", value=profile.get("devops_tools", ""))
            certifications = st.text_area("Certifications", value=profile.get("certifications", ""), height=100)

        st.markdown('<div class="studio-section-title">🧭 Leadership & Career Goals</div>', unsafe_allow_html=True)
        l1, l2 = st.columns(2)
        with l1:
            leadership_experience = st.text_area("Leadership Experience", value=profile.get("leadership_experience", ""), height=110)
            team_size = st.number_input("Largest Team Size Led", min_value=0, max_value=500, value=int(profile.get("team_size") or 0))
            projects_led = st.number_input("Projects Led", min_value=0, max_value=200, value=int(profile.get("projects_led") or 0))
            mentoring_experience = st.text_area("Mentoring Experience", value=profile.get("mentoring_experience", ""), height=90)
            communication_options = ["Beginner", "Intermediate", "Advanced", "Expert"]
            communication_level = st.selectbox("Communication Level", communication_options, index=communication_options.index(profile.get("communication_level")) if profile.get("communication_level") in communication_options else 1)
        with l2:
            career_goal = st.text_area("Career Goal", value=profile.get("career_goal", ""), height=110)
            preferred_roles = st.text_input("Preferred Job Roles", value=profile.get("preferred_roles", ""))
            target_company = st.text_input("Target Company", value=profile.get("target_company", ""))
            preferred_location = st.text_input("Preferred Location", value=profile.get("preferred_location", ""))
            current_salary = st.number_input("Current Salary (LPA)", min_value=0.0, max_value=500.0, step=0.5, value=float(profile.get("current_salary") or 0))
            expected_salary = st.number_input("Expected Salary (LPA)", min_value=0.0, max_value=500.0, step=0.5, value=float(profile.get("expected_salary") or 0))

        st.markdown('<div class="studio-section-title">🔗 Professional Links</div>', unsafe_allow_html=True)
        p1, p2, p3 = st.columns(3)
        with p1:
            linkedin_url = st.text_input("LinkedIn URL", value=profile.get("linkedin_url", ""))
        with p2:
            github_url = st.text_input("GitHub URL", value=profile.get("github_url", ""))
        with p3:
            portfolio_url = st.text_input("Portfolio URL", value=profile.get("portfolio_url", ""))

        save_professional = st.form_submit_button("💾 Save Professional Profile", width="stretch")

    if save_professional:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO professional_profiles (
                user_id, current_company, current_role, department, total_experience,
                employment_type, current_location, work_mode, phone, highest_qualification,
                technical_skills, programming_languages, frameworks, databases,
                cloud_platforms, devops_tools, certifications, leadership_experience,
                team_size, projects_led, mentoring_experience, communication_level,
                career_goal, preferred_roles, target_company, preferred_location,
                current_salary, expected_salary, notice_period, linkedin_url,
                github_url, portfolio_url, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                current_company=excluded.current_company, current_role=excluded.current_role,
                department=excluded.department, total_experience=excluded.total_experience,
                employment_type=excluded.employment_type, current_location=excluded.current_location,
                work_mode=excluded.work_mode, phone=excluded.phone,
                highest_qualification=excluded.highest_qualification,
                technical_skills=excluded.technical_skills,
                programming_languages=excluded.programming_languages,
                frameworks=excluded.frameworks, databases=excluded.databases,
                cloud_platforms=excluded.cloud_platforms, devops_tools=excluded.devops_tools,
                certifications=excluded.certifications,
                leadership_experience=excluded.leadership_experience,
                team_size=excluded.team_size, projects_led=excluded.projects_led,
                mentoring_experience=excluded.mentoring_experience,
                communication_level=excluded.communication_level,
                career_goal=excluded.career_goal, preferred_roles=excluded.preferred_roles,
                target_company=excluded.target_company,
                preferred_location=excluded.preferred_location,
                current_salary=excluded.current_salary, expected_salary=excluded.expected_salary,
                notice_period=excluded.notice_period, linkedin_url=excluded.linkedin_url,
                github_url=excluded.github_url, portfolio_url=excluded.portfolio_url,
                updated_at=excluded.updated_at
        """, (
            st.session_state.user_id, current_company, current_role, department,
            total_experience, employment_type, current_location, work_mode, phone,
            highest_qualification, technical_skills, programming_languages,
            frameworks, databases, cloud_platforms, devops_tools, certifications,
            leadership_experience, team_size, projects_led, mentoring_experience,
            communication_level, career_goal, preferred_roles, target_company,
            preferred_location, current_salary, expected_salary, notice_period,
            linkedin_url, github_url, portfolio_url, datetime.now().isoformat()
        ))
        connection.commit()
        connection.close()
        st.success("Professional profile saved successfully.")
        st.rerun()

elif menu == "🏢 Professional Dashboard":
    profile = get_professional_profile(st.session_state.user_id)
    metrics = professional_metrics(profile)
    matches = professional_role_matches(profile, metrics)
    top_role, top_score = matches[0]
    current_role = profile.get("current_role") or "Complete your profile"
    experience = float(profile.get("total_experience") or 0)

    st.markdown(f"""
    <div class="studio-hero">
        <span class="studio-badge">TalentSphere Professional Dashboard</span>
        <h1>Accelerate your professional growth.</h1>
        <p>Welcome, {st.session_state.user_name}. Track promotion readiness, market-aligned skills, salary growth and next-level career opportunities in one workspace.</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    kpis = [
        ("💼", "Current Role", current_role, f"{experience:g} years experience"),
        ("📈", "Promotion Readiness", f"{metrics['Promotion Readiness']}%", "Technical + leadership + communication"),
        ("💰", "Salary Growth Potential", f"+{max(0, metrics['Salary Growth'])}%", "Based on your expected salary"),
        ("🎯", "Top Job Match", f"{top_score}%", top_role)
    ]
    for col, (icon, label, value, sub) in zip(cols, kpis):
        with col:
            st.markdown(f'<div class="studio-kpi"><div class="studio-kpi-icon">{icon}</div><div class="studio-kpi-label">{label}</div><div class="studio-kpi-value">{value}</div><div class="studio-kpi-sub">{sub}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="studio-section-title">🧠 Professional Growth Intelligence</div>', unsafe_allow_html=True)
    left, right = st.columns([1.55, 1])
    with left:
        skill_df = pd.DataFrame({"Skill": ["Backend Development", "System Design", "Cloud Computing", "DevOps", "Leadership"], "Score": [metrics["Backend Development"], metrics["System Design"], metrics["Cloud Computing"], metrics["DevOps"], metrics["Leadership"]]})
        chart = px.bar(skill_df, x="Score", y="Skill", orientation="h", text="Score", title="Current Skill Progress")
        chart.update_layout(height=390, xaxis_range=[0,100], margin=dict(l=10,r=10,t=55,b=10))
        st.plotly_chart(chart, width="stretch")
    with right:
        st.markdown('<div class="studio-panel"><h3>Recommended Next Steps</h3>', unsafe_allow_html=True)
        steps = ["Complete one cloud certification", "Build Docker and Kubernetes skills", "Study system design and microservices", "Lead or mentor on one visible project"]
        for i, step in enumerate(steps,1):
            st.markdown(f'<div class="studio-action"><strong>{i}. {step}</strong><br><span>High-impact professional growth activity</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif menu == "📚 Professional Learning & Skill Development":
    profile = get_professional_profile(st.session_state.user_id)

    st.markdown("""
    <style>
    .learn-hero{
        position:relative; overflow:hidden;
        padding:38px 40px; border-radius:28px;
        background:
          radial-gradient(circle at 88% 18%,rgba(255,255,255,.18),transparent 25%),
          linear-gradient(135deg,#2938d6 0%,#4f46e5 50%,#7c3aed 100%);
        box-shadow:0 22px 55px rgba(79,70,229,.24);
        margin-bottom:24px;
    }
    .learn-hero:after{
        content:""; position:absolute; right:-55px; bottom:-95px;
        width:260px; height:260px; border-radius:50%;
        border:38px solid rgba(255,255,255,.09);
    }
    .learn-badge{
        display:inline-flex; padding:7px 12px; border-radius:999px;
        background:rgba(255,255,255,.15); border:1px solid rgba(255,255,255,.24);
        color:#fff!important; font-size:11px; font-weight:800;
        text-transform:uppercase; letter-spacing:.08em;
    }
    .learn-hero h1{
        color:#fff!important; font-size:42px!important; line-height:1.08!important;
        letter-spacing:-.035em; margin:16px 0 10px!important; max-width:800px;
    }
    .learn-hero p{
        color:rgba(255,255,255,.9)!important; font-size:15px!important;
        line-height:1.7!important; margin:0!important; max-width:820px;
    }
    .learn-stat{
        background:#fff; border:1px solid #e5e9f2; border-radius:18px;
        padding:18px 20px; box-shadow:0 8px 24px rgba(15,23,42,.055);
        min-height:118px;
    }
    .learn-stat-label{
        color:#667085!important; font-size:11px; font-weight:800;
        text-transform:uppercase; letter-spacing:.07em; margin-bottom:8px;
    }
    .learn-stat-value{color:#101828!important; font-size:23px; font-weight:850; line-height:1.15}
    .learn-stat-sub{color:#98a2b3!important; font-size:11px; margin-top:7px}
    .learn-card{
        background:#fff; border:1px solid #e6eaf2; border-radius:20px;
        padding:20px; box-shadow:0 9px 26px rgba(15,23,42,.05); height:100%;
    }
    .learn-card h3{color:#101828!important; font-size:18px!important; margin:0 0 8px!important}
    .learn-card p{color:#667085!important; font-size:13px!important; line-height:1.6!important}
    .learn-icon{
        width:42px;height:42px;border-radius:13px;background:#eef2ff;
        display:flex;align-items:center;justify-content:center;font-size:20px;margin-bottom:12px;
    }
    .learn-chip{
        display:inline-block; padding:6px 10px; margin:4px 5px 4px 0;
        border-radius:999px; background:#f3f4f6; color:#475467!important;
        border:1px solid #eaecf0; font-size:11px; font-weight:700;
    }
    .learn-road{
        background:#fff; border:1px solid #e6eaf2; border-left:4px solid #4f46e5;
        border-radius:15px; padding:15px 17px; margin-bottom:10px;
        box-shadow:0 5px 16px rgba(15,23,42,.04);
    }
    .learn-road-week{color:#4f46e5!important;font-size:11px;font-weight:850;text-transform:uppercase;letter-spacing:.07em}
    .learn-road-title{color:#101828!important;font-weight:800;margin-top:4px}
    .learn-road-sub{color:#667085!important;font-size:12px;margin-top:4px}
    .learn-project{
        background:#fff;border:1px solid #e6eaf2;border-radius:18px;padding:19px;
        min-height:165px;box-shadow:0 8px 22px rgba(15,23,42,.05)
    }
    .learn-project-level{font-size:10px;font-weight:850;color:#4f46e5!important;text-transform:uppercase;letter-spacing:.08em}
    .learn-project-title{font-size:17px;font-weight:850;color:#101828!important;margin:8px 0}
    .learn-project-desc{font-size:12px;color:#667085!important;line-height:1.55}
    div[data-testid="stTabs"] [data-baseweb="tab-list"]{
        gap:6px!important; background:#fff!important; border:1px solid #e7eaf1!important;
        padding:6px!important; border-radius:15px!important; box-shadow:0 6px 18px rgba(15,23,42,.04);
    }
    div[data-testid="stTabs"] button{
        border-radius:10px!important; padding:10px 14px!important; font-weight:700!important;
    }
    div[data-testid="stExpander"]{
        background:#fff!important;border:1px solid #e6eaf2!important;
        border-radius:14px!important;box-shadow:0 5px 15px rgba(15,23,42,.035)!important;
        margin-bottom:9px!important;
    }
    </style>

    <div class="learn-hero">
        <span class="learn-badge">Professional Learning Academy</span>
        <h1>Build job-ready skills with a clear learning path.</h1>
        <p>Choose a professional track, study structured course material, follow a
        six-week roadmap, practise with hands-on tasks, build portfolio projects
        and take the final technical assessment only after learning.</p>
    </div>
    """, unsafe_allow_html=True)

    learning_tracks = {
        "Backend Development": {
            "icon": "⚙️",
            "summary": "Build secure, scalable server-side applications and production-ready REST APIs.",
            "roles": ["Backend Engineer", "API Developer", "Software Engineer", "Senior Backend Engineer"],
            "prerequisites": ["Programming fundamentals", "Basic Python or Java", "Basic SQL", "Git fundamentals"],
            "modules": [
                ("1. Backend Foundations", "Client-server architecture, HTTP/HTTPS, request-response lifecycle, REST principles, JSON, status codes and API design conventions."),
                ("2. Python for Backend", "Functions, OOP, modules, exceptions, virtual environments, type hints, package management and clean-code practices."),
                ("3. FastAPI & REST APIs", "Routes, path/query parameters, Pydantic models, validation, CRUD APIs, dependency injection, Swagger documentation and async endpoints."),
                ("4. Databases & SQL", "Relational modelling, primary/foreign keys, joins, indexes, transactions, SQLite/PostgreSQL integration and ORM concepts."),
                ("5. Authentication & Security", "Password hashing, JWT authentication, RBAC, CORS, input validation, secrets management and common API security practices."),
                ("6. Production Engineering", "Testing, logging, caching, Docker, environment configuration, CI/CD basics, monitoring and cloud deployment.")
            ],
            "roadmap": [
                ("Week 1", "HTTP, REST, JSON and Python refresh"),
                ("Week 2", "FastAPI fundamentals and CRUD APIs"),
                ("Week 3", "SQL, database design and persistence"),
                ("Week 4", "JWT, RBAC and API security"),
                ("Week 5", "Testing, Docker and deployment"),
                ("Week 6", "Build and document a production-style backend project")
            ],
            "practice": [
                "Create GET, POST, PUT and DELETE endpoints for a task manager.",
                "Design users, roles and tasks tables with relationships.",
                "Implement registration, login and JWT-protected routes.",
                "Add validation and meaningful HTTP status codes.",
                "Write API tests and containerise the application with Docker."
            ],
            "projects": [
                ("Starter", "Task Management REST API", "CRUD + SQLite + validation"),
                ("Intermediate", "Authentication & RBAC API", "JWT + roles + protected routes"),
                ("Portfolio", "E-commerce Backend", "Users + products + orders + payments mock + deployment")
            ],
            "quiz": [
                ("Which HTTP method is normally used to create a resource?", ["GET", "POST", "DELETE", "PATCH"], "POST"),
                ("Which status code represents a successful resource creation?", ["200", "201", "301", "404"], "201"),
                ("What is the main purpose of JWT?", ["Database indexing", "Authentication/authorization", "CSS styling", "File compression"], "Authentication/authorization"),
                ("Which SQL operation combines related rows from tables?", ["JOIN", "DROP", "VACUUM", "ALTER"], "JOIN"),
                ("Why is password hashing used?", ["To display passwords", "To avoid storing plain-text passwords", "To speed up HTML", "To create database IDs"], "To avoid storing plain-text passwords")
            ]
        },
        "System Design": {
            "icon": "🏗️",
            "summary": "Learn to design reliable, scalable and maintainable software systems.",
            "roles": ["Senior Software Engineer", "Backend Architect", "Solutions Architect", "Tech Lead"],
            "prerequisites": ["Backend fundamentals", "Databases", "HTTP/APIs", "Basic networking"],
            "modules": [
                ("1. Design Fundamentals", "Requirements, functional/non-functional requirements, latency, throughput, availability, reliability and scalability."),
                ("2. Architecture Patterns", "Monoliths, layered architecture, microservices, event-driven systems and service boundaries."),
                ("3. Data Layer", "SQL vs NoSQL, replication, partitioning, indexing, consistency, transactions and data modelling."),
                ("4. Scaling Components", "Load balancers, horizontal scaling, caching, CDNs, queues and asynchronous processing."),
                ("5. Reliability", "Retries, timeouts, circuit breakers, idempotency, redundancy, observability and disaster recovery."),
                ("6. Design Interviews", "Capacity estimation, API design, high-level design, bottleneck analysis and trade-off communication.")
            ],
            "roadmap": [
                ("Week 1", "Scalability, latency, availability and estimation"),
                ("Week 2", "Databases, caching and data consistency"),
                ("Week 3", "Load balancing, queues and distributed systems"),
                ("Week 4", "Microservices and reliability patterns"),
                ("Week 5", "Design URL shortener, chat and notification systems"),
                ("Week 6", "Complete two timed system-design case studies")
            ],
            "practice": [
                "Estimate traffic and storage for a URL shortener.",
                "Choose SQL or NoSQL for three different use cases and justify each.",
                "Draw a scalable architecture for a notification service.",
                "Identify single points of failure in a sample architecture.",
                "Explain caching and invalidation strategy for a read-heavy service."
            ],
            "projects": [
                ("Starter", "URL Shortener Design", "APIs + database + cache"),
                ("Intermediate", "Notification Platform", "Queue + workers + retries"),
                ("Portfolio", "Scalable E-commerce Architecture", "Services + cache + database + observability")
            ],
            "quiz": [
                ("What does a load balancer primarily do?", ["Encrypt a database", "Distribute traffic", "Compile code", "Store passwords"], "Distribute traffic"),
                ("Caching is most useful for what?", ["Reducing repeated expensive reads", "Increasing source-code size", "Replacing authentication", "Creating CSS"], "Reducing repeated expensive reads"),
                ("Horizontal scaling means:", ["Adding more machines/instances", "Adding RAM only", "Deleting servers", "Changing language"], "Adding more machines/instances"),
                ("A message queue helps with:", ["Asynchronous processing", "HTML layout", "Password display", "DNS registration"], "Asynchronous processing"),
                ("Replication mainly improves:", ["Availability/read capacity", "CSS quality", "Variable naming", "File extensions"], "Availability/read capacity")
            ]
        },
        "Cloud Computing": {
            "icon": "☁️",
            "summary": "Understand cloud infrastructure, deployment, storage, networking and scalable services.",
            "roles": ["Cloud Engineer", "Cloud Developer", "Solutions Architect", "Platform Engineer"],
            "prerequisites": ["Networking basics", "Linux basics", "Application fundamentals"],
            "modules": [
                ("1. Cloud Fundamentals", "IaaS, PaaS, SaaS, regions, availability zones, shared responsibility and cloud economics."),
                ("2. Compute & Storage", "Virtual machines, serverless, object/block storage, autoscaling and managed services."),
                ("3. Networking", "VPC/VNet concepts, subnets, routing, security groups, DNS and load balancing."),
                ("4. Identity & Security", "IAM, least privilege, secrets, encryption, logging and cloud security basics."),
                ("5. Databases & Reliability", "Managed SQL/NoSQL, backups, replication, high availability and disaster recovery."),
                ("6. Cloud Architecture", "Cost optimisation, monitoring, scalable architecture and deployment patterns.")
            ],
            "roadmap": [
                ("Week 1", "Cloud concepts, IAM and networking"),
                ("Week 2", "Compute, storage and databases"),
                ("Week 3", "Deploy an application to a cloud platform"),
                ("Week 4", "Monitoring, scaling, security and backups"),
                ("Week 5", "Serverless and managed services"),
                ("Week 6", "Architecture project + certification revision")
            ],
            "practice": [
                "Map a traditional web application to cloud services.",
                "Design a VPC with public and private application tiers.",
                "Create an IAM least-privilege permission plan.",
                "Plan backups and recovery for a production database.",
                "Compare VM, container and serverless deployment choices."
            ],
            "projects": [
                ("Starter", "Static Website Deployment", "Storage + CDN concepts"),
                ("Intermediate", "Cloud-hosted API", "Compute + database + IAM"),
                ("Portfolio", "Highly Available Web Architecture", "Load balancer + autoscaling + monitoring")
            ],
            "quiz": [
                ("IaaS provides:", ["Virtual infrastructure", "Only email", "Only source code", "Only databases"], "Virtual infrastructure"),
                ("IAM is used for:", ["Identity and access control", "Image editing", "SQL joins", "CSS"], "Identity and access control"),
                ("Autoscaling helps:", ["Adjust compute capacity to demand", "Rename files", "Write resumes", "Tokenize text"], "Adjust compute capacity to demand"),
                ("Object storage is suitable for:", ["Files and media objects", "CPU registers", "HTML variables", "Password hashing only"], "Files and media objects"),
                ("Availability zones help improve:", ["Resilience", "Font size", "Programming syntax", "Git usernames"], "Resilience")
            ]
        },
        "DevOps": {
            "icon": "♾️",
            "summary": "Automate software delivery using Git, CI/CD, containers, orchestration and observability.",
            "roles": ["DevOps Engineer", "Platform Engineer", "SRE", "Cloud DevOps Engineer"],
            "prerequisites": ["Linux basics", "Git", "Application deployment basics", "Networking basics"],
            "modules": [
                ("1. DevOps Foundations", "DevOps culture, SDLC, Git workflows, branching and release practices."),
                ("2. Linux & Automation", "Shell basics, processes, permissions, environment variables and scripting."),
                ("3. CI/CD", "Build-test-deploy pipelines, quality gates, artifacts and deployment strategies."),
                ("4. Docker", "Images, containers, Dockerfiles, volumes, networks and Compose."),
                ("5. Kubernetes", "Pods, deployments, services, config, secrets, scaling and rolling updates."),
                ("6. Observability", "Logs, metrics, alerts, monitoring, incident response and reliability basics.")
            ],
            "roadmap": [
                ("Week 1", "Git, Linux and shell automation"),
                ("Week 2", "CI pipeline for an existing application"),
                ("Week 3", "Docker and Compose"),
                ("Week 4", "Kubernetes fundamentals"),
                ("Week 5", "Monitoring, logging and deployment strategies"),
                ("Week 6", "End-to-end automated deployment project")
            ],
            "practice": [
                "Create a clean Git branching workflow.",
                "Write a Dockerfile for a Python web application.",
                "Create a CI workflow that runs tests automatically.",
                "Deploy a container using Kubernetes deployment and service concepts.",
                "Define monitoring signals for a production API."
            ],
            "projects": [
                ("Starter", "Dockerised Web App", "Dockerfile + Compose"),
                ("Intermediate", "CI/CD Pipeline", "Test + build + deployment workflow"),
                ("Portfolio", "Kubernetes Deployment", "App + service + scaling + observability plan")
            ],
            "quiz": [
                ("A Docker image is:", ["A container template", "A database row", "A cloud region", "A password"], "A container template"),
                ("CI primarily means:", ["Continuous Integration", "Cloud Internet", "Code Inspection only", "Container Instance"], "Continuous Integration"),
                ("Kubernetes is mainly used for:", ["Container orchestration", "PDF extraction", "Resume writing", "SQL syntax"], "Container orchestration"),
                ("A CI/CD pipeline should commonly run:", ["Automated tests", "Only screenshots", "Manual passwords", "Nothing"], "Automated tests"),
                ("Observability commonly uses:", ["Logs, metrics and traces", "Only CSS", "Only Git branches", "Only PDFs"], "Logs, metrics and traces")
            ]
        },
        "Leadership": {
            "icon": "🧭",
            "summary": "Develop team leadership, mentoring, ownership, decision-making and delivery skills.",
            "roles": ["Tech Lead", "Engineering Lead", "Team Lead", "Engineering Manager"],
            "prerequisites": ["Professional experience", "Team collaboration", "Basic communication skills"],
            "modules": [
                ("1. Leadership Mindset", "Ownership, accountability, trust, influence and leading without authority."),
                ("2. Team Coordination", "Planning, delegation, prioritisation, meetings and delivery tracking."),
                ("3. Mentoring & Feedback", "Coaching, constructive feedback, one-to-ones and knowledge sharing."),
                ("4. Decision Making", "Trade-offs, risk analysis, data-informed decisions and escalation."),
                ("5. Conflict Resolution", "Active listening, difficult conversations, negotiation and psychological safety."),
                ("6. Technical Leadership", "Architecture influence, code quality, project ownership and stakeholder alignment.")
            ],
            "roadmap": [
                ("Week 1", "Ownership and communication habits"),
                ("Week 2", "Delegation and planning"),
                ("Week 3", "Mentor one colleague"),
                ("Week 4", "Lead a meeting or technical discussion"),
                ("Week 5", "Own a measurable delivery improvement"),
                ("Week 6", "Document impact and request structured feedback")
            ],
            "practice": [
                "Write a delegation plan for a small project.",
                "Prepare constructive feedback using situation-behaviour-impact.",
                "Create a decision record for a technical trade-off.",
                "Plan a one-to-one mentoring conversation.",
                "Write a concise project status update for stakeholders."
            ],
            "projects": [
                ("Starter", "Team Improvement Plan", "Goals + responsibilities + communication"),
                ("Intermediate", "Mentoring Sprint", "Four-week mentoring and feedback plan"),
                ("Portfolio", "Technical Initiative Leadership", "Proposal + execution + measurable impact")
            ],
            "quiz": [
                ("Effective delegation should include:", ["Clear outcome and ownership", "No context", "No deadline ever", "Only criticism"], "Clear outcome and ownership"),
                ("Constructive feedback should be:", ["Specific and actionable", "Personal and vague", "Publicly embarrassing", "Unrelated"], "Specific and actionable"),
                ("A strong leader handles conflict by:", ["Listening and addressing the issue", "Ignoring everyone", "Blaming immediately", "Avoiding all discussion"], "Listening and addressing the issue"),
                ("Mentoring primarily helps:", ["Develop another person's capability", "Hide knowledge", "Avoid teamwork", "Remove documentation"], "Develop another person's capability"),
                ("Ownership means:", ["Taking responsibility for outcomes", "Doing every task alone", "Avoiding decisions", "Never asking for help"], "Taking responsibility for outcomes")
            ]
        },
        "Communication": {
            "icon": "💬",
            "summary": "Communicate technical ideas clearly across teams, interviews, meetings and stakeholders.",
            "roles": ["All Professional Roles", "Tech Lead", "Consultant", "Engineering Manager"],
            "prerequisites": ["No technical prerequisite"],
            "modules": [
                ("1. Professional Communication", "Clarity, structure, audience awareness, tone and concise writing."),
                ("2. Technical Explanation", "Explaining architecture, code, incidents and trade-offs to technical and non-technical audiences."),
                ("3. Meetings & Collaboration", "Agendas, active listening, questions, notes, decisions and action items."),
                ("4. Presentations", "Story structure, slide discipline, demonstrations, confidence and handling questions."),
                ("5. Written Communication", "Professional email, status updates, documentation and asynchronous communication."),
                ("6. Interview Communication", "STAR method, project explanation, behavioural answers and technical reasoning.")
            ],
            "roadmap": [
                ("Week 1", "Clear writing and concise status updates"),
                ("Week 2", "Technical explanations"),
                ("Week 3", "Meeting and listening skills"),
                ("Week 4", "Five-minute professional presentation"),
                ("Week 5", "Behavioural interview practice"),
                ("Week 6", "Record, review and improve a complete project presentation")
            ],
            "practice": [
                "Summarise a technical issue in five sentences for a manager.",
                "Explain an API to a non-technical stakeholder.",
                "Write meeting notes with decisions and owners.",
                "Prepare a two-minute STAR answer.",
                "Record a five-minute project explanation and review clarity."
            ],
            "projects": [
                ("Starter", "Professional Update Pack", "Email + status update + meeting notes"),
                ("Intermediate", "Technical Presentation", "5–7 minute architecture explanation"),
                ("Portfolio", "Interview Communication Pack", "Introduction + project pitch + STAR stories")
            ],
            "quiz": [
                ("The STAR method stands for:", ["Situation, Task, Action, Result", "System, Test, API, REST", "Skill, Tool, Aim, Review", "None"], "Situation, Task, Action, Result"),
                ("A good status update should be:", ["Concise and action-oriented", "Vague", "Extremely unrelated", "Without outcomes"], "Concise and action-oriented"),
                ("Active listening includes:", ["Clarifying and confirming understanding", "Interrupting constantly", "Ignoring questions", "Changing topic"], "Clarifying and confirming understanding"),
                ("Technical communication should change based on:", ["Audience", "Random choice", "File size", "Screen colour"], "Audience"),
                ("Good meeting notes include:", ["Decisions and action owners", "Only greetings", "Passwords", "No next steps"], "Decisions and action owners")
            ]
        }
    }

    track_names = list(learning_tracks.keys())
    current_track = st.session_state.get("professional_learning_track", track_names[0])
    if current_track not in track_names:
        current_track = track_names[0]

    selected_track = st.selectbox(
        "Choose your learning track",
        track_names,
        index=track_names.index(current_track)
    )
    st.session_state.professional_learning_track = selected_track
    course = learning_tracks[selected_track]

    # Premium course header
    stat_cols = st.columns(4)
    stats = [
        ("Selected Track", selected_track, "Professional learning path"),
        ("Course Modules", str(len(course["modules"])), "Structured lessons"),
        ("Roadmap", "6 Weeks", "Step-by-step learning"),
        ("Final Quiz", f"{len(course['quiz'])} Qs", "Taken after learning"),
    ]
    for col, (label, value, sub) in zip(stat_cols, stats):
        with col:
            st.markdown(
                f'<div class="learn-stat"><div class="learn-stat-label">{label}</div>'
                f'<div class="learn-stat-value">{value}</div>'
                f'<div class="learn-stat-sub">{sub}</div></div>',
                unsafe_allow_html=True
            )

    st.write("")
    st.markdown(
        f'<div class="learn-card"><div class="learn-icon">{course["icon"]}</div>'
        f'<h3>{selected_track}</h3><p>{course["summary"]}</p>'
        f'<span class="learn-chip">Industry focused</span>'
        f'<span class="learn-chip">6-week roadmap</span>'
        f'<span class="learn-chip">Projects included</span>'
        f'<span class="learn-chip">Final assessment</span></div>',
        unsafe_allow_html=True
    )

    overview_tab, roadmap_tab, modules_tab, projects_tab, practice_tab, quiz_tab = st.tabs([
        "Overview", "Roadmap", "Modules", "Projects", "Practice", "Quiz & Results"
    ])

    with overview_tab:
        st.markdown("### About this learning track")
        a, b = st.columns(2)
        with a:
            roles_html = "".join(f'<span class="learn-chip">{role}</span>' for role in course["roles"])
            st.markdown(
                '<div class="learn-card"><div class="learn-icon">🎯</div>'
                '<h3>Career outcomes</h3><p>This learning path prepares you for roles such as:</p>'
                f'{roles_html}</div>',
                unsafe_allow_html=True
            )
        with b:
            prereq_html = "".join(f'<span class="learn-chip">{item}</span>' for item in course["prerequisites"])
            st.markdown(
                '<div class="learn-card"><div class="learn-icon">✅</div>'
                '<h3>Recommended prerequisites</h3><p>Start comfortably if you already know:</p>'
                f'{prereq_html}</div>',
                unsafe_allow_html=True
            )

        st.write("")
        st.info(
            "Recommended sequence: Overview → Roadmap → Modules → Practice → "
            "Projects → Quiz. The assessment is intended to validate what you learned."
        )

    with roadmap_tab:
        st.markdown(f"### {selected_track} learning roadmap")
        st.caption("Complete one milestone each week and build practical evidence as you progress.")
        for index, (week, focus) in enumerate(course["roadmap"], 1):
            st.markdown(
                f'<div class="learn-road"><div class="learn-road-week">Phase {index} · {week}</div>'
                f'<div class="learn-road-title">{focus}</div>'
                f'<div class="learn-road-sub">Study the related module, complete practice and save your notes/code.</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    with modules_tab:
        st.markdown("### Structured course material")
        st.caption("Open each module in order. Every module includes the core concept and an application-focused learning outcome.")
        for idx, (title, material) in enumerate(course["modules"], 1):
            with st.expander(title, expanded=(idx == 1)):
                st.markdown(f"**What you will learn**")
                st.write(material)
                st.markdown("**Learning outcome**")
                st.write(
                    "Explain the concept clearly, identify when it is used in industry, "
                    "and apply it in a practical task or project."
                )
                st.markdown("**Completion checklist**")
                st.checkbox("I reviewed the concepts", key=f"pro_module_read_{selected_track}_{idx}")
                st.checkbox("I completed a small practice task", key=f"pro_module_practice_{selected_track}_{idx}")

    with projects_tab:
        st.markdown("### Project-based learning")
        st.caption("Projects turn the course into portfolio evidence. Progress from starter to portfolio level.")
        cols = st.columns(3)
        for col, (level, project, build) in zip(cols, course["projects"]):
            with col:
                st.markdown(
                    f'<div class="learn-project"><div class="learn-project-level">{level}</div>'
                    f'<div class="learn-project-title">{project}</div>'
                    f'<div class="learn-project-desc">{build}</div>'
                    f'<div style="margin-top:14px"><span class="learn-chip">Portfolio evidence</span></div></div>',
                    unsafe_allow_html=True
                )
        st.write("")
        st.success(
            "Portfolio target: complete at least the Intermediate project and publish "
            "source code, README, screenshots/architecture and a short project explanation."
        )

    with practice_tab:
        st.markdown("### Hands-on practice")
        st.caption("Use these tasks to verify that you can apply the concepts before taking the final quiz.")
        for number, exercise in enumerate(course["practice"], 1):
            left, right = st.columns([0.92, 0.08])
            with left:
                st.markdown(
                    f'<div class="learn-road"><div class="learn-road-week">Practice {number}</div>'
                    f'<div class="learn-road-title">{exercise}</div>'
                    f'<div class="learn-road-sub">Complete this task independently and keep your output as evidence.</div></div>',
                    unsafe_allow_html=True
                )
            with right:
                st.checkbox("Done", key=f"pro_practice_done_{selected_track}_{number}")

    with quiz_tab:
        st.markdown(f"### Final {selected_track} assessment")
        st.caption("Attempt this only after completing the modules, practice tasks and at least one project.")

        result = st.session_state.get("professional_learning_quiz_result")

        quiz_left, quiz_right = st.columns([2.15, 0.85])
        with quiz_left:
            with st.form(f"professional_learning_quiz_{selected_track}"):
                answers = []
                for i, (question, options, correct) in enumerate(course["quiz"], 1):
                    st.markdown(f"**Question {i} of {len(course['quiz'])}**")
                    answer = st.radio(
                        question,
                        options,
                        index=None,
                        key=f"learning_{selected_track}_{i}"
                    )
                    answers.append(answer)
                submitted = st.form_submit_button(
                    "Submit Final Assessment",
                    width="stretch"
                )

            if submitted:
                unanswered = sum(answer is None for answer in answers)
                if unanswered:
                    st.error(f"Please answer all questions. {unanswered} question(s) are incomplete.")
                else:
                    correct_count = sum(
                        answer == question_data[2]
                        for answer, question_data in zip(answers, course["quiz"])
                    )
                    score = round(correct_count / len(course["quiz"]) * 100)
                    if score >= 80:
                        level = "Industry Ready"
                    elif score >= 60:
                        level = "Intermediate"
                    elif score >= 40:
                        level = "Developing"
                    else:
                        level = "Beginner"

                    st.session_state.professional_learning_quiz_result = {
                        "track": selected_track,
                        "score": score,
                        "level": level,
                        "correct": correct_count,
                        "total": len(course["quiz"])
                    }
                    st.rerun()

        with quiz_right:
            result = st.session_state.get("professional_learning_quiz_result")
            if result and result.get("track") == selected_track:
                st.markdown(
                    f'<div class="learn-card" style="text-align:center">'
                    f'<div class="learn-icon" style="margin:0 auto 14px">🏆</div>'
                    f'<h3>Your result</h3>'
                    f'<div style="font-size:42px;font-weight:900;color:#4f46e5">{result["score"]}%</div>'
                    f'<p>{result["correct"]}/{result["total"]} correct answers</p>'
                    f'<span class="learn-chip">{result["level"]}</span></div>',
                    unsafe_allow_html=True
                )
                st.progress(result["score"] / 100)
                if result["score"] >= 80:
                    st.success("Strong performance. Move to an advanced project or next track.")
                elif result["score"] >= 60:
                    st.info("Good foundation. Review weak concepts and strengthen your project.")
                else:
                    st.warning("Review the modules and practice tasks before retaking the quiz.")

                report = f"""TALENTSPHERE ELEVATE - PROFESSIONAL LEARNING REPORT
Learner: {st.session_state.user_name}
Learning Track: {selected_track}
Assessment Score: {result['score']}%
Skill Level: {result['level']}
Correct Answers: {result['correct']}/{result['total']}

ROADMAP
""" + "\n".join(f"{week}: {focus}" for week, focus in course["roadmap"])

                st.download_button(
                    "Download Learning Report",
                    report,
                    file_name=f"{selected_track.lower().replace(' ', '_')}_learning_report.txt",
                    mime="text/plain",
                    width="stretch"
                )
            else:
                st.markdown(
                    '<div class="learn-card" style="text-align:center">'
                    '<div class="learn-icon" style="margin:0 auto 14px">📝</div>'
                    '<h3>Assessment status</h3>'
                    '<p>No result yet. Complete the learning material and submit the final quiz.</p>'
                    '<span class="learn-chip">Not attempted</span></div>',
                    unsafe_allow_html=True
                )

elif menu == "🚀 Career Transition Suggestions":
    profile = get_professional_profile(st.session_state.user_id)
    metrics = professional_metrics(profile)
    matches = professional_role_matches(profile, metrics)
    st.title("🚀 AI Career Transition Suggestions")
    st.info(f"Current role: **{profile.get('current_role') or 'Not provided'}**")
    df = pd.DataFrame(matches, columns=["Suggested Next Role", "Match %"])
    st.dataframe(df, width="stretch", hide_index=True)
    fig = px.bar(df, x="Suggested Next Role", y="Match %", text="Match %", title="Career Path Match")
    fig.update_yaxes(range=[0,100])
    st.plotly_chart(fig, width="stretch")

elif menu == "📈 Promotion Readiness":
    profile = get_professional_profile(st.session_state.user_id)
    metrics = professional_metrics(profile)
    st.title("📈 Promotion Readiness Analysis")
    cols = st.columns(4)
    values = [("Promotion", metrics["Promotion Readiness"]), ("Technical", metrics["Technical Readiness"]), ("Leadership", metrics["Leadership"]), ("Communication", metrics["Communication"])]
    for col,(label,value) in zip(cols,values):
        with col: st.metric(label, f"{value}%")
    for label,value in values:
        st.write(f"**{label} Readiness**")
        st.progress(value/100)
    if metrics["Promotion Readiness"] >= 80:
        st.success("You show strong promotion readiness. Prepare a documented impact summary and discuss the next level with your manager.")
    elif metrics["Promotion Readiness"] >= 65:
        st.warning("You are progressing well. Increase leadership visibility and strengthen one high-demand technical area.")
    else:
        st.info("Focus on stronger technical depth, project ownership, communication and mentoring before seeking promotion.")

elif menu == "💰 Career & Salary Insights":
    profile = get_professional_profile(st.session_state.user_id)
    metrics = professional_metrics(profile)
    matches = professional_role_matches(profile, metrics)

    current_role = (profile.get("current_role") or "Current role not added").strip()
    experience = float(profile.get("total_experience") or 0)
    current_salary = float(profile.get("current_salary") or 0)

    target_role = (
        matches[0][0]
        if matches
        else (profile.get("preferred_roles") or "Target role not added")
    )
    role_match = matches[0][1] if matches else 0

    # Skill weights used to calculate professional salary readiness.
    skill_weights = {
        "Backend Development": 0.22,
        "System Design": 0.20,
        "Cloud Computing": 0.16,
        "DevOps": 0.14,
        "Leadership": 0.14,
        "Communication": 0.14,
    }

    skill_scores = {
        skill: int(metrics.get(skill, 0))
        for skill in skill_weights
    }

    weighted_skill_score = round(
        sum(skill_scores[skill] * weight for skill, weight in skill_weights.items())
    )

    # Experience score and career stage.
    if experience < 1:
        experience_score = 35
        experience_level = "Entry Level"
    elif experience < 3:
        experience_score = 55
        experience_level = "Early Career"
    elif experience < 5:
        experience_score = 72
        experience_level = "Mid Level"
    elif experience < 8:
        experience_score = 86
        experience_level = "Senior Level"
    else:
        experience_score = 95
        experience_level = "Lead / Expert Level"

    # Salary readiness = skills + experience + target-role fit.
    salary_readiness = round(
        weighted_skill_score * 0.55
        + experience_score * 0.30
        + role_match * 0.15
    )
    salary_readiness = max(0, min(100, salary_readiness))

    if salary_readiness >= 85:
        readiness_label = "Strong Salary Growth Potential"
    elif salary_readiness >= 70:
        readiness_label = "Good Salary Growth Potential"
    elif salary_readiness >= 55:
        readiness_label = "Moderate Salary Growth Potential"
    else:
        readiness_label = "Skill Development Required"

    ranked_skills = sorted(skill_scores.items(), key=lambda item: item[1])
    weakest_skills = ranked_skills[:3]
    strongest_skills = sorted(
        skill_scores.items(),
        key=lambda item: item[1],
        reverse=True
    )[:3]

    # Profile-based growth estimate. This is deliberately labeled as an estimate,
    # not as live market salary data.
    if salary_readiness >= 85:
        base_growth = 35
    elif salary_readiness >= 70:
        base_growth = 25
    elif salary_readiness >= 55:
        base_growth = 15
    else:
        base_growth = 8

    if experience < 2:
        experience_bonus = 8
    elif experience < 5:
        experience_bonus = 6
    elif experience < 8:
        experience_bonus = 4
    else:
        experience_bonus = 2

    lower_growth = max(5, base_growth - 5)
    upper_growth = min(55, base_growth + experience_bonus)

    estimated_low_salary = (
        round(current_salary * (1 + lower_growth / 100), 1)
        if current_salary > 0 else 0
    )
    estimated_high_salary = (
        round(current_salary * (1 + upper_growth / 100), 1)
        if current_salary > 0 else 0
    )

    st.markdown("""
    <style>
    .salary-hero{
        position:relative;
        overflow:hidden;
        padding:30px 34px;
        border-radius:24px;
        background:
            radial-gradient(circle at 89% 16%, rgba(255,255,255,.18), transparent 25%),
            linear-gradient(135deg,#2456e8 0%,#4f46e5 52%,#7c3aed 100%);
        box-shadow:0 18px 45px rgba(79,70,229,.20);
        margin-bottom:22px;
    }
    .salary-hero h1{
        color:white!important;
        margin:13px 0 8px!important;
        font-size:clamp(30px,3.2vw,42px)!important;
        line-height:1.08!important;
    }
    .salary-hero p{
        color:rgba(255,255,255,.90)!important;
        font-size:14px!important;
        line-height:1.65!important;
        max-width:840px;
        margin:0!important;
    }
    .salary-badge{
        display:inline-flex;
        padding:7px 11px;
        border-radius:999px;
        background:rgba(255,255,255,.15);
        border:1px solid rgba(255,255,255,.25);
        color:#fff!important;
        font-size:11px;
        font-weight:800;
        letter-spacing:.07em;
        text-transform:uppercase;
    }
    .salary-card{
        background:#fff;
        border:1px solid #E5EAF2;
        border-radius:18px;
        padding:20px;
        box-shadow:0 8px 24px rgba(15,23,42,.05);
        height:100%;
    }
    .salary-card h3{
        color:#0F172A!important;
        margin:0 0 12px!important;
        font-size:18px!important;
    }
    .salary-item{
        background:#F8FAFC;
        border:1px solid #E5EAF2;
        border-left:4px solid #2563EB;
        border-radius:12px;
        padding:12px 14px;
        margin-bottom:9px;
    }
    .salary-item strong{color:#0F172A!important}
    .salary-item span{color:#64748B!important;font-size:12px}
    .salary-chip{
        display:inline-block;
        padding:6px 10px;
        border-radius:999px;
        background:#EEF2FF;
        border:1px solid #E0E7FF;
        color:#3730A3!important;
        font-size:11px;
        font-weight:750;
        margin:3px 4px 3px 0;
    }
    </style>

    <div class="salary-hero">
        <span class="salary-badge">Skill & Experience Salary Intelligence</span>
        <h1>See how your skills and experience influence salary growth.</h1>
        <p>
            TalentSphere combines your technical skills, professional experience and
            target-role match to estimate salary readiness, identify high-value strengths
            and show which skill gaps may be limiting your next career move.
        </p>
    </div>
    """, unsafe_allow_html=True)

    top1, top2, top3, top4 = st.columns(4)
    top1.metric("Experience", f"{experience:g} years", experience_level)
    top2.metric("Skill Readiness", f"{weighted_skill_score}%")
    top3.metric("Target Role Match", f"{role_match}%")
    top4.metric("Salary Readiness", f"{salary_readiness}%")

    st.markdown("### 💰 Salary Growth Readiness")

    left, right = st.columns(2)

    with left:
        st.markdown(f"""
        <div class="salary-card">
            <h3>Professional Profile Analysis</h3>
            <div class="salary-item"><strong>Current Role</strong><br><span>{current_role}</span></div>
            <div class="salary-item"><strong>Target Role</strong><br><span>{target_role}</span></div>
            <div class="salary-item"><strong>Career Stage</strong><br><span>{experience_level}</span></div>
            <div class="salary-item"><strong>Growth Potential</strong><br><span>{readiness_label}</span></div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        if current_salary > 0:
            salary_range = f"₹{estimated_low_salary:g} – ₹{estimated_high_salary:g} LPA"
            growth_range = f"{lower_growth}% – {upper_growth}% estimated growth"
        else:
            salary_range = "Add current salary in Professional Profile"
            growth_range = "Complete your salary field to calculate"

        st.markdown(f"""
        <div class="salary-card">
            <h3>Profile-Based Salary Estimate</h3>
            <div class="salary-item"><strong>Current Salary</strong><br>
                <span>{f"₹{current_salary:g} LPA" if current_salary else "Not added"}</span>
            </div>
            <div class="salary-item"><strong>Estimated Next Range</strong><br>
                <span>{salary_range}</span>
            </div>
            <div class="salary-item"><strong>Estimated Growth</strong><br>
                <span>{growth_range}</span>
            </div>
            <div class="salary-item"><strong>Note</strong><br>
                <span>This is based on profile readiness, not live market salary data.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 📊 Skill Impact on Salary Potential")

    impact_rows = []
    for skill, score in sorted(
        skill_scores.items(),
        key=lambda item: item[1],
        reverse=True
    ):
        if score >= 80:
            impact = "Strong Positive"
            action = "Maintain and demonstrate through projects/work impact"
        elif score >= 65:
            impact = "Positive"
            action = "Strengthen to advanced level"
        elif score >= 50:
            impact = "Moderate"
            action = "Build more hands-on evidence"
        else:
            impact = "Growth Limiter"
            action = "High-priority learning area"

        impact_rows.append({
            "Skill": skill,
            "Readiness": f"{score}%",
            "Salary Impact": impact,
            "Recommended Action": action
        })

    st.dataframe(
        pd.DataFrame(impact_rows),
        width="stretch",
        hide_index=True
    )

    st.markdown("### 🎯 Strongest Skills vs Growth Gaps")

    strong_col, weak_col = st.columns(2)

    with strong_col:
        st.markdown("#### ✅ Salary-Supporting Strengths")
        for skill, score in strongest_skills:
            st.markdown(
                f'<div class="salary-item"><strong>{skill}</strong><br>'
                f'<span>{score}% readiness · strengthens your salary profile</span></div>',
                unsafe_allow_html=True
            )

    with weak_col:
        st.markdown("#### ⚠️ Skills Limiting Growth")
        for skill, score in weakest_skills:
            st.markdown(
                f'<div class="salary-item"><strong>{skill}</strong><br>'
                f'<span>{score}% readiness · improve this for stronger opportunities</span></div>',
                unsafe_allow_html=True
            )

    st.markdown("### 🧭 Experience-Based Career Strategy")

    if experience < 2:
        career_actions = [
            "Strengthen core technical fundamentals.",
            "Complete at least two practical portfolio projects.",
            "Focus on role-specific interview preparation.",
            "Build evidence of real-world problem solving."
        ]
    elif experience < 5:
        career_actions = [
            "Build deeper system design and production skills.",
            "Own features or modules end-to-end.",
            "Add cloud and deployment experience.",
            "Document measurable impact from your work."
        ]
    elif experience < 8:
        career_actions = [
            "Strengthen architecture and technical leadership.",
            "Lead larger initiatives and mentor team members.",
            "Improve stakeholder communication and delivery ownership.",
            "Target senior or lead-level responsibilities."
        ]
    else:
        career_actions = [
            "Focus on architecture, strategy and leadership impact.",
            "Demonstrate organisation-level technical ownership.",
            "Mentor engineers and influence engineering standards.",
            "Target lead, architect or engineering-management paths."
        ]

    for index, action in enumerate(career_actions, 1):
        st.markdown(
            f'<div class="salary-item"><strong>Step {index}</strong><br>'
            f'<span>{action}</span></div>',
            unsafe_allow_html=True
        )

    st.markdown("### 🚀 90-Day Salary Growth Plan")

    plan_rows = [
        {
            "Timeline": "Days 1–30",
            "Focus": weakest_skills[0][0],
            "Action": "Complete the related Learning & Skills track and practice tasks."
        },
        {
            "Timeline": "Days 31–60",
            "Focus": weakest_skills[1][0],
            "Action": "Build one practical project and add measurable evidence to your portfolio."
        },
        {
            "Timeline": "Days 61–90",
            "Focus": target_role,
            "Action": "Update resume/profile, practise interviews and target roles matching your readiness."
        }
    ]

    st.dataframe(
        pd.DataFrame(plan_rows),
        width="stretch",
        hide_index=True
    )

    st.info(
        "Salary growth shown here is a readiness estimate generated from your saved skills, "
        "experience and target-role fit. It should not be treated as verified market compensation data."
    )

elif menu == "🔥 Industry Trends":
    st.title("🔥 Industry Trend Recommendations")
    trend_df = pd.DataFrame({"Skill": ["Kubernetes", "AWS", "Microservices", "System Design", "AI Integration"], "Demand Growth": [38,32,28,25,24]})
    st.dataframe(trend_df.assign(**{"Demand Growth": trend_df["Demand Growth"].astype(str)+"%"}), width="stretch", hide_index=True)
    fig = px.bar(trend_df, x="Skill", y="Demand Growth", text="Demand Growth", title="Illustrative Industry Demand Forecast")
    st.plotly_chart(fig, width="stretch")
    st.caption("Demand percentages are demonstration values supplied in the project module specification.")

elif menu == "🎓 Certification Suggestions":
    profile = get_professional_profile(st.session_state.user_id)
    metrics = professional_metrics(profile)
    recommendations=[]
    if metrics["Cloud Computing"] < 75: recommendations.append(("AWS Solutions Architect", "High", "Cloud foundation and architecture"))
    if metrics["DevOps"] < 75: recommendations.extend([("Docker Certified Associate", "High", "Container fundamentals"), ("Certified Kubernetes Administrator", "Medium", "Container orchestration")])
    if metrics["System Design"] < 80: recommendations.append(("System Design Fundamentals", "Medium", "Scalable architecture skills"))
    if not recommendations: recommendations=[("Advanced Cloud Architecture", "Medium", "Deepen cloud design"), ("Technical Leadership", "Medium", "Prepare for engineering leadership")]
    st.title("🎓 Certification Suggestions")
    st.dataframe(pd.DataFrame(recommendations, columns=["Certification", "Priority", "Why Recommended"]), width="stretch", hide_index=True)

elif menu == "🧭 Leadership Evaluation":
    profile=get_professional_profile(st.session_state.user_id)
    metrics=professional_metrics(profile)
    base=metrics["Leadership"]
    scores={"Team Coordination":min(95,base+3),"Mentoring":min(95,base-4),"Decision Making":min(95,base+5),"Conflict Resolution":min(95,round((base+metrics['Communication'])/2)),"Project Ownership":min(95,base+1)}
    st.title("🧭 Leadership Skill Evaluation")
    for area,score in scores.items():
        st.write(f"**{area} — {score}%**")
        st.progress(score/100)

elif menu == "🎯 Advanced Job Matching":
    profile=get_professional_profile(st.session_state.user_id)
    metrics=professional_metrics(profile)
    matches=professional_role_matches(profile,metrics)
    st.title("🎯 Advanced Job Matching")
    rows=[]
    for role,score in matches:
        rows.append({"Role":role,"Match %":score,"Experience Fit":"Strong" if float(profile.get('total_experience') or 0)>=3 else "Developing","Salary Fit":"Aligned" if float(profile.get('expected_salary') or 0)>0 else "Add expectation"})
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)

elif menu == "🤖 AI Growth Report":
    profile=get_professional_profile(st.session_state.user_id)
    metrics=professional_metrics(profile)
    matches=professional_role_matches(profile,metrics)
    strongest=max(["Backend Development","System Design","Cloud Computing","DevOps","Leadership"], key=lambda x:metrics[x])
    weakest=min(["Backend Development","System Design","Cloud Computing","DevOps","Leadership"], key=lambda x:metrics[x])
    st.title("🤖 Professional Growth Opportunity Analysis")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Current Role", profile.get("current_role") or "Not provided")
    c2.metric("Next Best Role", matches[0][0])
    c3.metric("Promotion Ready", f"{metrics['Promotion Readiness']}%")
    c4.metric("Salary Growth", f"+{max(0,metrics['Salary Growth'])}%")
    a,b=st.columns(2)
    with a:
        st.success(f"Strong area: **{strongest} ({metrics[strongest]}%)**")
        st.write("Keep building: project delivery, measurable impact, API/design depth and stakeholder communication.")
    with b:
        st.warning(f"Priority area: **{weakest} ({metrics[weakest]}%)**")
        st.write("Focus next: cloud, Docker, Kubernetes, system design and leadership visibility as applicable.")
    plan=pd.DataFrame({"Month":["Month 1","Month 2","Month 3"],"Focus":["Cloud fundamentals and certification preparation","Docker, Kubernetes and deployment practice","System design, microservices and leadership project"]})
    st.subheader("90-Day Action Plan")
    st.dataframe(plan,width="stretch",hide_index=True)
    report_text=f"""TALENTSPHERE ELEVATE - PROFESSIONAL GROWTH REPORT
Name: {st.session_state.user_name}
Current Role: {profile.get('current_role') or 'Not provided'}
Experience: {profile.get('total_experience') or 0} years
Next Best Role: {matches[0][0]} ({matches[0][1]}%)
Promotion Readiness: {metrics['Promotion Readiness']}%
Technical Readiness: {metrics['Technical Readiness']}%
Leadership Readiness: {metrics['Leadership']}%
Salary Growth Potential: +{max(0,metrics['Salary Growth'])}%
Strongest Area: {strongest}
Priority Area: {weakest}

90-Day Plan:
Month 1: Cloud fundamentals
Month 2: Docker and Kubernetes
Month 3: System design, microservices and leadership project
"""
    st.download_button("⬇ Download Professional Growth Report", report_text, "professional_growth_report.txt", "text/plain", width="stretch")

# ==========================================================
# OTHER USER DASHBOARD
# ==========================================================

elif menu == "🏠 Dashboard":

    st.title("📊 Dashboard")

    st.success(
        f"Welcome, {st.session_state.user_name}"
    )

    st.info(
        f"You are logged in as: {st.session_state.user_role}"
    )

    st.write(
        "College Student and Professional features "
        "can be added in the next development stage."
    )


# ==========================================================
# OTHER USER PROFILE
# ==========================================================

elif menu == "👤 Profile":

    st.title("👤 User Profile")

    st.write(
        f"**Name:** {st.session_state.user_name}"
    )

    st.write(
        f"**Email:** {st.session_state.user_email}"
    )

    st.write(
        f"**Role:** {st.session_state.user_role}"
    )


# ==========================================================
# ABOUT PAGE
# ==========================================================

elif menu == "ℹ About":

    st.title("About TalentSphere Elevate")

    st.markdown("""
### 🎯 Vision

TalentSphere Elevate is an AI-powered career development platform.

### ✨ Main Features

- Secure registration and login
- Role-based navigation
- School student profile
- Career Explorer
- AI Subject Quiz
- Interest Assessment
- Skills Roadmap
- School Subjects
- Aptitude Practice
- Communication Skills
- Goal Tracker
- AI Study Mentor
- Performance Reports

### 👨‍💻 Technology Stack

- Python
- Streamlit
- SQLite
- Plotly
- Pandas
- HTML and CSS
    """)


# ==========================================================
# LOGOUT
# ==========================================================

elif menu == "🚪 Logout":

    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_name = ""
    st.session_state.user_email = ""
    st.session_state.user_role = None
    st.session_state.mentor_messages = []
    st.session_state.subject_quiz_result = None
    st.session_state.interest_result = None
    st.session_state.subject_quiz_questions = []
    st.session_state.subject_quiz_subject = ""
    st.session_state.subject_quiz_difficulty = ""
    st.session_state.subject_quiz_result = None

    st.success(
        "You have been logged out successfully."
    )

    st.rerun()


# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
    """
    <div class="app-footer">
        © 2026 TalentSphere Elevate |
        AI-Powered Career Development Platform
    </div>
    """,
    unsafe_allow_html=True
)