import talib
from backtesting import Strategy
from backtesting.lib import crossover


class MACDStrategy(Strategy):
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

        # classic macd trade, macd cross signal
        if crossover(self.macd, self.signal):
            self.position.close()
            self.buy(size=self.buy_amount)
        elif crossover(self.signal, self.macd):
            self.position.close()
            self.sell(size=self.buy_amount)
