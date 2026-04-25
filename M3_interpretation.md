# Milestone 3 Interpretation

## 1. Model A headline result

The Fixed Effects model demonstrates a strong relationship between macroeconomic conditions and cryptocurrency prices, with an overall within-panel R² of 0.977. This indicates that the model explains nearly all of the month-to-month variation in log cryptocurrency prices after controlling for entity and time fixed effects. The model explicitly includes both entity-specific fixed effects and time-specific fixed effects, which isolates within-cryptocurrency variation over time while accounting for common monthly shocks. The preferred benchmark for inference is the FE model with clustered standard errors, because clustering by entity accounts for heteroskedasticity and within-panel correlation in the residuals.

## 2. Economic interpretation of coefficients

- **Economic Policy Uncertainty (EPU index)**: The coefficient on `epu_index` is approximately -0.0188 and is statistically significant. In practical terms, a one-point increase in the economic policy uncertainty index is associated with a roughly 1.9% decline in the log price of a cryptocurrency, holding other controls constant. This suggests that heightened policy uncertainty is linked to weaker crypto price performance.

- **Federal funds rate**: The estimated coefficient of -0.211 indicates that a one-percentage-point increase in the federal funds rate is associated with a 21.1% reduction in cryptocurrency log price, all else equal. This finding is consistent with the idea that tighter monetary policy reduces risk-taking and lowers demand for speculative digital assets.

- **VIX volatility index**: The negative coefficient of -0.036 implies that a one-unit rise in the VIX is associated with a 3.6% decrease in crypto log price. This result is consistent with risk-off market sentiment reducing investor appetite for cryptocurrencies when overall equity market volatility spikes.

- **Log market capitalization**: The coefficient on `log_market_cap` is positive at 0.468, indicating that a 1% increase in market capitalization is associated with a 0.47% increase in log price. This reflects the expected scaling relationship between asset size and price level.

- **3-month price volatility**: The coefficient of -3.071 suggests that higher recent price volatility is strongly associated with lower current crypto prices. In economic terms, increased short-term volatility appears to depress price levels, likely because investors require a larger risk premium or reduce exposure in volatile environments.

## 3. Model B summary (Random Forest vs OLS)

The machine learning comparison confirms that the Random Forest model substantially outperforms a standard OLS benchmark in out-of-sample predictive accuracy.

- **OLS**: R² = 0.904, RMSE = 0.645
- **Random Forest**: R² = 0.957, RMSE = 0.431

The Random Forest model produces a higher R² and lower RMSE, indicating it captures nonlinear patterns and interactions that the linear OLS specification misses. However, the OLS model still provides a useful baseline for interpreting marginal effects and statistical significance.

## 4. Diagnostics interpretation

Diagnostic plots were used to assess model validity. The residuals versus fitted values plot shows residuals centered around zero and no clear funnel shape, suggesting that model bias is limited and heteroskedasticity is not immediately obvious. The Q-Q plot is broadly consistent with normal errors, supporting the use of standard inference for the linear model.

These diagnostics reinforce confidence that the Fixed Effects model is not dominated by extreme specification problems, although formal tests of heteroskedasticity and serial correlation should be considered in subsequent analysis.

## 5. Robustness check results

Three robustness checks confirm the core conclusions of the Fixed Effects specification:

- **Lag structure of the main driver**: EPU lag 1, lag 2, and lag 3 specifications all produce very similar explanatory power (R² around 0.976) and stable coefficients, indicating that the negative relationship between uncertainty and crypto prices is not sensitive to the chosen lag horizon.

- **Outlier exclusion**: Dropping periods with extreme price returns slightly improves model fit (R² = 0.978) and leaves the sign and magnitude of the main driver coefficient intact. This suggests that the key result is not driven by a few extreme months.

- **Clustered versus normal standard errors**: The clustered standard error specification produces nearly identical coefficient estimates and does not materially change the main inference. This lends support to the robustness of statistical significance when accounting for entity-level dependence across the panel.

## 6. Caveats and limitations

- **Limited entity coverage**: The panel contains only two cryptocurrencies, which restricts the generality of the findings. The results should be interpreted as applicable to the studied digital assets rather than to the broader crypto market.

- **Causal interpretation**: The model is associational and does not prove causality. While the Fixed Effects design controls for unobserved entity and time heterogeneity, omitted variables and reverse causality remain possible.

- **Model scope**: The Random Forest provides superior prediction but is less transparent than OLS. Its higher R² should be interpreted as improved forecasting performance rather than stronger economic interpretation.

- **Measurement and aggregation**: Monthly aggregation may smooth intra-month dynamics, and the economic policy uncertainty index is a proxy measure that may not capture all forms of regulatory or policy risk.

In summary, the econometric evidence suggests that macroeconomic uncertainty and financial conditions are meaningfully associated with cryptocurrency prices, and the core findings are robust across lag structures, outlier exclusion, and alternative standard error treatments.