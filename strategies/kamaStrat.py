import talib
from backtesting import Strategy


class KamaCrossStrategy(Strategy):
    buy_amount = 0.01

    def setBUY(self, buy):
        self.buy_amount = buy

    def name(self):
        return "kama"

    def init(self):
        self.kama = self.I(talib.KAMA, self.data.Close)

    def next(self):
        last_kam = self.kama[-2]
        kam = self.kama[-1]
        last_close = self.data.Close[-2]
        close = self.data.Close[-1]

        cross_above = (last_close <= last_kam) and (close > kam)

        cross_below = (last_close >= last_kam) and (close < kam)

        if cross_above:
            if self.position.is_short:
                self.position.close()
            self.buy(size=self.buy_amount)

        elif cross_below:
            if self.position.is_long:
                self.position.close()
            self.sell(size=self.buy_amount)
