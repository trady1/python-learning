import yfinance as yf
import matplotlib.pyplot as plt

data = yf.download("AAPL", period="3mo")


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))


ax1.plot(data.index, data["Close"], label="Price", color="blue")
ax1.set_title("Apple Stock - Price and Volume")
ax1.set_ylabel("Price (USD)")
ax1.legend()
ax1.grid(True)


ax2.bar(data.index, data["Volume"].squeeze(),
        label="Volume", color="orange", alpha=0.7)
ax2.set_ylabel("Volume")
ax2.set_xlabel("Date")
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()
