import sqlite3
conn=sqlite3.connect("company.db")
cur=conn.cursor()
cur.execute("UPDATE Employee SET salary=75000 WHERE emp_id=103")
conn.commit()
print("Rows Updated:",cur.rowcount)
conn.close()