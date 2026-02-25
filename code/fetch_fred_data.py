"""
Fetch FRED Data (Fed Funds Rate and VIX)
=========================================

This script fetches Federal Funds Rate and VIX data from FRED API via CSV downloads.

Data includes monthly Fed Funds Rate and daily VIX.

Output: data/raw/fred_raw.csv
"""

import pandas as pd
import requests
from datetime import datetime
from config_paths import RAW_DATA_DIR, ensure_directories

# Ensure directories exist
ensure_directories()

def download_fred_csv(series_id):
    """Download CSV for a FRED series."""
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        lines = response.text.split('\n')
        data = []
        for line in lines[1:]:  # Skip header
            if line.strip():
                parts = line.split(',')
                if len(parts) >= 2:
                    date_str = parts[0]
                    value_str = parts[1]
                    try:
                        date = datetime.strptime(date_str, '%Y-%m-%d')
                        value = float(value_str)
                        data.append({'date': date, series_id: value})
                    except:
                        continue
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Error downloading {series_id}: {e}")
        return pd.DataFrame()

def main():
    print("Fetching FRED data (Fed Funds Rate and VIX)...")

    # Download Fed Funds Rate (monthly)
    fedfunds_df = download_fred_csv('FEDFUNDS')
    fedfunds_df = fedfunds_df.rename(columns={'FEDFUNDS': 'fed_funds_rate'})

    # Download VIX (daily)
    vix_df = download_fred_csv('VIXCLS')
    vix_df = vix_df.rename(columns={'VIXCLS': 'vix'})

    # Merge on date
    df = pd.merge(fedfunds_df, vix_df, on='date', how='outer')
    df = df.sort_values('date')

    if not df.empty:
        output_path = RAW_DATA_DIR / 'fred_raw.csv'
        df.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}")
        print(f"Data shape: {df.shape}")
        print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    else:
        print("No data fetched")

if __name__ == "__main__":
    main()