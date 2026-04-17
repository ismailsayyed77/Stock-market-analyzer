import pandas as pd
import numpy as np

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