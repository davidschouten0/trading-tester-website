// ==========================================================
// 1. DATEN VORBEREITEN
// ==========================================================
const rawData = window.BACKTEST_DATA;
const strategy = window.STRATEGY;

const dates = rawData.map(row => {
    const rawString = row.Datetime || row.Date;
    const d = new Date(rawString);
    
    // Wir formatieren das Datum DIREKT in JavaScript exakt so, wie du es willst.
    // Ausgabe wird exakt: "Nov 5, 2026"
    return d.toLocaleDateString('en-US', {
        month: 'short', 
        day: 'numeric',
        year: 'numeric' // Das verhindert den Spaghetti-Fehler!
    });
});

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

// Der Fadenkreuz-Baustein (wird für X- und Y-Achse genutzt)
const crosshairSettings = {
    showspikes: true,
    spikemode: 'across', 
    spikesnap: 'cursor', // Die gestrichelte Linie folgt IMMER exakt deiner unsichtbaren Maus
    spikethickness: 1,   
    spikedash: 'dash',   
    spikecolor: '#9ca3af'
};

// Das Master-Layout für BEIDE Graphen
const baseLayout = {
    paper_bgcolor: 'transparent', 
    plot_bgcolor: 'transparent',
    font: { family: 'JetBrains Mono, sans-serif' }, 
    
    // DIE KORREKTUR: Verwende 'x unified', um eine feststehende Info-Box 
    // zu erstellen, die dem X-Cursor folgt und alle Daten anzeigt.
    hovermode: 'x unified', // Dies ist der TradingView-Style, den du wolltest.
    
    hoverlabel: {
        bgcolor: '#ffffff', 
        bordercolor: '#d1d5db', 
        font: { color: '#000000' }
    },
    margin: { l: 50, r: 20, t: 50, b: 50 },

    // Gemeinsame X-Achse (Gilt für Equity UND Candles)
    xaxis: { 
        title: 'Datum', 
        type: 'category', // Wichtig: Zieht Wochenenden bei BEIDEN Graphen zusammen!
        nticks: 5, 
        rangeslider: { visible: false },
        showgrid: true, 
        gridcolor: '#e5e7eb', 
        tickformat: '%b %-d, %Y', 
        
        // NEU: Das macht das Hover-Label (am Fadenkreuz) exakt gleich!
        hoverformat: '%b %-d, %Y',
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

Plotly.newPlot("price_chart", [traceCandles], layoutPrice, {responsive: true});