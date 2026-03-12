import talib
from backtesting import Strategy


class UltimateOscStrategy(Strategy):
    buy_amount = 0.01

    # states
    bull_state = 0
    bear_state = 0

    def setBUY(self, buy):
        self.buy_amount = buy

    def indicators(self):
        return [self.ult]

    def init(self):

        self.ult = self.I(talib.ULTOSC, self.data.High, self.data.Low, self.data.Close)

        self.first_low_price = None
        self.first_low_osc = None
        self.div_high = None
        self.oversold_seen = False

        self.first_high_price = None
        self.first_high_osc = None
        self.div_low = None
        self.overbought_seen = False

    def next(self):

        price = self.data.Close[-1]
        osc = self.ult[-1]

        if self.bull_state == 0:
            if (
                self.data.Close[-2] < self.data.Close[-3]
                and self.data.Close[-2] < price
            ):
                self.first_low_price = self.data.Close[-2]
                self.first_low_osc = self.ult[-2]
                self.div_high = self.ult[-2]
                self.oversold_seen = self.ult[-2] < 30
                self.bull_state = 1

        # second lower low
        elif self.bull_state == 1:
            if osc < 30:
                self.oversold_seen = True

            self.div_high = max(self.div_high, osc)

            if (
                price < self.first_low_price
                and osc > self.first_low_osc
                and self.oversold_seen
            ):
                self.bull_state = 2

        # breakout trigger
        elif self.bull_state == 2:
            if osc > self.div_high:
                if self.position.is_short:
                    self.position.close()

                if not self.position:
                    self.buy(size=self.buy_amount)

                self.bull_state = 0

        # first high
        if self.bear_state == 0:
            if (
                self.data.Close[-2] > self.data.Close[-3]
                and self.data.Close[-2] > price
            ):
                self.first_high_price = self.data.Close[-2]
                self.first_high_osc = self.ult[-2]
                self.div_low = self.ult[-2]
                self.overbought_seen = self.ult[-2] > 70
                self.bear_state = 1

        # second higher high
        elif self.bear_state == 1:
            if osc > 70:
                self.overbought_seen = True

            self.div_low = min(self.div_low, osc)

            if (
                price > self.first_high_price
                and osc < self.first_high_osc
                and self.overbought_seen
            ):
                self.bear_state = 2

        # breakout trigger
        elif self.bear_state == 2:
            if osc < self.div_low:
                if self.position.is_long:
                    self.position.close()

                if not self.position:
                    self.sell(size=self.buy_amount)

                self.bear_state = 0
