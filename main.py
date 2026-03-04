import flask
import yfinance as yf
from backtesting import Backtest

from utility.stratSwitcher import stratSwitcher

app = flask.Flask(__name__)


@app.route("/")
def index():
    return flask.render_template("index.html")
    return yf.Lookup(query=flask.request.form.get("ticker")).get_stock(
        count=5
    )  # wenn du ticker lookup willst


@app.route("/backtest", methods=["POST"])
def backtest():
    ticker = flask.request.form.get("ticker")
    strategy = flask.request.form.get("strategy")

    # given the stock and the strategy, the backtest will be done
    historic_data = yf.download(ticker, period="ytd", interval="1h")
    historic_data = (
        historic_data.droplevel("Ticker", axis=1).reset_index().set_index("Datetime")
    )
    historic_data = historic_data[["Open", "High", "Low", "Close", "Volume"]]

    strat = stratSwitcher(strategy=strategy)
    strat.setBUY(strat, buy=0.04)

    bt = Backtest(historic_data, strat, cash=100000, commission=(0.2, 0))

    data = bt.run()

    return flask.render_template(
        "backtest.html", ticker_html=ticker, strategy_html=strategy, data_html=data
    )


if __name__ == "__main__":
    app.run(debug=True)
