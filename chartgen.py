import pandas as pd
import plotly.graph_objects as go


def generator(data, symbol):
    data["timestamp"] = pd.to_datetime(data["timestamp"])

    fig = go.Figure()
    fig.add_trace(
        go.Candlestick(
            x=data["timestamp"],
            open=data["open"],
            high=data["high"],
            low=data["low"],
            close=data["close"],
        )
    )

    fig.write_html(symbol)
