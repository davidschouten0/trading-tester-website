from backtesting import Backtest, Strategy
from backtesting.lib import crossover 
from backtesting.test import SMA

import pandas as pd
import numpy as np
import yfinance as yf

data = yf.download('RYLPF', period='20y', interval='1d')
data.columns = [col[0] for col in data.columns]

class SmaCrossStrategy(Strategy):
    def init(self):
        self.sma50 = self.I(SMA, self.data.Close, 50)
        self.sma200 = self.I(SMA, self.data.Close, 200)

    def next(self):
        sma50_today = self.sma50[-1]
        sma200_today = self.sma200[-1]

        is_bullish = sma50_today > sma200_today
        if is_bullish and not self.position:
            self.buy(size=0.95)
        elif not is_bullish and self.position:
            self.position.close()

print(data)

bt = Backtest(data, SmaCrossStrategy, cash=10000, commission=0.002, finalize_trades=True)
strat = bt.run()
print(strat)
bt.plot()
# data['SMA_50'] = data['Close'].rolling(window=50).mean()
# data['SMA_200'] = data['Close'].rolling(window=200).mean()
# data['signal'] = np.where(data['SMA_50'] > data['SMA_200'], 1, 0)