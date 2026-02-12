import vectorbt as vbt
import pandas as pd
from datetime import datetime, timezone
import dateparser

def fetch_data(symbol: str, timeframe: str, start_date: str, end_date: str = None) -> pd.DataFrame:
    """
    Fetches historical OHLCV data using VectorBT's CCXT integration.
    
    Args:
        symbol (str): Trading pair symbol (e.g., 'BTC/USDT').
        timeframe (str): Timeframe (e.g., '1h', '4h', '1d').
        start_date (str): Start date string.
        end_date (str, optional): End date string. Defaults to None (now).
        
    Returns:
        pd.DataFrame: DataFrame containing Open, High, Low, Close, Volume data.
    """
    print(f"Fetching data for {symbol} ({timeframe}) from {start_date} to {end_date if end_date else 'Now'}...")
    
    # helper to parse dates
    def parse_dt(dt_str):
        if dt_str is None:
            return None
        # Use dateparser for flexible parsing
        dt = dateparser.parse(dt_str)
        if dt:
             # Ensure UTC
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        return dt_str # Return original if parsing fails (vbt might handle relative strings like '1 year ago')

    # Convert start/end to robust format or leave as string if it looks relative
    start = parse_dt(start_date) if 'ago' not in start_date else start_date
    end = parse_dt(end_date) if end_date and 'ago' not in end_date else end_date

    # If end is None, default to Now (UTC) explicitly to avoid ambiguity
    if end is None:
        end = datetime.now(timezone.utc)
    
    try:
        # vbt.CCXTData.download handles pagination and rate limits automatically
        data = vbt.CCXTData.download(
            symbols=symbol,
            timeframe=timeframe,
            start=start,
            end=end,
            exchange='binance',  # Explicitly use Binance
            missing_index='drop',
            retries=3,
            delay=0.5 # Delay to avoid rate limits
        )
        
        ohlcv = data.get()
        
        print(f"Successfully fetched {len(ohlcv)} rows.")
        return ohlcv
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        raise e

if __name__ == "__main__":
    # Quick test
    df = fetch_data('BTC/USDT', '4h', '2023-01-01')
    print(df.head())
