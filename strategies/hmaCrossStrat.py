# recommends using his moving average for directional signals and not for crossovers which could be distorted by the lag, long when HMA up, short when HMA down | It would make sense to introduce a longer-term moving average to signal trend direction, then only take trades in the direction of the trend.
#
import talib
from backtesting import Strategy
from backtesting.lib import cross


class HMACrossStrategy(Strategy):
    buy_amount = 0.01

    def setBUY(self, buy):
        self.buy_amount = buy

    def indicators(self):
        return [self.hma]

    def init(self):
        self.fasterwma = self.I(talib.WMA, self.data.Close, timeperiod=8)
        self.longwma = self.I(talib.WMA, self.data.Close, timeperiod=16)
        self.midstep = self.I(lambda a, b: 2 * a - b, self.fasterwma, self.longwma)
        self.hma = self.I(talib.WMA, self.midstep, timeperiod=4)

    def next(self):

        if self.hma[-1] > self.hma[-2] and self.data.Close[-1] > self.hma[-1]:
            if self.position.is_short:
                self.position.close()
            self.buy(size=self.buy_amount)

        elif self.hma[-1] < self.hma[-2] and self.data.Close[-1] < self.hma[-1]:
            if self.position.is_long:
                self.position.close()
            self.sell(size=self.buy_amount)
