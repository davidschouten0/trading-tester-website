# above -20 -> overbough
# below -80 -> oversold
#   but buy oversold when %R == -100, and 5 days since -100% reached, %R rises above -95 or -85
#
import talib
from backtesting import Strategy


class WilliamsStrategy(Strategy):
    buy_amount = 0.01
    days_passed_100 = 0
    seen_100 = False
    seen_0 = False
    days_passed_0 = 0

    def setBUY(self, buy):
        self.buy_amount = buy

    def indicators(self):
        return {"williams": self.william}

    def init(self):
        self.william = self.I(
            talib.WILLR, self.data.High, self.data.Low, self.data.Close
        )

    def next(self):
        if self.seen_100:
            self.days_passed_100 += 1

        if self.william[-1] <= -100:
            self.seen_100 = True
            self.days_passed_100 = 0

        if self.seen_0:
            self.days_passed_0 += 1

        if self.william[-1] >= 0:
            self.seen_100 = True
            self.days_passed_0 = 0

        if self.days_passed_100 > 5 and self.william[-1] > -90:
            if self.position.is_short:
                self.position.close()
            self.buy(size=self.buy_amount)

        if self.days_passed_0 > 5 and self.william[-1] < -10:
            if self.position.is_long:
                self.position.close()
            self.sell(size=self.buy_amount)
