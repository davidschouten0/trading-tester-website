import numpy as np
import pandas as pd
import talib
from backtesting import Strategy
from backtesting.lib import crossover


class IchimokuCloudStrategy(Strategy):
    buy_amount = 0.01

    def setBUY(self, buy):
        self.buy_amount = buy

    def indicators(self):
        return {
            "tenkan": self.tenkan,
            "kijun": self.kijun,
            "senkouA_lead": self.senkouA_lead,
            "senkouB_lead": self.senkouB_lead,
        }
        # idk if need pass self.senkouA, self.senkouB,

    def init(self):
        high = self.data.High
        low = self.data.Low

        # Tenkan
        high9 = self.I(talib.MAX, high, timeperiod=9, plot=False)
        low9 = self.I(talib.MIN, low, timeperiod=9, plot=False)

        # Kijun
        high26 = self.I(talib.MAX, high, timeperiod=26, plot=False)
        low26 = self.I(talib.MIN, low, timeperiod=26, plot=False)

        self.tenkan = self.I(lambda a, b: (a + b) / 2, high9, low9, name="tenkan")
        self.kijun = self.I(lambda a, b: (a + b) / 2, high26, low26, name="kijun")

        # Senkou spans (no shift for trading)
        high52 = self.I(talib.MAX, high, timeperiod=52, plot=False)
        low52 = self.I(talib.MIN, low, timeperiod=52, plot=False)

        self.senkouA = self.I(lambda a, b: (a + b) / 2, self.tenkan, self.kijun)
        self.senkouB = self.I(lambda a, b: (a + b) / 2, high52, low52)

        self.senkouA_lead = self.I(
            lambda x: pd.Series(x).shift(26).values,
            (self.tenkan + self.kijun) / 2,
            name="Senkou A",
            overlay=True,
        )
        self.senkouB_lead = self.I(
            lambda x: pd.Series(x).shift(26).values,
            (high52 + low52) / 2,
            name="Senkou B",
            overlay=True,
        )

    def next(self):
        if np.isnan(self.senkouA_lead[-1]) or np.isnan(self.senkouB_lead[-1]):
            return

        price = self.data.Close[-1]

        cloud_top = max(self.senkouA_lead[-1], self.senkouB_lead[-1])
        cloud_bottom = min(self.senkouA_lead[-1], self.senkouB_lead[-1])

        if price < cloud_top and price > cloud_bottom:
            self.position.close()
        elif (
            price > cloud_top
            and self.senkouA_lead[-1] > self.senkouB_lead[-1]
            and self.tenkan[-1] > self.kijun[-1]
        ):
            if not self.position.is_long:
                self.position.close()
                self.buy(size=self.buy_amount)

        elif (
            price < cloud_bottom
            and self.senkouA_lead[-1] < self.senkouB_lead[-1]
            and self.tenkan[-1] < self.kijun[-1]
        ):
            if not self.position.is_short:
                self.position.close()
                self.sell(size=self.buy_amount)

    #     min9, max9 = (
    #         self.I(talib.MIN, self.data.Low, timeperiod=9, plot=False),
    #         self.I(talib.MAX, self.data.High, timeperiod=9, plot=False),
    #     )
    #     min26, max26 = (
    #         self.I(talib.MIN, self.data.Low, timeperiod=26, plot=False),
    #         self.I(talib.MAX, self.data.High, timeperiod=26, plot=False),
    #     )
    #     min52, max52 = (
    #         self.I(talib.MIN, self.data.Low, timeperiod=52, plot=False),
    #         self.I(talib.MAX, self.data.High, timeperiod=52, plot=False),
    #     )

    #     self.tenkan = self.I(lambda a, b: (a + b) / 2, max9, min9, name="tenkan")
    #     self.kijun = self.I(lambda a, b: (a + b) / 2, max26, min26, name="kijun")

    #     self.chikou = self.I(
    #         lambda c: pd.Series(c).shift(26).values,
    #         self.data.Close,
    #         name="Chikou",
    #         overlay=True,
    #     )

    #     self.senkouA = (self.tenkan + self.kijun) / 2
    #     self.senkouB = (max52 + min52) / 2

    #     self.senkouA_lead = self.I(
    #         lambda x: pd.Series(x).shift(-26).values,
    #         (self.tenkan + self.kijun) / 2,
    #         name="Senkou A",
    #         overlay=True,
    #     )
    #     self.senkouB_lead = self.I(
    #         lambda x: pd.Series(x).shift(-26).values,
    #         (max52 + min52) / 2,
    #         name="Senkou B",
    #         overlay=True,
    #     )

    # def next(self):

    #     cloud_top = max(self.senkouA[-1], self.senkouB[-1])
    #     cloud_bottom = min(self.senkouA[-1], self.senkouB[-1])

    #     if crossover(self.tenkan, self.kijun) and self.data.Close[-1] > cloud_top:
    #         self.position.close()
    #         self.buy(size=self.buy_amount)

    #     elif crossover(self.kijun, self.tenkan) and self.data.Close[-1] < cloud_bottom:
    #         self.position.close()
    #         self.sell(size=self.buy_amount)

    #     if self.senkouA_lead > self.data.Close and self.senkouB_lead < self.data.Close:
    #         self.position.close()
    #     else:
    #         if (
    #             crossover(self.tenkan[-1], self.kijun[-1])
    #             and self.senkouA_lead > self.senkouB_lead
    #         ):
    #             if self.position.is_short:
    #                 self.position.close()
    #             self.buy(size=self.buy_amount)
    #         elif (
    #             crossover(self.kijun[-1], self.tenkan[-1])
    #             and self.senkouA_lead < self.senkouB_lead
    #         ):
    #             if self.position.is_long:
    #                 self.position.close()
    #             self.sell(size=self.buy_amount)
