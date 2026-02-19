import talib
from backtesting import Strategy


class KamaCrossStrategy(Strategy):
    buy_amount = 500

    def setBUY(self, buy):
        self.buy_amount = buy

    def init(self):
        self.kama = self.I(talib.KAMA, self.data.Close, timeperiod=30)

    def next(self):

        last_kam = self.kama[-2]
        kam = self.kama[-1]
        last_close = self.data.Close[-2]
        close = self.data.Close[-1]
        above = None
        if last_kam - kam < 1.5 and last_kam - kam > -1.5:
            ...
        else:
            if last_close <= last_kam and kam < close:
                above = True
            if last_close >= last_kam and kam > close:
                above = False

            if above:
                self.buy(size=self.buy_amount)
            elif not above and self.position:
                self.position.close
