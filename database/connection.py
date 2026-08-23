import sqlite3

from core.config import DATABASE_PATH


def get_connection():

    connection = sqlite3.connect(
        str(DATABASE_PATH),
        check_same_thread=False
    )

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection