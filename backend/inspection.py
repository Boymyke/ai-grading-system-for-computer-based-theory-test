import sqlite3

conn = sqlite3.connect("fyp_database.db") 
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in the database:", tables)

table_name = "Tests" 
cursor.execute(f"SELECT * FROM {table_name} LIMIT 1000;") 

rows = cursor.fetchall()
for row in rows:
    print(row)

table_name = "Student_Test" 
cursor.execute(f"PRAGMA table_info({table_name});")
schema = cursor.fetchall()

for column in schema:
    print(column)

conn.close()


