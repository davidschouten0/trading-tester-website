import os
from datetime import datetime

import requests
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from dotenv import load_dotenv

load_dotenv()
secret_key = os.getenv("SECRET_KEY")
api_key = os.getenv("API_KEY")


def request(symbol):
    client = StockHistoricalDataClient(api_key, secret_key)

    # response = requests.get(
    #     f"http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={symbol}&region=1&lang=en"
    # ).json()
    # print(response)

    request_params = StockBarsRequest(
        symbol_or_symbols=[symbol],
        timeframe=TimeFrame(6, TimeFrameUnit(TimeFrameUnit.Hour)),
        start=datetime.strptime("2023-01-01", "%Y-%m-%d"),
    )

    bars = client.get_stock_bars(request_params)

    # convert to dataframe
    df = bars.df  # this works idk what yapping about
    df = df.reset_index().set_index("timestamp")
    df = df[["open", "high", "low", "close", "volume"]]
    df = df.rename(str.capitalize, axis="columns")
    print(df)
    return df
