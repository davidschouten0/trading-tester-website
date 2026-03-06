import talib
from backtesting import Strategy


class BollingerSqueezeStrategy(Strategy):
    buy_amount = 0.01

    squeeze_lookback = 20
    breakout_lookback = 10

    def setBUY(self, buy):
        self.buy_amount = buy

    @staticmethod
    def name():
        return "BollingerSqueeze"

    def init(self):

        self.highbband, self.midbband, self.lowbband = self.I(
            talib.BBANDS, self.data.Close, timeperiod=20
        )
        self.distance = self.highbband - self.lowbband

        self.squeeze = False

    def next(self):
        recent_widths = self.distance[-self.squeeze_lookback :]

        if self.distance[-1] <= min(recent_widths):
            self.squeeze = True

        if self.squeeze:
            # Bull
            if self.data.Close[-1] > self.highbband[-1]:
                if self.position.is_short:
                    self.position.close()

                if not self.position:
                    self.buy(size=self.buy_amount)

                self.squeeze = False

            # Bear
            elif self.data.Close[-1] < self.lowbband[-1]:
                if self.position.is_long:
                    self.position.close()

                if not self.position:
                    self.sell(size=self.buy_amount)

                self.squeeze = False
