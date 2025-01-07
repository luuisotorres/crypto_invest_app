import yfinance as yf
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
from utils import calculate_bollinger_bands, calculate_macd, calculate_rsi

# Configuração da interface do Streamlit
st.title("Plataforma de Análise e Previsão de Criptomoedas")
st.write("Explore tendências, indicadores técnicos e previsões para tomar decisões informadas.")

# Seleção da criptomoeda
crypto_symbols = {
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Binance Coin (BNB)": "BNB-USD",
    "Ripple (XRP)": "XRP-USD",
}

crypto = st.selectbox("Escolha a criptomoeda:", list(crypto_symbols.keys()))
symbol = crypto_symbols[crypto]

# Seleção do período
period = st.radio("Selecione o período para análise:", ["1mo", "3mo", "6mo", "1y", "5y"])

# Baixar os dados do Yahoo Finance
data = yf.download(symbol, period=period)
data = data.reset_index()
data.columns = data.columns.get_level_values(0)
data.rename(columns={"index": 'Date'}, inplace=True)
st.write("### Dados Históricos de Preços")
st.dataframe(data.tail())

# Cálculo das Médias Móveis
data["SMA_20"] = data["Close"].rolling(window=20).mean()
data["EMA_10"] = data["Close"].ewm(span=10, adjust=False).mean()

# Adding Candlestick chart
st.write('### Gráfico de Preços')

fig = go.Figure(data=[go.Candlestick(
    x=data['Date'],
    open=data['Open'],
    high=data['High'],
    low=data['Low'],
    close=data['Close'],
    increasing_line_color = 'green',
    decreasing_line_color='red'
)])

fig.update_layout(
    title=f'Gráfico de Preços: {crypto}',
    xaxis_title = 'Data',
    yaxis_title = 'Preço (USD)',
    xaxis_rangeslider_visible = False,
    template = 'plotly_white'
)

fig.add_trace(go.Scatter(
    x=data['Date'],
    y=data['SMA_20'],
    mode='lines',
    name='SMA 20',
    line=dict(color="blue", width=2)
))

fig.add_trace(go.Scatter(
    x=data['Date'],
    y=data['EMA_10'],
    mode='lines',
    name='EMA 10',
    line=dict(color="yellow", width=2)
))

st.plotly_chart(fig, use_container_width=True)


data["RSI"] = calculate_rsi(data)
st.write("### RSI (Índice de Força Relativa)")
st.line_chart(data["RSI"])

data = calculate_bollinger_bands(data)
st.write("### Bandas de Bollinger")
st.line_chart(data[["Close", "Bollinger_Upper", "Bollinger_Lower"]])

data = calculate_macd(data)
st.write("### MACD (Convergência/Divergência de Médias Móveis)")
st.line_chart(data[["MACD", "Signal_Line"]])

# Previsão com Regressão Linear
data["Days"] = (data.Date - data.Date[0]).days
X = np.array(data["Days"]).reshape(-1, 1)
y = data["Close"]

model = LinearRegression()
model.fit(X, y)
data["Linear_Prediction"] = model.predict(X)

st.write("### Previsão com Regressão Linear")
st.line_chart(data[["Close", "Linear_Prediction"]])

# Previsão com ARIMA
def arima_forecast(data, periods=10):
    model = ARIMA(data["Close"], order=(1, 1, 1))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=periods)
    return forecast

forecast = arima_forecast(data)
st.write("### Previsão com ARIMA (Próximos 10 dias)")
st.write(forecast)

# Simulador de Investimento
st.write("### Simulador de Investimento")
initial_investment = st.number_input("Valor inicial de investimento (USD):", value=1000.0)
if initial_investment > 0:
    closing_prices = data["Close"].values
    if len(closing_prices) > 0:
        investment_return = initial_investment * (closing_prices[-1] / closing_prices[0])
        st.write(f"Com um investimento inicial de **${initial_investment:.2f}**, o retorno seria **${investment_return:.2f}** no período escolhido.")

# Estratégia Baseada no RSI
def rsi_strategy(data):
    signals = []
    for rsi in data["RSI"]:
        if rsi < 30:
            signals.append("Comprar")
        elif rsi > 70:
            signals.append("Vender")
        else:
            signals.append("Manter")
    return signals

data["Estratégia RSI"] = rsi_strategy(data)
st.write("### Sinal de Estratégia RSI")
st.dataframe(data[["Close", "RSI", "Estratégia RSI"]])
