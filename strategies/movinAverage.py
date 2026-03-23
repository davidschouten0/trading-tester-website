import talib
from backtesting import Strategy
from backtesting.lib import crossover


# ! wouldnt mind being able to set different time periods
class MovinAverageCrossStrategy(Strategy):
    buy_amount = 0.01

    def setBUY(self, buy):
        self.buy_amount = buy

    def indicators(self):
        return [self.shortAvg, self.longAvg]

    def init(self):
        self.shortAvg = self.I(talib.MA, self.data.Close, timeperiod=50)
        self.longAvg = self.I(talib.MA, self.data.Close, timeperiod=200)

    def next(self):
        golden_cross = crossover(self.shortAvg, self.longAvg)

        death_cross = crossover(self.longAvg, self.shortAvg)

        if golden_cross:
            if self.position.is_short:
                self.position.close()
            self.buy(size=self.buy_amount)

        elif death_cross:
            if self.position.is_long:
                self.position.close()
            self.sell(size=self.buy_amount)
