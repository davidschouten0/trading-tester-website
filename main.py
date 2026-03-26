import flask
import yfinance as yf
from backtesting import Backtest
import requests
from utility import graph_helper

from utility.strategies import get_strategy
from utility.strategies import strategy_is_valid
from utility.strategies import get_strategy_description

app = flask.Flask(__name__)

#show index
@app.route("/")
def index():
    return flask.render_template("index.html")


#run a backtest
@app.route("/backtest", methods=["POST"])
def backtest():

    # get the infos, and validate them
    
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

    #ticker
    ticker = flask.request.form.get("ticker", "AAPL")

    
    # get historic data from yahoo finance

    historic_data = yf.download(ticker, period="ytd", interval="1h")

    #problemhandling with bad data
    if historic_data.empty:
        return flask.render_template("index.html", error_message=f"Den Ticker \"{ticker}\" gibt es nicht oder er hat keine Daten.")

    historic_data = (
        historic_data.droplevel("Ticker", axis=1).reset_index().set_index("Datetime")
    )
    historic_data = historic_data[["Open", "High", "Low", "Close", "Volume"]]


    # configure the strategy and run the backtest

    strat = get_strategy(strategy)
    strat.setBUY(strat, buy=float(equity_per_trade)/100)

    starting_capital = float(cash)

    bt = Backtest(historic_data, strat, cash=starting_capital, commission=(0.2, 0))

    data = bt.run()

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

    print(data.head)


    # turn the data in something plottable

    description = get_strategy_description(strategy=strategy)

    equity_curve = graph_helper.equity_curve(data)

    buy_and_hold_curve = graph_helper.buy_and_hold_curve(historic_data, starting_capital)

    #fuer den fetten graphen brauch ich: candles (x), buy/sell signals (x), equity curve (\/)

    return flask.render_template(
        "backtest.html", ticker_html=ticker, strategy_html=strategy, equity_curve=equity_curve, buy_and_hold_curve=buy_and_hold_curve, description=description
    )

#search for tickers
@app.route("/search_ticker")
def search_ticker():
    query = flask.request.args.get("q", "")
    return yf.Lookup(query=query).get_stock(count=5).exchange.index.to_list()
    #one day maybe with requests and caching ...
    

if __name__ == "__main__":
    app.run(debug=True)