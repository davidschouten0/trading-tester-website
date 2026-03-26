import talib
from backtesting import Strategy
from backtesting.lib import cross, crossover


class MeanRevCrossStrategy(Strategy):
    buy_amount = 0.01

    def setBUY(self, buy):
        self.buy_amount = buy

    def indicators(self):
        return {"bollingerlow": self.bollingerlow, "bollingerhigh": self.bollingerhigh, "ma": self.ma}

    def init(self):
        self.bollingerlow = self.I(talib.BBANDS, self.data.Close)[-1]
        self.bollingerhigh = self.I(talib.BBANDS, self.data.Close)[-3]
        self.ma = self.I(talib.MA, self.data.Close, timeperiod=4)

    def next(self):
        print(self.bollingerlow[-1])
        print(self.bollingerhigh[-1])

        if crossover(self.data.Close, self.bollingerhigh):
            if self.position.is_long:
                self.position.close()
            self.sell(size=self.buy_amount)
        elif cross(self.data.Close, self.ma):
            self.position.close()
        elif crossover(self.bollingerlow, self.data.Close):
            if self.position.is_short:
                self.position.close()
            self.buy(size=self.buy_amount)
