import vectorbt as vbt
import pandas as pd
import numpy as np
from src.strategy import get_rsi_crossover_signals

def run_optimization(close_price: pd.DataFrame, 
                     rsi_window_start=5, 
                     rsi_window_end=50, 
                     step=1):
    """
    Runs a backtest optimization over a range of RSI windows.
    
    Args:
        close_price (pd.DataFrame): Historical close prices.
        rsi_window_start (int): Start of RSI window range.
        rsi_window_end (int): End of RSI window range.
        step (int): Step size.
    """
    print(f"Running optimization for RSI Window {rsi_window_start} to {rsi_window_end}...")
    
    # 1. Define Parameter Grid
    windows = np.arange(rsi_window_start, rsi_window_end + 1, step)
    
    # 2. Run Strategy (Vectorized)
    # This will compute RSI for ALL windows simultaneously
    entries, exits = get_rsi_crossover_signals(close_price, rsi_window=windows)
    
    # 3. Run Portfolio Backtest
    # 'freq' should be inferred or passed. 
    # If using standard pandas index with datetime, vbt infers it.
    portfolio = vbt.Portfolio.from_signals(
        close_price, 
        entries, 
        exits, 
        init_cash=10000,
        fees=0.001, # 0.1% fee (Binance standard)
        freq='1h' # Assuming 1h timeframe, but better to detect
    )
    
    # 4. Analyze Results
    total_return = portfolio.total_return()
    
    print("\n--- Top 5 Configurations ---")
    print(total_return.sort_values(ascending=False).head(5))
    
    # 5. Visualization (Heatmap)
    # Plot Total Return vs RSI Window
    # Since we only varied Window, it's a 1D plot (Line or Bar), but we can map it.
    # If we varied two params (e.g. window and threshold), it would be a heatmap.
    # For now, let's plot the metric.
    
    fig = total_return.vbt.plot(
        title='Total Return by RSI Window',
        xaxis_title='RSI Window',
        yaxis_title='Total Return (%)'
    )
    
    # Create results directory if it doesn't exist
    import os
    os.makedirs('results', exist_ok=True)
    
    # Save chart
    output_path = "results/rsi_optimization.html"
    fig.write_html(output_path)
    print(f"\nOptimization chart saved to {output_path}")
    
    return portfolio
