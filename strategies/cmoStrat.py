import talib
from backtesting import Strategy
from backtesting.lib import crossover


class CMOStrategy(Strategy):
    buy_amount = 0.01

    def setBUY(self, buy):
        self.buy_amount = buy

    def indicators(self):
        return [self.cmo, self.signal50, self.signal200]

    def init(self):
        self.cmo = self.I(talib.CMO, self.data.Close)
        self.signal50 = self.I(talib.SMA, self.data.Close, timeperiod=50)
        self.signal200 = self.I(talib.SMA, self.data.Close, timeperiod=200)

    def next(self):
        if (
            crossover(self.signal50, self.signal200)
            and self.cmo[-1] > 0
            and not self.position.is_long
        ):
            if self.position.is_short:
                self.position.close()
            self.buy(size=self.buy_amount)
        elif (
            crossover(self.signal200, self.signal50)
            and self.cmo[-1] < 0
            and not self.position.is_short
        ):
            if self.position.is_long:
                self.position.close()
            self.sell(size=self.buy_amount)
