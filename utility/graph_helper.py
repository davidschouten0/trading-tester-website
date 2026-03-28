def create_master_json(historic_data, data, indicator_list, starting_capital):
    
    master_df = historic_data.copy()

    master_df["Equity_Strat"] = data["_equity_curve"]["Equity"]
    
    initial_price = master_df["Close"].iloc[0]
    master_df["Equity_BnH"] = (master_df["Close"] / initial_price) * starting_capital

    return master_df.reset_index().to_json(orient="records", date_format="iso")

