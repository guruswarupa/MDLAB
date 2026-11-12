import sqlite3

conn=sqlite3.connect("company.db")
cur=conn.cursor()
cur.execute("SELECT * FROM Employee")
for row in cur.fetchall():
    print(row)
conn.close()