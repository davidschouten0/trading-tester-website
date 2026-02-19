Structure of the project:
- language used: python
- backtesting data - alpaca-py - inorder to be able to do paper trading in the future
- pandas for data conversion etc.
- backtesting.py - backtesting library, that runs test
- ta-lib - library of different algorithms to test / math functions

to get started run:
  python3 -m venv .venv
  source .venv/bin/activate
  pip install alpaca-py backtesting TA-Lib plotly pytz python-dotenv

then, 
- create an alpaca account and get an api-key for market data requests
- create a .env file in this format:
```
ALPACA_URL=https://paper-api.alpaca.markets/v2
SECRET_KEY=
API_KEY=
```
