"""
Clean FRED Data
===============

This script cleans the raw FRED data.

- Parses dates
- Handles missing values
- Filters to 2018-2024

Output: data/processed/fred_clean.csv
"""

import pandas as pd
from config_paths import RAW_DATA_DIR, PROCESSED_DATA_DIR, ensure_directories

# Ensure directories exist
ensure_directories()

def clean_fred_data():
    """Clean FRED data."""
    raw_path = RAW_DATA_DIR / 'fred_raw.csv'
    df = pd.read_csv(raw_path)

    # Parse date
    df['date'] = pd.to_datetime(df['date'])

    # Convert to numeric, handle missing
    df['fed_funds_rate'] = pd.to_numeric(df['fed_funds_rate'], errors='coerce')
    df['vix'] = pd.to_numeric(df['vix'], errors='coerce')

    # Filter to 2018-2024
    df = df[(df['date'] >= '2018-01-01') & (df['date'] <= '2024-12-31')]

    # Sort
    df = df.sort_values('date')

    return df

def main():
    print("Cleaning FRED data...")
    df = clean_fred_data()
    output_path = PROCESSED_DATA_DIR / 'fred_clean.csv'
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")
    print(f"Shape: {df.shape}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")

if __name__ == "__main__":
    main()