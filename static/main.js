const rawData = window.BACKTEST_DATA;
const trades = window.TRADES_DATA || [];
const strategy = window.STRATEGY;

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

// 1. Die Engine bekommt die Uhrzeit (Dein bisheriger Code bleibt hier exakt so!)
const dates = rawData.map(row => formatMyDate(row.Datetime || row.Date));

// ==========================================================
// === DER MAGISCHE TRICK FÜR DIE X-ACHSE ===
// ==========================================================
const myTickVals = [];
const myTickText = [];
const numberOfTicks = 6; // Wie viele Datums-Stempel unten angezeigt werden sollen
const step = Math.max(1, Math.floor(dates.length / numberOfTicks));

for (let i = 0; i < dates.length; i += step) {
    // Die exakte, unsichtbare ID für Plotly (MIT Uhrzeit)
    myTickVals.push(dates[i]); 
    
    // Wir schneiden den Text nach dem 3. Leerzeichen ab (entfernt die Uhrzeit!)
    let cleanDate = dates[i].split(' ').slice(0, 3).join(' '); 
    myTickText.push(cleanDate); // Das ist das, was du unten auf der Achse sehen wirst
}

// Daten entpacken
const equityStrat = rawData.map(row => row.Equity_Strat);
const equityBuyAndHold = rawData.map(row => row.Equity_BnH);
const opens = rawData.map(row => row.Open);
const highs = rawData.map(row => row.High);
const lows = rawData.map(row => row.Low);
const closes = rawData.map(row => row.Close);


// ==========================================================
// 2. DAS ULTIMATIVE BASIS-LAYOUT (DRY)
// ==========================================================
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
        type: 'category', // Dein heiliger Gral für die Wochenenden!
        
        // HIER KOMMT UNSERE MASKE ZUM EINSATZ:
        tickmode: 'array',
        tickvals: myTickVals, // Interne Logik
        ticktext: myTickText, // Das, was für den User gedruckt wird
        
        rangeslider: { visible: false },
        showgrid: true, 
        gridcolor: '#e5e7eb', 
        ...crosshairSettings 
    }
};


// ==========================================================
// 3. GRAPH 1: EQUITY CURVE
// ==========================================================
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
    ...baseLayout, // Erbt alles von oben!
    title: 'Kapitalentwicklung (Equity Curve)',
    yaxis: { 
        title: 'Kontostand ($)', 
        showgrid: true, gridcolor: '#e5e7eb',
        // Entferne crosshairSettings von der Y-Achse, 
        // da 'x unified' keine Y-Crosshairs für die Info-Box benötigt
        ...crosshairSettings
    }
};

Plotly.newPlot("equity_curve", [traceStrat, traceBuyAndHold], layoutEquity, {responsive: true});


// ==========================================================
// 4. GRAPH 2: PRICE CHART (CANDLES)
// ==========================================================
const traceCandles = {
    x: dates,
    open: opens, high: highs, low: lows, close: closes,
    type: 'candlestick', name: 'Price Action'
};

const layoutPrice = {
    ...baseLayout, // Erbt alles von oben!
    title: 'Fetter Price Chart',
    yaxis: { 
        title: 'Preis ($)', 
        showgrid: true, gridcolor: '#e5e7eb',
        // Entferne crosshairSettings von der Y-Achse, 
        // da 'x unified' keine Y-Crosshairs für die Info-Box benötigt
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

// Trades durchlaufen und Buy/Sell Punkte trennen
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

// Trace für die Käufe (Grüne Pfeile)
const traceBuys = {
    x: buyDates,
    y: buyPrices,
    type: 'scatter',
    mode: 'markers', // Wichtig: markers statt lines
    name: 'Buy',
    marker: {
        symbol: 'triangle-up', // Dreieck nach oben
        color: '#10b981',      // Saftiges Grün
        size: 14,              // Schön groß
        line: { width: 1, color: 'black' } // Leichte Umrandung für besseren Kontrast
    },
    hoverinfo: 'x+y'
};

// Trace für die Verkäufe (Rote Pfeile)
const traceSells = {
    x: sellDates,
    y: sellPrices,
    type: 'scatter',
    mode: 'markers',
    name: 'Sell',
    marker: {
        symbol: 'triangle-down', // Dreieck nach unten
        color: '#ef4444',        // Kräftiges Rot
        size: 14,
        line: { width: 1, color: 'black' }
    },
    hoverinfo: 'x+y'
};

Plotly.newPlot("price_chart", [traceCandles, traceBuys, traceSells], layoutPrice, {responsive: true});