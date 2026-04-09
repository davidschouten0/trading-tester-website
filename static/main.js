//#region constants

const rawData = window.BACKTEST_DATA || [];
const trades = window.TRADES_DATA || [];
const explanation = window.EXPLANATION_DATA || {};

const strategy = explanation.strategy
const ticker = explanation.ticker
//#endregion

//#region static functions  
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
//#endregion

//#region explanations
function renderOverviewTable(stats) {
    const table = document.getElementById("overview_table");
    
    table.innerHTML = `
        <tr>
            <th>Metrik</th>
            <th>Wert</th>
        </tr>
    `;

    const ignoreKeys = ["explanation_quick", "explanation_buying", "ticker", "strategy", "Return (Ann.) [%]"];

    for (const [key, value] of Object.entries(stats)) {
        if (ignoreKeys.includes(key)) continue; 

        const tr = document.createElement("tr");
        const tdKey = document.createElement("td");
        tdKey.textContent = key;
        
        const tdValue = document.createElement("td");
        tdValue.style.textAlign = "right"; 
        
        if (typeof value === "number") {
            tdValue.textContent = value.toFixed(2);
        } else {
            tdValue.textContent = value; 
        }

        tr.appendChild(tdKey);
        tr.appendChild(tdValue);
        table.appendChild(tr);
    }
}
function renderExplanations(stats) {
    const explanation_quick = document.getElementById("explanation_quick");
    if(explanation_quick) explanation_quick.innerHTML = stats.explanation_quick;

    const explanation_buying = document.getElementById("explanation_buying");
    if(explanation_buying) explanation_buying.innerHTML = stats.explanation_buying;
}
//#endregion

//#region graphing
function renderCharts() {
//#region prep data
const dates = rawData.map(row => formatMyDate(row.Datetime || row.Date));
const equityStrat = rawData.map(row => row.Equity_Strat);
const equityBuyAndHold = rawData.map(row => row.Equity_BnH);
const opens = rawData.map(row => row.Open);
const highs = rawData.map(row => row.High);
const lows = rawData.map(row => row.Low);
const closes = rawData.map(row => row.Close);

const myTickVals = [];
const myTickText = [];
const numberOfTicks = 6; 
const step = Math.max(1, Math.floor(dates.length / numberOfTicks));

for (let i = 0; i < dates.length; i += step) {
    myTickVals.push(dates[i]); 
    let cleanDate = dates[i].split(' ').slice(0, 3).join(' '); 
    myTickText.push(cleanDate);
}
//#endregion

//#region base layouts
const crosshairSettings = {
        showspikes: true, spikemode: 'across', spikesnap: 'cursor', 
        spikethickness: 1, spikedash: 'dash', spikecolor: '#9ca3af'
    };

const baseLayout = {
    paper_bgcolor: 'transparent', plot_bgcolor: 'transparent',
    font: { family: 'JetBrains Mono, sans-serif' }, 
    hovermode: 'x unified', 
    hoverlabel: { bgcolor: '#ffffff', bordercolor: '#d1d5db', font: { color: '#000000' } },
    margin: { l: 50, r: 20, t: 50, b: 50 },
    xaxis: { 
        title: 'Datum', type: 'category', tickmode: 'array',
        tickvals: myTickVals, ticktext: myTickText, rangeslider: { visible: false },
        showgrid: true, gridcolor: '#e5e7eb', ...crosshairSettings 
    }
};
//#endregion

//#region equity chart
const traceStrat = { x: dates, y: equityStrat, type: 'scatter', mode: 'lines', name: strategy, line: { color: '#10b981', width: 2, shape: 'spline' } };
const traceBuyAndHold = { x: dates, y: equityBuyAndHold, type: 'scatter', mode: 'lines', name: 'Buy and Hold', line: { color: '#9ca3af', width: 2, shape: 'spline', dash: 'dash' } };
const layoutEquity = { ...baseLayout, title: 'Kapitalentwicklung (Equity Curve)', yaxis: { title: 'Kontostand ($)', showgrid: true, gridcolor: '#e5e7eb', ...crosshairSettings } };
Plotly.newPlot("equity_curve", [traceStrat, traceBuyAndHold], layoutEquity, {responsive: true});
//#endregion

//#region price chart
const traceCandles = { x: dates, open: opens, high: highs, low: lows, close: closes, type: 'candlestick', name: 'Price Action' };
    
const buyDates = [], buyPrices = [], sellDates = [], sellPrices = [];
const gap = 0.005;

trades.forEach(trade => {
    let entryTimeFormatted = formatMyDate(trade.EntryTime);
    let exitTimeFormatted = formatMyDate(trade.ExitTime);
    if (trade.Size > 0) {
        buyDates.push(entryTimeFormatted); buyPrices.push(trade.EntryPrice * (1 - gap));
        sellDates.push(exitTimeFormatted); sellPrices.push(trade.ExitPrice * (1 + gap));
    } else if (trade.Size < 0) {
        sellDates.push(entryTimeFormatted); sellPrices.push(trade.EntryPrice * (1 + gap));
        buyDates.push(exitTimeFormatted); buyPrices.push(trade.ExitPrice * (1 - gap));
    }
});

const traceBuys = { x: buyDates, y: buyPrices, type: 'scatter', mode: 'markers', name: 'Buy', marker: { symbol: 'triangle-up', color: '#10b981', size: 14, line: { width: 1, color: 'black' } }, hoverinfo: 'x+y' };
const traceSells = { x: sellDates, y: sellPrices, type: 'scatter', mode: 'markers', name: 'Sell', marker: { symbol: 'triangle-down', color: '#ef4444', size: 14, line: { width: 1, color: 'black' } }, hoverinfo: 'x+y' };
//#endregion

//#region indicator chart
const standardKeys = ["Datetime", "Date", "Open", "High", "Low", "Close", "Volume", "Equity_Strat", "Equity_BnH"];
const indicatorNames = Object.keys(rawData[0]).filter(key => !standardKeys.includes(key));
const dynamicIndicatorTraces = [];

indicatorNames.forEach(indName => {
    dynamicIndicatorTraces.push({ x: dates, y: rawData.map(row => row[indName]), type: 'scatter', mode: 'lines', name: indName, line: { width: 1.5 }, hoverinfo: 'none' });
});

const layoutPrice = { ...baseLayout, title: 'Fetter Price Chart', yaxis: { title: 'Preis ($)', showgrid: true, gridcolor: '#e5e7eb', ...crosshairSettings } };
Plotly.newPlot("price_chart", [traceCandles, traceBuys, traceSells, ...dynamicIndicatorTraces], layoutPrice, {responsive: true});

if (dynamicIndicatorTraces.length > 0) {
    const layoutIndicator = { ...baseLayout, title: 'Indicator Chart', yaxis: { title: 'Wert', showgrid: true, gridcolor: '#e5e7eb', ...crosshairSettings } };
    Plotly.newPlot("indicator_chart", dynamicIndicatorTraces, layoutIndicator, {responsive:true});
}
//#endregion
}
//#endregion

//#region init
function initApp() {
    console.log("Starte Pingu Trader Dashboard...");
    
    renderOverviewTable(explanation);
    renderExplanations(explanation);
    
    renderCharts();
}

initApp();
//#endregion
