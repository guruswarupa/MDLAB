import sqlite3

conn=sqlite3.connect("company.db")
cur=conn.cursor()
cur.execute("SELECT * FROM Employee WHERE department='CSE'")
for row in cur.fetchall():
    print(row)
conn.close()