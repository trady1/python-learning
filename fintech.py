import yfinance as yf

stock = yf.download("AAPL", period="3mo")


print(stock.head())
print(stock.tail())
print(stock.describe())

stock["daily_return"] = stock["Close"].pct_change() * 100
print(stock["daily_return"].head(63))

total_return = ((stock["Close"].iloc[-1].values[0] -
                stock["Close"].iloc[0].values[0]) / stock["Close"].iloc[0].values[0]) * 100
print(f"Apple's total return over 3 months: {float(total_return):.2f}%")

print(f"Best day: {stock['daily_return'].max():.2f}%")
print(f"Worst day: {stock['daily_return'].min():.2f}%")
