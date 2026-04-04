const rawData = window.BACKTEST_DATA;
const trades = window.TRADES_DATA || [];
const explanation = window.EXPLANATION_DATA || [];

function formatMyDate(rawString) {
    const d = new Date(rawString);
    let dateString = d.toLocaleDateString('en-US', {
        month: 'short', day: 'numeric', year: 'numeric'
    });

    if (d.getHours() !== 0 || d.getMinutes() !== 0) {
        let timeString = d.toLocaleTimeString('en-US', {
            hour: '2-digit', minute: '2-digit', hour12: false
        });
        return `${dateString} ${timeString}`;
    }
    return dateString;
}

const dates = rawData.map(row => formatMyDate(row.Datetime || row.Date));

//#region get data
const myTickVals = [];
const myTickText = [];
const numberOfTicks = 6; // amount of date stamps
const step = Math.max(1, Math.floor(dates.length / numberOfTicks));

for (let i = 0; i < dates.length; i += step) {
    myTickVals.push(dates[i]); 
    let cleanDate = dates[i].split(' ').slice(0, 3).join(' '); 
    myTickText.push(cleanDate);
}


const equityStrat = rawData.map(row => row.Equity_Strat);
const equityBuyAndHold = rawData.map(row => row.Equity_BnH);
const opens = rawData.map(row => row.Open);
const highs = rawData.map(row => row.High);
const lows = rawData.map(row => row.Low);
const closes = rawData.map(row => row.Close);

const strategy = explanation.map(row => row.strategy)
const ticker = explanation.map(row => row.ticker)

const standardKeys = ["Datetime", "Date", "Open", "High", "Low", "Close", "Volume", "Equity_Strat", "Equity_BnH"];
//#endregion

//#region baselayouts
const crosshairSettings = {
    showspikes: true,
    spikemode: 'across', 
    spikesnap: 'cursor', 
    spikethickness: 1,   
    spikedash: 'dash',   
    spikecolor: '#9ca3af'
};

const baseLayout = {
    paper_bgcolor: 'transparent', 
    plot_bgcolor: 'transparent',
    font: { family: 'JetBrains Mono, sans-serif' }, 
    hovermode: 'x unified', 
    hoverlabel: {
        bgcolor: '#ffffff', 
        bordercolor: '#d1d5db', 
        font: { color: '#000000' }
    },
    margin: { l: 50, r: 20, t: 50, b: 50 },

    xaxis: { 
        title: 'Datum', 
        type: 'category', // dont touch!!!!!!
        
        tickmode: 'array',
        tickvals: myTickVals, 
        ticktext: myTickText,
        
        rangeslider: { visible: false },
        showgrid: true, 
        gridcolor: '#e5e7eb', 
        ...crosshairSettings 
    }
};
//#endregion

//#region equity vs buy and hold 
const traceStrat = {
    x: dates, y: equityStrat,
    type: 'scatter', mode: 'lines',
    name: strategy,
    line: { color: '#10b981', width: 2, shape: 'spline' }
};

const traceBuyAndHold = {
    x: dates, y: equityBuyAndHold,
    type: 'scatter', mode: 'lines',
    name: 'Buy and Hold',
    line: { color: '#9ca3af', width: 2, shape: 'spline', dash: 'dash' }
};

const layoutEquity = {
    ...baseLayout,
    title: 'Kapitalentwicklung (Equity Curve)',
    yaxis: { 
        title: 'Kontostand ($)', 
        showgrid: true, gridcolor: '#e5e7eb',
        ...crosshairSettings
    }
};
//#endregion

Plotly.newPlot("equity_curve", [traceStrat, traceBuyAndHold], layoutEquity, {responsive: true});

//#region buy signals
const traceCandles = {
    x: dates,
    open: opens, high: highs, low: lows, close: closes,
    type: 'candlestick', name: 'Price Action'
};

const layoutPrice = {
    ...baseLayout, 
    title: 'Fetter Price Chart',
    yaxis: { 
        title: 'Preis ($)', 
        showgrid: true, gridcolor: '#e5e7eb',
        ...crosshairSettings
    }
};

const buyDates = [];
const buyPrices = [];
const buyTexts = []; 
const sellDates = [];
const sellPrices = [];
const sellTexts = [];
const gap = 0.005;

trades.forEach(trade => {
    let entryTimeFormatted = formatMyDate(trade.EntryTime);
    let exitTimeFormatted = formatMyDate(trade.ExitTime);

    if (trade.Size > 0) {
        buyDates.push(entryTimeFormatted);
        buyPrices.push(trade.EntryPrice * (1 - gap));
        buyTexts.push(`Kauf: $${trade.EntryPrice.toFixed(2)}`);
        
        sellDates.push(exitTimeFormatted);
        sellPrices.push(trade.ExitPrice * (1 + gap));
        sellTexts.push(`Verkauf: $${trade.ExitPrice.toFixed(2)}`);
    } 
    else if (trade.Size < 0) {
        sellDates.push(entryTimeFormatted);
        sellPrices.push(trade.EntryPrice * (1 + gap));
        sellTexts.push(`Sell (Short): $${trade.EntryPrice.toFixed(2)}`);
        
        buyDates.push(exitTimeFormatted);
        buyPrices.push(trade.ExitPrice * (1 - gap));
        buyTexts.push(`Buy (Cover): $${trade.ExitPrice.toFixed(2)}`);
    }
});

const traceBuys = {
    x: buyDates,
    y: buyPrices,
    type: 'scatter',
    mode: 'markers',
    name: 'Buy',
    marker: {
        symbol: 'triangle-up', 
        color: '#10b981',     
        size: 14,            
        line: { width: 1, color: 'black' } 
    },
    hoverinfo: 'x+y'
};

const traceSells = {
    x: sellDates,
    y: sellPrices,
    type: 'scatter',
    mode: 'markers',
    name: 'Sell',
    marker: {
        symbol: 'triangle-down',
        color: '#ef4444',      
        size: 14,
        line: { width: 1, color: 'black' }
    },
    hoverinfo: 'x+y'
};

const firstRow = rawData[0];
const indicatorNames = Object.keys(firstRow).filter(key => !standardKeys.includes(key));
const dynamicIndicatorTraces = [];

indicatorNames.forEach(indName => {
    const indData = rawData.map(row => row[indName]);
    
    dynamicIndicatorTraces.push({
        x: dates, 
        y: indData,
        type: 'scatter', 
        mode: 'lines',
        name: indName,
        line: { width: 1.5 },
        hoverinfo: 'none'
    });
});
//#endregion

Plotly.newPlot("price_chart", [traceCandles, traceBuys, traceSells, ...dynamicIndicatorTraces], layoutPrice, {responsive: true});


const layoutIndicator = {
    title: 'Indicator Chart',
    yaxis: { 
        title: 'value :p', 
        showgrid: true, gridcolor: '#e5e7eb',
        ...crosshairSettings
    }
}

Plotly.newPlot("indicator_chart", [...dynamicIndicatorTraces], layoutIndicator, {responsive:true});

//create a string to shove into div

const bigString = ""
const description = explanation.map(row => row.description)
const sharpe = explanation.map(row => row.Sharpe_Ratio) // how are spaces interpreted when turning the data to json
