import flask
import yfinance as yf
from backtesting import Backtest
import requests
from utility import graph_helper

from utility.strat_switcher import get_strategy

app = flask.Flask(__name__)

#show index
@app.route("/")
def index():
    return flask.render_template("index.html")


#run a backtest
@app.route("/backtest", methods=["POST"])
def backtest():
    ticker = flask.request.form.get("ticker")
    strategy = (
        flask.request.form.get("strategy")
        if flask.request.form.get("strategy") is not None
        else "SMA"
    )

    # given the stock and the strategy, the backtest will be done
    historic_data = yf.download(ticker, period="ytd", interval="1h")
    historic_data = (
        historic_data.droplevel("Ticker", axis=1).reset_index().set_index("Datetime")
    )
    historic_data = historic_data[["Open", "High", "Low", "Close", "Volume"]]

    strat = get_strategy(strategy)
    strat.setBUY(strat, buy=0.04)

    starting_capital = 100000

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

    equity_curve = graph_helper.equity_curve(data)
    buy_and_hold_curve = graph_helper.buy_and_hold_curve(historic_data, starting_capital)

    return flask.render_template(
        "backtest.html", ticker_html=ticker, strategy_html=strategy, equity_curve=equity_curve, buy_and_hold_curve=buy_and_hold_curve
    )

#search for tickers
@app.route("/search_ticker")
def search_ticker():
    query = flask.request.args.get("q", "")
    return yf.Lookup(query=query).get_stock(count=5).exchange.index.to_list()
    #one day maybe with requests and caching ...
    

if __name__ == "__main__":
    app.run(debug=True)