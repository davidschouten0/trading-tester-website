import talib
from backtesting import Strategy


class SmaCrossStrategy(Strategy):
    buy_amount = 0.01

    def setBUY(self, buy):
        self.buy_amount = buy

    def init(self):
        self.sma = self.I(talib.SMA, self.data.Close)

    def next(self):

        last_kam = self.sma[-2]
        kam = self.sma[-1]
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
