"""
===============================================================================
Project : Securitisation Risk Analytics Platform
File    : ifrs9_model.py (PART 2A)
Author  : Garvit Mehta

Purpose
-------
This module performs IFRS 9 Expected Credit Loss (ECL) calculations on the
loan portfolio dataset.

Formula Used
------------
ECL = PD × LGD × EAD

Outputs
-------
ECL_Output.xlsx

===============================================================================
"""

import pandas as pd  # type: ignore[import]
import numpy as np
from pathlib import Path

# =============================================================================
# PROJECT PATHS
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = (
    BASE_DIR /
    "Datasets" /
    "auto_loan_securitisation_data.csv"
)

OUTPUT_FILE = (
    BASE_DIR /
    "Python" /
    "ECL_Output.xlsx"
)

# =============================================================================
# REQUIRED COLUMNS
# =============================================================================

REQUIRED_COLUMNS = [

    "LoanID",

    "CurrentBalance",

    "PD_Estimate",

    "LGD_Estimate",

    "EAD",

    "ECL_Provision",

    "IFRS9_Stage",

    "DelinquencyDays",

    "InterestRate",

    "CurrentVehicleValue",

    "LTV_Current",

    "CIBIL_Score_Current",

    "Region",

    "State"

]

# =============================================================================
# LOAD DATASET
# =============================================================================

print("=" * 75)
print("IFRS 9 EXPECTED CREDIT LOSS ENGINE")
print("=" * 75)

if not DATASET_PATH.exists():

    raise FileNotFoundError(
        f"\nDataset not found:\n{DATASET_PATH}"
    )

loan_df = pd.read_csv(DATASET_PATH)

print("\nDataset Loaded Successfully")

print(f"Rows    : {len(loan_df):,}")

print(f"Columns : {len(loan_df.columns)}")

# =============================================================================
# VALIDATE COLUMNS
# =============================================================================

missing_columns = [

    col

    for col in REQUIRED_COLUMNS

    if col not in loan_df.columns

]

if missing_columns:

    # Raise a more specific error for missing required columns
    raise KeyError(f"\nMissing Required Columns:\n{missing_columns}")

print("\nRequired Column Validation : PASSED")

# =============================================================================
# DATA CLEANING
# =============================================================================

loan_df["PD_Estimate"] = pd.to_numeric(

    loan_df["PD_Estimate"],

    errors="coerce"

)

loan_df["LGD_Estimate"] = pd.to_numeric(

    loan_df["LGD_Estimate"],

    errors="coerce"

)

loan_df["EAD"] = pd.to_numeric(

    loan_df["EAD"],

    errors="coerce"

)

loan_df["ECL_Provision"] = pd.to_numeric(

    loan_df["ECL_Provision"],

    errors="coerce"

)

loan_df.fillna(

    {

        "PD_Estimate":0,

        "LGD_Estimate":0,

        "EAD":0,

        "ECL_Provision":0

    },

    inplace=True

)

# =============================================================================
# IFRS 9 CALCULATION
# =============================================================================

loan_df["Calculated_ECL"] = (

    loan_df["PD_Estimate"]

    *

    loan_df["LGD_Estimate"]

    *

    loan_df["EAD"]

).round(2)

loan_df["Provision_Variance"] = (

    loan_df["Calculated_ECL"]

    -

    loan_df["ECL_Provision"]

).round(2)

loan_df["Provision_Status"] = np.where(

    loan_df["Provision_Variance"] > 0,

    "Under Provisioned",

    np.where(

        loan_df["Provision_Variance"] < 0,

        "Over Provisioned",

        "Balanced"

    )

)

# =============================================================================
# RISK CATEGORIES
# =============================================================================

conditions = [

    loan_df["PD_Estimate"] < 0.02,

    loan_df["PD_Estimate"].between(0.02,0.05),

    loan_df["PD_Estimate"].between(0.05,0.10),

    loan_df["PD_Estimate"] >= 0.10

]

labels = [

    "Low",

    "Moderate",

    "High",

    "Very High"

]

loan_df["Risk_Category"] = np.select(

    conditions,

    labels,

    default="Unknown"

)

# =============================================================================
# PORTFOLIO KPIs
# =============================================================================

portfolio_summary = {

    "Total Loans":

        len(loan_df),

    "Portfolio Balance":

        loan_df["CurrentBalance"].sum(),

    "Total Exposure (EAD)":

        loan_df["EAD"].sum(),

    "Existing ECL":

        loan_df["ECL_Provision"].sum(),

    "Calculated ECL":

        loan_df["Calculated_ECL"].sum(),

    "Average PD":

        loan_df["PD_Estimate"].mean(),

    "Average LGD":

        loan_df["LGD_Estimate"].mean(),

    "Average Interest Rate":

        loan_df["InterestRate"].mean(),

    "Average LTV":

        loan_df["LTV_Current"].mean(),

    "Average CIBIL":

        loan_df["CIBIL_Score_Current"].mean()

}

portfolio_summary_df = pd.DataFrame(

    portfolio_summary.items(),

    columns=["Metric","Value"]

)

# =============================================================================
# IFRS STAGE SUMMARY
# =============================================================================

stage_summary = (

    loan_df

    .groupby("IFRS9_Stage")

    .agg(

        Loan_Count=("LoanID","count"),

        Portfolio_Balance=("CurrentBalance","sum"),

        Exposure=("EAD","sum"),

        Existing_ECL=("ECL_Provision","sum"),

        Calculated_ECL=("Calculated_ECL","sum"),

        Avg_PD=("PD_Estimate","mean"),

        Avg_LGD=("LGD_Estimate","mean"),

        Avg_CIBIL=("CIBIL_Score_Current","mean")

    )

    .reset_index()

)

print("\nStage Summary Prepared Successfully")

# -------------------------
# END OF PART 2A
# Continue with Part 2B
# -------------------------
# =============================================================================
# REGION SUMMARY
# =============================================================================

region_summary = (

    loan_df

    .groupby("Region")

    .agg(

        Loan_Count=("LoanID", "count"),

        Portfolio_Balance=("CurrentBalance", "sum"),

        Exposure=("EAD", "sum"),

        Calculated_ECL=("Calculated_ECL", "sum"),

        Average_PD=("PD_Estimate", "mean"),

        Average_LGD=("LGD_Estimate", "mean")

    )

    .reset_index()

    .sort_values(

        by="Calculated_ECL",

        ascending=False

    )

)

# =============================================================================
# STATE SUMMARY
# =============================================================================

state_summary = (

    loan_df

    .groupby("State")

    .agg(

        Loan_Count=("LoanID", "count"),

        Portfolio_Balance=("CurrentBalance", "sum"),

        Exposure=("EAD", "sum"),

        Calculated_ECL=("Calculated_ECL", "sum"),

        Average_PD=("PD_Estimate", "mean"),

        Average_LGD=("LGD_Estimate", "mean")

    )

    .reset_index()

    .sort_values(

        by="Calculated_ECL",

        ascending=False

    )

)

# =============================================================================
# RISK CATEGORY SUMMARY
# =============================================================================

risk_summary = (

    loan_df

    .groupby("Risk_Category")

    .agg(

        Loan_Count=("LoanID", "count"),

        Exposure=("EAD", "sum"),

        Portfolio_Balance=("CurrentBalance", "sum"),

        Total_ECL=("Calculated_ECL", "sum")

    )

    .reset_index()

)

# =============================================================================
# TOP 20 HIGH-RISK LOANS
# =============================================================================

top_risk_loans = (

    loan_df

    .sort_values(

        by="Calculated_ECL",

        ascending=False

    )

    .head(20)

)

# =============================================================================
# COVERAGE RATIO
# =============================================================================

portfolio_balance = loan_df["CurrentBalance"].sum()

calculated_ecl = loan_df["Calculated_ECL"].sum()

coverage_ratio = 0

if portfolio_balance != 0:

    coverage_ratio = (

        calculated_ecl /

        portfolio_balance

    ) * 100

coverage_df = pd.DataFrame({

    "Metric":[

        "Portfolio Balance",

        "Calculated ECL",

        "Coverage Ratio (%)"

    ],

    "Value":[

        portfolio_balance,

        calculated_ecl,

        round(coverage_ratio,2)

    ]

})

# =============================================================================
# EXPORT TO EXCEL
# =============================================================================

print("\nGenerating Excel Report...")

with pd.ExcelWriter(

    OUTPUT_FILE,

    engine="openpyxl"

) as writer:

    portfolio_summary_df.to_excel(

        writer,

        sheet_name="Portfolio Summary",

        index=False

    )

    stage_summary.to_excel(

        writer,

        sheet_name="IFRS Stage Summary",

        index=False

    )

    region_summary.to_excel(

        writer,

        sheet_name="Region Summary",

        index=False

    )

    state_summary.to_excel(

        writer,

        sheet_name="State Summary",

        index=False

    )

    risk_summary.to_excel(

        writer,

        sheet_name="Risk Summary",

        index=False

    )

    coverage_df.to_excel(

        writer,

        sheet_name="Coverage Ratio",

        index=False

    )

    top_risk_loans.to_excel(

        writer,

        sheet_name="Top 20 High Risk Loans",

        index=False

    )

    loan_df.to_excel(

        writer,

        sheet_name="Loan Level ECL",

        index=False

    )

# =============================================================================
# CONSOLE OUTPUT
# =============================================================================

print("\n" + "=" * 75)
print("IFRS 9 MODEL EXECUTED SUCCESSFULLY")
print("=" * 75)

print(f"\nOutput File : {OUTPUT_FILE}")

print("\n---------------- PORTFOLIO KPIs ----------------")

print(f"Total Loans               : {len(loan_df):,}")

print(f"Portfolio Balance         : {portfolio_balance:,.2f}")

print(f"Total Exposure (EAD)      : {loan_df['EAD'].sum():,.2f}")

print(f"Existing ECL             : {loan_df['ECL_Provision'].sum():,.2f}")

print(f"Calculated ECL           : {loan_df['Calculated_ECL'].sum():,.2f}")

print(f"Coverage Ratio           : {coverage_ratio:.2f}%")

print(f"Average PD               : {loan_df['PD_Estimate'].mean():.4f}")

print(f"Average LGD              : {loan_df['LGD_Estimate'].mean():.4f}")

print(f"Average Interest Rate    : {loan_df['InterestRate'].mean():.2f}%")

print(f"Average LTV              : {loan_df['LTV_Current'].mean():.2f}%")

print(f"Average CIBIL            : {loan_df['CIBIL_Score_Current'].mean():.2f}")

print("\n---------------- IFRS STAGE DISTRIBUTION ----------------")

print(stage_summary)

print("\n---------------- RISK CATEGORY DISTRIBUTION ----------------")

print(risk_summary)

print("\nTop 10 Highest Expected Credit Loss Loans")

print(

    top_risk_loans[

        [

            "LoanID",

            "IFRS9_Stage",

            "CurrentBalance",

            "PD_Estimate",

            "LGD_Estimate",

            "Calculated_ECL",

            "Risk_Category"

        ]

    ].head(10)

)

print("\nExcel report generated successfully.")

print("\nNext Step : Execute stress_testing.py")

print("\nDone.")

# =============================================================================
# END OF FILE
# =============================================================================