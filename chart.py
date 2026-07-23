import yfinance as yf
import matplotlib.pyplot as plt

tickers = ["AAPL", "GOOGL", "MSFT", "TSLA"]
data = yf.download(tickers, period="3mo")["Close"]


plt.figure(figsize=(12, 6))

for ticker in tickers:
    plt.plot(data.index, data[ticker], label=ticker)

plt.title("Stock Prices - Last 3 Months")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.show()
