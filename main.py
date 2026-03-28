import flask
import numpy as np
import yfinance as yf
from backtesting import Backtest

from utility.strategy_switcher import get_strategy
from utility.strategy_switcher import strategy_is_valid
from utility.strategy_switcher import get_strategy_description

from utility import graph_helper

app = flask.Flask(__name__)


# show index
@app.route("/")
def index():
    return flask.render_template("index.html")


# run a backtest
@app.route("/backtest", methods=["POST"])
def backtest():

    # region get the infos, and validate them
    
    #strat
    strategy = flask.request.form.get("strategy", "SMA")
    if not strategy_is_valid(strategy):
        return flask.render_template("index.html", error_message=f"The Strategie \"{strategy}\" existiert (noch) nicht")
    
    #cash
    cash = flask.request.form.get("cash", "100000")
    try:
        if not (1 <= float(cash) <= 10000000):
            return flask.render_template("index.html", error_message=f"Choose a starting cash between 1 and 10.000.000 $ (\"{cash}\" is not in that range)")
    except ValueError:
        return flask.render_template("index.html", error_message=f"Please enter a valid number as starting cash. (\"{cash}\" is not a good input)")   

    #ept
    equity_per_trade = flask.request.form.get("equity_per_trade", "5")
    try:
        if not (0.01 <= float(equity_per_trade) <= 100):
            return flask.render_template("index.html", error_message=f"The equity per trade needs to be between 0.01 and 100 (\"{equity_per_trade}\" is not in that range)")
    except ValueError:
        return flask.render_template("index.html", error_message=f"Please enter a valid number for the percentage per trade. (\"{equity_per_trade}\" is not a good input)")   

    #period
    period_input = flask.request.form.get("period", "1y")
    valid_periods = ["1mo", "3mo", "6mo", "ytd", "1y", "2y", "max"]
    if period_input not in valid_periods:
        return flask.render_template("index.html", error_message=f"Please enter a valid period. (\"{equity_per_trade}\" is not a supported time period)")
    if period_input == "max":
        fetch_interval = "1d"
    else:
        fetch_interval = "1h"

    #ticker
    ticker = flask.request.form.get("ticker", "AAPL")

    # endregion

    # region get historic data from yahoo finance

    historic_data = yf.download(ticker, period=period_input, interval=fetch_interval)

    #problemhandling with bad data
    if historic_data.empty:
        return flask.render_template("index.html", error_message=f"Den Ticker \"{ticker}\" gibt es nicht oder er hat keine Daten.")

    historic_data = historic_data.droplevel("Ticker", axis=1).reset_index()

    date_col = historic_data.columns[0] 
    historic_data = historic_data.set_index(date_col)
    
    historic_data = historic_data[["Open", "High", "Low", "Close", "Volume"]]


    strat = get_strategy(name=strategy)
    strat.setBUY(strat, buy=0.04)

    # endregion

    # configure the strategy and run the backtest

    strat = get_strategy(strategy)
    strat.setBUY(strat, buy=float(equity_per_trade)/100)

    starting_capital = float(cash)

    bt = Backtest(historic_data, strat, cash=starting_capital, commission=(0.2, 0), finalize_trades=True)

    data = bt.run()

    indicator_list = (data["_strategy"]).indicators()

    # region data columns
    """
    this is 'data' btw:

    Index(['Start', 'End', 'Duration', 'Exposure Time [%]', 'Equity Final [$]',
       'Equity Peak [$]', 'Commissions [$]', 'Return [%]',
       'Buy & Hold Return [%]', 'Return (Ann.) [%]', 'Volatility (Ann.) [%]',
       'CAGR [%]', 'Sharpe Ratio', 'Sortino Ratio', 'Calmar Ratio',
       'Alpha [%]', 'Beta', 'Max. Drawdown [%]', 'Avg. Drawdown [%]',
       'Max. Drawdown Duration', 'Avg. Drawdown Duration', '# Trades',
       'Win Rate [%]', 'Best Trade [%]', 'Worst Trade [%]', 'Avg. Trade [%]',
       'Max. Trade Duration', 'Avg. Trade Duration', 'Profit Factor',
       'Expectancy [%]', 'SQN', 'Kelly Criterion', '_strategy',
       '_equity_curve', '_trades'],
      dtype='str')
    """
    # endregion

    master_json = graph_helper.create_master_json(historic_data, data, indicator_list, starting_capital)

    return flask.render_template(
        "backtest.html",
        ticker_html=ticker,
        strategy_html=strategy, 
        strategy_description=get_strategy_description(strategy),
        master_json=master_json
    )

# search for tickers
@app.route("/search_ticker")
def search_ticker():
    query = flask.request.args.get("q", "")
    return yf.Lookup(query=query).get_stock(count=5).exchange.index.to_list()
    # one day maybe with requests and caching ...


if __name__ == "__main__":
    app.run(debug=True)
