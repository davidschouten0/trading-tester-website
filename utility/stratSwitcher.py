import strategies.kamaStrat as kma
import strategies.smaStrat as sma


def stratSwitcher(strategy="SMA"):
    return {
        "KAMA": kma.KamaCrossStrategy,
        "SMA": sma.SmaCrossStrategy,
    }[strategy]
