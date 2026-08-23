import json
import sqlite3
from pathlib import Path


# ==========================================================
# DATABASE PATH
# ==========================================================

DB_PATH = (
    Path(__file__).resolve().parent.parent
    / "talentsphere.db"
)


# ==========================================================
# PROFILE FIELDS
# ==========================================================

FIELDS = [
    "full_name",
    "current_role",
    "company",
    "industry",
    "experience_years",
    "highest_education",
    "tech_stack",
    "technical_level",
    "leadership_exposure",
    "communication_level",
    "current_salary_lpa",
    "target_salary_lpa",
    "target_role",
    "target_industry",
    "career_goal",
    "promotion_goal",
    "transition_goal",
    "certifications",
    "achievements",
    "projects",
    "responsibilities",
    "linkedin_url",
    "github_url",
    "portfolio_url",
    "preferred_learning_hours",
]


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def _connect():

    connection = sqlite3.connect(
        DB_PATH
    )

    connection.row_factory = (
        sqlite3.Row
    )

    return connection


# ==========================================================
# CREATE / MIGRATE TABLE
# ==========================================================

def _ensure_table():

    with _connect() as con:

        con.execute(
            """
            CREATE TABLE IF NOT EXISTS professional_profiles (

                user_id INTEGER PRIMARY KEY,

                full_name TEXT DEFAULT '',

                current_role TEXT DEFAULT '',

                company TEXT DEFAULT '',

                industry TEXT DEFAULT '',

                experience_years REAL DEFAULT 0,

                highest_education TEXT DEFAULT '',

                tech_stack TEXT DEFAULT '',

                technical_level TEXT DEFAULT '',

                leadership_exposure TEXT DEFAULT '',

                communication_level TEXT DEFAULT '',

                current_salary_lpa REAL DEFAULT 0,

                target_salary_lpa REAL DEFAULT 0,

                target_role TEXT DEFAULT '',

                target_industry TEXT DEFAULT '',

                career_goal TEXT DEFAULT '',

                promotion_goal TEXT DEFAULT '',

                transition_goal TEXT DEFAULT '',

                certifications TEXT DEFAULT '',

                achievements TEXT DEFAULT '',

                projects TEXT DEFAULT '',

                responsibilities TEXT DEFAULT '',

                linkedin_url TEXT DEFAULT '',

                github_url TEXT DEFAULT '',

                portfolio_url TEXT DEFAULT '',

                preferred_learning_hours REAL DEFAULT 5,

                updated_at TEXT DEFAULT CURRENT_TIMESTAMP

            )
            """
        )


        # ==================================================
        # AUTO MIGRATION
        # ==================================================

        existing_columns = {

            row["name"]

            for row in con.execute(
                """
                PRAGMA table_info(
                    professional_profiles
                )
                """
            ).fetchall()

        }


        required_columns = {

            "full_name":
                "TEXT DEFAULT ''",

            "current_role":
                "TEXT DEFAULT ''",

            "company":
                "TEXT DEFAULT ''",

            "industry":
                "TEXT DEFAULT ''",

            "experience_years":
                "REAL DEFAULT 0",

            "highest_education":
                "TEXT DEFAULT ''",

            "tech_stack":
                "TEXT DEFAULT ''",

            "technical_level":
                "TEXT DEFAULT ''",

            "leadership_exposure":
                "TEXT DEFAULT ''",

            "communication_level":
                "TEXT DEFAULT ''",

            "current_salary_lpa":
                "REAL DEFAULT 0",

            "target_salary_lpa":
                "REAL DEFAULT 0",

            "target_role":
                "TEXT DEFAULT ''",

            "target_industry":
                "TEXT DEFAULT ''",

            "career_goal":
                "TEXT DEFAULT ''",

            "promotion_goal":
                "TEXT DEFAULT ''",

            "transition_goal":
                "TEXT DEFAULT ''",

            "certifications":
                "TEXT DEFAULT ''",

            "achievements":
                "TEXT DEFAULT ''",

            "projects":
                "TEXT DEFAULT ''",

            "responsibilities":
                "TEXT DEFAULT ''",

            "linkedin_url":
                "TEXT DEFAULT ''",

            "github_url":
                "TEXT DEFAULT ''",

            "portfolio_url":
                "TEXT DEFAULT ''",

            "preferred_learning_hours":
                "REAL DEFAULT 5",

            "updated_at":
                "TEXT DEFAULT CURRENT_TIMESTAMP",

        }


        for (
            column_name,
            definition
        ) in required_columns.items():

            if (
                column_name
                not in existing_columns
            ):

                con.execute(
                    f"""
                    ALTER TABLE
                    professional_profiles
                    ADD COLUMN
                    {column_name}
                    {definition}
                    """
                )


# ==========================================================
# GET PROFESSIONAL PROFILE
# ==========================================================

def get_professional_profile(
    user_id
):

    _ensure_table()


    if not user_id:

        return {}


    with _connect() as con:

        row = con.execute(
            """
            SELECT *
            FROM professional_profiles
            WHERE user_id = ?
            """,
            (
                user_id,
            ),
        ).fetchone()


    if not row:

        return {}


    return dict(
        row
    )


# ==========================================================
# SAVE PROFESSIONAL PROFILE
# ==========================================================

def save_professional_profile(
    user_id,
    data
):

    _ensure_table()


    if not user_id:

        raise ValueError(
            "Missing user_id."
        )


    clean = {}


    for field in FIELDS:

        value = data.get(
            field,
            ""
        )


        # Convert complex values to JSON
        if isinstance(
            value,
            (
                list,
                tuple,
                set,
                dict,
            )
        ):

            if isinstance(
                value,
                dict
            ):

                value = json.dumps(
                    value
                )

            else:

                value = json.dumps(
                    list(
                        value
                    )
                )


        clean[
            field
        ] = value


    columns = [
        "user_id",
        *FIELDS,
    ]


    placeholders = ", ".join(
        ["?"]
        * len(
            columns
        )
    )


    update_clause = ", ".join(

        f"""
        {field}
        =
        excluded.{field}
        """

        for field in FIELDS

    )


    values = [

        user_id,

        *[
            clean[
                field
            ]
            for field in FIELDS
        ],

    ]


    with _connect() as con:

        con.execute(
            f"""
            INSERT INTO
            professional_profiles
            (
                {", ".join(columns)}
            )

            VALUES
            (
                {placeholders}
            )

            ON CONFLICT(user_id)
            DO UPDATE SET

                {update_clause},

                updated_at =
                CURRENT_TIMESTAMP
            """,

            values,
        )


    return (
        get_professional_profile(
            user_id
        )
    )


# ==========================================================
# DELETE PROFESSIONAL PROFILE
# OPTIONAL
# ==========================================================

def delete_professional_profile(
    user_id
):

    _ensure_table()


    if not user_id:

        return False


    with _connect() as con:

        con.execute(
            """
            DELETE FROM
            professional_profiles
            WHERE user_id = ?
            """,
            (
                user_id,
            ),
        )


    return True


# ==========================================================
# CHECK PROFILE EXISTS
# ==========================================================

def professional_profile_exists(
    user_id
):

    profile = (
        get_professional_profile(
            user_id
        )
    )


    return bool(
        profile
    )