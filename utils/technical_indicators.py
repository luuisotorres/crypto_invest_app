# Calculating RSI
def calculate_rsi(data, window=14):
    """
    This function calculates the RSI (Relative Strength Index) for a specific dataset

    Args:
        data (pd.DataFrame): Pandas DF containing a 'Close' column.
        window (int): Number of periods for the RSI

    Returns:
        pd.Series: RSI values for the dataset
    """
    delta = data["Close"].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))
    return data

# Calculating Bollinger Bands
def calculate_bollinger_bands(data, window=20):
    """
    This function calculates Bollinger Bands to define upper and lower price bands based on a 
    moving average and standard deviation.

    Args:
        data (pd.DataFrame): Pandas DataFrame containing a 'Close' column with closing prices.
        window (int): Number of periods to calculate the Simple Moving Average and Standard Deviation.

    Returns:
        pd.DataFrame: DataFrame with additional columns:
            - 'Bollinger_Upper': Upper Bollinger Band
            - 'Bollinger_Lower': Lower Bollinger Band
    """
    sma = data["Close"].rolling(window=window).mean()
    std = data["Close"].rolling(window=window).std()
    data["Bollinger_Upper"] = sma + (std * 2)
    data["Bollinger_Lower"] = sma - (std * 2)
    return data

# Calculate MACD
def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    """
    This function calculates the MACD, a momentum indicator that shows the relationship between 
    two moving averages of an asset's price.

    Args:
        data (pd.DataFrame): Pandas DataFrame containing a 'Close' column with closing prices.
        short_window (int): Period for the short-term Exponential Moving Average (EMA).
        long_window (int): Period for the long-term Exponential Moving Average (EMA).
        signal_window (int): Period for the Signal Line, which is an EMA of the MACD.

    Returns:
        pd.DataFrame: DataFrame with additional columns:
            - 'MACD': The difference between the short-term and long-term EMAs.
            - 'Signal_Line': EMA of the MACD, used as a signal line.
    """
    short_ema = data["Close"].ewm(span=short_window, adjust=False).mean()
    long_ema = data["Close"].ewm(span=long_window, adjust=False).mean()
    data["MACD"] = short_ema - long_ema
    data["Signal_Line"] = data["MACD"].ewm(span=signal_window, adjust=False).mean()
    return data