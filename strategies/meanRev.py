import talib
from backtesting import Strategy


class MeanRevCrossStrategy(Strategy):
    buy_amount = 0.01

    def setBUY(self, buy):
        self.buy_amount = buy

    @staticmethod
    def name():
        return "MeanRev"

    def init(self):
        self.ma50 = self.I(talib.MA, self.data.Close, timeperiod=50)
        self.ma100 = self.I(talib.MA, self.data.Close, timeperiod=100)

    def next(self):
        close = self.data.Close[-1]
        last_ma100 = self.ma100[-2]
        ma100 = self.ma100[-1]

        golden_cross = (last_ma50 <= last_ma100) and (ma50 > ma100)

        death_cross = (last_ma50 >= last_ma100) and (ma50 < ma100)

        if golden_cross:
            if self.position.is_short:
                self.position.close()
            self.buy(size=self.buy_amount)

        elif death_cross:
            if self.position.is_long:
                self.position.close()
            self.sell(size=self.buy_amount)
