import talib
from backtesting import Strategy


class AdxStrategy(Strategy):
    buy_amount = 0.5

    def setBUY(self, buy):
        self.buy_amount = buy

    @staticmethod
    def name():
        return "ADX"

    def init(self):
        # upmove = self.data.High[-1]- self.data.High[-2]
        # downmove = self.data.Low[-2]- self.data.Low[-1]

        # if upmove > downmove and upmove>0:
        #     self.dmplus = upmove
        # else:
        #     self.dmplus = 0

        # if downmove> upmove and downmove > 0:
        #     self.dmminus = downmove
        # else:
        #     self.dmminus = 0

        # self.atr = talib.ATR(self.data.High, self.data.Low, self.data.Close)

        # self.temp = self.dmplus/self.atr
        # self.sma = talib.SMA(self.temp)

        # self.diplus = self.I(lambda a: 100 * a, self.sma)

        # self.tempplu = self.dmminus/self.atr
        # self.smamin = talib.SMA(self.tempplu)

        # self.diminus = self.I(lambda a: 100 * a, self.smamin)

        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close)
        self.diplus = self.I(
            talib.PLUS_DI, self.data.High, self.data.Low, self.data.Close
        )
        self.diminus = self.I(
            talib.MINUS_DI, self.data.High, self.data.Low, self.data.Close
        )

    def next(self):
        #  One of the best buy signals is when ADX turns up when below both Directional Lines and +DI is above -DI. You would sell when ADX turns back down.[
        if (
            self.adx[-2] < self.adx[-3]
            and self.adx[-1] > self.adx[-2]
            and self.adx[-1] < self.diminus[-1]
            and self.diplus[-1] > self.diminus[-1]
        ):
            if not self.position:
                self.buy(size=self.buy_amount)

        if self.position and self.adx[-1] < self.adx[-2]:
            self.position.close()
