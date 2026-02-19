from backtesting import Backtest

import datarequest
import strategies.kamaStrat as kma
import strategies.smaStrat as sma


def main():
    symbol = input("Enter a symbol: ")
    data = datarequest.request(symbol)

    strat = input("Which strategy are we testing today? (KAMA(1), SMA(2), AMV(3))")

    switcher = {
        "1": kma.KamaCrossStrategy,
        "2": sma.SmaCrossStrategy,
    }
    switcher[strat].setBUY(switcher[strat], buy=0.04)

    bt = Backtest(data, switcher[strat], cash=100000, commission=(0.2, 0))

    strat = bt.run()
    print(strat)
    bt.plot(filename="plots/" + str(switcher[strat].name()))


if __name__ == "__main__":
    main()
