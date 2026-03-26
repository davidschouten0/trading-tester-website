import numpy as np
import talib
from backtesting import Strategy
from backtesting.lib import crossover


class DPOStrategy(Strategy):
    buy_amount = 0.01
    period = 20

    def setBUY(self, buy):
        self.buy_amount = buy

    def indicators(self):
        return {"dpo": self.dpo}

    def init(self):
        self.ma = self.I(talib.SMA, self.data.Close, timeperiod=50)

        period = self.period
        shift = int(period / 2 + 1)

        sma = self.I(talib.SMA, self.data.Close, timeperiod=period)

        def dpo(close, sma):
            result = np.empty_like(close)
            result[:] = np.nan
            result[shift:] = close[:-shift] - sma[shift:]
            return result

        self.dpo = self.I(dpo, self.data.Close, sma)

    def next(self):
        price = self.data.Close[-1]

        if crossover(self.dpo, 0) and price > self.ma[-1]:
            if self.position.is_short:
                self.position.close()

            if not self.position:
                self.buy(size=self.buy_amount)

        elif crossover(0, self.dpo) and price < self.ma[-1]:
            if self.position.is_long:
                self.position.close()

            if not self.position:
                self.sell(size=self.buy_amount)
