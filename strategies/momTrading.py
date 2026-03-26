import talib
from backtesting import Strategy

# ! wouldnt mind being able to set different time periods


class MomentumCrossStrategy(Strategy):
    buy_amount = 0.01

    def setBUY(self, buy):
        self.buy_amount = buy

    def indicators(self):
        return {"roc": self.roc, "rsi": self.rsi, "std": self.std, "avroc": self.avroc}

    def init(self):
        self.roc = self.I(talib.ROC, self.data.Close)
        self.rsi = self.I(talib.RSI, self.data.Close)
        self.std = self.I(talib.STDDEV, self.roc, timeperiod=20)
        self.avroc = self.I(talib.SMA, self.roc, timeperiod=20)
        self.zscore = (self.roc - self.avroc) / self.std

    def next(self):
        if self.rsi[-1] > 50 and self.zscore[-1] > self.zscore[-2]:
            # check if rsi is going against or with prices up
            if self.rsi[-1] < 55:
                self.position.close()
            else:
                if self.position.size == 0 or self.position.is_short:
                    self.position.close()
                    self.buy(size=self.buy_amount)

            # if min(self.rsi[-1], self.rsi[-2], self.rsi[-3]) == self.rsi[-2] and self.rsi[-2] < self.lowest_low:
            #     self.lowest_low = self.rsi[-2]
            # elif min(self.rsi[-1], self.rsi[-2], self.rsi[-3]) == self.rsi[-2] and self.rsi[-2] > self.lowest_low:
            #     #higher low
            # else:
            # self.lowest_low = 50

        elif self.rsi[-1] < 50 and self.zscore[-1] < self.zscore[-2]:
            if self.rsi[-1] > 45:
                self.position.close()
            else:
                if self.position.size == 0 or self.position.is_short:
                    self.position.close()
                    self.sell(size=self.buy_amount)
        elif self.rsi[-1] > 45 and self.rsi[-1] < 55:
            self.position.close()
