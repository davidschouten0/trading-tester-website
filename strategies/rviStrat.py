import numpy as np
from backtesting import Strategy
from backtesting.lib import crossover


class RVIStrategy(Strategy):
    buy_amount = 0.01
    period = 10

    def setBUY(self, buy):
        self.buy_amount = buy

    @staticmethod
    def name():
        return "RVI"

    def init(self):

        def rvi_calc(open_, high, low, close, period):

            numerator = close - open_
            denominator = high - low

            denominator = np.where(denominator == 0, 1, denominator)

            value = numerator / denominator

            rvi = np.convolve(value, np.ones(period) / period, mode="same")
            signal = np.convolve(rvi, np.ones(4) / 4, mode="same")

            return rvi, signal

        self.rvi, self.signal = self.I(
            rvi_calc,
            self.data.Open,
            self.data.High,
            self.data.Low,
            self.data.Close,
            self.period,
        )

    def next(self):
        if (
            crossover(self.rvi, self.signal)
            and not self.position.is_long
            and self.rvi[-1] > self.rvi[-2]
            and self.rvi[-2] > self.rvi[-3]
        ):
            if self.position.is_short:
                self.position.close()
            self.buy(size=self.buy_amount)
        elif (
            crossover(self.signal, self.rvi)
            and not self.position.is_short
            and self.rvi[-1] < self.rvi[-2]
            and self.rvi[-2] < self.rvi[-3]
        ):
            if self.position.is_long:
                self.position.close()
            self.sell(size=self.buy_amount)
