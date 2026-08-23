from datetime import datetime

from database.connection import get_connection


# ==========================================================
# REQUIRED COLLEGE PROFILE COLUMNS
# ==========================================================

PROFILE_COLUMNS = {

    "college_name":
        "TEXT DEFAULT ''",

    "degree":
        "TEXT DEFAULT ''",

    "branch":
        "TEXT DEFAULT ''",

    "current_year":
        "TEXT DEFAULT ''",

    "semester":
        "TEXT DEFAULT ''",

    "graduation_year":
        "TEXT DEFAULT ''",

    "cgpa":
        "REAL DEFAULT 0",

    "backlogs":
        "INTEGER DEFAULT 0",

    "technical_skills":
        "TEXT DEFAULT ''",

    "soft_skills":
        "TEXT DEFAULT ''",

    "projects":
        "TEXT DEFAULT ''",

    "internships":
        "TEXT DEFAULT ''",

    "certifications":
        "TEXT DEFAULT ''",

    "preferred_role":
        "TEXT DEFAULT ''",

    "placement_goal":
        "TEXT DEFAULT ''",

    "github_url":
        "TEXT DEFAULT ''",

    "linkedin_url":
        "TEXT DEFAULT ''",

    "portfolio_url":
        "TEXT DEFAULT ''",

    "coding_platforms":
        "TEXT DEFAULT ''",

    "achievements":
        "TEXT DEFAULT ''",
}


# ==========================================================
# CREATE BASE TABLE
# ==========================================================

def create_college_profile_table():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS college_profiles (

            user_id INTEGER PRIMARY KEY,

            college_name TEXT DEFAULT '',

            degree TEXT DEFAULT '',

            branch TEXT DEFAULT '',

            current_year TEXT DEFAULT '',

            semester TEXT DEFAULT '',

            graduation_year TEXT DEFAULT '',

            cgpa REAL DEFAULT 0,

            backlogs INTEGER DEFAULT 0,

            technical_skills TEXT DEFAULT '',

            soft_skills TEXT DEFAULT '',

            projects TEXT DEFAULT '',

            internships TEXT DEFAULT '',

            certifications TEXT DEFAULT '',

            preferred_role TEXT DEFAULT '',

            placement_goal TEXT DEFAULT '',

            github_url TEXT DEFAULT '',

            linkedin_url TEXT DEFAULT '',

            portfolio_url TEXT DEFAULT '',

            coding_platforms TEXT DEFAULT '',

            achievements TEXT DEFAULT ''

        )
        """
    )


    connection.commit()

    connection.close()


# ==========================================================
# DATABASE MIGRATION
# ==========================================================

def migrate_college_profile_table():

    create_college_profile_table()


    connection = get_connection()

    cursor = connection.cursor()


    # ------------------------------------------------------
    # READ EXISTING COLUMNS
    # ------------------------------------------------------

    cursor.execute(
        """
        PRAGMA table_info(college_profiles)
        """
    )


    rows = cursor.fetchall()


    existing_columns = set()


    for row in rows:

        try:

            # sqlite3.Row
            existing_columns.add(
                row["name"]
            )

        except Exception:

            # Normal tuple:
            # cid, name, type, notnull, default, pk
            existing_columns.add(
                row[1]
            )


    # ------------------------------------------------------
    # ADD MISSING COLUMNS
    # ------------------------------------------------------

    for (
        column_name,
        column_definition,
    ) in PROFILE_COLUMNS.items():

        if (
            column_name
            not in existing_columns
        ):

            cursor.execute(
                f"""
                ALTER TABLE college_profiles
                ADD COLUMN
                {column_name}
                {column_definition}
                """
            )


    connection.commit()

    connection.close()


# ==========================================================
# INITIALIZE ALL COLLEGE TABLES
# ==========================================================

def create_college_tables():

    migrate_college_profile_table()


    connection = get_connection()

    cursor = connection.cursor()


    # ------------------------------------------------------
    # PLACEMENT TRACKER
    # ------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS college_placements (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            company TEXT NOT NULL,

            role TEXT NOT NULL,

            status TEXT NOT NULL,

            applied_date TEXT DEFAULT '',

            notes TEXT DEFAULT '',

            created_at TEXT NOT NULL

        )
        """
    )


    # ------------------------------------------------------
    # INTERNSHIP TRACKER
    # ------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS college_internships (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            company TEXT NOT NULL,

            role TEXT NOT NULL,

            duration TEXT DEFAULT '',

            status TEXT DEFAULT '',

            notes TEXT DEFAULT ''

        )
        """
    )


    # ------------------------------------------------------
    # HACKATHON TRACKER
    # ------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS college_hackathons (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            name TEXT NOT NULL,

            team TEXT DEFAULT '',

            result TEXT DEFAULT '',

            project TEXT DEFAULT '',

            notes TEXT DEFAULT ''

        )
        """
    )


    connection.commit()

    connection.close()


# ==========================================================
# ROW TO DICTIONARY
# ==========================================================

def row_to_dict(
    row,
    columns,
):

    if not row:

        return {}


    try:

        return dict(
            row
        )

    except Exception:

        return dict(
            zip(
                columns,
                row,
            )
        )


# ==========================================================
# GET COLLEGE PROFILE
# ==========================================================

def get_college_profile(
    user_id,
):

    create_college_tables()


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT
            user_id,
            college_name,
            degree,
            branch,
            current_year,
            semester,
            graduation_year,
            cgpa,
            backlogs,
            technical_skills,
            soft_skills,
            projects,
            internships,
            certifications,
            preferred_role,
            placement_goal,
            github_url,
            linkedin_url,
            portfolio_url,
            coding_platforms,
            achievements

        FROM college_profiles

        WHERE user_id = ?
        """,
        (
            user_id,
        ),
    )


    row = cursor.fetchone()


    connection.close()


    columns = [

        "user_id",

        "college_name",

        "degree",

        "branch",

        "current_year",

        "semester",

        "graduation_year",

        "cgpa",

        "backlogs",

        "technical_skills",

        "soft_skills",

        "projects",

        "internships",

        "certifications",

        "preferred_role",

        "placement_goal",

        "github_url",

        "linkedin_url",

        "portfolio_url",

        "coding_platforms",

        "achievements",

    ]


    return row_to_dict(
        row,
        columns,
    )


# ==========================================================
# SAVE COLLEGE PROFILE
# ==========================================================

def save_college_profile(
    user_id,
    college_name="",
    degree="",
    branch="",
    current_year="",
    semester="",
    graduation_year="",
    cgpa=0.0,
    backlogs=0,
    technical_skills="",
    soft_skills="",
    projects="",
    internships="",
    certifications="",
    preferred_role="",
    placement_goal="",
    github_url="",
    linkedin_url="",
    portfolio_url="",
    coding_platforms="",
    achievements="",
):

    create_college_tables()


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

            graduation_year,

            cgpa,

            backlogs,

            technical_skills,

            soft_skills,

            projects,

            internships,

            certifications,

            preferred_role,

            placement_goal,

            github_url,

            linkedin_url,

            portfolio_url,

            coding_platforms,

            achievements

        )

        VALUES (

            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,

            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?

        )

        ON CONFLICT(user_id)

        DO UPDATE SET

            college_name =
                excluded.college_name,

            degree =
                excluded.degree,

            branch =
                excluded.branch,

            current_year =
                excluded.current_year,

            semester =
                excluded.semester,

            graduation_year =
                excluded.graduation_year,

            cgpa =
                excluded.cgpa,

            backlogs =
                excluded.backlogs,

            technical_skills =
                excluded.technical_skills,

            soft_skills =
                excluded.soft_skills,

            projects =
                excluded.projects,

            internships =
                excluded.internships,

            certifications =
                excluded.certifications,

            preferred_role =
                excluded.preferred_role,

            placement_goal =
                excluded.placement_goal,

            github_url =
                excluded.github_url,

            linkedin_url =
                excluded.linkedin_url,

            portfolio_url =
                excluded.portfolio_url,

            coding_platforms =
                excluded.coding_platforms,

            achievements =
                excluded.achievements
        """,

        (

            user_id,

            str(
                college_name
                or ""
            ).strip(),

            str(
                degree
                or ""
            ).strip(),

            str(
                branch
                or ""
            ).strip(),

            str(
                current_year
                or ""
            ).strip(),

            str(
                semester
                or ""
            ).strip(),

            str(
                graduation_year
                or ""
            ).strip(),

            float(
                cgpa
                or 0
            ),

            int(
                backlogs
                or 0
            ),

            str(
                technical_skills
                or ""
            ).strip(),

            str(
                soft_skills
                or ""
            ).strip(),

            str(
                projects
                or ""
            ).strip(),

            str(
                internships
                or ""
            ).strip(),

            str(
                certifications
                or ""
            ).strip(),

            str(
                preferred_role
                or ""
            ).strip(),

            str(
                placement_goal
                or ""
            ).strip(),

            str(
                github_url
                or ""
            ).strip(),

            str(
                linkedin_url
                or ""
            ).strip(),

            str(
                portfolio_url
                or ""
            ).strip(),

            str(
                coding_platforms
                or ""
            ).strip(),

            str(
                achievements
                or ""
            ).strip(),

        ),
    )


    connection.commit()

    connection.close()


# ==========================================================
# ADD PLACEMENT
# ==========================================================

def add_placement(
    user_id,
    company,
    role,
    status,
    applied_date,
    notes="",
):

    create_college_tables()


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        INSERT INTO college_placements (

            user_id,

            company,

            role,

            status,

            applied_date,

            notes,

            created_at

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,

        (

            user_id,

            company,

            role,

            status,

            applied_date,

            notes,

            datetime.now().isoformat(),

        ),
    )


    connection.commit()

    connection.close()


# ==========================================================
# GET PLACEMENTS
# ==========================================================

def get_placements(
    user_id,
):

    create_college_tables()


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *

        FROM college_placements

        WHERE user_id = ?

        ORDER BY id DESC
        """,
        (
            user_id,
        ),
    )


    rows = cursor.fetchall()


    connection.close()


    columns = [

        "id",

        "user_id",

        "company",

        "role",

        "status",

        "applied_date",

        "notes",

        "created_at",

    ]


    return [

        row_to_dict(
            row,
            columns,
        )

        for row in rows

    ]


# ==========================================================
# DELETE PLACEMENT
# ==========================================================

def delete_placement(
    placement_id,
):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        DELETE FROM college_placements

        WHERE id = ?
        """,
        (
            placement_id,
        ),
    )


    connection.commit()

    connection.close()


# ==========================================================
# ADD INTERNSHIP
# ==========================================================

def add_internship(
    user_id,
    company,
    role,
    duration,
    status,
    notes="",
):

    create_college_tables()


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        INSERT INTO college_internships (

            user_id,

            company,

            role,

            duration,

            status,

            notes

        )

        VALUES (?, ?, ?, ?, ?, ?)
        """,

        (

            user_id,

            company,

            role,

            duration,

            status,

            notes,

        ),
    )


    connection.commit()

    connection.close()


# ==========================================================
# GET INTERNSHIPS
# ==========================================================

def get_internships(
    user_id,
):

    create_college_tables()


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *

        FROM college_internships

        WHERE user_id = ?

        ORDER BY id DESC
        """,
        (
            user_id,
        ),
    )


    rows = cursor.fetchall()


    connection.close()


    columns = [

        "id",

        "user_id",

        "company",

        "role",

        "duration",

        "status",

        "notes",

    ]


    return [

        row_to_dict(
            row,
            columns,
        )

        for row in rows

    ]


# ==========================================================
# ADD HACKATHON
# ==========================================================

def add_hackathon(
    user_id,
    name,
    team,
    result,
    project,
    notes="",
):

    create_college_tables()


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        INSERT INTO college_hackathons (

            user_id,

            name,

            team,

            result,

            project,

            notes

        )

        VALUES (?, ?, ?, ?, ?, ?)
        """,

        (

            user_id,

            name,

            team,

            result,

            project,

            notes,

        ),
    )


    connection.commit()

    connection.close()


# ==========================================================
# GET HACKATHONS
# ==========================================================

def get_hackathons(
    user_id,
):

    create_college_tables()


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *

        FROM college_hackathons

        WHERE user_id = ?

        ORDER BY id DESC
        """,
        (
            user_id,
        ),
    )


    rows = cursor.fetchall()


    connection.close()


    columns = [

        "id",

        "user_id",

        "name",

        "team",

        "result",

        "project",

        "notes",

    ]


    return [

        row_to_dict(
            row,
            columns,
        )

        for row in rows

    ]