import sys
import os

# Ensure we can import from src
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_loader import fetch_data
from src.backtest_engine import run_optimization

def main():
    print("=== Antigravity Backtesting Infrastructure ===")
    
    # 1. Configuration
    SYMBOL = 'BTC/USDT'
    TIMEFRAME = '4h'
    START_DATE = '2020-01-01' # 4-5 years of data
    
    # 2. Fetch Data
    try:
        # Load data (OHLCV)
        # For this simple RSI strategy, we mainly need 'Close', but we fetch full OHLCV
        ohlcv = fetch_data(SYMBOL, TIMEFRAME, START_DATE)
        
        if ohlcv is None or ohlcv.empty:
            print("Error: No data fetched.")
            return

        print(f"Data loaded: {len(ohlcv)} records from {ohlcv.index.min()} to {ohlcv.index.max()}")
        
        # 3. Running Backtest Optimization
        # We pass the 'Close' series to the engine
        close_price = ohlcv['Close']
        
        # Run optimization for RSI windows 5 to 50
        print("Starting optimization...")
        portfolio = run_optimization(close_price, rsi_window_start=5, rsi_window_end=50, step=1)
        
        print("\n=== Optimization Complete ===")
        print(f"Best Total Return: {portfolio.total_return().max():.2f}%")
        print(f"Best RSI Window: {portfolio.total_return().idxmax()}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
