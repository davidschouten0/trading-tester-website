def equity_curve(data):
    equity_df = data["_equity_curve"].reset_index()
    return equity_df.to_json(orient="records", date_format="iso")

def buy_and_hold_curve(data, starting_capital):
    initial_price = data["Close"].iloc[0]
    equity_series = (data["Close"] / initial_price) * starting_capital

    bnh_df = equity_series.to_frame(name="Equity").reset_index()
    
    return bnh_df.to_json(orient="records", date_format="iso")

