# =============================================================================
# PROJECT: Analyzing US Census and Public Health Data to Support Policy Decisions
# AUTHOR: J. Casey Brookshier
# DATE: July 31, 2025
# =============================================================================

# pathlib to provide OS-independent way to work w/ file paths
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import statsmodels.api as sm


# wrap workflow in function
def main():
    # -------------------------------------------------------------------------
    # Project Paths
    # -------------------------------------------------------------------------
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    DATA_DIR = PROJECT_ROOT / "data" / "cleaned"
    OUTPUT_DIR = PROJECT_ROOT / "outputs"
    # make output directory if doesn't exist
    OUTPUT_DIR.mkdir(exist_ok=True)

    # define paths for csv's
    ACS_FILE = DATA_DIR / "ACS_cleaned.csv"
    LLCP_FILE = DATA_DIR / "LLCP2019_cleaned.csv"
    MERGED_FILE = DATA_DIR / "Final_Merged_County_Data.csv"

    # -------------------------------------------------------------------------
    # Defensive File Validation -> map read friendly names to required paths
    # -------------------------------------------------------------------------
    required_files = {
        "ACS cleaned data": ACS_FILE,
        "LLCP cleaned BMI data": LLCP_FILE,
        "Merged analysis dataset": MERGED_FILE
    }
    # list missing files if path doesn't exist, stop execution
    missing = [name for name, path in required_files.items() if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing required cleaned files:\n" + "\n".join(missing)
        )
    # Load Data
    merged = pd.read_csv(MERGED_FILE)

    # -------------------------------------------------------------------------
    # Validate Required Columns -> define analysis required variables
    # convert to numeric, invalid to NaN
    # -------------------------------------------------------------------------
    required_cols = ["Median_Household_Income", "BMI"]
    for col in required_cols:
        if col not in merged.columns:
            raise KeyError(f"Required column missing: {col}")

    merged["Median_Household_Income"] = pd.to_numeric(
        merged["Median_Household_Income"], errors="coerce"
    )
    merged["BMI"] = pd.to_numeric(merged["BMI"], errors="coerce")

    # retain only rows with income/BMI
    analysis_df = merged.dropna(subset=required_cols)

    # prevent analysis observations <3
    if len(analysis_df) < 3:
        print("Insufficient data for statistical analysis.")
        return

    # -------------------------------------------------------------------------
    # Correlation Test -> compute/print pearson correlation coef, p-value
    # -------------------------------------------------------------------------
    corr, p_value = pearsonr(
        analysis_df["Median_Household_Income"],
        analysis_df["BMI"]
    )

    print("\nIncome vs Obesity (BMI) Statistical Results")
    print(f"Pearson correlation: {corr:.4f}")
    print(f"P-value: {p_value:.4g}")

    # -------------------------------------------------------------------------
    # Linear Regression -> add intercept term,define BMI as dependent var
    # fit ordinary least squares regression model, print result
    # -------------------------------------------------------------------------
    X = sm.add_constant(analysis_df["Median_Household_Income"])
    y = analysis_df["BMI"]
    model = sm.OLS(y, X).fit()
    print("\nRegression Summary:")
    print(model.summary())

    # -------------------------------------------------------------------------
    # Visualization -> create scatterplot (income vs BMI)
    # -------------------------------------------------------------------------
    plt.figure(figsize=(8, 6))
    sns.regplot(
        data=analysis_df,
        x="Median_Household_Income",
        y="BMI",
        scatter_kws={"alpha": 0.4},
        line_kws={"color": "red"}
    )
    plt.title("Median Household Income vs Obesity (BMI)")
    plt.tight_layout() # prevent label clipping

    plot_path = OUTPUT_DIR / "income_vs_bmi.png"
    plt.savefig(plot_path, dpi=300)
    plt.close()

    print(f"\nPlot saved to: {plot_path}")

# ensure main() only runs when script executed directly
if __name__ == "__main__":
    main()
