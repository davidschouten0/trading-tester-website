# In backtest_engine.py

from backtesting import Backtest, Strategy
import yfinance as yf
import pandas as pd
import pandas_ta as ta

class SmaCrossStrategy(Strategy):
    n1 = 50
    n2 = 200

    def init(self):
        self.sma1 = self.I(lambda: self.data.SMA_short, name=f"SMA({self.n1})")
        self.sma2 = self.I(lambda: self.data.SMA_long, name=f"SMA({self.n2})")

    def next(self):
        sma1_today = self.sma1[-1]
        sma2_today = self.sma2[-1]

        is_bullish = sma1_today > sma2_today

        if is_bullish and not self.position:
            self.buy(size=0.95) # Benutze 95% des Kapitals
        
        elif not is_bullish and self.position:
            self.position.close()


def run_my_backtest(ticker, sma_short, sma_long, start_cash):
    
    data = yf.download(ticker, period='20y', interval='1d')
    if data.empty:
        print(f"Keine Daten für Ticker {ticker} gefunden.")
        return None, None

    #Sanatizing yfinance data for plotly
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] for col in data.columns]
    data.columns = [col.capitalize() for col in data.columns]


    data.ta.sma(close=data["Close"], length=sma_short, append=True, col_names=('SMA_short',))
    data.ta.sma(close=data["Close"], length=sma_long, append=True, col_names=('SMA_long',))

    data = data.dropna()
    
    SmaCrossStrategy.n1 = sma_short
    SmaCrossStrategy.n2 = sma_long

    bt = Backtest(data, SmaCrossStrategy,
                  cash=start_cash,
                  commission=0.002,
                  finalize_trades=True)

    stats = bt.run()

    return stats, data