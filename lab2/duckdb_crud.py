import duckdb

con = duckdb.connect()
con.execute("""
    CREATE TABLE student(
    id INTEGER,
    name VARCHAR,
    marks INTEGER
)""")

con.execute("""
    INSERT INTO student VALUES
    (1, 'Arun', 85),
    (2, 'Rahul', 78),
    (3, 'Priya', 92)
""")
print("Records:")
print(con.execute("SELECT * FROM student").fetchall())
con.execute("""
    UPDATE student
    SET marks = 82
    WHERE id = 2
""")
con.execute("DELETE FROM student WHERE id = 3")
print("After Update and Delete:")
print(con.execute("SELECT * FROM student").fetchall())
con.close()