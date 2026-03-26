import yfinance as yf
from backtesting import Backtest
import strategies.sarStrat as rev
import time
import requests
import timeit

def run_backtest():
    historic_data = yf.download("AAPL", period="ytd", interval="1h")
    historic_data = (
        historic_data.droplevel("Ticker", axis=1).reset_index().set_index("Datetime")
    )
    historic_data = historic_data[["Open", "High", "Low", "Close", "Volume"]]

    bt = Backtest(historic_data, rev.SarCrossStrategy, cash=100000, commission=(0.2, 0))
    results = bt.run()
    print(results)
    bt.plot()


def benchmark_ticker():
    query = "AAP"

    start1 = time.time()

    for _ in range(100):
        yf.Lookup(query=query).get_stock(count=5).exchange.index.to_list()

    end1 = time.time()

    start2 = time.time()
    for _ in range(100):
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}"

        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers) #goes to the URL and gets the data
        data = response.json() 

        valid_tickers = []
        if "quotes" in data:
            for quote in data["quotes"]:
                if "symbol" in quote and (quote["quoteType"] == "EQUITY" or quote["quoteType"] == "ETF"):
                    valid_tickers.append(quote["symbol"])
                    
    end2 = time.time()

    print("\n")
    print("-------")
    print(f"yf lookup: {end1-start1} ")
    print(f"query lookup: {end2-start2} ")


def benchmar_ticker2():
    query = "apple"  # test with a sample query

    # Method 1: Direct API
    def method1():
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        data = response.json()
        valid_tickers = []
        if "quotes" in data:
            for quote in data["quotes"]:
                if "symbol" in quote and (quote["quoteType"] == "EQUITY" or quote["quoteType"] == "ETF"):
                    valid_tickers.append(quote["symbol"])
        return valid_tickers

    # Method 2: yfinance Lookup
    def method2():
        return yf.Lookup(query=query).get_stock(count=5).exchange.index.to_list()

    # Run benchmarks
    time1 = timeit.timeit(method1, number=10)
    time2 = timeit.timeit(method2, number=10)

    print(f"Method 1 (requests): {time1/10:.4f}s per call")
    print(f"Method 2 (yfinance): {time2/10:.4f}s per call")
    print(f"Faster: {'Method 1' if time1 < time2 else 'Method 2'} ({abs(time1-time2)/max(time1, time2)*100:.1f}% faster)")