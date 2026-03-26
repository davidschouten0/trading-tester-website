import talib
from backtesting import Strategy


class RSICrossStrategy(Strategy):
    buy_amount = 0.01

    def setBUY(self, buy):
        self.buy_amount = buy

    def indicators(self):
        return {"rsi": self.rsi}

    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close)

    def next(self):
        if self.rsi[-1] >= 70:
            if self.position.is_long:
                self.position.close()
            self.sell(size=self.buy_amount)
        elif self.rsi[-1] <= 30:
            if self.position.is_short:
                self.position.close()
            self.buy(size=self.buy_amount)
