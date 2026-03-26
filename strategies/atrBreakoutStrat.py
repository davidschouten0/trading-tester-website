import talib
from backtesting import Strategy


class ATRBreakoutStrategy(Strategy):
    buy_amount = 0.01

    def setBUY(self, buy):
        self.buy_amount = buy

    def indicators(self):
        return {"atr": self.atr}

    def init(self):
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close)

    def next(self):
        last_close = self.data.Close[-2]
        last_close += self.atr[-2]

        if self.data.Close[-1] > last_close:
            self.buy(size=self.buy_amount)

        last_close -= 2 * self.atr[-2]

        if self.data.Close[-1] < last_close:
            self.position.close()
