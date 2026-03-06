import sqlite3

conn = sqlite3.connect("office.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS meetings(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT,
date TEXT,
time TEXT,
created_by TEXT
)
""")

conn.commit()
conn.close()

print("Meetings table created successfully")