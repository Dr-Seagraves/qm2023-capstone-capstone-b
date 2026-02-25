# Data Dictionary: Cryptocurrency Analysis Panel

## Dataset Overview

This dataset contains a merged panel of macroeconomic indicators and cryptocurrency data for analyzing the impact of regulatory announcements on cryptocurrency volatility.

- **Entities**: 2 cryptocurrencies (Bitcoin - BTC, Ethereum - ETH)
- **Time Periods**: 84 monthly observations
- **Date Range**: January 2018 to December 2024
- **Total Observations**: 168 rows (84 months × 2 entities)
- **File Location**: `data/final/crypto_analysis_panel.csv`

## Variable Definitions

| Variable | Description | Type | Source | Units |
|----------|-------------|------|--------|-------|
| `date` | Month-end date for the observation | Date | Derived | YYYY-MM-DD |
| `fed_funds_rate` | Federal Funds Rate - the interest rate at which depository institutions lend reserve balances to each other overnight | Numeric | Federal Reserve Economic Data (FRED) | Percent (%) |
| `vix` | CBOE Volatility Index - measures market expectations of near-term volatility conveyed by S&P 500 stock index option prices | Numeric | Federal Reserve Economic Data (FRED) | Index value |
| `epu_index` | Economic Policy Uncertainty Index - measures economic policy uncertainty based on newspaper coverage | Numeric | policyuncertainty.com | Index value (normalized) |
| `symbol` | Cryptocurrency identifier | String | CoinMetrics | btc/eth |
| `price` | Cryptocurrency closing price at month-end | Numeric | CoinMetrics | USD |
| `market_cap` | Cryptocurrency market capitalization at month-end | Numeric | CoinMetrics | USD |

## Cleaning Decisions Summary

### FRED Data (Federal Funds Rate and VIX)
- **Source**: Downloaded from FRED API using `fredapi` Python package
- **Frequency**: Daily data downloaded, then aggregated to monthly averages
- **Date Filtering**: Limited to 2018-01-01 through 2024-12-31
- **Missing Values**: No missing values in the cleaned dataset; original daily data was complete for the period
- **Aggregation**: Monthly averages calculated from daily observations

### EPU Data (Economic Policy Uncertainty Index)
- **Source**: Downloaded from policyuncertainty.com as CSV file
- **Frequency**: Monthly data
- **Date Filtering**: Filtered to include only dates from 2018-01 through 2024-12
- **Missing Values**: No missing values in the filtered period
- **Processing**: Converted date column to datetime format, filtered by date range

### Cryptocurrency Data (BTC and ETH)
- **Source**: CoinMetrics CSV dataset (OpenData_rows.csv)
- **Frequency**: Monthly aggregated data
- **Date Filtering**: Limited to 2018-01 through 2024-12
- **Variables Selected**: price (close) and market_cap for BTC and ETH
- **Missing Values**: No missing values in the selected period and variables
- **Processing**: Reshaped from wide to long format with symbol column

### Final Panel Merge
- **Merge Key**: Date (monthly) and symbol (crypto identifier)
- **Join Type**: Left join starting with crypto data, adding macroeconomic indicators
- **Date Alignment**: All datasets aligned to monthly frequency
- **Duplicate Handling**: No duplicates present in source datasets
- **Final Validation**: Verified 168 observations (84 months × 2 cryptos) with complete data for all variables