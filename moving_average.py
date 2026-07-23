import yfinance as yf
import matplotlib.pyplot as plt


data = yf.download("AAPL", period="6mo")


data["MA20"] = data["Close"].rolling(window=20).mean()
data["MA50"] = data["Close"].rolling(window=50).mean()


plt.figure(figsize=(12, 6))
plt.plot(data.index, data["Close"], label="Price", alpha=0.5)
plt.plot(data.index, data["MA20"], label="MA20 (short term)", linewidth=2)
plt.plot(data.index, data["MA50"], label="MA50 (long term)", linewidth=2)

plt.title("Apple Stock - Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.show()
