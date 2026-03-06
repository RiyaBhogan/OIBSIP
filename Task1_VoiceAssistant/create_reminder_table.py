import sqlite3

conn = sqlite3.connect("office.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reminders(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT,
date TEXT,
time TEXT,
user_email TEXT
)
""")

conn.commit()
conn.close()