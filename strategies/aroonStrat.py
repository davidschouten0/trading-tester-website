# hoher aroon up wert und kleiner aroon down oder anders herum sind gut um trendstärke zu zeigen!

import talib
from backtesting import Strategy
from backtesting.lib import crossover


class AroonStrategy(Strategy):
    buy_amount = 0.01
    crossedUp = False
    crossedDown = False

    def setBUY(self, buy):
        self.buy_amount = buy

    def indicators(self):
        return [self.aroonUp, self.aroonDown]

    def init(self):
        self.aroonUp, self.aroonDown = self.I(
            talib.AROON, self.data.High, self.data.Low, timeperiod=14
        )

    def next(self):
        if (
            self.crossedUp
            and self.aroonUp[-1] > 60
            and self.aroonDown[-1] < 40
            and not self.position
        ):
            self.buy(size=self.buy_amount)
            self.crossedUp = False
        elif (
            self.crossedDown
            and self.aroonDown[-1] > 60
            and self.aroonUp[-1] < 40
            and not self.position
        ):
            self.sell(size=self.buy_amount)
            self.crossedDown = False

        if crossover(self.aroonUp, self.aroonDown):
            if self.position.is_short:
                self.position.close()
            self.crossedUp = True
            self.crossedDown = False

        elif crossover(self.aroonDown, self.aroonUp):
            if self.position.is_long:
                self.position.close()
            self.crossedDown = True
            self.crossedUp = False
