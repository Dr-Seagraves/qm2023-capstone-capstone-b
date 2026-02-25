"""
Clean Crypto Data
=================

This script cleans the raw crypto data from CoinMetrics.

- Parses dates
- Filters to 2018-2024
- Selects relevant columns: date, symbol, price, market_cap

Output: data/processed/crypto_clean.csv
"""

import pandas as pd
from config_paths import RAW_DATA_DIR, PROCESSED_DATA_DIR, ensure_directories

# Ensure directories exist
ensure_directories()

def clean_crypto_data():
    """Clean crypto data."""
    raw_path = RAW_DATA_DIR / 'crypto_raw.csv'
    try:
        df = pd.read_csv(raw_path)
    except FileNotFoundError:
        print("Crypto raw data not found. Please run fetch_crypto_data.py first.")
        return pd.DataFrame()

    # Assume CoinMetrics format: time, asset, PriceUSD, CapMrktCurUSD, etc.
    # Rename columns to standard
    df = df.rename(columns={
        'time': 'date',
        'asset': 'symbol',
        'PriceUSD': 'price',
        'CapMrktCurUSD': 'market_cap'
    })

    # Parse date
    df['date'] = pd.to_datetime(df['date'])

    # Select columns
    df = df[['date', 'symbol', 'price', 'market_cap']]

    # Filter to 2018-2024
    df = df[(df['date'] >= '2018-01-01') & (df['date'] <= '2024-12-31')]

    # Drop missing prices
    df = df.dropna(subset=['price'])

    # Sort
    df = df.sort_values(['symbol', 'date'])

    return df

def main():
    print("Cleaning crypto data...")
    df = clean_crypto_data()
    if not df.empty:
        output_path = PROCESSED_DATA_DIR / 'crypto_clean.csv'
        df.to_csv(output_path, index=False)
        print(f"Cleaned data saved to {output_path}")
        print(f"Shape: {df.shape}")
        print(f"Symbols: {df['symbol'].nunique()}")
        print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    else:
        print("No data to clean")

if __name__ == "__main__":
    main()