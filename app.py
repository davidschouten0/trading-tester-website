# In app.py

from flask import Flask, render_template, request, redirect, url_for
from backtest_engine import run_my_backtest # Importiere dein "Gehirn"
import plotly.graph_objects as go
import json
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/run_backtest', methods=['POST'])
def run_backtest_route():

    ticker = request.form.get('ticker')
    sma_short = int(request.form.get('sma_short'))
    sma_long = int(request.form.get('sma_long'))
    start_cash = int(request.form.get('start_cash'))


    stats, data = run_my_backtest(ticker, sma_short, sma_long, start_cash)

    if stats is None:
        return "Fehler: Ticker nicht gefunden oder keine Daten."

    trades = stats._trades
    
    fig = go.Figure()

    #Candlestick-Chart
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Candlesticks'
    ))

    #SMA-Linien
    fig.add_trace(go.Scatter(
        x=data.index, 
        y=data['SMA_short'], 
        name=f'SMA {sma_short}', 
        mode='lines',
        line=dict(color='blue', width=1.5)
    ))
    fig.add_trace(go.Scatter(
        x=data.index, 
        y=data['SMA_long'], 
        name=f'SMA {sma_long}', 
        mode='lines',
        line=dict(color='orange', width=1.5)
    ))

    #Kauf-/Verkaufs-Pfeile
    buy_trades = trades[trades['Size'] > 0]
    sell_trades = trades[trades['Size'] < 0]

    fig.add_trace(go.Scatter(
        x=buy_trades['EntryTime'],
        y=buy_trades['EntryPrice'] * 0.98,
        name='Kauf-Signal',
        mode='markers',
        marker_symbol='triangle-up',
        marker_color='green',
        marker_size=10
    ))
    fig.add_trace(go.Scatter(
        x=sell_trades['EntryTime'],
        y=sell_trades['EntryPrice'] * 1.02,
        name='Verkauf-Signal',
        mode='markers',
        marker_symbol='triangle-down',
        marker_color='red',
        marker_size=10
    ))

    #Hintergrund-Zonen
    for index, trade in trades.iterrows():
        fig.add_shape(
            type="rect",
            x0=trade['EntryTime'],
            x1=trade['ExitTime'],
            y0=trade['EntryPrice'],
            y1=trade['ExitPrice'],
            fillcolor='green' if trade['PnL'] > 0 else 'red',
            opacity=0.2,
            layer='below',
            line_width=0
        )

    #Dark Mode
    fig.update_layout(
        title=f'Backtest: {ticker} (SMA {sma_short}/{sma_long})',
        template="plotly_dark",
        xaxis_title='Datum',
        yaxis_title='Preis (USD)',
        xaxis_rangeslider_visible=False
    )

    chart_json = fig.to_json()

    stats_dict = stats.to_dict()
    stats_dict_rounded = {k: (f"{v:.2f}" if isinstance(v, float) else v) for k, v in stats_dict.items()}

    return render_template('results.html', stats_data=stats_dict_rounded, chart_json=chart_json)

if __name__ == '__main__':
    app.run(debug=True)