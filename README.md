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

lass so das repo machen zu so ein repo von all den bekannten/available trading algorithms, und dann so eine website publishen wo die leute das sehen können und auswählen und mit interagieren können
halt einfach eine Webseite, bei der man einen stock auswählen kann und eine Strategie und sehen kann, ob die strategie performt oder nicht. WIr können dazu noch ein bissl die strategien beschreiben so als lernplattform, und wir können auch die strategie bewerten so in ner Skala, 



TODO 
  Frontend:
    Beautify more
    Add Explanation
    Add Interactive Stoplight (to rate the Strategy)

  Other:
    Implement more Strategies
    Make Backtesting faster?
    Implement Tailwind




Implementing Strategies:

1. **Moving Average Crossover**: Buy when a short-term MA crosses above a long-term MA; sell on the reverse.

2. **Mean Reversion**: Trade assuming prices revert to the mean, using indicators like Bollinger Bands to identify deviations.

3. **Momentum Trading**: Buy assets showing upward price momentum (e.g., via Rate of Change or Momentum indicator) and sell on weakness.

4. **RSI Overbought/Oversold**: Buy when RSI drops below 30 (oversold); sell above 70 (overbought).

5. **MACD Crossover**: Buy on MACD line crossing above signal line; sell on the reverse.

6. **Bollinger Bands Squeeze**: Enter trades when bands contract (low volatility) and expand, signaling breakouts.

7. **Ichimoku Cloud**: Buy when price is above the cloud and conversion line crosses base line; sell on reverses.

8. **Parabolic SAR**: Use SAR dots to trail stops; buy when dots flip below price, sell above.

9. **Stochastic Oscillator**: Buy when %K crosses above %D in oversold territory; sell in overbought.

10. **ADX Trend Strength**: Combine with DI+ / DI- for directional trades when ADX > 25 indicates strong trends.

11. **Commodity Channel Index (CCI)**: Buy on CCI crossing above -100 from below; sell below +100 from above.

12. **Williams %R**: Similar to Stochastic; buy above -80 from below, sell below -20 from above.

13. **Average True Range (ATR) Breakout**: Use ATR multiples for entry/exit thresholds in volatile markets.

14. **Volume Weighted Average Price (VWAP)**: Buy below VWAP, sell above, assuming reversion.

15. **Pairs Trading**: Identify cointegrated pairs and trade spreads using correlation and z-scores (with MA for signals).

16. **Donchian Channel Breakout**: Buy on new highs above upper channel; sell on lows below lower channel.

17. **Keltner Channel**: Trade breakouts or mean reversion based on channel bands (EMA + ATR).

18. **Triple Exponential Moving Average (TEMA) Crossover**: Faster MA variant for crossovers with reduced lag.

19. **Hull Moving Average (HMA) Crossover**: Use HMA for smoother signals in trending markets.

20. **Aroon Indicator**: Buy when Aroon Up crosses above Aroon Down; indicates trend start.

21. **Ultimate Oscillator**: Buy on divergences or oversold crossings; combines multiple timeframes.

22. **TRIX (Triple Exponential Average)**: Buy on positive crossovers; filters noise in trends.

23. **Detrended Price Oscillator (DPO)**: Identify cycles by removing trends; trade overbought/oversold.

24. **Chande Momentum Oscillator (CMO)**: Buy above -50 from below; sell below +50 from above.

25. **Relative Vigor Index (RVI)**: Buy on RVI crossing above signal line; measures closing strength.
