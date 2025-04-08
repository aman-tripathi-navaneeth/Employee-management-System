import sqlite3

conn = sqlite3.connect("employees.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM employees")
rows = cursor.fetchall()

print("\nAll Employees:")
for row in rows:
    print(f"ID: {row[0]}, Name: {row[1]}, Role: {row[2]}")

conn.close()
