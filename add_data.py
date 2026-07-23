import sqlite3

conn = sqlite3.connect("portfolio.db")
cursor = conn.cursor()

# only add the user if they don't already exist
cursor.execute("SELECT id FROM users WHERE name = ?", ("Aron",))
existing_user = cursor.fetchone()

if existing_user:
    user_id = existing_user[0]
else:
    cursor.execute("INSERT INTO users (name) VALUES (?)", ("Aron",))
    user_id = cursor.lastrowid

# add some holdings
holdings = [
    (user_id, "AAPL", 10, 265.92),
    (user_id, "GOOGL", 3, 170.50),
    (user_id, "MSFT", 2, 420.00),
]

cursor.executemany(
    "INSERT INTO holdings (user_id, ticker, shares, buy_price) VALUES (?, ?, ?, ?)",
    holdings
)

conn.commit()
conn.close()

print("Data added successfully!")
