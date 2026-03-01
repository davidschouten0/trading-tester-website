import flask

app = flask.Flask(__name__)

@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/backtest", methods=["POST"])
def backtest():
    ticker = flask.request.form.get("ticker")
    strategy = flask.request.form.get("strategy")

    #given the stock and the strategy, the backtest will be done
    data = 0

    return flask.render_template("backtest.html", ticker_html=ticker, strategy_html=strategy, data_html=data)

if __name__ == "__main__":
    app.run(debug=True)