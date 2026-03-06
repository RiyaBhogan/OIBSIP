import sqlite3

conn = sqlite3.connect("office.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS email_logs (
id INTEGER PRIMARY KEY AUTOINCREMENT,
sender TEXT,
group_name TEXT,
subject TEXT,
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Email logs table created")