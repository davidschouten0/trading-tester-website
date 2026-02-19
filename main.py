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
    switcher[strat].setBUY(switcher[strat], buy=800)

    bt = Backtest(
        data, switcher[strat], cash=10000, commission=0.002, finalize_trades=True
    )

    strat = bt.run()
    print(strat)
    bt.plot()
    # data['SMA_50'] = data['Close'].rolling(window=50).mean()
    # data['SMA_200'] = data['Close'].rolling(window=200).mean()
    # data['signal'] = np.where(data['SMA_50'] > data['SMA_200'], 1, 0)


if __name__ == "__main__":
    main()
