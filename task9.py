import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER
)''')

cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Aron", 22))
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("John", 30))
conn.commit()
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")

    conn.close()
