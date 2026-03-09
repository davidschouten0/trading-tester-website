import talib
from backtesting import Strategy
from backtesting.lib import crossover


class StochasticStrategy(Strategy):
    buy_amount = 0.01

    def setBUY(self, buy):
        self.buy_amount = buy

    @staticmethod
    def name():
        return "Stochastic"

    def init(self):
        last5low = self.I(talib.MIN, self.data.Low, timeperiod=5)
        last5high = self.I(talib.MAX, self.data.High, timeperiod=5)

        self.kpercent = self.I(
            lambda a, b, c: ((a - b) / (c - b)) * 100,
            self.data.Close,
            last5low,
            last5high,
        )

        self.dpercent = self.I(talib.SMA, self.kpercent, timeperiod=3)

    def next(self):

        if crossover(self.kpercent, self.dpercent):
            self.position.close()
            self.buy(size=self.buy_amount)
        elif crossover(self.dpercent, self.kpercent):
            self.position.close()
            self.sell(size=self.buy_amount)
