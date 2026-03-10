import flask
import yfinance as yf
from backtesting import Backtest
import requests

from utility.stratSwitcher import stratSwitcher

app = flask.Flask(__name__)


@app.route("/")
def index():
    return flask.render_template("index.html")
    #return yf.Lookup(query=flask.request.form.get("ticker")).get_stock(
    #    count=5
    #)  wenn du ticker lookup willst


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

@app.route("/search_ticker")
def search_ticker():
    query = flask.request.args.get("q", "")
    
    #if there is no query, return an empty JSON
    if len(query) < 1:
        return flask.jsonify([])
    
    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}"

    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers) #goes to the URL and gets the data
    data = response.json() 

    valid_tickers = []
    if "quotes" in data:
        for quote in data["quotes"]:
            if "symbol" in quote and (quote["quoteType"] == "EQUITY" or quote["quoteType"] == "ETF"):
                valid_tickers.append(quote["symbol"]) 

    return flask.jsonify(valid_tickers)

if __name__ == "__main__":
    app.run(debug=True)