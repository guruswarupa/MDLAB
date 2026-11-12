import json
import psycopg2
from psycopg2.extras import Json

config = {
    "host": "localhost",
    "port": "5432",
    "user": "postgres",
    "password": "admin"
}

conn = psycopg2.connect(database="postgres", **config)
conn.autocommit = True
cur = conn.cursor()
cur.execute("SELECT 1 FROM pg_database WHERE datname = %s",
("json_database",))
if not cur.fetchone():
    cur.execute("CREATE DATABASE json_database")
    print("Database created.")
cur.close()
conn.close()

conn = psycopg2.connect(database="json_database", **config)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS students_json (
id SERIAL PRIMARY KEY, student_data JSONB
)
""")

with open("students.json", "r") as file:
    students = json.load(file)
for student in students:
    cur.execute("INSERT INTO students_json (student_data) VALUES (%s)",
                (Json(student),))
conn.commit()
print("JSON records inserted successfully.")

cur.execute("SELECT student_data FROM students_json")
print("\nALL STUDENTS:")
for row in cur.fetchall():
    print(row[0])

cur.execute("""
SELECT student_data ->> 'name' FROM students_json
WHERE student_data ->> 'department' = 'CSE'
""")
print("\nCSE STUDENTS:")
for row in cur.fetchall():
    print(row[0])

cur.execute("""
SELECT student_data ->> 'name',
(student_data ->> 'marks')::INTEGER
FROM students_json
WHERE (student_data ->> 'marks')::INTEGER > 80
""")
print("\nSTUDENTS WITH MARKS ABOVE 80:")
for row in cur.fetchall():
    print(row)

cur.execute("""
SELECT student_data ->> 'name' FROM students_json
WHERE student_data -> 'skills' ? 'Python'
""")
print("\nSTUDENTS WITH PYTHON SKILL:")
for row in cur.fetchall():
    print(row[0])

cur.execute("""
CREATE TABLE IF NOT EXISTS students (
id SERIAL PRIMARY KEY, name VARCHAR(50),
department VARCHAR(20), marks INTEGER
)
""")
cur.execute("""
INSERT INTO students (name, department, marks)
VALUES ('Arun', 'CSE', 85), ('Bala', 'ISE', 90)
""")
conn.commit()

cur.execute("""
SELECT json_build_object(
'name', name, 'department', department, 'marks', marks
) FROM students
""")
print("\nJSON OBJECTS:")
for row in cur.fetchall():
    print(row[0])

cur.execute("""
SELECT json_agg(json_build_object('name', name, 'marks', marks))
FROM students
""")
print("\nJSON ARRAY:")
print(cur.fetchone()[0])

cur.close()
conn.close()
print("\nConnection closed.")