[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/gp9US0IQ)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=22865819&assignment_repo_type=AssignmentRepo)
# QM 2023 Capstone Project

Semester-long capstone for Statistics II: Data Analytics.

## Team Members and Roles
- [Your Name]: [Role, e.g., Data Engineer]
- Alec Ko: Observer
- Olivia Lauderback: Director

## Research Question
How do major regulatory announcements (SEC enforcement actions, exchange bans) affect cryptocurrency return volatility across token types?

## Dataset Overview
- **Primary Dataset**: CoinGecko or CoinMetrics Open Dataset Catalog - Daily prices, volume, market cap for 100+ tokens (2018-2024)
- **Supplementary Datasets**:
  - Economic Policy Uncertainty Index (policyuncertainty.com) - Monthly uncertainty scores
  - FRED API (via pandas-datareader) - Fed Funds Rate, VIX (market fear gauge)

## Preliminary Hypotheses
1. Regulatory announcements increase volatility more for DeFi tokens than for centralized exchange tokens.
2. Tokens with higher market capitalization exhibit lower sensitivity to regulatory shocks.
3. Stablecoins show minimal volatility response to regulatory events compared to other token types.

## Key Variables
- **Outcome**: 30-day realized volatility for each token
- **Driver**: Regulatory event indicator (binary: SEC action dates)
- **Controls**: Market cap, trading volume, Bitcoin correlation
- **Groups**: DeFi tokens vs. centralized exchange tokens vs. stablecoins

## Why It's Interesting
Crypto markets respond violently to regulation -- but not uniformly. When the SEC sued Coinbase in 2023, some tokens crashed while Bitcoin barely moved. This project quantifies which token characteristics predict sensitivity to regulatory shocks.

## Project Structure
```
QM-2023-Capstone-Repo/
├── code/
│   ├── config_paths.py                 # Path management
│   ├── fetch_crypto_data.py            # Fetch + clean primary dataset (crypto prices)
│   ├── fetch_epu_data.py               # Fetch + clean Economic Policy Uncertainty data
│   ├── fetch_fred_data.py              # Fetch + clean FRED data (Fed Funds Rate, VIX)
│   └── merge_final_panel.py            # Merge processed datasets into final panel
├── data/
│   ├── raw/
│   │   ├── crypto_raw.csv              # Original crypto data
│   │   ├── epu_raw.csv                 # Original EPU data
│   │   └── fred_raw.csv                # Original FRED data
│   ├── processed/
│   │   ├── crypto_clean.csv            # Cleaned crypto data
│   │   ├── epu_clean.csv               # Cleaned EPU data
│   │   └── fred_clean.csv              # Cleaned FRED data
│   └── final/
│       ├── crypto_analysis_panel.csv   # Final merged dataset
│       └── data_dictionary.md          # Variable definitions
├── results/
│   ├── figures/                        # Visualizations
│   ├── reports/                        # Milestone memos
│   └── tables/                         # Regression tables, summary stats
├── tests/
│   └── .gitkeep                        # Placeholder for tests
├── README.md                           # This file
├── M1_data_quality_report.md           # Data quality documentation
└── AI_AUDIT_APPENDIX.md                # AI disclosure (REQUIRED)
```

## How to Run the Pipeline
1. Ensure all dependencies are installed (see requirements.txt if available).
2. Run `python code/config_paths.py` to verify paths.
3. Execute fetch scripts in order:
   - `python code/fetch_crypto_data.py`
   - `python code/fetch_epu_data.py`
   - `python code/fetch_fred_data.py`
4. Run the merge script: `python code/merge_final_panel.py`
5. Check `data/final/crypto_analysis_panel.csv` for the final dataset.
