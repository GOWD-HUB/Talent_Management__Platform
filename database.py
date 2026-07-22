import sqlite3

conn = sqlite3.connect("database/talentsphere.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    category TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Database and users table created successfully!")