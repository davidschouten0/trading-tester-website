import numpy as np
from backtesting import Strategy
from backtesting.lib import crossover


class VWAPStrategy(Strategy):
    buy_amount = 0.01

    def setBUY(self, buy):
        self.buy_amount = buy

    def indicators(self):
        return {"vwap": self.vwap}

    def init(self):
        def vwap(close, volume):
            pv = close * volume
            cum_pv = np.cumsum(pv)
            cum_vol = np.cumsum(volume)
            return cum_pv / cum_vol

        self.vwap = self.I(vwap, self.data.Close, self.data.Volume)

    def next(self):
        if crossover(self.data.Close, self.vwap):
            if self.position.is_short:
                self.position.close()
            self.buy(size=self.buy_amount)

        elif crossover(self.vwap, self.data.Close):
            if self.position.is_long:
                self.position.close()
            self.sell(size=self.buy_amount)
