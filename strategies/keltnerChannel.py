import talib
from backtesting import Strategy
from backtesting.lib import crossover


class KeltnerStrategy(Strategy):
    buy_amount = 0.01

    def setBUY(self, buy):
        self.buy_amount = buy

    def indicators(self):
        return [self.keltner, self.upline, self.downline]

    def init(self):
        self.typicalprice = self.I(
            lambda a, b, c: (a + b + c) / 3,
            self.data.Close,
            self.data.High,
            self.data.Low,
            plot=False,
        )
        self.keltner = self.I(talib.EMA, self.typicalprice, timeperiod=10)

        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=20,
        )

        self.upline = self.I(lambda a, b: a + 2 * b, self.keltner, self.atr)
        self.downline = self.I(lambda a, b: a - 2 * b, self.keltner, self.atr)

    def next(self):

        if crossover(self.data.Close, self.upline):
            if self.position.is_short:
                self.position.close()

            if not self.position:
                self.buy(size=self.buy_amount)

        elif crossover(self.downline, self.data.Close):
            if self.position.is_long:
                self.position.close()

            if not self.position:
                self.sell(size=self.buy_amount)
