"""
Capstone Project - Milestone 3: Econometric Models
==================================================

This script implements econometric analysis for the cryptocurrency volatility study,
examining the relationship between macroeconomic indicators and cryptocurrency prices.

University of [University Name] - Quantitative Methods Capstone Project
Spring 2026

Authors: [Your Names]
Date: April 2026

Inputs:
- data/final/crypto_analysis_panel.csv (panel dataset)

Outputs:
- results/figures/ (diagnostic plots and model comparisons)
- results/tables/ (regression tables and model summaries)

Sections:
1. Imports and data loading
2. Feature engineering
3. Model A – Fixed Effects regression
4. Model B – Machine Learning comparison (Random Forest vs OLS)
5. Diagnostics
6. Robustness checks
7. Save regression tables and figures
"""

# ==============================================================================
# 1. IMPORTS AND DATA LOADING
# ==============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Import project paths
from config_paths import FINAL_DATA_DIR, FIGURES_DIR, TABLES_DIR

# Statistical and econometric libraries
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor
from linearmodels import PanelOLS, RandomEffects
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# Set plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_panel_data():
    """Load the final panel dataset."""
    panel_path = FINAL_DATA_DIR / 'crypto_analysis_panel.csv'
    df = pd.read_csv(panel_path)

    # Convert date and set as datetime index
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(['symbol', 'date']).set_index(['symbol', 'date'])

    print(f"Loaded panel dataset with {len(df)} observations")
    print(f"Entities: {df.index.get_level_values('symbol').unique().tolist()}")
    print(f"Date range: {df.index.get_level_values('date').min()} to {df.index.get_level_values('date').max()}")

    return df

# Load data
df = load_panel_data()

# ==============================================================================
# 2. FEATURE ENGINEERING
# ==============================================================================

def create_features(df):
    """Create additional features for modeling."""
    df = df.copy()

    # Log transformations for price and market cap
    df['log_price'] = np.log(df['price'])
    df['log_market_cap'] = np.log(df['market_cap'])

    # Lagged variables
    df['log_price_lag1'] = df.groupby('symbol')['log_price'].shift(1)
    df['fed_funds_rate_lag1'] = df.groupby('symbol')['fed_funds_rate'].shift(1)
    df['vix_lag1'] = df.groupby('symbol')['vix'].shift(1)
    df['epu_index_lag1'] = df.groupby('symbol')['epu_index'].shift(1)
    df['epu_index_lag2'] = df.groupby('symbol')['epu_index'].shift(2)
    df['epu_index_lag3'] = df.groupby('symbol')['epu_index'].shift(3)

    # Returns (percentage change)
    df['price_return'] = df.groupby('symbol')['price'].pct_change()
    df['log_return'] = df.groupby('symbol')['log_price'].diff()

    # Volatility measures (rolling standard deviation)
    df['price_volatility_3m'] = df.groupby('symbol')['price_return'].rolling(3).std().reset_index(0, drop=True)
    df['price_volatility_6m'] = df.groupby('symbol')['price_return'].rolling(6).std().reset_index(0, drop=True)

    # Dummy variables for cryptocurrency
    df['is_btc'] = (df.index.get_level_values('symbol') == 'btc').astype(int)

    # Time trends
    df['month'] = df.index.get_level_values('date').month
    df['year'] = df.index.get_level_values('date').year

    # Seasonal dummies
    for month in range(1, 13):
        df[f'month_{month}'] = (df['month'] == month).astype(int)

    return df

# Create features
df_featured = create_features(df)

# Remove rows with NaN from lagging
df_model = df_featured.dropna()

print(f"Dataset after feature engineering: {len(df_model)} observations")

# ==============================================================================
# 3. MODEL A – FIXED EFFECTS REGRESSION
# ==============================================================================

def run_fixed_effects_model(df):
    """Run fixed effects regression model and return clustered standard errors output."""
    # Model specification: log_price as dependent variable
    formula = 'log_price ~ fed_funds_rate + vix + epu_index + log_market_cap + price_volatility_3m'

    # Fixed effects model (entity and time fixed effects)
    model_fe = PanelOLS.from_formula(formula, data=df, drop_absorbed=True)
    results_fe = model_fe.fit()
    results_fe_clustered = model_fe.fit(cov_type='clustered', cluster_entity=True)

    print("Fixed Effects Model Results (Clustered SE):")
    print(results_fe_clustered.summary)

    return results_fe, results_fe_clustered

# Run fixed effects model
fe_results, fe_results_clustered = run_fixed_effects_model(df_model)

# ==============================================================================
# 4. MODEL B – MACHINE LEARNING COMPARISON (RANDOM FOREST VS OLS)
# ==============================================================================

def prepare_ml_data(df):
    """Prepare data for machine learning models."""
    features = ['fed_funds_rate', 'vix', 'epu_index', 'log_market_cap', 'price_volatility_3m']
    X = df[features]
    y = df['log_price']
    return X, y

def run_ml_comparison(df):
    """Compare Random Forest and OLS models."""
    X, y = prepare_ml_data(df)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Fit OLS using statsmodels
    X_train_const = sm.add_constant(X_train)
    X_test_const = sm.add_constant(X_test)
    ols_model = sm.OLS(y_train, X_train_const).fit()
    ols_pred = ols_model.predict(X_test_const)

    # Fit Random Forest Regression
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)

    # Evaluate models
    ols_rmse = np.sqrt(mean_squared_error(y_test, ols_pred))
    rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))

    comparison = pd.DataFrame({
        'Model': ['OLS', 'Random Forest'],
        'R_squared': [r2_score(y_test, ols_pred), r2_score(y_test, rf_pred)],
        'RMSE': [ols_rmse, rf_rmse]
    })

    print("Machine Learning Model Comparison:")
    print(comparison.to_string(index=False, float_format='%.4f'))

    # Feature importance for Random Forest
    feature_importances = pd.DataFrame({
        'feature': X.columns,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)

    print("\nRandom Forest Feature Importance:")
    print(feature_importances.to_string(index=False, float_format='%.4f'))

    models_results = {
        'OLS': {
            'model': ols_model,
            'predictions': ols_pred,
            'mse': mean_squared_error(y_test, ols_pred),
            'rmse': ols_rmse,
            'r2': comparison.loc[comparison['Model'] == 'OLS', 'R_squared'].iloc[0]
        },
        'Random Forest': {
            'model': rf_model,
            'predictions': rf_pred,
            'mse': mean_squared_error(y_test, rf_pred),
            'rmse': rf_rmse,
            'r2': comparison.loc[comparison['Model'] == 'Random Forest', 'R_squared'].iloc[0],
            'feature_importances': feature_importances
        }
    }

    return models_results, X_test, y_test

# Run ML comparison
ml_results, X_test, y_test = run_ml_comparison(df_model)

# ==============================================================================
# 5. DIAGNOSTICS
# ==============================================================================

def create_diagnostic_plots(fe_results, ml_results, X_test, y_test):
    """Create diagnostic plots for the Fixed Effects model."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Residuals vs Fitted
    axes[0].scatter(fe_results.fitted_values, fe_results.resids, alpha=0.6, edgecolor='k')
    axes[0].axhline(y=0, color='red', linestyle='--', linewidth=1)
    axes[0].set_xlabel('Fitted Values')
    axes[0].set_ylabel('Residuals')
    axes[0].set_title('Residuals vs Fitted Values - Fixed Effects Model')
    axes[0].grid(True, alpha=0.2)

    # Q-Q Plot
    sm.qqplot(fe_results.resids, line='45', ax=axes[1])
    axes[1].set_title('Normal Q-Q Plot of Fixed Effects Residuals')
    axes[1].grid(True, alpha=0.2)

    plt.tight_layout()
    return fig

# Create diagnostic plots
diag_fig = create_diagnostic_plots(fe_results, ml_results, X_test, y_test)

# Diagnostics: heteroskedasticity and multicollinearity

def run_breusch_pagan_test(results, df):
    """Run Breusch-Pagan test using residuals from the primary Fixed Effects model."""
    X = df[['fed_funds_rate', 'vix', 'epu_index', 'log_market_cap', 'price_volatility_3m']]
    X_const = sm.add_constant(X)
    resid = results.resids
    lm_stat, lm_pvalue, f_stat, f_pvalue = het_breuschpagan(resid, X_const)

    print("\nBreusch-Pagan Heteroskedasticity Test:")
    print(f"LM statistic: {lm_stat:.4f}")
    print(f"p-value: {lm_pvalue:.4f}")
    if lm_pvalue < 0.05:
        print("Interpretation: p < 0.05, heteroskedasticity exists and clustered standard errors are needed.")
    else:
        print("Interpretation: p >= 0.05, evidence of heteroskedasticity is weak.")

    return {
        'lm_stat': lm_stat,
        'lm_pvalue': lm_pvalue,
        'f_stat': f_stat,
        'f_pvalue': f_pvalue
    }


def calculate_vif(df):
    """Calculate VIF for the Fixed Effects predictors."""
    X = df[['fed_funds_rate', 'vix', 'epu_index', 'log_market_cap', 'price_volatility_3m']]
    X_const = sm.add_constant(X)
    vif_data = pd.DataFrame({
        'Variable': X.columns,
        'VIF': [variance_inflation_factor(X_const.values, i + 1) for i in range(len(X.columns))]
    })

    print("\nVariance Inflation Factor (VIF):")
    print(vif_data)
    if any(vif_data['VIF'] > 10):
        print("Interpretation: VIF > 10 indicates serious multicollinearity. Consider combining or dropping predictors.")
    else:
        print("Interpretation: VIF values are within acceptable ranges.")

    return vif_data

# Run diagnostics
bp_results = run_breusch_pagan_test(fe_results_clustered, df_model)
vif_results = calculate_vif(df_model)

# ==============================================================================
# 6. ROBUSTNESS CHECKS
# ==============================================================================

def robustness_checks(df):
    """Perform robustness checks with three alternative specifications."""
    robustness_results = {}
    base_controls = 'fed_funds_rate + vix + log_market_cap + price_volatility_3m'

    # 1. Compare lag1, lag2, lag3 for the main driver variable
    for lag in [1, 2, 3]:
        formula = f'log_price ~ epu_index_lag{lag} + {base_controls}'
        model = PanelOLS.from_formula(formula, data=df, drop_absorbed=True)
        results = model.fit()
        robustness_results[f'EPU Lag {lag}'] = results

    # 2. Re-estimate the model excluding outlier periods
    cutoff = df['price_return'].abs().quantile(0.95)
    df_no_outliers = df[df['price_return'].abs() <= cutoff]
    formula_no_outliers = f'log_price ~ epu_index + {base_controls}'
    model_no_outliers = PanelOLS.from_formula(formula_no_outliers, data=df_no_outliers, drop_absorbed=True)
    results_no_outliers = model_no_outliers.fit()
    robustness_results['No Outlier Periods'] = results_no_outliers

    # 3. Compare clustered standard errors vs normal standard errors
    formula_se = f'log_price ~ epu_index + {base_controls}'
    model_se = PanelOLS.from_formula(formula_se, data=df, drop_absorbed=True)
    results_normal_se = model_se.fit()
    results_clustered_se = model_se.fit(cov_type='clustered', cluster_entity=True)
    robustness_results['Normal SE'] = results_normal_se
    robustness_results['Clustered SE'] = results_clustered_se

    print("Robustness Checks:")
    for name, results in robustness_results.items():
        print(f"\n{name} Model:")
        print(f"R-squared: {results.rsquared:.4f}")
        print(f"Observations: {int(results.nobs)}")
        if hasattr(results, 'params'):
            main_coef = results.params.get('epu_index', results.params.filter(like='epu_index').iloc[0] if 'epu_index' in results.params.index else None)
            if main_coef is not None:
                print(f"Main driver coefficient: {main_coef:.4f}")

    return robustness_results

# Run robustness checks
robustness_results = robustness_checks(df_model)

# ==============================================================================
# 7. SAVE REGRESSION TABLES AND FIGURES
# ==============================================================================

def save_results(fe_results, fe_results_clustered, ml_results, robustness_results, diag_fig):
    """Save all results to files."""

    # Save regression tables
    with open(TABLES_DIR / 'fixed_effects_results.txt', 'w') as f:
        f.write("FIXED EFFECTS REGRESSION RESULTS\n")
        f.write("=" * 50 + "\n\n")
        f.write(str(fe_results.summary))

    # Save ML results
    ml_summary = pd.DataFrame({
        'Model': ['OLS', 'Random Forest'],
        'MSE': [ml_results['OLS']['mse'], ml_results['Random Forest']['mse']],
        'R_squared': [ml_results['OLS']['r2'], ml_results['Random Forest']['r2']]
    })
    ml_summary.to_csv(TABLES_DIR / 'ml_model_comparison.csv', index=False)

    # Save publication-ready regression comparison table
    def significance_star(p):
        if pd.isna(p):
            return ''
        if p < 0.01:
            return '***'
        if p < 0.05:
            return '**'
        if p < 0.10:
            return '*'
        return ''

    publication_rows = []
    publication_rows.append({
        'Model': 'FE Baseline',
        'Main Driver Coefficient': fe_results.params.get('epu_index', np.nan),
        'Std_Err': fe_results.std_errors.get('epu_index', np.nan),
        'P_value': fe_results.pvalues.get('epu_index', np.nan),
        'Significance': significance_star(fe_results.pvalues.get('epu_index', np.nan)),
        'R_squared': fe_results.rsquared,
        'N': int(fe_results.nobs),
        'RMSE': np.nan,
        'Notes': 'Baseline FE model with entity/time fixed effects'
    })
    publication_rows.append({
        'Model': 'FE Clustered SE',
        'Main Driver Coefficient': fe_results_clustered.params.get('epu_index', np.nan),
        'Std_Err': fe_results_clustered.std_errors.get('epu_index', np.nan),
        'P_value': fe_results_clustered.pvalues.get('epu_index', np.nan),
        'Significance': significance_star(fe_results_clustered.pvalues.get('epu_index', np.nan)),
        'R_squared': fe_results_clustered.rsquared,
        'N': int(fe_results_clustered.nobs),
        'RMSE': np.nan,
        'Notes': 'Preferred benchmark: accounts for entity-level heteroskedasticity and panel dependence'
    })
    ols_model = ml_results['OLS']['model']
    publication_rows.append({
        'Model': 'OLS',
        'Main Driver Coefficient': ols_model.params.get('epu_index', np.nan),
        'Std_Err': ols_model.bse.get('epu_index', np.nan),
        'P_value': ols_model.pvalues.get('epu_index', np.nan),
        'Significance': significance_star(ols_model.pvalues.get('epu_index', np.nan)),
        'R_squared': ols_model.rsquared,
        'N': int(ols_model.nobs),
        'RMSE': ml_results['OLS']['rmse'],
        'Notes': 'Linear benchmark for comparison'
    })
    publication_rows.append({
        'Model': 'Random Forest',
        'Main Driver Coefficient': np.nan,
        'Std_Err': np.nan,
        'P_value': np.nan,
        'Significance': '',
        'R_squared': ml_results['Random Forest']['r2'],
        'N': len(ml_results['Random Forest']['predictions']),
        'RMSE': ml_results['Random Forest']['rmse'],
        'Notes': 'Machine learning performance summary'
    })

    publication_df = pd.DataFrame(publication_rows)
    publication_df = publication_df[['Model', 'Main Driver Coefficient', 'Std_Err', 'P_value', 'Significance', 'R_squared', 'N', 'RMSE', 'Notes']]
    publication_df.to_csv(TABLES_DIR / 'M3_regression_table.csv', index=False)

    # Save robustness results
    robustness_summary = []
    for name, results in robustness_results.items():
        robustness_summary.append({
            'Model': name,
            'R_squared': results.rsquared,
            'F_statistic': results.f_statistic.stat,
            'F_p_value': results.f_statistic.pval,
            'Observations': int(results.nobs)
        })

    robustness_df = pd.DataFrame(robustness_summary)
    robustness_df.to_csv(TABLES_DIR / 'robustness_checks.csv', index=False)

    # Save robustness comparison table
    comparison_rows = []
    for name, results in robustness_results.items():
        coef = results.params.get('epu_index', np.nan) if 'epu_index' in results.params.index else np.nan
        comparison_rows.append({
            'Model': name,
            'R_squared': results.rsquared,
            'Observations': int(results.nobs),
            'Main Driver Coefficient': coef
        })

    comparison_df = pd.DataFrame(comparison_rows)
    comparison_df.to_csv(TABLES_DIR / 'robustness_comparison_table.csv', index=False)

    # Save diagnostic plots
    diag_fig.savefig(FIGURES_DIR / 'model_diagnostics.png', dpi=300, bbox_inches='tight')
    plt.close(diag_fig)

    print(f"\nResults saved to:")
    print(f"- Tables: {TABLES_DIR}")
    print(f"- Figures: {FIGURES_DIR}")

# Save all results
save_results(fe_results, fe_results_clustered, ml_results, robustness_results, diag_fig)

print("\n" + "="*60)
print("MILESTONE 3 ECONOMETRIC ANALYSIS COMPLETED")
print("="*60)
print("Summary of findings:")
print(f"- Fixed Effects R-squared: {fe_results.rsquared:.4f}")
print(f"- Best ML model: {'Random Forest' if ml_results['Random Forest']['r2'] > ml_results['OLS']['r2'] else 'OLS'}")
print(f"- Results saved in results/ directory")