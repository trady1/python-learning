import yfinance as yf


portfolio = {
    "AAPL": 1000,
    "GOOGL": 1000,
    "MSFT": 1000,
    "TSLA": 1000
}

tickers = list(portfolio.keys())
data = yf.download(tickers, period="3mo")["Close"]

print("--- Portfolio Tracker ---\n")

total_invested = 0
total_current = 0

for ticker in tickers:
    invested = portfolio[ticker]
    start_price = float(data[ticker].iloc[0])
    current_price = float(data[ticker].iloc[-1])

    shares = invested / start_price

    current_value = shares * current_price

    profit_loss = current_value - invested
    return_pct = (profit_loss / invested) * 100

    total_invested += invested
    total_current += current_value

    print(f"{ticker}:")
    print(f"  Invested:      ${invested:.2f}")
    print(f"  Current value: ${current_value:.2f}")
    print(f"  Profit/Loss:   ${profit_loss:.2f}")
    print(f"  Return:        {return_pct:.2f}%\n")

total_profit = total_current - total_invested
total_return = (total_profit / total_invested) * 100

print(f"--- Total Portfolio ---")
print(f"Invested:      ${total_invested:.2f}")
print(f"Current value: ${total_current:.2f}")
print(f"Profit/Loss:   ${total_profit:.2f}")
print(f"Return:        {total_return:.2f}%")
