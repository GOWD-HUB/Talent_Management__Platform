import os
import sqlite3

from auth.security import (
    hash_password,
    verify_password,
)


# ==========================================================
# DATABASE PATH
# ==========================================================

DB_PATH = os.path.join(
    "database",
    "talentsphere.db"
)


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_connection():

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    return connection


# ==========================================================
# GET USERS TABLE COLUMNS
# ==========================================================

def get_user_columns():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "PRAGMA table_info(users)"
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        row["name"]
        for row in rows
    ]


# ==========================================================
# FIND COLUMN
# ==========================================================

def find_column(possible_names):

    columns = get_user_columns()

    for column in possible_names:

        if column in columns:
            return column

    return None


# ==========================================================
# EMAIL COLUMN
# ==========================================================

def get_email_column():

    return find_column(
        [
            "email",
            "email_address",
            "user_email",
        ]
    )


# ==========================================================
# PASSWORD COLUMN
# ==========================================================

def get_password_column():

    return find_column(
        [
            "password",
            "password_hash",
            "hashed_password",
        ]
    )


# ==========================================================
# ROLE COLUMN
# ==========================================================

def get_role_column():

    return find_column(
        [
            "role",
            "user_role",
            "user_type",
            "account_type",
        ]
    )


# ==========================================================
# OPTIONAL NAME COLUMN
# ==========================================================

def get_name_column():

    return find_column(
        [
            "name",
            "full_name",
            "username",
            "first_name",
            "student_name",
            "user_name",
        ]
    )


# ==========================================================
# CHECK EMAIL
# ==========================================================

def email_exists(email):

    email_column = get_email_column()

    if not email_column:
        return False

    connection = get_connection()
    cursor = connection.cursor()

    query = f"""
        SELECT id
        FROM users
        WHERE LOWER({email_column}) = LOWER(?)
        LIMIT 1
    """

    cursor.execute(
        query,
        (
            email.strip(),
        ),
    )

    result = cursor.fetchone()

    connection.close()

    return result is not None


# ==========================================================
# LOGIN USER
# ==========================================================

def login_user(
    email,
    password,
):

    email = email.strip().lower()

    if not email or not password:
        return None


    # ======================================================
    # DETECT DATABASE COLUMNS
    # ======================================================

    email_column = get_email_column()
    password_column = get_password_column()
    role_column = get_role_column()
    name_column = get_name_column()


    if not email_column:

        raise RuntimeError(
            "Email column was not found in the users table."
        )


    if not password_column:

        raise RuntimeError(
            "Password column was not found in the users table."
        )


    if not role_column:

        raise RuntimeError(
            "Role column was not found in the users table."
        )


    # ======================================================
    # BUILD QUERY
    # ======================================================

    if name_column:

        query = f"""
            SELECT
                id,
                {name_column} AS display_name,
                {email_column} AS email,
                {password_column} AS stored_password,
                {role_column} AS role

            FROM users

            WHERE LOWER({email_column}) = LOWER(?)

            LIMIT 1
        """

    else:

        # No name column exists.
        # That is completely fine for authentication.

        query = f"""
            SELECT
                id,
                {email_column} AS email,
                {password_column} AS stored_password,
                {role_column} AS role

            FROM users

            WHERE LOWER({email_column}) = LOWER(?)

            LIMIT 1
        """


    # ======================================================
    # FETCH USER
    # ======================================================

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        query,
        (
            email,
        ),
    )

    user = cursor.fetchone()

    connection.close()


    if not user:

        return None


    # ======================================================
    # PASSWORD CHECK
    # ======================================================

    stored_password = (
        user["stored_password"]
        or ""
    )

    valid_password = False


    # ------------------------------------------------------
    # HASHED PASSWORD
    # ------------------------------------------------------

    try:

        valid_password = verify_password(
            password,
            stored_password,
        )

    except Exception:

        valid_password = False


    # ------------------------------------------------------
    # SUPPORT OLD PLAIN-TEXT PASSWORDS
    # ------------------------------------------------------

    if not valid_password:

        if password == stored_password:

            valid_password = True


    if not valid_password:

        return None


    # ======================================================
    # DISPLAY NAME
    # ======================================================

    if name_column:

        display_name = (
            user["display_name"]
            or ""
        ).strip()

    else:

        display_name = ""


    # If database doesn't store a name,
    # derive it from email.

    if not display_name:

        display_name = (
            user["email"]
            .split("@")[0]
            .replace(".", " ")
            .replace("_", " ")
            .title()
        )


    # ======================================================
    # NORMALIZE ROLE
    # ======================================================

    role = (
        user["role"]
        or ""
    ).strip()


    # Support old role labels
    role_aliases = {

        "school": "School Student",

        "school student":
            "School Student",

        "student":
            "School Student",

        "college":
            "College Student",

        "college student":
            "College Student",

        "professional":
            "Professional",

        "working professional":
            "Professional",
    }


    normalized_role = role_aliases.get(
        role.lower(),
        role
    )


    # ======================================================
    # SUCCESS
    # ======================================================

    return {
        "id": user["id"],
        "name": display_name,
        "email": user["email"],
        "role": normalized_role,
    }


# ==========================================================
# REGISTER USER
# ==========================================================

def register_user(
    name,
    email,
    password,
    role,
):

    name = name.strip()
    email = email.strip().lower()
    role = role.strip()


    # ======================================================
    # VALIDATION
    # ======================================================

    if not name:

        return (
            False,
            "Please enter your name."
        )


    if not email:

        return (
            False,
            "Please enter your email address."
        )


    if "@" not in email or "." not in email:

        return (
            False,
            "Please enter a valid email address."
        )


    if len(password) < 6:

        return (
            False,
            "Password must contain at least 6 characters."
        )


    valid_roles = [
        "School Student",
        "College Student",
        "Professional",
    ]


    if role not in valid_roles:

        return (
            False,
            "Please select a valid user role."
        )


    if email_exists(email):

        return (
            False,
            "An account with this email already exists."
        )


    # ======================================================
    # DETECT DATABASE COLUMNS
    # ======================================================

    email_column = get_email_column()
    password_column = get_password_column()
    role_column = get_role_column()
    name_column = get_name_column()


    if not email_column:

        return (
            False,
            "Email column is missing from users table."
        )


    if not password_column:

        return (
            False,
            "Password column is missing from users table."
        )


    if not role_column:

        return (
            False,
            "Role column is missing from users table."
        )


    hashed_password = hash_password(
        password
    )


    connection = get_connection()
    cursor = connection.cursor()


    try:

        # ==================================================
        # DATABASE HAS NAME COLUMN
        # ==================================================

        if name_column:

            query = f"""
                INSERT INTO users (
                    {name_column},
                    {email_column},
                    {password_column},
                    {role_column}
                )

                VALUES (?, ?, ?, ?)
            """

            values = (
                name,
                email,
                hashed_password,
                role,
            )


        # ==================================================
        # DATABASE DOES NOT HAVE NAME COLUMN
        # ==================================================

        else:

            query = f"""
                INSERT INTO users (
                    {email_column},
                    {password_column},
                    {role_column}
                )

                VALUES (?, ?, ?)
            """

            values = (
                email,
                hashed_password,
                role,
            )


        cursor.execute(
            query,
            values,
        )

        connection.commit()

        connection.close()


        return (
            True,
            "Account created successfully."
        )


    except sqlite3.IntegrityError:

        connection.close()

        return (
            False,
            "An account with this email already exists."
        )


    except Exception as error:

        connection.close()

        return (
            False,
            f"Registration failed: {error}"
        )