from datetime import datetime

from database.connection import get_connection


# ==========================================================
# EMPTY PROFILE
# ==========================================================

def empty_school_profile():

    return {
        "school_name": "",
        "current_class": "",
        "board": "",
        "city": "",
        "parent_name": "",
        "phone": "",
        "percentage": "",
        "favourite_subjects": "",
        "interests": "",
        "skills": "",
        "dream_career": "",
        "academic_goal": "",
        "target_course": "",
        "achievements": "",
        "updated_at": None,
    }


# ==========================================================
# GET TABLE COLUMNS
# ==========================================================

def get_school_profile_columns():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "PRAGMA table_info(school_profiles)"
    )

    rows = cursor.fetchall()

    connection.close()

    columns = []

    for row in rows:

        try:
            columns.append(row["name"])
        except Exception:
            columns.append(row[1])

    return columns


# ==========================================================
# GET SCHOOL PROFILE
# ==========================================================

def get_school_profile(user_id):

    profile = empty_school_profile()

    columns = get_school_profile_columns()

    if "user_id" not in columns:
        return profile

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM school_profiles
        WHERE user_id = ?
        LIMIT 1
        """,
        (user_id,),
    )

    row = cursor.fetchone()

    connection.close()

    if not row:
        return profile

    for field in profile.keys():

        if field in columns:

            try:
                value = row[field]
            except Exception:
                value = None

            profile[field] = (
                value
                if value is not None
                else ""
            )

    return profile


# ==========================================================
# SAVE SCHOOL PROFILE
# ==========================================================

def save_school_profile(
    user_id,
    school_name,
    current_class,
    board,
    city,
    parent_name,
    phone,
    percentage,
    favourite_subjects,
    interests,
    skills,
    dream_career,
    academic_goal,
    target_course,
    achievements,
):

    columns = get_school_profile_columns()

    if "user_id" not in columns:
        return False, "school_profiles table is missing user_id."

    values = {
        "school_name": school_name.strip(),
        "current_class": current_class.strip(),
        "board": board.strip(),
        "city": city.strip(),
        "parent_name": parent_name.strip(),
        "phone": phone.strip(),
        "percentage": percentage.strip(),
        "favourite_subjects": favourite_subjects.strip(),
        "interests": interests.strip(),
        "skills": skills.strip(),
        "dream_career": dream_career.strip(),
        "academic_goal": academic_goal.strip(),
        "target_course": target_course.strip(),
        "achievements": achievements.strip(),
        "updated_at": datetime.now().isoformat(),
    }

    usable_fields = [
        field
        for field in values
        if field in columns
    ]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT user_id
        FROM school_profiles
        WHERE user_id = ?
        LIMIT 1
        """,
        (user_id,),
    )

    existing = cursor.fetchone()

    try:

        if existing:

            assignments = ", ".join(
                [
                    f"{field} = ?"
                    for field in usable_fields
                ]
            )

            query = f"""
                UPDATE school_profiles
                SET {assignments}
                WHERE user_id = ?
            """

            params = [
                values[field]
                for field in usable_fields
            ]

            params.append(user_id)

            cursor.execute(
                query,
                params,
            )

        else:

            insert_columns = [
                "user_id"
            ] + usable_fields

            placeholders = ", ".join(
                ["?"] * len(insert_columns)
            )

            query = f"""
                INSERT INTO school_profiles (
                    {", ".join(insert_columns)}
                )
                VALUES ({placeholders})
            """

            params = [
                user_id
            ] + [
                values[field]
                for field in usable_fields
            ]

            cursor.execute(
                query,
                params,
            )

        connection.commit()
        connection.close()

        return True, "Profile saved successfully."

    except Exception as error:

        connection.close()

        return (
            False,
            f"Unable to save profile: {error}",
        )