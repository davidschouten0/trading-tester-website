# good trend and reversal indicator

import talib
from backtesting import Strategy
from backtesting.lib import crossover


class TRIXStrategy(Strategy):
    buy_amount = 0.01

    def setBUY(self, buy):
        self.buy_amount = buy

    def indicators(self):
        return {"trix": self.trix, "signal": self.signal, "ma": self.ma}

    def init(self):
        self.trix = self.I(talib.TRIX, self.data.Close)
        self.signal = self.I(talib.SMA, self.trix, timeperiod=9)
        self.ma = self.I(talib.MA, self.data.Close)

    def next(self):

        if (
            crossover(self.trix, self.signal)
            and self.trix[-1] > self.trix[-2]
            and self.data.Close[-1] > self.ma[-1]
            and not self.position.is_long
            and self.trix[-1] > 0
        ):
            if self.position.is_short:
                self.position.close()
            self.buy(size=self.buy_amount)

        elif (
            crossover(self.signal, self.trix)
            and self.trix[-1] < self.trix[-2]
            and self.data.Close[-1] < self.ma[-1]
            and not self.position.is_short
            and self.trix[-1] < 0
        ):
            if self.position.is_long:
                self.position.close()
            self.sell(size=self.buy_amount)
