import sqlite3

conn = sqlite3.connect("college.db")
cursor = conn.cursor()
cursor.execute("INSERT INTO Student VALUES (1,'Rahul',20,'ISE')")
cursor.execute("INSERT INTO Student VALUES (2,'Sneha',21,'CSE')")
cursor.execute("INSERT INTO Student VALUES (3,'Anil',22,'ECE')")
conn.commit()
conn.close()
print("Records inserted successfully.")