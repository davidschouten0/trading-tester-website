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


def get_strategy(name="SMA"):
    return STRATEGIES.get(name)

def strategy_is_valid(strategy):
    return strategy in STRATEGIES