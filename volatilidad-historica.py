import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px

# Function to calculate volatility
def calculate_volatility(data, window):
    returns = data.pct_change()  # Calculate daily percentage change
    volatility = returns.rolling(window=window).std() * np.sqrt(window)  # Rolling standard deviation
    return volatility

# Function to calculate moving average of volatility
def calculate_moving_average(volatility_data, ma_window):
    return volatility_data.rolling(window=ma_window).mean()

# Streamlit app
st.title("Historical Volatility Comparison with Custom Timeframe")

# Input fields for the user
tickers_input = st.text_input("Enter ticker symbols (separated by commas):", value="AAPL, MSFT, GOOG")
tickers = [ticker.strip().upper() for ticker in tickers_input.split(',')]

start_date = st.date_input("Start date", value=pd.to_datetime("2020-01-01"))
end_date = st.date_input("End date", value=pd.to_datetime("today"))

# Input for custom timeframe (trading days)
custom_window = st.number_input("Enter the rolling window in trading days for volatility calculation:", min_value=1, value=21)

# Option to show moving averages of the volatility instead of raw volatility
show_ma = st.checkbox("Show Moving Average of Historical Volatility")

# Input for moving average window (only if checkbox is selected)
if show_ma:
    ma_window = st.number_input("Enter the moving average window (in trading days):", min_value=1, value=10)

# Fetch data and calculate volatility
if st.button("Get Data and Plot Volatility"):
    data = yf.download(tickers, start=start_date, end=end_date)["Adj Close"]

    # Calculate volatility for each ticker
    volatility_data = pd.DataFrame()
    avg_volatility_data = pd.Series(dtype=float)

    for ticker in tickers:
        ticker_volatility = calculate_volatility(data[ticker], custom_window)
        
        # If moving average is selected, calculate it instead of showing raw volatility
        if show_ma:
            ticker_volatility = calculate_moving_average(ticker_volatility, ma_window)
        
        volatility_data[ticker] = ticker_volatility
        avg_volatility_data[ticker] = ticker_volatility.mean()

    # Plotting
    st.subheader(f"Historical Volatility ({custom_window} trading days) {'with Moving Average' if show_ma else ''}")

    volatility_data = volatility_data.dropna()  # Drop rows with NaN values
    fig = px.line(volatility_data, title=f"Volatility Comparison ({custom_window} Trading Days) {'with Moving Average' if show_ma else ''}", 
                  labels={"value": "Volatility", "index": "Date"})

    # Adding average lines for each ticker
    for ticker in tickers:
        fig.add_scatter(x=volatility_data.index, y=[avg_volatility_data[ticker]] * len(volatility_data), 
                        mode='lines', name=f'{ticker} Avg Volatility')

    st.plotly_chart(fig)
