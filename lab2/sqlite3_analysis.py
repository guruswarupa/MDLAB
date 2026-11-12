import sqlite3
import csv
import time

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("""
    CREATE TABLE sales(
    order_date TEXT,
    total_cost REAL
)""")

with open("sales_1000000.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cur.execute(
            "INSERT INTO sales VALUES (?, ?)",
            (row["Order Date"], row["Total Cost"])
        )

con.commit()
start = time.time()

result = cur.execute("""
    SELECT order_date,
    COUNT(*) AS total_orders,
    AVG(total_cost) AS average_cost,
    SUM(total_cost) AS total_cost
    FROM sales
    GROUP BY order_date
    ORDER BY total_cost DESC
""").fetchall()

end = time.time()
print("SQLite Result:")
for row in result:
    print(row)
print("SQLite Time:", round(end - start, 6), "seconds")
con.close()