import vectorbt as vbt
import numpy as np

def get_rsi_crossover_signals(close, rsi_window=14, entry_threshold=30, exit_threshold=70):
    """
    Generates entry and exit signals based on RSI Crossover.
    
    Long Entry: RSI crosses over entry_threshold (e.g. 30).
    Long Exit: RSI crosses under exit_threshold (e.g. 70).
    
    Args:
        close (pd.Series or pd.DataFrame): Close prices.
        rsi_window (int OR list): RSI period. VectorBT supports broadcasting.
        entry_threshold (int): RSI level to buy when crossed over.
        exit_threshold (int): RSI level to sell when crossed under.
        
    Returns:
        tuple: (entries, exits)
    """
    # 1. Calculate RSI
    # vbt.RSI.run supports broadcasting, so rsi_window can be a list/range
    rsi = vbt.RSI.run(close, window=rsi_window)
    
    # 2. Generate Signals
    # Cross over 30 -> Buy
    entries = rsi.rsi_crossed_above(entry_threshold)
    
    # Cross under 70 -> Sell
    exits = rsi.rsi_crossed_below(exit_threshold)
    
    return entries, exits
