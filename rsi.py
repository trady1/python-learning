import yfinance as yf
import matplotlib.pyplot as plt
import ta

data = yf.download("AAPL", period="6mo")
data.columns = data.columns.get_level_values(0)


data["RSI"] = ta.momentum.RSIIndicator(data["Close"]).rsi()


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

ax1.plot(data.index, data["Close"], label="Price", color="blue")
ax1.set_title("Apple Stock - Price and RSI")
ax1.legend()
ax1.grid(True)

ax2.plot(data.index, data["RSI"], label="RSI", color="purple")
ax2.axhline(70, color="red", linestyle="--", label="Overbought (70)")
ax2.axhline(30, color="green", linestyle="--", label="Oversold (30)")
ax2.set_ylabel("RSI")
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()
