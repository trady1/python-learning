import yfinance as yf

data = yf.download("AAPL", period="6mo")
data.columns = data.columns.get_level_values(0)

data["MA20"] = data["Close"].rolling(window=20).mean()
data["MA50"] = data["Close"].rolling(window=50).mean()

data["signal"] = 0
data.loc[data["MA20"] > data["MA50"], "signal"] = 1


data["daily_return"] = data["Close"].pct_change()


data["strategy_return"] = data["daily_return"] * data["signal"].shift(1)


buy_and_hold = (1 + data["daily_return"]).prod() - 1
strategy = (1 + data["strategy_return"]).prod() - 1

print(f"Buy and Hold return: {buy_and_hold * 100:.2f}%")
print(f"Strategy return:     {strategy * 100:.2f}%")
