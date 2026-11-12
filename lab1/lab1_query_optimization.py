import mysql.connector
import random
import time

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sunil@123",
    database="company_db"
)
cursor = conn.cursor()
print("Connected to MySQL successfully")

cursor.execute("DELETE FROM employee")
employees = []
for i in range(1, 10001):
    name = "Employee_" + str(i)
    salary = random.randint(20000, 150000)
    dept_id = random.randint(1, 5)
    employees.append(
        (i, name, salary, dept_id)
    )
)
cursor.executemany(
"""
INSERT INTO employee
(emp_id, emp_name, salary, dept_id)
VALUES (%s, %s, %s, %s)
""",
employees
)
conn.commit()
print("10,000 employee records inserted")

print("\n--- WITHOUT INDEX ---")
start_time = time.perf_counter()
cursor.execute("""
SELECT *
FROM employee
WHERE salary = 50000
""")
result = cursor.fetchall()
end_time = time.perf_counter()
without_index = end_time - start_time
print("Records found:", len(result))
print("Execution time:",
without_index, "seconds")

try:
cursor.execute("DROP INDEX idx_salary ON employee")
except mysql.connector.Error:
pass
cursor.execute("""
CREATE INDEX idx_salary
ON employee(salary)
""")
conn.commit()
print("\nIndex created on salary column")

print("\n--- WITH INDEX ---")
start_time = time.perf_counter()
cursor.execute("""
SELECT *
FROM employee
WHERE salary = 50000
""")
result = cursor.fetchall()
end_time = time.perf_counter()
with_index = end_time - start_time
print("Records found:", len(result))
print("Execution time:",
with_index, "seconds")

print("\n--- EFFICIENT WHERE CLAUSE ---")
start_time = time.perf_counter()
cursor.execute("""
SELECT emp_name, salary
FROM employee
WHERE salary > 120000
""")
result = cursor.fetchall()
end_time = time.perf_counter()
print("Records found:", len(result))
print("Execution time:",
end_time - start_time, "seconds")

print("\n--- LIMITING DATA ---")
start_time = time.perf_counter()
cursor.execute("""
SELECT emp_id, emp_name, salary
FROM employee
WHERE salary > 50000
LIMIT 10
""")
result = cursor.fetchall()
end_time = time.perf_counter()
print("Records returned:", len(result))
print("Execution time:",
end_time - start_time, "seconds")

print("\n--- EFFICIENT JOIN ---")
start_time = time.perf_counter()
cursor.execute("""
SELECT e.emp_name,
e.salary,
d.dept_name
FROM employee e
JOIN department d
ON e.dept_id = d.dept_id
WHERE d.dept_name = 'CSE'
""")
result = cursor.fetchall()
end_time = time.perf_counter()
print("CSE employees:", len(result))
print("Execution time:",
end_time - start_time, "seconds")

cursor.close()
conn.close()
print("\nExperiment completed successfully.")