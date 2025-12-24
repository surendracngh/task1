import sqlite3

# Connect to database (creates database if not exists)
conn = sqlite3.connect("student.db")

print("Database connected successfully")

# Create a cursor object
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER
)
""")

print("Table created successfully")

# Close connection
conn.close()
