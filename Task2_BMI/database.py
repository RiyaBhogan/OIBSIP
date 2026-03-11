import sqlite3


def create_connection():
    return sqlite3.connect("database.db")


# Users table
def create_table():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


# Weight tracker table
def create_weight_table():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weight_tracker(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        weight REAL,
        target_weight REAL
    )
    """)

    conn.commit()
    conn.close()