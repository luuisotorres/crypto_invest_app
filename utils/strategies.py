import pandas as pd

# RSI Strategy
def rsi_strategy(data):
    """
    This function creates a simple RSI strategy. 

    When RSI is higher than 70 (overbought), we sell. 
    When RSI is lower than 30 (oversold), we buy.
    """
    signals = []
    for rsi in data["RSI"]:
        if rsi < 30:
            signals.append("Buy")
        elif rsi > 70:
            signals.append("Sell")
        else:
            signals.append("Do nothing")
    return signals

# Bollinger Bands Strategy
def bollinger_bands_stragy(data):
    """
    For Bollinger Bands:

    Sell: When price closes avove the upper band (overbought)
    Buy: When price closes below the lower band (oversold)
    """

    signals = []
    for close, upper, lower in zip(data["Close"], data["Bollinger_Upper"], data["Bollinger_Lower"]):
        if close < lower:
            signals.append("Buy")
        elif close > upper:
            signals.append("Sell")
        else:
            signals.append("Do nothing")
    return signals

def macd_strategy(data):
    """
    For MACD:

    Sell: When the MACD line crosses below the Signal line
    Buy: When the MACD line corsses above the Signal line
    """

    signals = []
    for macd, signal in zip(data["MACD"], data["Signal_Line"]):
        if macd > signal:
            signals.append("Buy")
        elif macd < signal:
            signals.append("Sell")
        else:
            signals.append("Do nothing")
    return signals