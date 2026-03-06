import yfinance as yf
from backtesting import Backtest

import strategies.momTrading as rev

historic_data = yf.download("AAPL", period="ytd", interval="1h")
historic_data = (
    historic_data.droplevel("Ticker", axis=1).reset_index().set_index("Datetime")
)
historic_data = historic_data[["Open", "High", "Low", "Close", "Volume"]]

bt = Backtest(
    historic_data, rev.MomentumCrossStrategy, cash=100000, commission=(0.2, 0)
)
results = bt.run()
print(results)
bt.plot()
