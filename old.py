import numpy as np
import pandas as pd
import talib
import yfinance as yf
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

# data = yf.download("RYLPF", period="20y", interval="1d")
# data.columns = [col[0] for col in data.columns]
small_data = yf.download("GOOG", period="5y", interval="1d")
small_data.columns = [col[0] for col in small_data.columns]
small_data = small_data[["Open", "High", "Low", "Close", "Volume"]]


user_input = None
strategy = None
while user_input != 1 and user_input != 2 and user_input != 3:
    user_input = input("Which strategy are we testing today? (KAMA(1), SMA(2), AMV(3))")


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


class KamaStrat(Strategy):
    timeperiod = 30

    def init(self):
        self.kama = self.I(talib.MAMA, self.data.Close, timeperiod=self.timeperiod)

        # list = []
        # for date in small_data.index:
        #    for data in small_data.loc[date].at["Close"]:
        #        list.append(data)
        # small_data["Close"].to_numpy(dtype=np.float64)
        # close_prices = np.array(list, dtype=np.float64)
        # print(close_prices)
        # self.kama = talib.KAMA(close_prices, timeperiod=10)
        # print(self.kama)

    def next(self):
        if len(self.data) < self.timeperiod + 1:
            return

        # Current and previous values
        current_close = self.data.Close[-1]
        previous_close = self.data.Close[-2]
        current_kama = self.kama[-1]
        previous_kama = self.kama[-2]

        # Manual crossover check: price crosses ABOVE KAMA
        cross_above = (previous_close <= previous_kama) and (
            current_close > current_kama
        )

        # Manual crossover check: price crosses BELOW KAMA
        cross_below = (previous_close >= previous_kama) and (
            current_close < current_kama
        )

        if cross_above:
            if not self.position:
                self.buy(size=0.95)

        elif cross_below:
            if self.position:
                self.position.close()


class AdaptiveMomentumVolatility(Strategy):
    risk_per_trade = 0.95  # 2% of capital per trade

    def init(self):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low

        # Indicators
        self.kama = self.I(talib.KAMA, close, timeperiod=30)
        self.rsi = self.I(talib.RSI, close, timeperiod=14)
        self.adx = self.I(talib.ADX, high, low, close, timeperiod=14)
        self.atr = self.I(talib.ATR, high, low, close, timeperiod=14)

    def next(self):
        if len(self.data) < 30:
            return

        close = self.data.Close[-1]
        kama = self.kama[-1]
        rsi = self.rsi[-1]
        adx = self.adx[-1]
        atr = self.atr[-1]

        # Risk-based position sizing
        capital = self.equity
        risk_amount = capital * self.risk_per_trade
        stop_loss = atr * 2
        position_size = risk_amount / stop_loss if stop_loss > 0 else 0

        # Conditions
        bullish = close > kama and rsi > 55 and adx > 25 and atr / close < 0.05
        bearish = close < kama or rsi < 45 or adx < 20

        # Entries
        if bullish and not self.position:
            if position_size > 0 and 1.1 > position_size:
                self.buy(size=position_size)
            else:
                self.buy(size=self.risk_per_trade)
        # Exits
        elif bearish and self.position:
            self.position.close()


if user_input == 1:
    strategy = KamaStrat
elif user_input == 2:
    strategy = SmaCrossStrategy
else:
    strategy = AdaptiveMomentumVolatility

if small_data is not None:
    bt = Backtest(
        small_data,
        strategy,
        cash=100000,  # Starting capital
        commission=0.002,  # e.g., 0.2% per trade
        exclusive_orders=True,  # Avoid multiple orders on same bar
    )
stats = bt.run()
print(stats)
bt.plot()
# print(data)

# bt = Backtest(
#    data, SmaCrossStrategy, cash=10000, commission=0.002, finalize_trades=True
# )
# strat = bt.run()
# print(strat)
# bt.plot()
# data['SMA_50'] = data['Close'].rolling(window=50).mean()
# data['SMA_200'] = data['Close'].rolling(window=200).mean()
# data['signal'] = np.where(data['SMA_50'] > data['SMA_200'], 1, 0)
