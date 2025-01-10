import pandas as pd

def get_crypto_symbols():
    """
    This function scrapes the Yahoo Finance Cryptocurrency page and returns a dictionary of 
    Crypto symbols.
    """

    url = 'https://finance.yahoo.com/markets/crypto/all/'
    df_list = pd.read_html(url)

    df = df_list[0]

    df = df[df['Symbol'] != 'Symbol']

    crypto_symbols = {
        f"{row['Name']} ({row['Symbol']})": f"{row['Symbol']}"
        for _, row in df.iterrows()
    }

    return crypto_symbols