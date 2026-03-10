def equity_curve(data):
    equity_df = data["_equity_curve"].reset_index()
    return equity_df.to_json(orient="records", date_format="iso")