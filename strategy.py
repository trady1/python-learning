import yfinance as yf
import matplotlib.pyplot as plt

data = yf.download("AAPL", period="6mo")
data.columns = data.columns.get_level_values(0)

data["MA20"] = data["Close"].rolling(window=20).mean()
data["MA50"] = data["Close"].rolling(window=50).mean()


data["signal"] = 0
data.loc[data["MA20"] > data["MA50"], "signal"] = 1


data["position"] = data["signal"].diff()


plt.figure(figsize=(12, 6))
plt.plot(data.index, data["Close"], label="Price", alpha=0.5)
plt.plot(data.index, data["MA20"], label="MA20")
plt.plot(data.index, data["MA50"], label="MA50")


buy_signals = data[data["position"] == 1]
plt.scatter(buy_signals.index,
            buy_signals["Close"], marker="^", color="green", s=200, label="BUY")


sell_signals = data[data["position"] == -1]
plt.scatter(sell_signals.index,
            sell_signals["Close"], marker="v", color="red", s=200, label="SELL")

plt.title("Apple - Moving Average Crossover Strategy")
plt.legend()
plt.grid(True)
plt.show()
