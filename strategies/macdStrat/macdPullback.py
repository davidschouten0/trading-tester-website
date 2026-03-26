import talib
from backtesting import Strategy


# ! wouldnt mind being able to set different time periods
class MACDPullbackStrategy(Strategy):
    buy_amount = 0.01

    def setBUY(self, buy):
        self.buy_amount = buy

    def indicators(self):
        return {"macd": self.macd, "sma": self.sma}

    def init(self):
        self.fastema = self.I(talib.EMA, self.data.Close, timeperiod=12)
        self.slowema = self.I(talib.EMA, self.data.Close, timeperiod=26)
        self.macd = self.fastema - self.slowema

        self.sma = self.I(talib.SMA, self.data.Close, timeperiod=20)
        self.trend = None
        self.waiting_pullback = False
        self.pullback_seen = False

    def next(self):
        if self.macd[-1] > 0 and self.macd[-2] <= 0:
            self.trend = "bull"
            self.waiting_pullback = True
            self.pullback_seen = False

        if self.macd[-1] < 0 and self.macd[-2] >= 0:
            self.trend = "bear"
            self.waiting_pullback = True
            self.pullback_seen = False

        if self.trend == "bull" and self.waiting_pullback:
            # price pulls back to MA
            if self.data.Close[-1] <= self.sma[-1]:
                self.pullback_seen = True

            # price resumes upward
            if self.pullback_seen and self.data.Close[-1] > self.sma[-1]:
                if not self.position:
                    self.buy(size=self.buy_amount)

                self.waiting_pullback = False

        if self.trend == "bear" and self.waiting_pullback:
            if self.data.Close[-1] >= self.sma[-1]:
                self.pullback_seen = True

            if self.pullback_seen and self.data.Close[-1] < self.sma[-1]:
                if not self.position:
                    self.sell(size=self.buy_amount)

                self.waiting_pullback = False
