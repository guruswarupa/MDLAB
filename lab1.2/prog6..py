import sqlite3
conn=sqlite3.connect("company.db")
cur=conn.cursor()
cur.execute("DELETE FROM Employee WHERE emp_id=105")
conn.commit()
print("Rows Deleted:",cur.rowcount)
conn.close()