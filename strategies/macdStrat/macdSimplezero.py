import talib
from backtesting import Strategy


# ! wouldnt mind being able to set different time periods
class MACDzeroCrossStrategy(Strategy):
    buy_amount = 0.01

    def setBUY(self, buy):
        self.buy_amount = buy

    def indicators(self):
        return [self.macd]

    def init(self):
        self.fastema = self.I(talib.EMA, self.data.Close, timeperiod=12)
        self.slowema = self.I(talib.EMA, self.data.Close, timeperiod=26)
        self.macd = self.fastema - self.slowema

    def next(self):
        if self.macd[-1] > 0 and self.macd[-2] <= 0:
            if self.position.is_long:
                self.position.close()
            self.sell(size=self.buy_amount)
        elif self.macd[-1] < 0 and self.macd[-2] >= 0:
            if self.position.is_short:
                self.position.close()
            self.buy(size=self.buy_amount)
