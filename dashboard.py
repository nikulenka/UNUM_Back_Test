import streamlit as st
import pandas as pd
import vectorbt as vbt
import sys
import os
from datetime import datetime, timedelta

# Ensure correct path to src
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from src.data_loader import fetch_data
from src.strategy import get_rsi_crossover_signals
from src.backtest_engine import run_optimization

# --- Page Config ---
st.set_page_config(
    page_title="Antigravity Backtester",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Antigravity Backtesting Sandbox")

# --- Sidebar: Configuration ---
st.sidebar.header("⚙️ Configuration")

symbol = st.sidebar.text_input("Symbol", value="BTC/USDT")
timeframe = st.sidebar.selectbox("Timeframe", ["1h", "4h", "1d"], index=1)

# Date Picker (Default to last 4 years)
today = datetime.now()
default_start = today - timedelta(days=365*4)
start_date = st.sidebar.date_input("Start Date", value=default_start, min_value=datetime(2010, 1, 1))
end_date = st.sidebar.date_input("End Date", value=today, min_value=datetime(2010, 1, 1))

st.sidebar.markdown("---")
st.sidebar.header("RSI Parameters")

# Optimization Range
rsi_min = st.sidebar.number_input("RSI Window (Min)", 5, 100, 5)
rsi_max = st.sidebar.number_input("RSI Window (Max)", 5, 100, 50)
rsi_step = st.sidebar.number_input("App Step", 1, 10, 1)

# Single Run Params
st.sidebar.markdown("---")
st.sidebar.subheader("Single Run Config")
rsi_window_single = st.sidebar.slider("RSI Window (Single)", 5, 100, 14)
rsi_entry = st.sidebar.number_input("Entry Threshold (<)", 10, 50, 30)
rsi_exit = st.sidebar.number_input("Exit Threshold (>)", 50, 90, 70)

# --- Main Logic ---

if st.sidebar.button("Run Backtest"):
    with st.spinner("Fetching Data and Running Backtest..."):
        try:
            # 1. Fetch Data
            # Convert dates to strings for our data loader
            ohlcv = fetch_data(
                symbol, 
                timeframe, 
                start_date.strftime("%Y-%m-%d"), 
                end_date.strftime("%Y-%m-%d")
            )
            
            if ohlcv is None or ohlcv.empty:
                st.error("No data fetched. Check symbol or date range.")
            else:
                st.success(f"Loaded {len(ohlcv)} bars.")
                close_price = ohlcv['Close']
                
                # Create Tabs
                tab1, tab2 = st.tabs(["📈 Single Strategy Analysis", "🔥 Parameter Optimization"])
                
                # --- TAB 1: Single Strategy ---
                with tab1:
                    st.subheader(f"Single Run: RSI {rsi_window_single} ({rsi_entry}/{rsi_exit})")
                    
                    # Run Strategy
                    entries, exits = get_rsi_crossover_signals(
                        close_price, 
                        rsi_window=rsi_window_single, 
                        entry_threshold=rsi_entry, 
                        exit_threshold=rsi_exit
                    )
                    
                    portfolio = vbt.Portfolio.from_signals(
                        close_price, 
                        entries, 
                        exits, 
                        init_cash=10000,
                        fees=0.001,
                        freq=timeframe
                    )
                    
                    # Metrics
                    col1, col2, col3 = st.columns(3)
                    total_return = portfolio.total_return()
                    win_rate = portfolio.trades.win_rate()
                    max_drawdown = portfolio.drawdown().max()
                    
                    col1.metric("Total Return [%]", f"{total_return * 100:.2f}%")
                    col2.metric("Win Rate [%]", f"{win_rate * 100:.2f}%")
                    col3.metric("Max Drawdown [%]", f"{max_drawdown * 100:.2f}%")
                    
                    # Plots
                    st.plotly_chart(portfolio.plot(), use_container_width=True)
                    
                # --- TAB 2: Optimization ---
                with tab2:
                    st.subheader("Optimization Heatmap")
                    if rsi_max <= rsi_min:
                        st.warning("Max Window must be > Min Window for optimization.")
                    else:
                        portfolio_opt = run_optimization(
                            close_price, 
                            rsi_window_start=rsi_min, 
                            rsi_window_end=rsi_max, 
                            step=rsi_step
                        )
                        
                        # Results
                        returns = portfolio_opt.total_return()
                        
                        # Plot
                        # Since it's 1D optimization (Window), it's a line chart, but we can make it look nice
                        fig = returns.vbt.plot(
                            title='Total Return by RSI Window',
                            xaxis_title='RSI Window',
                            yaxis_title='Total Return (%)'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Top 5 Table
                        st.write("Top 5 Configurations:")
                        st.dataframe(returns.sort_values(ascending=False).head(5))

        except Exception as e:
            st.error(f"Error: {e}")
            # st.exception(e) # Uncomment for debug stack trace

else:
    st.info("👈 Configure settings in the sidebar and click 'Run Backtest'")
