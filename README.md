# UNUM Back Test 📊

Advanced backtesting engine for the UNUM trading strategy.

## Key Features
- High-performance backtesting using pandas and numpy.
- Multi-timeframe signal confirmation.
- Advanced risk management simulation (Trailing stops, Break-even).
- Performance analytics (Sharpe, Sortino, Max Drawdown).

## Project Structure
- `data/`: Historical OHLCV data.
- `src/`: Core logic.
  - `core/`: Backtest engine and indicators.
  - `utils/`: Data fetching and helpers.
- `results/`: Backtest reports and charts.

## Quick Start
1. Install dependencies: `pip install -r requirements.txt`
2. Fetch data: `python src/fetch_data.py`
3. Run backtest: `python main.py`
