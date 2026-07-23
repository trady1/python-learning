import yfinance as yf
import mplfinance as mpf

data = yf.download("AAPL", period="3mo")


data.columns = data.columns.get_level_values(0)

mpf.plot(data, type="candle", volume=True,
         title="Apple Stock - Candlestick Chart", style="yahoo")
