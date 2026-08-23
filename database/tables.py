from database.connection import get_connection


def create_tables():

    connection = get_connection()

    cursor = connection.cursor()


    # ======================================================
    # USERS
    # ======================================================

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


    # ======================================================
    # SCHOOL PROFILE
    # ======================================================

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

            FOREIGN KEY(user_id)
            REFERENCES users(id)
        )
    """)


    # ======================================================
    # COLLEGE PROFILE
    # ======================================================

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

            cgpa REAL DEFAULT 0,

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

            linkedin_pdf_path TEXT,

            github_url TEXT,

            portfolio_url TEXT,

            placement_status TEXT,

            updated_at TEXT,

            FOREIGN KEY(user_id)
            REFERENCES users(id)
        )
    """)


    # ======================================================
    # PROFESSIONAL PROFILE
    # ======================================================

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

            FOREIGN KEY(user_id)
            REFERENCES users(id)
        )
    """)


    # ======================================================
    # STUDENT GOALS
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_goals (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            title TEXT NOT NULL,

            target_date TEXT,

            priority TEXT,

            progress INTEGER DEFAULT 0,

            created_at TEXT,

            FOREIGN KEY(user_id)
            REFERENCES users(id)
        )
    """)


    # ======================================================
    # QUIZ RESULTS
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            quiz_type TEXT NOT NULL,

            result TEXT,

            score INTEGER,

            completed_at TEXT,

            FOREIGN KEY(user_id)
            REFERENCES users(id)
        )
    """)


    # ======================================================
    # CODING RESULTS
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coding_results (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            topic TEXT,

            difficulty TEXT,

            score INTEGER,

            completed_at TEXT,

            FOREIGN KEY(user_id)
            REFERENCES users(id)
        )
    """)


    # ======================================================
    # MOCK INTERVIEW
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mock_interview_results (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            interview_type TEXT,

            score INTEGER,

            feedback TEXT,

            completed_at TEXT,

            FOREIGN KEY(user_id)
            REFERENCES users(id)
        )
    """)


    # ======================================================
    # PLACEMENT APPLICATION
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS placement_applications (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            company TEXT,

            role TEXT,

            application_date TEXT,

            status TEXT,

            next_round TEXT,

            notes TEXT,

            created_at TEXT,

            FOREIGN KEY(user_id)
            REFERENCES users(id)
        )
    """)


    # ======================================================
    # JOB MATCHING
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_match_results (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            role TEXT,

            match_score INTEGER,

            reasons TEXT,

            created_at TEXT,

            FOREIGN KEY(user_id)
            REFERENCES users(id)
        )
    """)


    connection.commit()

    connection.close()