import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import yfinance as yf
import numpy as np
import os
from datetime import datetime

os.makedirs('output', exist_ok=True)

def download_stock(ticker, start='2023-01-01', end='2024-01-01'):
    """Download stock data. Returns DataFrame or None on failure."""
    print(f'Downloading {ticker}...')
    try:
        data = yf.download(ticker, start=start, end=end, progress=False)
        if data.empty:
            print(f'No data for {ticker}')
            return None
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        print(f'OK - {len(data)} trading days downloaded')
        return data
    except Exception as e:
        print(f'Error: {e}')
        return None

def explore_data(data, name):
    """Print complete summary before doing analysis."""
    if data is None:
        return
    print(f"\n=== {name} Summary ===")
    print(f"Date range:    {data.index[0].date()} to {data.index[-1].date()}")
    print(f"Trading days:  {len(data)}")
    print(f"Columns:       {list(data.columns)}")
    print(f"\nFirst 3 rows:")
    print(data.head(3))
    print(f"\nKey Statistics:")
    print(f"  Highest close: {float(data['Close'].max()):.2f}")
    print(f"  Lowest close:  {float(data['Close'].min()):.2f}")
    print(f"  Average close: {float(data['Close'].mean()):.2f}")
    print(f"  Missing values:{data.isnull().sum().sum()}")

def add_moving_averages(data):
    """Add 50-day and 200-day MAs plus daily return %."""
    if data is None:
        return None
    data = data.copy()
    data['MA50']         = data['Close'].rolling(window=50).mean()
    data['MA200']        = data['Close'].rolling(window=200).mean()
    data['daily_return'] = data['Close'].pct_change() * 100
    print("Moving averages added (MA50, MA200, daily_return)")
    return data

def calculate_rsi(data, period=14):
    """Calculate RSI indicator."""
    if data is None:
        return None
    data     = data.copy()
    delta    = data['Close'].diff()
    gain     = delta.where(delta > 0, 0)
    loss     = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs       = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))
    print(f"RSI calculated with period {period}")
    return data

def plot_stock_analysis(data, ticker):
    """Create a 3-panel chart: Price + Volume + RSI."""
    if data is None:
        return

    fig, (ax1, ax2, ax3) = plt.subplots(
        3, 1,
        figsize=(14, 10),
        gridspec_kw={'height_ratios': [3, 1, 1]},
        sharex=True
    )
    fig.suptitle(f'{ticker} — Technical Analysis', fontsize=16, fontweight='bold')

    # Panel 1: Price + Moving Averages
    ax1.plot(data.index, data['Close'], label='Close',  color='#2E86AB', linewidth=1.5)
    ax1.plot(data.index, data['MA50'],  label='MA50',   color='#F18F01', linewidth=1.2, linestyle='--')
    ax1.plot(data.index, data['MA200'], label='MA200',  color='#C73E1D', linewidth=1.2, linestyle='-.')
    ax1.set_ylabel('Price (INR)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Panel 2: Volume
    ax2.bar(data.index, data['Volume'], color='#5C6BC0', alpha=0.6)
    ax2.set_ylabel('Volume')
    ax2.grid(True, alpha=0.3)

    # Panel 3: RSI
    if 'RSI' in data.columns:
        ax3.plot(data.index, data['RSI'], color='#7B2D8B', linewidth=1.2)
        ax3.axhline(70, color='red',   linestyle='--', alpha=0.7, label='Overbought (70)')
        ax3.axhline(30, color='green', linestyle='--', alpha=0.7, label='Oversold (30)')
        ax3.fill_between(data.index, data['RSI'], 70, where=(data['RSI'] >= 70), color='red',   alpha=0.2)
        ax3.fill_between(data.index, data['RSI'], 30, where=(data['RSI'] <= 30), color='green', alpha=0.2)
        ax3.set_ylabel('RSI')
        ax3.set_ylim(0, 100)
        ax3.legend()
        ax3.grid(True, alpha=0.3)

    plt.xlabel('Date')
    plt.tight_layout()
    filename = f"output/{ticker.replace('.', '_')}_analysis.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f'Chart saved: {filename}')
    plt.show()

def analyze_trend(data, ticker):
    """Analyze trend using MAs and RSI."""
    if data is None or data['MA50'].isna().all():
        print('Not enough data to analyze.')
        return

    latest = data.iloc[-1]
    ma50   = float(latest['MA50'])
    ma200  = float(latest['MA200'])
    close  = float(latest['Close'])
    rsi    = float(latest['RSI']) if 'RSI' in data.columns else None

    print(f'\n=== Trend Report: {ticker} ===')
    print(f'  Close: {close:.2f}')
    print(f'  MA50:  {ma50:.2f}')
    print(f'  MA200: {ma200:.2f}')

    if ma50 > ma200:
        print('  SIGNAL: UPTREND — Golden Cross (50MA > 200MA)')
    else:
        print('  SIGNAL: DOWNTREND — Death Cross (50MA < 200MA)')

    if close > ma50:
        print('  Price is ABOVE 50-Day MA (bullish short-term)')
    else:
        print('  Price is BELOW 50-Day MA (bearish short-term)')

    if rsi is not None:
        label = 'OVERBOUGHT' if rsi > 70 else ('OVERSOLD' if rsi < 30 else 'Neutral')
        print(f'  RSI: {rsi:.1f} — {label}')

def compare_stocks(tickers, start='2023-01-01', end='2024-01-01'):
    """Compare stocks on a normalized chart (all start at 100)."""
    plt.figure(figsize=(14, 7))
    colors  = ['#2E86AB', '#F18F01', '#C73E1D', '#5C6BC0']
    results = {}

    for i, ticker in enumerate(tickers):
        data = download_stock(ticker, start, end)
        if data is None:
            continue
        normalized = (data['Close'] / data['Close'].iloc[0]) * 100
        plt.plot(normalized, label=ticker, color=colors[i % len(colors)], linewidth=1.8)
        results[ticker] = {
            'total_return': float((data['Close'].iloc[-1] / data['Close'].iloc[0] - 1) * 100),
            'volatility':   float(data['Close'].pct_change().std() * 100)
        }

    plt.axhline(100, color='gray', linestyle='--', alpha=0.5)
    plt.title('Stock Comparison (Normalized to 100)', fontsize=14, fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('Normalized Price')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('output/comparison.png', dpi=150, bbox_inches='tight')
    plt.show()

    print(f'\n{"Ticker":<15} {"Return":>12} {"Volatility":>12}')
    print('-' * 41)
    for t, s in results.items():
        print(f'{t:<15} {s["total_return"]:>11.2f}% {s["volatility"]:>11.2f}%')

# ══════════════════════════════════════════════
# LIVE PRICE FEATURES  (new)
# ══════════════════════════════════════════════

def get_live_price(ticker):
    """
    Fetch the current live market price for a single stock.
    Works during NSE hours (9:15 AM - 3:30 PM IST, Mon-Fri).
    Outside hours it returns the last closing price.
    """
    try:
        stock = yf.Ticker(ticker)
        price = stock.fast_info['last_price']
        change = stock.fast_info.get('regularMarketChange', 0)
        change_pct = stock.fast_info.get('regularMarketChangePercent', 0)
        high  = stock.fast_info.get('dayHigh', 0)
        low   = stock.fast_info.get('dayLow', 0)
        now   = datetime.now().strftime('%H:%M:%S')

        direction = '▲' if change >= 0 else '▼'
        color_tag = '+' if change >= 0 else ''

        print(f"\n{'='*45}")
        print(f"  {ticker} — Live Price  [{now}]")
        print(f"{'='*45}")
        print(f"  Price:   ₹{price:.2f}  {direction} {color_tag}{change:.2f} ({color_tag}{change_pct:.2f}%)")
        print(f"  Day High: ₹{high:.2f}   Day Low: ₹{low:.2f}")
        print(f"{'='*45}")

        return price
    except Exception as e:
        print(f'Could not fetch live price for {ticker}: {e}')
        return None


def get_all_live_prices(tickers):
    """
    Fetch and display live prices for multiple stocks
    in a clean comparison table.
    """
    print(f"\n{'='*60}")
    print(f"  LIVE PRICES  —  {datetime.now().strftime('%d %b %Y  %H:%M:%S')}")
    print(f"  (During market hours: real-time  |  After hours: last close)")
    print(f"{'='*60}")
    print(f"  {'Ticker':<15} {'Price':>10} {'Change':>10} {'Change%':>10}")
    print(f"  {'-'*50}")

    prices = {}
    for ticker in tickers:
        try:
            stock      = yf.Ticker(ticker)
            price      = stock.fast_info['last_price']
            change     = stock.fast_info.get('regularMarketChange', 0)
            change_pct = stock.fast_info.get('regularMarketChangePercent', 0)
            direction  = '▲' if change >= 0 else '▼'
            sign       = '+' if change >= 0 else ''
            print(f"  {ticker:<15} ₹{price:>8.2f}  {direction} {sign}{change:>6.2f}  {sign}{change_pct:>6.2f}%")
            prices[ticker] = price
        except Exception as e:
            print(f"  {ticker:<15}  Error: {e}")

    print(f"{'='*60}\n")
    return prices


def plot_live_prices(tickers):
    """
    Fetch live prices for all tickers and show a bar chart.
    Green bar = price up today, Red bar = price down today.
    Also saves the chart to output/live_prices.png.
    """
    print("Fetching live prices for chart...")

    names   = []
    prices  = []
    changes = []
    colors  = []

    for ticker in tickers:
        try:
            stock      = yf.Ticker(ticker)
            price      = stock.fast_info['last_price']
            change_pct = stock.fast_info.get('regularMarketChangePercent', 0)
            names.append(ticker.replace('.NS', ''))
            prices.append(round(price, 2))
            changes.append(round(change_pct, 2))
            colors.append('#2ECC71' if change_pct >= 0 else '#E74C3C')
        except Exception as e:
            print(f'Skipping {ticker}: {e}')

    if not prices:
        print('No live data available.')
        return

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    fig.suptitle(
        f"Live Stock Prices  —  {datetime.now().strftime('%d %b %Y  %H:%M:%S')}",
        fontsize=14, fontweight='bold'
    )

    # Top chart — Current Price bars
    bars = ax1.bar(names, prices, color=colors, edgecolor='white', linewidth=1.2, width=0.5)
    ax1.set_ylabel('Current Price (₹)', fontsize=11)
    ax1.set_title('Current Price per Stock', fontsize=12)
    ax1.grid(True, axis='y', alpha=0.3)

    # Add price labels on top of each bar
    for bar, price in zip(bars, prices):
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(prices) * 0.01,
            f'₹{price:.2f}',
            ha='center', va='bottom',
            fontsize=11, fontweight='bold'
        )

    # Bottom chart — % Change bars
    change_colors = ['#2ECC71' if c >= 0 else '#E74C3C' for c in changes]
    bars2 = ax2.bar(names, changes, color=change_colors, edgecolor='white', linewidth=1.2, width=0.5)
    ax2.set_ylabel('Change % Today', fontsize=11)
    ax2.set_title('Price Change % Today', fontsize=12)
    ax2.axhline(0, color='gray', linewidth=0.8)
    ax2.grid(True, axis='y', alpha=0.3)

    # Add % labels on bars
    for bar, chg in zip(bars2, changes):
        sign = '+' if chg >= 0 else ''
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + (0.05 if chg >= 0 else -0.15),
            f'{sign}{chg:.2f}%',
            ha='center', va='bottom',
            fontsize=11, fontweight='bold', color='white'
        )

    plt.tight_layout()
    filename = 'output/live_prices.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f'Live price chart saved: {filename}')
    plt.show()


def live_price_tracker(tickers, refreshes=5, interval_seconds=30):
    """
    Track live prices over time and plot how they move.
    Fetches price every 'interval_seconds' seconds, 'refreshes' times.
    Default: fetches 5 times every 30 seconds = ~2.5 minutes of tracking.
    Only useful during market hours (9:15 AM - 3:30 PM IST).
    """
    import time

    print(f"\nStarting live tracker — {refreshes} readings every {interval_seconds}s")
    print("Press Ctrl+C to stop early\n")

    history = {t: [] for t in tickers}
    times   = []

    try:
        for i in range(refreshes):
            now = datetime.now().strftime('%H:%M:%S')
            times.append(now)
            print(f"Reading {i+1}/{refreshes}  [{now}]")

            for ticker in tickers:
                try:
                    price = yf.Ticker(ticker).fast_info['last_price']
                    history[ticker].append(round(price, 2))
                    print(f"  {ticker}: ₹{price:.2f}")
                except:
                    history[ticker].append(None)

            if i < refreshes - 1:
                print(f"  Waiting {interval_seconds}s...\n")
                time.sleep(interval_seconds)

    except KeyboardInterrupt:
        print("\nTracker stopped early.")

    # Plot the tracked prices
    plt.figure(figsize=(12, 6))
    colors = ['#2E86AB', '#F18F01', '#C73E1D', '#5C6BC0']

    for i, ticker in enumerate(tickers):
        valid_times  = [t for t, p in zip(times, history[ticker]) if p is not None]
        valid_prices = [p for p in history[ticker] if p is not None]
        if valid_prices:
            plt.plot(valid_times, valid_prices,
                     label=ticker,
                     color=colors[i % len(colors)],
                     marker='o', linewidth=2, markersize=6)

    plt.title('Live Price Tracker', fontsize=14, fontweight='bold')
    plt.xlabel('Time')
    plt.ylabel('Price (₹)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('output/live_tracker.png', dpi=150, bbox_inches='tight')
    print('\nTracker chart saved: output/live_tracker.png')
    plt.show()


# ══════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════

def main():
    """Main entry point — runs the full analysis pipeline."""
    print('=== Stock Market Trend Analyzer ===')

    STOCKS = ['WIPRO.NS', 'INFY.NS', 'TCS.NS']
    START  = '2025-01-01'
    END    = '2026-01-01'

    # ── Historical Analysis ──
    for ticker in STOCKS:
        print(f'\n--- Processing {ticker} ---')
        data = download_stock(ticker, START, END)
        data = add_moving_averages(data)
        data = calculate_rsi(data)
        explore_data(data, ticker)
        analyze_trend(data, ticker)
        plot_stock_analysis(data, ticker)

    compare_stocks(STOCKS, START, END)

    # ── Live Price Features ──
    print('\n--- Live Prices ---')

    # 1. Single stock live price
    get_live_price('RELIANCE.NS')

    # 2. All stocks live price table
    get_all_live_prices(STOCKS)

    # 3. Live price bar chart (saves to output/live_prices.png)
    plot_live_prices(STOCKS)

    # 4. Live tracker — uncomment to track prices over time
    # Only useful during market hours (9:15 AM - 3:30 PM IST Mon-Fri)
    # live_price_tracker(STOCKS, refreshes=5, interval_seconds=30)

    print('\nDone! All charts saved to output/ folder.')


if __name__ == '__main__':
    main()