[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/gp9US0IQ)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=22865819&assignment_repo_type=AssignmentRepo)
# QM 2023 Capstone Project

Semester-long capstone for Statistics II: Data Analytics.

## Project Structure

- **code/** — Python scripts and notebooks. Use `config_paths.py` for paths.
- **data/OpenData_rows.csv**
- **data/raw/** — Original data (read-only)
- **data/processed/** — Intermediate cleaning outputs
- **data/final/** — M1 output: analysis-ready panel
- **results/figures/** — Visualizations
- **results/tables/** — Regression tables, summary stats
- **results/reports/** — Milestone memos
- **tests/** — Autograding test suite

Run `python code/config_paths.py` to verify paths.

Option B: Cryptocurrency Volatility & Regulation (Open Dataset Catalog)
Research Question: How do major regulatory announcements (SEC enforcement actions, exchange bans)
affect cryptocurrency return volatility across token types?
Datasets:
Dataset Source What It Provides
CoinGecko or CoinMetrics Open Dataset Catalog Daily prices, volume, market cap for 100+ tokens
(2018-2024)
Economic Policy Uncertainty
Index policyuncertainty.com Monthly uncertainty scores
FRED pandas-datareader
API Fed Funds Rate, VIX (market fear gauge)
Key Variables:
Outcome: 30-day realized volatility for each token
Driver: Regulatory event indicator (binary: SEC action dates)
Controls: Market cap, trading volume, Bitcoin correlation
Groups: DeFi tokens vs. centralized exchange tokens vs. stablecoins
Why It's Interesting: Crypto markets respond violently to regulation -- but not uniformly. When the SEC sued
Coinbase in 2023, some tokens crashed while Bitcoin barely moved. You'd quantify which token characteristics
predict sensitivity to regulatory shocks.
