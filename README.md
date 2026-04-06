Structure of the project:
- language used: python
- backtesting data - yfinance - fast and easy to get data
- pandas for data conversion etc.
- backtesting.py - backtesting library, that runs test
- ta-lib - library of different algorithms to test / math functions

to get started run:
- python3 -m venv .venv
- source .venv/bin/activate
- pip install -r requirements.txt
- python3 main.py


---
lass so das repo machen zu so ein repo von all den bekannten/available trading algorithms, und dann so eine website publishen wo die leute das sehen können und auswählen und mit interagieren können
halt einfach eine Webseite, bei der man einen stock auswählen kann und eine Strategie und sehen kann, ob die strategie performt oder nicht. WIr können dazu noch ein bissl die strategien beschreiben so als lernplattform, und wir können auch die strategie bewerten so in ner Skala, 


---

*style:*
vars:
- camelCase nuh uh, PascalCase NUH UH, kebab-case-also-nuh-uh
- only_like_this (pls)



---

TODO:
- indicator graph (i think works)
- index beautify (line it up differently, try different things)
- explanation system (system setup; missing table for key values, like sharpe)
- writing explanations


TODOs:
  - cooler charts, slight tweaks (heikin ashi, label position)
  - beautify (general html layout, favicons, mobile-support, dark mode)

  - Implement strategies from daytraders and course sellers? 

  - launch

  - vergleichen von strategien



Implementing Strategies:

x1. **Moving Average Crossover**: Buy when a short-term MA crosses above a long-term MA; sell on the reverse. - finished

x2. **Mean Reversion**: Trade assuming prices revert to the mean, using indicators like Bollinger Bands to identify deviations. - finished

o3. **Momentum Trading**: Buy assets showing upward price momentum (e.g., via Rate of Change or Momentum indicator) and sell on weakness. - finished (can be improved)

o4. **RSI Overbought/Oversold**: Buy when RSI drops below 30 (oversold); sell above 70 (overbought). - finished (you sure it not other way, when oversold, sell, overbought buy)

x5. **MACD Crossover**: Buy on MACD line crossing above signal line; sell on the reverse. - finished

x6. **Bollinger Bands Squeeze**: Enter trades when bands contract (low volatility) and expand, signaling breakouts. - finished

o7. **Ichimoku Cloud**: Buy when price is above the cloud and conversion line crosses base line; sell on reverses. - finished, has lots of potential need to revisit, think im doing it wrong

o8. **Parabolic SAR**: Use SAR dots to trail stops; buy when dots flip below price, sell above.
  - used for trailing stop and loss, entry and exit points determining
  - works best in trending markets: 
    - Wilder recommends first establishing the direction or change in direction of the trend through the use of parabolic SAR, and then using a different indicator such as the Average Directional Index to determine the strength of the trend. 
  - parabola below can be used as support, above as resistance

x9. **Stochastic Oscillator**: Buy when %K crosses above %D in oversold territory; sell in overbought. - finished

x10. **ADX Trend Strength**: Combine with DI+ / DI- for directional trades when ADX > 25 indicates strong trends.  - finished, money makerrr
  - trend strength indicator not direction!
  - <20, weak trend, >40 strong trend, >50 super strong trend
  - <20 usually chart pattern after

x11. **Commodity Channel Index (CCI)**: Buy on CCI crossing above -100 from below; sell below +100 from above. - this for commodities, kein bock, rather stocks

x12. **Williams %R**: Similar to Stochastic; buy above -80 from below, sell below -20 from above.  - finsihed

x13. **Average True Range (ATR) Breakout**: Use ATR multiples for entry/exit thresholds in volatile markets. - used for commodities mainly, finished

x14. **Volume Weighted Average Price (VWAP)**: Buy below VWAP, sell above, assuming reversion. - finished

x16. **Donchian Channel Breakout**: Buy on new highs above upper channel; sell on lows below lower channel.    - finished

x17. **Keltner Channel**: Trade breakouts or mean reversion based on channel bands (EMA + ATR). - finished

x18. **Triple Exponential Moving Average (TEMA) Crossover**: Faster MA variant for crossovers with reduced lag. -finished

x19. **Hull Moving Average (HMA) Crossover**: Use HMA for smoother signals in trending markets. - finished

x20. **Aroon Indicator**: Buy when Aroon Up crosses above Aroon Down; indicates trend start. - finished
 
x21. **Ultimate Oscillator**: Buy on divergences or oversold crossings; combines multiple timeframes. - finished

x22. **TRIX (Triple Exponential Average)**: Buy on positive crossovers; filters noise in trends. - finsihed

x23. **Detrended Price Oscillator (DPO)**: Identify cycles by removing trends; trade overbought/oversold. - finished

x24. **Chande Momentum Oscillator (CMO)**: Buy above -50 from below; sell below +50 from above. - finished

x25. **Relative Vigor Index (RVI)**: Buy on RVI crossing above signal line; measures closing strength. - finished

o15. **Pairs Trading**: Identify cointegrated pairs and trade spreads using correlation and z-scores (with MA for signals). - seems very complex, should do, difficult as backtesting.py only can do 1 asset

o.   algo which tells if market is sideways market
