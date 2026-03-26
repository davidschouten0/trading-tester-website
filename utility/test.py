import numpy as np
import yfinance as yf
from backtesting import Backtest

from utility.strat_switcher import get_strategy

historic_data = yf.download("AAPL", period="ytd", interval="1h")
historic_data = (
    historic_data.droplevel("Ticker", axis=1).reset_index().set_index("Datetime")
)
historic_data = historic_data[["Open", "High", "Low", "Close", "Volume"]]

bt = Backtest(
    historic_data, get_strategy("Stochastic"), cash=100000, commission=(0.2, 0)
)


results = bt.run()

strategy = results["_strategy"]
indicator_list = strategy.indicators()

# indicator_data = {}
# for i, ind in enumerate(indicator_list):
#     # Convert to list for JSON serialization, handle NaNs
#     values = [None if np.isnan(v) else v for v in ind]
#     indicator_data[f"indicator_{i}"] = values

print(indicator_list)
