import sqlite3

conn = sqlite3.connect("college.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM Student")
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()