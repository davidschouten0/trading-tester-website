import talib
from backtesting import Strategy
from backtesting.lib import crossover


class TEMACrossStrategy(Strategy):
    buy_amount = 0.01

    def setBUY(self, buy):
        self.buy_amount = buy

    @staticmethod
    def name():
        return "TEMA"

    def init(self):
        self.tema = self.I(talib.TEMA, self.data.Close)

    def next(self):

        if crossover(self.data.Close, self.tema):
            if self.position.is_short:
                self.position.close()
            self.buy(size=self.buy_amount)

        elif crossover(self.tema, self.data.Close):
            if self.position.is_long:
                self.position.close()
            self.sell(size=self.buy_amount)
