import yfinance as yf
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
from utils import calculate_bollinger_bands, calculate_macd, calculate_rsi
from utils import get_crypto_symbols
from utils import rsi_strategy, macd_strategy, bollinger_bands_stragy

# Setting title
st.title("CoinVision ₿")
st.write("Explore trends, technical indicators, and many more!")

# Selecting cryptocurrency
crypto_symbols = get_crypto_symbols()
crypto = st.selectbox("Choose cryptocurrency:", sorted(crypto_symbols.keys()))
symbol = crypto_symbols[crypto]

# Selecting period
period = st.radio("Select period for analysis:", ["1mo", "3mo", "6mo", "1y", "5y"])

# Downloading Yahoo Finance data
data = yf.download(symbol, period=period)
data = data.reset_index()
data.columns = data.columns.get_level_values(0)
data.rename(columns={"index": 'Date'}, inplace=True)
st.write("### Price History")
st.dataframe(data.tail())

# Calculating indicators
data["SMA_20"] = data["Close"].rolling(window=20).mean()
data["EMA_10"] = data["Close"].ewm(span=10, adjust=False).mean()
data["RSI"] = calculate_rsi(data)
data = calculate_bollinger_bands(data)
data = calculate_macd(data)

# Plotting Candlestick chart
st.write('### Price Chart')

indicator = st.selectbox(
    "Select indicator:",
    ["RSI", "Bollinger Bands", "MACD"]
)

fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.15,
    row_heights=[.7,.3]
)

fig.add_trace(go.Candlestick(
    x=data['Date'],
    open=data['Open'],
    high=data['High'],
    low=data['Low'],
    close=data['Close'],
    increasing_line_color = 'green',
    decreasing_line_color='red',
    name = 'Candlestick'
),
row = 1, col = 1
)

fig.add_trace(go.Scatter(
    x=data['Date'],
    y=data['SMA_20'],
    mode='lines',
    name='SMA 20',
    line=dict(color="blue", width=2)
),
row = 1, col = 1)

fig.add_trace(go.Scatter(
    x=data['Date'],
    y=data['EMA_10'],
    mode='lines',
    name='EMA 10',
    line=dict(color="yellow", width=2)
),
row = 1, col = 1)

fig['layout']['yaxis2']['title'] = indicator

if indicator == "RSI":
    fig.add_trace(
        go.Scatter(
            x=data['Date'],
            y=data['RSI'],
            mode='lines',
            name = 'RSI'
        ),
        row = 2, col = 1
    )

elif indicator == 'Bollinger Bands':
    fig.add_trace(
        go.Scatter(
            x=data['Date'],
            y=data['Close'],
            mode='lines',
            name = 'Bollinger Bands'
        ),
        row = 2, col = 1
    )

    fig.add_trace(
        go.Scatter(
            x=data['Date'],
            y=data['Bollinger_Upper'],
            mode='lines',
            name="Upper Band",
            line=dict(color='red', dash='dot')
        ),
        row = 2, col = 1
    )

    fig.add_trace(
        go.Scatter(
            x=data['Date'],
            y=data['Bollinger_Lower'],
            mode='lines',
            name='Lower Band',
            line=dict(color='red', dash='dot')
        ),
        row=2, col=1
    )

elif indicator == "MACD":
    fig.add_trace(
        go.Scatter(
            x=data['Date'],
            y=data['MACD'],
            mode='lines',
            name='MACD'
        ),
        row = 2, col = 1
    )

    fig.add_trace(
        go.Scatter(
            x=data['Date'],
            y=data['Signal_Line'],
            mode='lines',
            name='Signal Line'
        ),
        row = 2, col = 1 
    )
fig.update_layout(
    title=f'Price Chart: {crypto}',
    xaxis_title = 'Date',
    yaxis_title = 'Price (USD)',
    xaxis_rangeslider_visible = False,
    template = 'plotly_white',
    hovermode='x unified',
    height = 800, width = 1000
)
st.plotly_chart(fig, use_container_width=True)

# Computing Strategies
data["RSI Strategy"] = rsi_strategy(data)
data["Bollinger Bands Strategy"] = bollinger_bands_stragy(data)
data["MACD Strategy"] = macd_strategy(data)

st.write(f"### {indicator} Strategy Signal")
if indicator == "RSI":
    st.dataframe(data[["Date", "Close", "RSI", "RSI Strategy"]].dropna()[::-1])

elif indicator == "Bollinger Bands":
    st.dataframe(data[["Date", "Close", "Bollinger Bands Strategy"]].dropna()[::-1])

elif indicator == "MACD":
    st.dataframe(data[["Date", "Close", "MACD Strategy"]].dropna()[::-1])