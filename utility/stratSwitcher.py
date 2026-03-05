import strategies.kamaStrat as kma
import strategies.meanRev as rev
import strategies.momTrading as mom
import strategies.movinAverage as mov
import strategies.smaStrat as sma


def stratSwitcher(strategy="SMA"):
    return {
        "KAMA": kma.KamaCrossStrategy,
        "SMA": sma.SmaCrossStrategy,
        "MEANREV": rev.MeanRevCrossStrategy,
        "MA": mov.MovinAverageCrossStrategy,
        "MOMENT": mom.MomentumCrossStrategy,
    }[strategy]
