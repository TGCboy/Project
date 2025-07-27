import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import date

# Page setup
st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.title("📈 Stock Market Dashboard")

# Sidebar inputs
st.sidebar.header("User Input")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")
start_date = st.sidebar.date_input("Start Date", value=date(2000, 1, 1))
end_date = st.sidebar.date_input("End Date", value=date.today())

@st.cache_data
def load_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end, interval='1d')
    data.reset_index(inplace=True)

    # Flatten multi-level columns (if any)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [' '.join(col).strip() for col in data.columns.values]

    # Convert 'Date' column to date only (no time)
    if 'Date' in data.columns:
        data['Date'] = pd.to_datetime(data['Date']).dt.date
    return data

data = load_data(ticker, start_date, end_date)

# Show raw data table
st.subheader(f"Raw Data for {ticker}")
st.dataframe(data.tail())

# Convert Date back to datetime for plotting
data['Date'] = pd.to_datetime(data['Date'])

# Find the column that contains 'Close' (e.g., 'Close AAPL')
close_col = [col for col in data.columns if 'Close' in col][0]

# Plot the data
fig = px.line(data, x='Date', y=close_col, title=f"{ticker} Closing Price Over Time")
st.plotly_chart(fig, use_container_width=True)


