import talib
from backtesting import Strategy


class SarCrossStrategy(Strategy):
    buy_amount = 0.01

    def setBUY(self, buy):
        self.buy_amount = buy

    def indicators(self):
        return {"sar": self.sar}

    def init(self):
        self.sar = self.I(talib.SAR, self.data.High, self.data.Low, scatter=True)

    def next(self):

        price = self.data.Close

        if price > self.sar[-1] and not self.position.is_long:
            self.position.close()
            self.buy(size=self.buy_amount)
        elif price < self.sar[-1] and not self.position.is_short:
            self.position.close()
            self.sell(size=self.buy_amount)
