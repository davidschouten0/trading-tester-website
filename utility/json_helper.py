import utility.strategy_switcher as strat_switch

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

def create_explanation_json(data, ticker, strategy):
    explanation_series = data.drop(labels=['_strategy', '_equity_curve', '_trades'])

    explanation_series["ticker"] = ticker
    explanation_series["strategy"] = strategy
    
    explanation_series["explanation_quick"] = strat_switch.get_strategy_explanation_quick(strategy)
    explanation_series["explanation_buying"] = strat_switch.get_strategy_explanation_buying(strategy)

    return explanation_series.to_json()