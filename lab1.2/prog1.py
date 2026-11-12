import sqlite3

conn=sqlite3.connect("company.db")
cur=conn.cursor()
cur.execute("""
    CREATE TABLE Employee(
    emp_id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary REAL,
    experience INTEGER,
    city TEXT
)""")
conn.commit()
conn.close()
print("Employee table created.")