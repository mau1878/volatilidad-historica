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

# Streamlit app
st.title("Historical Volatility Comparison")

# Input fields for the user
tickers_input = st.text_input("Enter ticker symbols (separated by commas):", value="AAPL, MSFT, GOOG")
tickers = [ticker.strip().upper() for ticker in tickers_input.split(',')]

start_date = st.date_input("Start date", value=pd.to_datetime("2020-01-01"))
end_date = st.date_input("End date", value=pd.to_datetime("today"))

# Dropdown menu for volatility timeframe
volatility_timeframe = st.selectbox("Select volatility timeframe", options=["Daily", "Weekly", "Monthly"])
window = 1
if volatility_timeframe == "Weekly":
    window = 5  # Approximation for weekly window
elif volatility_timeframe == "Monthly":
    window = 21  # Approximation for monthly window

# Fetch data and calculate volatility
if st.button("Get Data and Plot Volatility"):
    data = yf.download(tickers, start=start_date, end=end_date)["Adj Close"]

    # Calculate volatility for each ticker
    volatility_data = pd.DataFrame()
    for ticker in tickers:
        volatility_data[ticker] = calculate_volatility(data[ticker], window)
    
    # Plotting
    st.subheader(f"Historical Volatility ({volatility_timeframe})")
    volatility_data = volatility_data.dropna()  # Drop rows with NaN values
    fig = px.line(volatility_data, title="Volatility Comparison", labels={"value": "Volatility", "index": "Date"})
    st.plotly_chart(fig)

