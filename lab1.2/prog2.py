import sqlite3

conn=sqlite3.connect("company.db")
cur=conn.cursor()
employees=[
(101,"Amit","CSE",65000,5,"Bangalore"),
(102,"Neha","ISE",55000,3,"Mysore"),
(103,"Ravi","ECE",70000,7,"Bangalore"),
(104,"Pooja","CSE",60000,4,"Hubli"),
(105,"Kiran","ISE",50000,2,"Mangalore")
]
cur.executemany("INSERT INTO Employee VALUES(?,?,?,?,?,?)",employees)
conn.commit()
conn.close()
print("Records inserted.")