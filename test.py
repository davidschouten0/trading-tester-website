from backtesting import Backtest, Strategy
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
import plotly.io as pio
import json
import pandas as pd

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


    data.ta.sma(length=sma_short, append=True, col_names=('SMA_short',))
    data.ta.sma(length=sma_long, append=True, col_names=('SMA_long',))

    data = data.dropna()
    
    SmaCrossStrategy.n1 = sma_short
    SmaCrossStrategy.n2 = sma_long

    bt = Backtest(data, SmaCrossStrategy,
                  cash=start_cash,
                  commission=0.002,
                  finalize_trades=True)

    stats = bt.run()

    bt.plot()

    print(data)
    print(stats)

    return stats, data

stats, data = run_my_backtest("AAPL", 50, 200, 10000)

if stats is None:
    print("Fehler: Ticker nicht gefunden oder keine Daten.")

trades = stats._trades

fig = go.Figure()

# --- Ebene 1: Candlestick-Chart ---
fig.add_trace(go.Candlestick(
    x=data.index,
    open=data['Open'],
    high=data['High'],
    low=data['Low'],
    close=data['Close'],
    name='Candlesticks'
))

# --- Ebene 2: SMA-Linien ---
fig.add_trace(go.Scatter(
    x=data.index, 
    y=data['SMA_short'], 
    name=f'SMA {50}', 
    mode='lines',
    line=dict(color='blue', width=1.5)
))
fig.add_trace(go.Scatter(
    x=data.index, 
    y=data['SMA_long'], 
    name=f'SMA {200}', 
    mode='lines',
    line=dict(color='orange', width=1.5)
))

# --- Ebene 3: Kauf-/Verkaufs-Pfeile ---
# Trenne Kauf- und Verkaufs-Trades für saubere Plots
buy_trades = trades[trades['Size'] > 0]
sell_trades = trades[trades['Size'] < 0]

fig.add_trace(go.Scatter(
    x=buy_trades['EntryTime'],
    y=buy_trades['EntryPrice'] * 0.98, # Platziere Pfeil knapp unter der Kerze
    name='Kauf-Signal',
    mode='markers',
    marker_symbol='triangle-up',
    marker_color='green',
    marker_size=10
))
fig.add_trace(go.Scatter(
    x=sell_trades['EntryTime'], # HINWEIS: Bei 'close_position' ist EntryTime die ExitTime
    y=sell_trades['EntryPrice'] * 1.02, # Platziere Pfeil knapp über der Kerze
    name='Verkauf-Signal',
    mode='markers',
    marker_symbol='triangle-down',
    marker_color='red',
    marker_size=10
))

# --- Ebene 4: Hintergrund-Zonen (Profit/Loss) ---
for index, trade in trades.iterrows():
    fig.add_shape(
        type="rect",
        # Zeit-Achse (X)
        x0=trade['EntryTime'],
        x1=trade['ExitTime'],
        # Preis-Achse (Y)
        y0=trade['EntryPrice'],
        y1=trade['ExitPrice'],
        fillcolor='green' if trade['PnL'] > 0 else 'red',
        opacity=0.2,
        layer='below', # Hinter die Kerzen legen
        line_width=0
    )

# --- Mach es hübsch (Dark Mode) ---
fig.update_layout(
    title=f'Backtest: AAPL (SMA sma/smal)',
    template="plotly_dark",
    xaxis_title='Datum',
    yaxis_title='Preis (USD)',
    xaxis_rangeslider_visible=False # Deaktiviert den kleinen "Slider"
)

fig.show()

# 4. DIE MAGIE (TEIL 2): In JSON umwandeln
chart_json = fig.to_json()

roundtrip = pio.from_json(chart_json)
roundtrip.show()



# Wandle die Statistik-Tabelle (ein pd.Series) in ein Dictionary um
# Wir runden die Werte für eine saubere Anzeige
stats_dict = stats.to_dict()
stats_dict_rounded = {k: (f"{v:.2f}" if isinstance(v, float) else v) for k, v in stats_dict.items()}
