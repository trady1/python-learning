import yfinance as yf


tickers = ["AAPL", "GOOGL", "MSFT", "TSLA"]
data = yf.download(tickers, period="3mo")["Close"]


returns = data.pct_change() * 100


for ticker in tickers:
    total = ((data[ticker].iloc[-1] - data[ticker].iloc[0]) /
             data[ticker].iloc[0]) * 100
    print(f"{ticker}: {float(total):.2f}%")

portfolio_return = sum([23.10, 5.14, -5.66, -1.63]) / 4
print(f"Portfolio return: {portfolio_return:.2f}%")
