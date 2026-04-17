# 📈 Stock Market Trend Analyzer

A Python-based stock market analysis tool that downloads real NSE market data, calculates technical indicators, detects trend signals, and tracks live prices — all visualized through professional multi-panel charts.

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-2.x-013243?logo=numpy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.x-orange)
![yfinance](https://img.shields.io/badge/yfinance-latest-green)

---

## ✨ Features

- 📥 **Real Data** — Downloads historical stock data for NSE-listed companies via Yahoo Finance
- 📊 **Moving Averages** — Calculates 50-day and 200-day MAs to identify short and long-term trends
- 📉 **RSI Indicator** — Implements Relative Strength Index from scratch using NumPy (no external indicator library)
- 🔔 **Trend Signals** — Automatically detects Golden Cross (uptrend) and Death Cross (downtrend)
- 💹 **Live Prices** — Fetches real-time market prices during NSE hours (9:15 AM – 3:30 PM IST)
- 📈 **Live Price Chart** — Color-coded bar chart showing current price and % change per stock
- 🔄 **Live Tracker** — Tracks price movement over time and plots the trend
- 🖼️ **3-Panel Charts** — Professional Price + Volume + RSI charts saved as PNG files
- ⚖️ **Stock Comparison** — Normalized performance chart comparing multiple stocks on the same scale

---

## 📁 Project Structure

```
stock-market-analyzer/
│
├── stock_analysis.py        # Main script — data download, charts, live prices
│
├── utils/
│   ├── __init__.py          # Makes utils an importable Python package
│   └── indicators.py        # Reusable indicator functions (MA, RSI, Trend)
│
├── output/                  # Auto-created — all saved charts go here
│   ├── RELIANCE_NS_analysis.png
│   ├── INFY_NS_analysis.png
│   ├── TCS_NS_analysis.png
│   ├── comparison.png
│   └── live_prices.png
│
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/stock-market-analyzer.git
cd stock-market-analyzer
```

### 2. Install dependencies
```bash
pip install pandas numpy matplotlib yfinance
```

### 3. Run the analyzer
```bash
python stock_analysis.py
```

> **Note:** Charts are saved automatically to the `output/` folder. Close each chart window to continue to the next stock.

---

## 📊 Sample Output

### 3-Panel Technical Analysis Chart
Each stock gets a chart with 3 panels:
- **Top** — Close price with 50-day and 200-day Moving Averages
- **Middle** — Daily trading volume
- **Bottom** — RSI with overbought (70) and oversold (30) zones highlighted

### Stock Comparison Chart
All stocks normalized to a base of 100 so performance is comparable regardless of actual price level.

### Live Price Chart
Color-coded bar charts:
- 🟢 **Green** — Price is up today
- 🔴 **Red** — Price is down today

---

## 📡 Live Price Feature

```python
# Single stock live price
get_live_price('RELIANCE.NS')

# All stocks in a table
get_all_live_prices(['RELIANCE.NS', 'INFY.NS', 'TCS.NS'])

# Bar chart of live prices
plot_live_prices(['RELIANCE.NS', 'INFY.NS', 'TCS.NS'])

# Track prices over time (useful during market hours)
live_price_tracker(['RELIANCE.NS', 'INFY.NS', 'TCS.NS'], refreshes=5, interval_seconds=30)
```

> **Market Hours:** Live prices update during NSE hours only — Monday to Friday, 9:15 AM to 3:30 PM IST. Outside these hours, the last closing price is shown.

---

## 🧠 How the Indicators Work

### Moving Averages
| Indicator | Window | Purpose |
|-----------|--------|---------|
| MA50 | 50 days | Short-term trend direction |
| MA200 | 200 days | Long-term trend direction |

**Golden Cross** — MA50 crosses above MA200 → Uptrend signal 📈  
**Death Cross** — MA50 crosses below MA200 → Downtrend signal 📉

### RSI (Relative Strength Index)
```
RSI = 100 - (100 / (1 + RS))
where RS = Average Gain / Average Loss over 14 days
```
| RSI Value | Signal |
|-----------|--------|
| Above 70 | Overbought — possible pullback |
| Below 30 | Oversold — possible recovery |
| 30 to 70 | Neutral momentum |

---

## 🗂️ Supported Tickers

Any NSE-listed stock using Yahoo Finance format:

```python
# Examples
'RELIANCE.NS'    # Reliance Industries
'INFY.NS'        # Infosys
'TCS.NS'         # Tata Consultancy Services
'HDFCBANK.NS'    # HDFC Bank
'ICICIBANK.NS'   # ICICI Bank
'WIPRO.NS'       # Wipro
'BAJFINANCE.NS'  # Bajaj Finance
'TATAMOTORS.NS'  # Tata Motors
'ADANIENT.NS'    # Adani Enterprises
'SUNPHARMA.NS'   # Sun Pharma
```

To change the stocks being analyzed, edit the `STOCKS` list in `main()`:
```python
STOCKS = ['HDFCBANK.NS', 'WIPRO.NS', 'ICICIBANK.NS']
```

---

## 🐛 Known Issues & Fixes

### pandas 2.x Compatibility
Newer versions of pandas return a `Series` instead of a scalar for `.max()`, `.min()`, `.mean()`. Fixed by wrapping with `float()`:
```python
float(data['Close'].max())
```

### yfinance MultiIndex Columns
Newer yfinance versions return MultiIndex columns. Fixed by flattening after download:
```python
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)
```

---

## 🚀 Future Improvements

- [ ] Add CSV caching so data isn't re-downloaded every run
- [ ] Build a Streamlit web dashboard for browser-based use
- [ ] Add MACD and Bollinger Bands indicators
- [ ] Connect to Zerodha Kite API for true real-time data
- [ ] Add email/Telegram alerts when Golden Cross is detected

---

## 📚 What I Learned

- Working with real-world time-series financial data using Pandas
- Implementing RSI from scratch using NumPy array operations instead of relying on libraries
- Debugging version compatibility issues between pandas 2.x and yfinance
- Building multi-panel data visualizations with Matplotlib
- Structuring Python projects with reusable modules (`utils/indicators.py`)
- Writing clean functions with proper error handling and docstrings

---

## 👤 Author

**ismail sayyed**  
Electronics & Telecom Engineering Student  
📧 [maazsayyed555@gmail.com]  
🔗 [www.linkedin.com/in/
ismail-sayyed-8a5b66318]  
🐙 [https://github.com/ismailsayyed77/Stock-market-analyzer]
---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

> ⭐ If you found this useful, consider starring the repo!