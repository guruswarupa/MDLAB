import duckdb
import time

con = duckdb.connect()
start = time.time()

result = con.execute("""
    SELECT "Order Date",
    COUNT(*) AS total_orders,
    AVG("Total Cost") AS average_cost,
    SUM("Total Cost") AS total_cost
    FROM read_csv_auto('sales_1000000.csv')
    GROUP BY "Order Date"
    ORDER BY total_cost DESC
""").fetchall()

end = time.time()

print("DuckDB Result:")
for row in result:
    print(row)
print("DuckDB Time:", round(end - start, 6), "seconds")
con.close()