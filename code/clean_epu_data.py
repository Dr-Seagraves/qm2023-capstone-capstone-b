"""
Clean EPU Data
==============

This script cleans the raw EPU data.

- Creates date column from Year and Month
- Filters to relevant period (2018-2024)
- Renames columns

Output: data/processed/epu_clean.csv
"""

import pandas as pd
from config_paths import RAW_DATA_DIR, PROCESSED_DATA_DIR, ensure_directories

# Ensure directories exist
ensure_directories()

def clean_epu_data():
    """Clean EPU data."""
    raw_path = RAW_DATA_DIR / 'epu_raw.csv'
    df = pd.read_csv(raw_path)

    # Create date column
    df['date'] = pd.to_datetime(df[['Year', 'Month']].assign(day=1))

    # Rename column
    df = df.rename(columns={'News_Based_Policy_Uncert_Index': 'epu_index'})

    # Select columns
    df = df[['date', 'epu_index']]

    # Filter to 2018-2024
    df = df[(df['date'] >= '2018-01-01') & (df['date'] <= '2024-12-31')]

    # Sort
    df = df.sort_values('date')

    return df

def main():
    print("Cleaning EPU data...")
    df = clean_epu_data()
    output_path = PROCESSED_DATA_DIR / 'epu_clean.csv'
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")
    print(f"Shape: {df.shape}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")

if __name__ == "__main__":
    main()