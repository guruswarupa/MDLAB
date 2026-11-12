import sqlite3

conn = sqlite3.connect("college.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE Student(
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    department TEXT
)""")
conn.commit()
conn.close()
print("Table created successfully.")