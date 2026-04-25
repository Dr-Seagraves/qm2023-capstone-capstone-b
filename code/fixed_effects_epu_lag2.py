import pandas as pd
import numpy as np
from config_paths import FINAL_DATA_DIR, TABLES_DIR
from linearmodels import PanelOLS
import warnings
warnings.filterwarnings('ignore')

def run_fixed_effects_regression():
    """Run Fixed Effects regression with entity and time fixed effects."""

    # Load the panel dataset
    panel_path = FINAL_DATA_DIR / 'crypto_analysis_panel.csv'
    df = pd.read_csv(panel_path)

    # Convert date and set multi-index
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index(['symbol', 'date']).sort_index()

    # Create lag2 for the driver variable
    driver_var = 'epu_index'
    df[f'{driver_var}_lag2'] = df.groupby('symbol')[driver_var].shift(2)

    # Drop rows with missing lag values
    df = df.dropna(subset=[f'{driver_var}_lag2'])

    print(f"Dataset after creating lag2: {len(df)} observations")

    # Define the regression formula
    # Outcome: price
    # Predictors: epu_index_lag2, fed_funds_rate, vix, market_cap
    formula = 'price ~ epu_index_lag2 + fed_funds_rate + vix + market_cap'

    # Run Fixed Effects model with entity and time fixed effects
    # Clustered standard errors by entity
    model = PanelOLS.from_formula(
        formula,
        data=df,
        drop_absorbed=True
    )

    # Fit the model with clustered standard errors
    results = model.fit(cov_type='clustered', cluster_entity=True)

    # Print the summary
    print("\n" + "="*80)
    print("FIXED EFFECTS REGRESSION RESULTS")
    print("="*80)
    print(results.summary)

    # Save the results to file
    output_path = TABLES_DIR / 'fixed_effects_epu_lag2_results.txt'
    with open(output_path, 'w') as f:
        f.write("FIXED EFFECTS REGRESSION: Price ~ EPU_Index_Lag2 + Controls\n")
        f.write("="*80 + "\n\n")
        f.write(str(results.summary))
        f.write("\n\nModel Specification:\n")
        f.write("- Entity Fixed Effects: Yes\n")
        f.write("- Time Fixed Effects: Yes\n")
        f.write("- Standard Errors: Clustered by Entity\n")
        f.write(f"- Observations: {len(df)}\n")
        f.write(f"- Entities: {df.index.get_level_values('symbol').nunique()}\n")
        f.write(f"- Time periods: {df.index.get_level_values('date').nunique()}\n")

    print(f"\nResults saved to: {output_path}")

    return results

if __name__ == "__main__":
    results = run_fixed_effects_regression()