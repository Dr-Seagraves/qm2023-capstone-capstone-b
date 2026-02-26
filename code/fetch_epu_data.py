"""
Fetch Economic Policy Uncertainty (EPU) Data
=============================================

This script downloads the US Economic Policy Uncertainty Index data
from policyuncertainty.com.

Data includes monthly EPU scores.

Output: data/raw/epu_raw.csv
"""

import pandas as pd
import requests
from config_paths import RAW_DATA_DIR, ensure_directories

# Ensure directories exist
ensure_directories()

def download_epu_data():
    """Download EPU data from policyuncertainty.com."""
    url = "https://www.policyuncertainty.com/media/US_Policy_Uncertainty_Data.csv"
    try:
        response = requests.get(url)
        response.raise_for_status()
        # Save raw data
        raw_path = RAW_DATA_DIR / 'epu_raw.csv'
        with open(raw_path, 'wb') as f:
            f.write(response.content)
        print(f"EPU data downloaded to {raw_path}")
        return raw_path
    except Exception as e:
        print(f"Error downloading EPU data: {e}")
        return None

def main():
    print("Downloading Economic Policy Uncertainty data...")
    path = download_epu_data()
    if path:
        # Quick preview
        df = pd.read_csv(path)
        print(f"Data shape: {df.shape}")
        print(f"Date range: {df['Year'].min()}-{df['Year'].max()}")
        print("Columns:", list(df.columns))

if __name__ == "__main__":
    main()