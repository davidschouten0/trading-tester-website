from strategies.adxStrat import AdxStrategy
from strategies.aroonStrat import AroonStrategy
from strategies.atrBreakoutStrat import ATRBreakoutStrategy
from strategies.bollingerSqueeze import BollingerSqueezeStrategy
from strategies.cmoStrat import CMOStrategy
from strategies.donchianChannel import DonchianStrategy
from strategies.dpoStrat import DPOStrategy
from strategies.hmaCrossStrat import HMACrossStrategy
from strategies.ichimokuCloud import IchimokuCloudStrategy
from strategies.kamaStrat import KamaCrossStrategy
from strategies.keltnerChannel import KeltnerStrategy
from strategies.macdStrat.macdCross import MACDStrategy
from strategies.macdStrat.macdPullback import MACDPullbackStrategy
from strategies.macdStrat.macdSignalZero import MACDSignalZeroCrossStrategy
from strategies.macdStrat.macdSimplezero import MACDzeroCrossStrategy
from strategies.meanRev import MeanRevCrossStrategy
from strategies.momTrading import MomentumCrossStrategy
from strategies.movinAverage import MovinAverageCrossStrategy
from strategies.rsiStrat import RSICrossStrategy
from strategies.rviStrat import RVIStrategy
from strategies.sarStrat import SarCrossStrategy
from strategies.smaStrat import SmaCrossStrategy
from strategies.stochasticStrat import StochasticStrategy
from strategies.temaStrat import TEMACrossStrategy
from strategies.trixStrat import TRIXStrategy
from strategies.ultimateOscillator import UltimateOscStrategy
from strategies.vwapStrat import VWAPStrategy
from strategies.williamsStrat import WilliamsStrategy

STRATEGIES = {
    "ADX": AdxStrategy,
    "Aroon": AroonStrategy,
    "ATRBreakout": ATRBreakoutStrategy,
    "BollingerSqueeze": BollingerSqueezeStrategy,
    "CMO": CMOStrategy,
    "Donchian": DonchianStrategy,
    "DPO": DPOStrategy,
    "HMACross": HMACrossStrategy,
    "Ichimoku": IchimokuCloudStrategy,
    "Kama": KamaCrossStrategy,
    "Keltner": KeltnerStrategy,
    "MACD": MACDStrategy,
    "MACDPullback": MACDPullbackStrategy,
    "MACDSignalZero": MACDSignalZeroCrossStrategy,
    "MACDZero": MACDzeroCrossStrategy,
    "MeanReversion": MeanRevCrossStrategy,
    "Momentum": MomentumCrossStrategy,
    "MovingAverage": MovinAverageCrossStrategy,
    "RSI": RSICrossStrategy,
    "RVI": RVIStrategy,
    "SAR": SarCrossStrategy,
    "SMA": SmaCrossStrategy,
    "Stochastic": StochasticStrategy,
    "TEMA": TEMACrossStrategy,
    "TRIX": TRIXStrategy,
    "UltimateOscillator": UltimateOscStrategy,
    "VWAP": VWAPStrategy,
    "Williams": WilliamsStrategy,
}

STRATEGY_EXPLANATION_QUICK = {
    "ADX": "The Average Directional Index (ADX) measures the absolute strength of a trend, regardless of its direction. This strategy generates buy signals when a strong uptrend is confirmed by rising directional indicators.",
    "Aroon": "The Aroon indicator detects the start of new trends by measuring the time since the last high or low. A buy signal occurs when the upward momentum (Aroon Up) crosses above the downward momentum (Aroon Down).",
    "ATRBreakout": "This breakout strategy uses the Average True Range (ATR) to measure normal market volatility. It buys when the price breaks significantly above its normal fluctuation range – a sign of explosive, new momentum.",
    "BollingerSqueeze": "Based on Bollinger Bands. When the bands narrow extremely (the Squeeze), there is an unusual calm in the market. The strategy positions itself for the immediately following, strong price breakout to the upside.",
    "CMO": "The Chande Momentum Oscillator (CMO) calculates market momentum by directly comparing up and down days. Buy signals occur when the value crosses above the zero line from the oversold territory.",
    "Donchian": "The classic breakout strategy of the famous 'Turtle Traders'. It consistently buys when the price reaches a new high of the last X periods, breaking through the upper band of the Donchian Channel.",
    "DPO": "The Detrended Price Oscillator (DPO) mathematically removes long-term market trends to reveal pure, short-term price cycles. It buys at the isolated historical low points of these rhythms.",
    "HMACross": "Uses the Hull Moving Average (HMA), an extremely responsive and smoothed average that tracks the price with almost zero lag. It buys when the short-term HMA line crosses above the longer-term one.",
    "Ichimoku": "The Ichimoku Cloud is a comprehensive Japanese trend-following system. A buy signal is triggered when the price dynamically breaks out above the 'Cloud' (the resistance zone) and the uptrend is confirmed.",
    "Kama": "Kaufman's Adaptive Moving Average (KAMA) intelligently adapts to market speed: it remains flat in choppy, sideways markets and reacts quickly during true trends. This filters out noise and provides clean buy signals upon crossovers.",
    "Keltner": "Keltner Channels place dynamic bands around the price based on actual volatility (ATR). The strategy buys when the price has enough strength to dynamically break above the upper band.",
    "MACD": "The classic trend and momentum indicator. A buy signal occurs when the fast-reacting MACD line crosses above the slower signal line, indicating increasing upward momentum.",
    "MACDPullback": "Looks for established, strong uptrends in the MACD, but strategically waits for a short-term price retracement (pullback). It 'buys the dip' into temporary weakness before the main trend resumes.",
    "MACDSignalZero": "A very conservative and long-term MACD variant. The buy signal is only generated here when the slow signal line crosses above the central zero line, marking a stable, overarching trend change.",
    "MACDZero": "A classic signal generator for the transition from a bear to a bull market. It buys exactly when the main MACD line crosses the zero line into positive territory.",
    "MeanReversion": "The 'rubber band' strategy. Based on the statistical assumption that prices always return to their average after extreme movements. It buys counter-cyclically after strong, irrational sell-offs.",
    "Momentum": "Focuses on the pure acceleration of price movement. It buys when the current price significantly exceeds the price from X periods ago, indicating an intact and strong upward rally.",
    "MovingAverage": "The flexible standard among trend followers. It buys when a short-term moving price average breaks through a longer-term average from below to above.",
    "RSI": "The Relative Strength Index (RSI) identifies panic and euphoria. The strategy buys when the indicator value drops low (the market is 'oversold') and the price subsequently stabilizes and turns upwards.",
    "RVI": "The Relative Vigor Index (RVI) measures buyer conviction by comparing closing prices to opening prices. It buys when the momentum shifts into positive territory and a crossover signal occurs.",
    "SAR": "The Parabolic SAR places visual dots on the chart that follow the price like a trailing stop-loss. A fresh buy signal is generated when these dots flip from 'above the price' to the underside.",
    "SMA": "The absolute foundation of technical analysis. It buys at the famous 'Golden Cross', where a fast Simple Moving Average significantly crosses above a slow moving average.",
    "Stochastic": "This oscillator compares the current closing price with the price range of the recent past. It buys when the price breaks upwards out of the extremely oversold area (bear panic).",
    "TEMA": "The Triple Exponential Moving Average smooths the price three times. This almost completely eliminates the usual lag of moving average lines, allowing for extremely early and aggressive buy signals during trend changes.",
    "TRIX": "A momentum oscillator that ignores minor price fluctuations because it is based on a triple-smoothed price. A clean buy signal occurs when the TRIX line breaks through the zero line from bottom to top.",
    "UltimateOscillator": "Combines short-, medium-, and long-term momentum into a single value to avoid the usual false signals of standard oscillators. It typically buys during strong bullish divergences in the lower range.",
    "VWAP": "The Volume Weighted Average Price (VWAP) is one of the most important tools for institutional traders as it combines price and actual trading volume. A buy occurs when the price dynamically exceeds the volume-weighted average.",
    "Williams": "The Williams %R indicator measures momentum on a negative scale (0 to -100). The strategy looks for highly oversold markets and buys when the value dynamically breaks out upwards from the extreme negative range (below -80)."
}

STRATEGY_EXPLANATION_BUYING={
    "ADX": "CONCEPT: Measures pure trend strength. BUY TRIGGER: The ADX value crosses above the 25 threshold (confirming a valid trend) AND the +DI (Positive Directional Indicator) crosses above the -DI from below. SELL TRIGGER: The +DI crosses below the -DI (trend reversal) OR the ADX drops below 20 (the uptrend loses its structural strength).",
    "Aroon": "CONCEPT: Measures the time elapsed since the highest high or lowest low. BUY TRIGGER: The Aroon Up line crosses above the Aroon Down line from below AND the Aroon Up value rises above 50 (often pushing toward 100). SELL TRIGGER: The Aroon Down line crosses above the Aroon Up line, meaning new lows are being reached faster than new highs.",
    "ATRBreakout": "CONCEPT: Volatility-based breakout beyond normal fluctuation ranges. BUY TRIGGER: The closing price of the current candle closes above a defined resistance (or moving average) PLUS a multiplier of the Average True Range (e.g., +1.5x ATR). SELL TRIGGER: The price falls below an ATR-based trailing stop (e.g., highest high minus 2x ATR).",
    "BollingerSqueeze": "CONCEPT: Volatility contraction followed by an explosive expansion. BUY TRIGGER: The bandwidth of the Bollinger Bands reaches a historical minimum (the squeeze) AND the current candle closes significantly above the upper Bollinger Band. SELL TRIGGER: The price loses momentum and crosses below the middle Bollinger Band (the 20-period SMA).",
    "CMO": "CONCEPT: Pure price momentum based on the sum of up days versus down days. BUY TRIGGER: The CMO was previously in the extreme oversold zone (below -50) and now crosses the zero line from below to confirm the reversal. SELL TRIGGER: The CMO reaches the overbought zone (above +50) and subsequently crosses back below the zero line.",
    "Donchian": "CONCEPT: Pure highest-high/lowest-low breakout system. BUY TRIGGER: The current price breaks through the absolute highest high of the last X periods (e.g., 20 days), breaching the upper Donchian band. SELL TRIGGER: The price falls below the absolute lowest low of a shorter timeframe (e.g., the last 10 days), mathematically sealing the trend break.",
    "DPO": "CONCEPT: Isolates short-term cycles by mathematically stripping out the macro trend. BUY TRIGGER: The DPO line drops deep below the zero line (historical cycle trough) and aggressively hooks upward toward the zero line. SELL TRIGGER: The DPO line surges far above the zero line to a cycle peak and hooks back downward.",
    "HMACross": "CONCEPT: Zero-lag trend detection using weighted moving average smoothing. BUY TRIGGER: A fast Hull Moving Average (e.g., 9-period) crosses above a slow Hull Moving Average (e.g., 21-period) from below. SELL TRIGGER: The fast HMA crosses below the slow HMA (immediate exit, as the indicator is extremely sensitive).",
    "Ichimoku": "CONCEPT: Multi-factor confirmation system. BUY TRIGGER: The closing price breaks out above the Kumo (Cloud) AND the Tenkan-Sen line crosses above the Kijun-Sen line AND the Chikou Span (lagging line) is strictly above the price from 26 periods ago. SELL TRIGGER: The price falls back below the Kijun-Sen line (standard support) or completely drops below the Cloud.",
    "Kama": "CONCEPT: Noise reduction through volatility adaptation. BUY TRIGGER: The price or a short-term KAMA crosses above a medium-term KAMA from below, while the slope of the main KAMA turns positive. SELL TRIGGER: The price definitively breaks below the adaptive main KAMA.",
    "Keltner": "CONCEPT: Dynamic channel breakouts. BUY TRIGGER: A green (bullish) candle closes completely outside and above the upper Keltner Channel band, proving abnormal buyer strength. SELL TRIGGER: The price returns inside the channel and breaks below the midline (typically the 20-EMA).",
    "MACD": "CONCEPT: Momentum via the convergence and divergence of moving averages. BUY TRIGGER: The fast MACD line (EMA12 - EMA26) crosses above the slower Signal line (EMA9 of the MACD) from below. SELL TRIGGER: The fast MACD line crosses below the Signal line.",
    "MACDPullback": "CONCEPT: Re-entry into intact uptrends. BUY TRIGGER: The price is above the 200-SMA (macro uptrend). The MACD histogram temporarily drops below zero (pullback) but then flips back to positive (histogram turns green). SELL TRIGGER: The MACD histogram drops below zero again or the price closes below a relevant short-term average (e.g., 50-SMA).",
    "MACDSignalZero": "CONCEPT: Conservative trend reversal. BUY TRIGGER: The slow, smoothed MACD Signal line crosses the central zero line from below into positive territory (transition to a fundamental bull market). SELL TRIGGER: The Signal line crosses back below the zero line into bear territory.",
    "MACDZero": "CONCEPT: Aggressive trend reversal. BUY TRIGGER: The primary, faster MACD line breaks through the zero line from below into positive territory. SELL TRIGGER: The primary MACD line falls back below the zero line into negative territory.",
    "MeanReversion": "CONCEPT: Counter-cyclical trading based on extremes. BUY TRIGGER: The price's Z-Score falls below -2 (or RSI < 20) AND the first daily candle subsequently closes higher than its open (reversal confirmation). SELL TRIGGER: The price reverts to its statistical mean (e.g., touching the 20-period SMA).",
    "Momentum": "CONCEPT: Velocity measurement of price action. BUY TRIGGER: The Momentum value (current price minus the price N periods ago) dynamically crosses the zero line from below. SELL TRIGGER: The Momentum value crosses below the zero line (velocity becomes negative; current price is lower than N periods ago).",
    "MovingAverage": "CONCEPT: Moving average crossover. BUY TRIGGER: A shorter moving average (e.g., 20-SMA) crosses above a longer moving average (e.g., 50-SMA) from below. SELL TRIGGER: The shorter moving average crosses below the longer moving average.",
    "RSI": "CONCEPT: Measures overbought/oversold extremes. BUY TRIGGER: The RSI value (usually 14-period) drops below 30 (oversold) AND subsequently crosses back above the 30 line from below. SELL TRIGGER: The RSI rises above 70 (overbought) AND subsequently breaks back below the 70 line.",
    "RVI": "CONCEPT: Intraday buying power (Close vs. Open). BUY TRIGGER: The main RVI line crosses above its Signal line from below, deep in negative territory. SELL TRIGGER: The RVI line crosses below the Signal line in positive territory.",
    "SAR": "CONCEPT: Dynamic trend-following stop. BUY TRIGGER: The current price rises high enough to 'touch' the SAR dot above it. In the next period, the SAR dot mathematically flips to the underside of the price. SELL TRIGGER: The price drops and touches the SAR dot from above, causing the indicator to flip back above the price.",
    "SMA": "CONCEPT: Long-term macro signals. BUY TRIGGER: A 'Golden Cross' occurs: The Simple Moving Average of the last 50 days crosses above the 200-day Simple Moving Average. SELL TRIGGER: A 'Death Cross' occurs: The 50-day SMA crosses below the 200-day SMA.",
    "Stochastic": "CONCEPT: Range-based momentum oscillator. BUY TRIGGER: Both lines (%K and %D) fall below 20 (bear dominance). The buy triggers exactly when the fast %K line crosses above the slow %D line from below, ideally breaking back above the 20 threshold. SELL TRIGGER: The %K line crosses below the %D line in the overbought zone (above 80).",
    "TEMA": "CONCEPT: Noise-free, aggressive trend following. BUY TRIGGER: The current closing price crosses above the TEMA (Triple Exponential Moving Average) line OR a fast TEMA crosses above a slow TEMA. SELL TRIGGER: The closing price cleanly drops back below the TEMA line.",
    "TRIX": "CONCEPT: Percentage rate of change of a triple-smoothed EMA. BUY TRIGGER: The TRIX line crosses above the central zero line (trend confirmation) OR crosses above its own Signal line from below (earlier entry signal). SELL TRIGGER: The TRIX line falls below its Signal line OR drops through the zero line into negative territory.",
    "UltimateOscillator": "CONCEPT: Weighted blend of three timeframes (short, medium, long). BUY TRIGGER: A 'Bullish Divergence' occurs. The price drops to a lower low, but the indicator stays above 30 and prints a higher low. The buy is triggered when the oscillator breaks above its recent intermediary peak. SELL TRIGGER: A bearish divergence forms in the overbought zone (above 70) or the oscillator drops cleanly below 50.",
    "VWAP": "CONCEPT: Volume-weighted average price for institutions. BUY TRIGGER: The price breaks upward through the VWAP line accompanied by a significant surge in trading volume. SELL TRIGGER: The price closes below the VWAP line on an intraday or daily basis.",
    "Williams": "CONCEPT: Momentum measurement on an inverted scale (0 to -100). BUY TRIGGER: The Williams %R value drops into the extreme zone below -80. As soon as the indicator aggressively pivots and crosses back above the -80 mark from below, a buy is triggered. SELL TRIGGER: The value rises above -20 into the extreme zone and subsequently crosses back below the -20 mark."
}


def get_strategy(name="SMA"):
    return STRATEGIES.get(name)

def strategy_is_valid(strategy):
    return strategy in STRATEGIES

def get_strategy_explanation_quick(strategy):
    return STRATEGY_EXPLANATION_QUICK[strategy]

def get_strategy_explanation_buying(strategy):
    return STRATEGY_EXPLANATION_BUYING[strategy]