# The Donchian channel is a useful indicator for seeing the volatility of a market price. If a price is stable the Donchian channel will be relatively narrow. If the price fluctuates, a lot the Donchian channel will be wider.

import talib
from backtesting import Strategy


class DonchianStrategy(Strategy):
    buy_amount = 0.01

    def setBUY(self, buy):
        self.buy_amount = buy

    def indicators(self):
        return [self.upper, self.lower, self.middle]

    def init(self):
        self.upper = self.I(talib.MAX, self.data.High, timeperiod=20)
        self.lower = self.I(talib.MIN, self.data.Low, timeperiod=20)
        self.middle = self.I(lambda a, b: (a + b) / 2, self.upper, self.lower)

    def next(self):
        price = self.data.Close[-1]

        if not self.position.is_long and price > self.upper[-2]:
            self.position.close()
            self.buy(size=self.buy_amount)

        if not self.position.is_short and price < self.lower[-2]:
            self.position.close()
            self.sell(size=self.buy_amount)
