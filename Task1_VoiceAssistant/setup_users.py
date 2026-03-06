import sqlite3

conn = sqlite3.connect("office.db")
cursor = conn.cursor()

users = [
    ("riya1970463@gmail.com", "1234", "hr"),
    ("amit@company.com", "1234", "manager"),
    ("john@company.com", "1234", "employee"),
    ("neha@company.com", "1234", "employee")
]

cursor.executemany(
    "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
    users
)

conn.commit()
conn.close()

print("Default users added")