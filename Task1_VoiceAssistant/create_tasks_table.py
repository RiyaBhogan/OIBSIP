import sqlite3

conn = sqlite3.connect("office.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT,
date TEXT,
time TEXT,
status TEXT,
user_email TEXT
)
""")

conn.commit()
conn.close()

print("Tasks table created successfully")