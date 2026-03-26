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

STRATEGY_DESCRIPTIONS = {
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


def get_strategy(name="SMA"):
    return STRATEGIES.get(name)

def strategy_is_valid(strategy):
    return strategy in STRATEGIES

def get_strategy_description(strategy):
    return STRATEGY_DESCRIPTIONS[strategy]