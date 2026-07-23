import sqlite3
import yfinance as yf

conn = sqlite3.connect("portfolio.db")
cursor = conn.cursor()

cursor.execute(
    "SELECT ticker, shares, buy_price FROM holdings WHERE user_id = 1")
holdings = cursor.fetchall()

conn.close()

print("--- My Portfolio ---\n")

total_value = 0
total_invested = 0

for ticker, shares, buy_price in holdings:
    current_price = float(yf.Ticker(ticker).history(
        period="1d")["Close"].iloc[-1])

    invested = shares * buy_price
    current_value = shares * current_price
    profit_loss = current_value - invested
    return_pct = (profit_loss / invested) * 100

    total_invested += invested
    total_value += current_value

    print(f"{ticker}: {shares} shares")
    print(f"  Bought at:     ${buy_price:.2f}")
    print(f"  Current price: ${current_price:.2f}")
    print(f"  Invested:      ${invested:.2f}")
    print(f"  Current value: ${current_value:.2f}")
    print(f"  Return:        {return_pct:.2f}%\n")

total_return = ((total_value - total_invested) / total_invested) * 100
print(f"--- Total Portfolio ---")
print(f"Invested:      ${total_invested:.2f}")
print(f"Current value: ${total_value:.2f}")
print(f"Return:        {total_return:.2f}%")
