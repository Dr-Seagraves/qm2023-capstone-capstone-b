"""
Fetch Cryptocurrency Data from CoinMetrics
===========================================

This script fetches historical daily price data for the top 100 cryptocurrencies
from CoinMetrics GitHub repository (free CSV downloads).

Data includes: date, price, marketcap, etc.

Output: data/raw/crypto_raw.csv
"""

import pandas as pd
import requests
import io
from config_paths import RAW_DATA_DIR, ensure_directories

# Ensure directories exist
ensure_directories()

def get_top_coins(limit=10):
    """Get list of top coins symbols."""
    # Fallback list of top crypto symbols
    return ['btc', 'eth', 'usdt', 'bnb', 'xrp', 'ada', 'sol', 'dot', 'doge', 'avax'][:limit]

def download_coinmetrics_data(symbol):
    """Download CSV for a coin from CoinMetrics."""
    url = f"https://raw.githubusercontent.com/coinmetrics/data/master/csv/{symbol}.csv"
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(io.StringIO(response.text))
        df['symbol'] = symbol
        return df
    except Exception as e:
        print(f"Error downloading {symbol}: {e}")
        return pd.DataFrame()

def main():
    print("Fetching cryptocurrency data from CoinMetrics...")

    # Get top 10 for demo (to avoid too many downloads)
    top_symbols = get_top_coins(10)  # Change to 100 if needed
    print(f"Found {len(top_symbols)} top symbols: {top_symbols}")

    all_data = []

    for symbol in top_symbols:
        print(f"Downloading {symbol}")
        df = download_coinmetrics_data(symbol)
        if not df.empty:
            all_data.append(df)

    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        output_path = RAW_DATA_DIR / 'crypto_raw.csv'
        combined_df.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}")
        print(f"Total rows: {len(combined_df)}")
        print(f"Symbols: {combined_df['symbol'].nunique()}")
    else:
        print("No data fetched")

if __name__ == "__main__":
    main()