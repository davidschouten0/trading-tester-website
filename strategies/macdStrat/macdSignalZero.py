import talib
from backtesting import Strategy


# ! wouldnt mind being able to set different time periods
class MACDSignalZeroCrossStrategy(Strategy):
    buy_amount = 0.01

    def setBUY(self, buy):
        self.buy_amount = buy

    def indicators(self):
        return {"macd": self.macd, "signal": self.signal}

    def init(self):
        self.fastema = self.I(talib.EMA, self.data.Close, timeperiod=12)
        self.slowema = self.I(talib.EMA, self.data.Close, timeperiod=26)
        self.macd = self.fastema - self.slowema
        self.signal = self.I(talib.EMA, self.macd, timeperiod=9)

    def next(self):
        if self.signal[-1] > 0 and self.signal[-2] <= 0:
            if self.position.is_long:
                self.position.close()
            self.sell(size=self.buy_amount)
        elif self.signal[-1] < 0 and self.signal[-2] >= 0:
            if self.position.is_short:
                self.position.close()
            self.buy(size=self.buy_amount)
