from utility.strategy_switcher import get_strategy_description

def create_master_json(historic_data, data, indicator_list, starting_capital):

    master_df = historic_data.copy()

    master_df["Equity_Strat"] = data["_equity_curve"]["Equity"]
    
    initial_price = master_df["Close"].iloc[0]
    master_df["Equity_BnH"] = (master_df["Close"] / initial_price) * starting_capital

    for indicator_name, indicator_val in indicator_list.items():
        master_df[indicator_name] = indicator_val

    return master_df.reset_index().to_json(orient="records", date_format="iso")

def create_trades_json(data):
    return data["_trades"].to_json(orient="records", date_format="iso")

def create_explanation_json(data, ticker):
    strategy = data["_strategy"]["name"] #or something like that

    explanation_df = data["."] #every short data, that is like 1 value, get the strategy from _strategy

    explanation_df["strategy"] = strategy
    
    explanation_df["description"] = get_strategy_description(strategy)

    explanation_df["ticker"] = ticker

    return explanation_df.to_json()