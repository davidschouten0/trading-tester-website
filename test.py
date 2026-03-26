import timeit

import requests
import yfinance as yf

query = "apple"  # test with a sample query


# Method 1: Direct API
def method1():
    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    data = response.json()
    valid_tickers = []
    if "quotes" in data:
        for quote in data["quotes"]:
            if "symbol" in quote and (
                quote["quoteType"] == "EQUITY" or quote["quoteType"] == "ETF"
            ):
                valid_tickers.append(quote["symbol"])
    return valid_tickers


# Method 2: yfinance Lookup
def method2():
    return yf.Lookup(query=query).get_stock(count=5).exchange.index.to_list()


# Run benchmarks
time1 = timeit.timeit(method1, number=10)
time2 = timeit.timeit(method2, number=10)

print(f"Method 1 (requests): {time1 / 10:.4f}s per call")
print(f"Method 2 (yfinance): {time2 / 10:.4f}s per call")
print(
    f"Faster: {'Method 1' if time1 < time2 else 'Method 2'} ({abs(time1 - time2) / max(time1, time2) * 100:.1f}% faster)"
)
