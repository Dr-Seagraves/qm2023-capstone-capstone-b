"""
Merge Final Panel Dataset
=========================

This script combines the cleaned datasets into a final analysis-ready panel.

Inputs:
- data/processed/crypto_clean.csv
- data/processed/epu_clean.csv
- data/processed/fred_clean.csv

Output: data/final/crypto_analysis_panel.csv
"""

import pandas as pd
from config_paths import PROCESSED_DATA_DIR, FINAL_DATA_DIR, ensure_directories

# Ensure directories exist
ensure_directories()

def load_cleaned_data():
    """Load all cleaned datasets."""
    crypto_df = None
    epu_df = None
    fred_df = None

    try:
        crypto_df = pd.read_csv(PROCESSED_DATA_DIR / 'crypto_clean.csv')
    except FileNotFoundError:
        print("Crypto data not found, proceeding without it.")

    try:
        epu_df = pd.read_csv(PROCESSED_DATA_DIR / 'epu_clean.csv')
    except FileNotFoundError:
        print("EPU data not found.")

    try:
        fred_df = pd.read_csv(PROCESSED_DATA_DIR / 'fred_clean.csv')
    except FileNotFoundError:
        print("FRED data not found.")

    return crypto_df, epu_df, fred_df

def merge_datasets(crypto_df, epu_df, fred_df):
    """Merge datasets into panel format."""
    # Convert dates
    crypto_df['date'] = pd.to_datetime(crypto_df['date'])
    epu_df['date'] = pd.to_datetime(epu_df[['Year', 'Month']].assign(day=1))
    fred_df['date'] = pd.to_datetime(fred_df['date'])

    # Start with crypto data
    panel_df = crypto_df.copy()

    # Merge FRED on date
    panel_df = pd.merge(panel_df, fred_df, on='date', how='left')

    # For EPU (monthly), merge on year-month
    panel_df['year_month'] = panel_df['date'].dt.to_period('M')
    epu_df['year_month'] = epu_df['date'].dt.to_period('M')
    panel_df = pd.merge(panel_df, epu_df[['year_month', 'epu_index']],
                       on='year_month', how='left')

    # Clean up
    panel_df = panel_df.drop(columns=['year_month'])

    # Sort
    panel_df = panel_df.sort_values(['symbol', 'date'])

    return panel_df

def main():
    print("Merging final panel dataset...")

    crypto_df, epu_df, fred_df = load_cleaned_data()

    if fred_df is None:
        print("No data to merge")
        return

    # Start with FRED data
    panel_df = fred_df.copy()
    panel_df['date'] = pd.to_datetime(panel_df['date'])

    if epu_df is not None:
        epu_df['date'] = pd.to_datetime(epu_df['date'])
        panel_df = pd.merge(panel_df, epu_df, on='date', how='left')

    if crypto_df is not None:
        crypto_df['date'] = pd.to_datetime(crypto_df['date'])
        # Since crypto is monthly, merge on date
        panel_df = pd.merge(panel_df, crypto_df, on='date', how='left')

    # Sort
    panel_df = panel_df.sort_values(['date', 'symbol'])

    output_path = FINAL_DATA_DIR / 'crypto_analysis_panel.csv'
    panel_df.to_csv(output_path, index=False)
    print(f"Final dataset saved to {output_path}")
    print(f"Shape: {panel_df.shape}")

if __name__ == "__main__":
    main()