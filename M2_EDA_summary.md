# M2 EDA Summary

## Key Findings

- The primary outcome is the monthly log return of cryptocurrency prices, and it shows high volatility across the sample. This makes economic sense because crypto returns are driven by sentiment, liquidity, and macro risk factors.
- The correlation heatmap shows that the outcome has a strong negative relationship with the fed funds rate and a moderate negative relationship with VIX. This suggests that rising interest rates and market uncertainty are associated with lower crypto returns.
- Group analysis by symbol indicates that BTC and ETH have different return distributions and sensitivity to the fed funds rate, implying heterogeneous exposure across assets.
- Lagged effect analysis identifies the driver-response timing that best explains the outcome. A nonzero optimal lag suggests the macro driver affects crypto returns with a delayed transmission.
- Seasonal decomposition reveals that the aggregate outcome series contains a trend and residual structure, meaning time effects and shocks should be modeled explicitly in regression.

## Hypotheses for M3

- **H1: Lagged Fed Funds Rate Effect**\
  Model: outcome ~ fed_funds_rate_lag_optimal + controls + fixed effects\
  Expected sign: negative\
  Reasoning: higher interest rates raise the cost of capital and reduce risk appetite, which should lower crypto returns with a lag.

- **H2: VIX Risk Premium**\
  Model: outcome ~ vix + controls + fixed effects\
  Expected sign: negative\
  Reasoning: higher implied volatility reflects greater market uncertainty, which should be associated with lower crypto returns.

- **H3: Economic Policy Uncertainty**\
  Model: outcome ~ epu_index + controls + fixed effects\
  Expected sign: negative\
  Reasoning: greater policy uncertainty increases risk and may reduce investor demand for speculative assets like crypto.

- **H4: Group Heterogeneity**\
  Model: outcome ~ driver + controls + symbol * driver\
  Expected sign: heterogeneous across symbols\
  Reasoning: different tokens have distinct sensitivity to macro factors due to varying liquidity, use cases, and investor bases.

## Data Quality Flags

- **Missing values**: The outcome variable is computed as log returns, which creates NaNs for the first observation per symbol. These are dropped before analysis. Model specification should account for panel coverage and possible unbalanced data.
- **Outlier periods**: Crypto returns contain extreme spikes and drawdowns. Use robust regression, winsorize extreme values, or include dummy variables for crisis months to mitigate influence.
- **Heteroskedasticity**: Return volatility is not constant over time. Use robust standard errors or cluster by symbol/date in M3 to address conditional heteroskedasticity.
- **Multicollinearity**: Some controls such as fed funds rate, VIX, and EPU may be correlated. Check variance inflation factors in M3 and avoid including highly collinear control combinations.
- **Seasonal and trend effects**: Time series decomposition shows structured trend and residual patterns. Include time fixed effects or seasonal dummies in the regression to avoid omitted variable bias.
