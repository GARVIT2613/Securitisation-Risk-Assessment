"""
===============================================================================
Project : Securitisation Risk Analytics Platform
File    : data_validation.py
Author  : Garvit Mehta
Purpose : Validate all project datasets before IFRS 9 and Stress Testing

This script performs:
✔ Missing Value Analysis
✔ Duplicate LoanID Detection
✔ Date Validation
✔ Negative Value Checks
✔ PD/LGD Range Validation
✔ CIBIL Score Validation
✔ DPD Validation
✔ Summary Report Generation

Output:
--------
Validation_Report.xlsx

Required Libraries:
-------------------
pip install pandas openpyxl numpy

===============================================================================
"""

import pandas as pd
import numpy as np
from pathlib import Path

# =============================================================================
# PROJECT PATHS
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_FOLDER = BASE_DIR / "Datasets"

DYNAMIC_LOSS_NAME = "Dynamic Loss"
DPD_HISTORY_NAME = "DPD History"

FILES = {
    "Auto Loans": DATASET_FOLDER / "auto_loan_securitisation_data.csv",
    DPD_HISTORY_NAME: DATASET_FOLDER / "dpd_snapshot_history.csv",
    DYNAMIC_LOSS_NAME: DATASET_FOLDER / "dynamic_loss_monthly.csv",
    "Vintage": DATASET_FOLDER / "static_pool_vintage_data.csv"
}

OUTPUT_FILE = BASE_DIR / "Python" / "Validation_Report.xlsx"

# =============================================================================
# REQUIRED COLUMNS
# =============================================================================

AUTO_REQUIRED = [
    "LoanID",
    "OriginationDate",
    "CutoffDate",
    "MaturityDate",
    "CurrentBalance",
    "OriginalLoanAmount",
    "PD_Estimate",
    "LGD_Estimate",
    "EAD",
    "ECL_Provision",
    "CIBIL_Score_Current"
]

DPD_REQUIRED = [
    "LoanID",
    "SnapshotDate",
    "DPD_Days"
]

LOSS_REQUIRED = [
    "ReportingDate",
    "GrossLoss_ThisMonth",
    "NetLoss_ThisMonth"
]

VINTAGE_REQUIRED = [
    "VintageID",
    "VintageStartDate",
    "PoolFactor"
]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def load_dataset(file_path):
    """Load CSV file"""

    if not file_path.exists():
        raise FileNotFoundError(f"\nDataset not found:\n{file_path}")

    return pd.read_csv(file_path)


def check_required_columns(df, required):

    missing = [col for col in required if col not in df.columns]

    return missing


def check_missing_values(df):

    result = (
        df.isnull()
        .sum()
        .reset_index()
    )

    result.columns = ["Column", "MissingValues"]

    result["MissingPercentage"] = (
        result["MissingValues"] / len(df) * 100
    ).round(2)

    return result


def check_duplicate_loanid(df):

    if "LoanID" not in df.columns:
        return pd.DataFrame()

    duplicates = df[df.duplicated("LoanID", keep=False)]

    return duplicates


def validate_dates(df):

    date_columns = [
        col for col in df.columns
        if "Date" in col
    ]

    results = []

    for col in date_columns:

        converted = pd.to_datetime(
            df[col],
            errors="coerce"
        )

        invalid = converted.isna().sum()

        results.append({

            "DateColumn": col,

            "InvalidDates": invalid

        })

    return pd.DataFrame(results)


def check_negative_values(df):

    numeric = df.select_dtypes(include=np.number).columns

    records = []

    for col in numeric:

        negative = (df[col] < 0).sum()

        records.append({

            "Column": col,

            "NegativeValues": int(negative)

        })

    return pd.DataFrame(records)


def validate_pd_lgd(df):

    output = []

    if "PD_Estimate" in df.columns:

        invalid_pd = (
            (df["PD_Estimate"] < 0) |
            (df["PD_Estimate"] > 1)
        ).sum()

        output.append({

            "Metric": "PD Estimate",

            "InvalidRows": int(invalid_pd)

        })

    if "LGD_Estimate" in df.columns:

        invalid_lgd = (
            (df["LGD_Estimate"] < 0) |
            (df["LGD_Estimate"] > 1)
        ).sum()

        output.append({

            "Metric": "LGD Estimate",

            "InvalidRows": int(invalid_lgd)

        })

    return pd.DataFrame(output)


def validate_cibil(df):

    if "CIBIL_Score_Current" not in df.columns:
        return pd.DataFrame()

    invalid = df[
        (df["CIBIL_Score_Current"] < 300) |
        (df["CIBIL_Score_Current"] > 900)
    ]

    return invalid


def validate_dpd(df):

    if "DPD_Days" not in df.columns:
        return pd.DataFrame()

    invalid = df[df["DPD_Days"] < 0]

    return invalid


def create_summary(dataset_name,
                   df,
                   duplicates,
                   cibil,
                   pdlgd):

    summary = {

        "Dataset": dataset_name,

        "Rows": len(df),

        "Columns": len(df.columns),

        "Duplicate LoanIDs": len(duplicates),

        "Invalid CIBIL Rows": len(cibil),

        "Invalid PD/LGD Rows": pdlgd["InvalidRows"].sum()
        if not pdlgd.empty else 0

    }

    return pd.DataFrame([summary])


# =============================================================================
# MAIN PROGRAM
# =============================================================================

print("=" * 75)
print("SECURITISATION RISK ANALYTICS PLATFORM")
print("DATA VALIDATION")
print("=" * 75)

writer = pd.ExcelWriter(
    OUTPUT_FILE,
    engine="openpyxl"
)

overall_summary = []

# =============================================================================
# AUTO LOAN DATASET
# =============================================================================

print("\nLoading Auto Loan Dataset...")

auto = load_dataset(FILES["Auto Loans"])

missing_columns = check_required_columns(
    auto,
    AUTO_REQUIRED
)

if missing_columns:
    raise ValueError(
        f"Missing Columns:\n{missing_columns}"
    )

missing = check_missing_values(auto)

duplicates = check_duplicate_loanid(auto)

dates = validate_dates(auto)

negative = check_negative_values(auto)

pdlgd = validate_pd_lgd(auto)

cibil = validate_cibil(auto)

summary = create_summary(
    "Auto Loans",
    auto,
    duplicates,
    cibil,
    pdlgd
)

overall_summary.append(summary)

missing.to_excel(
    writer,
    sheet_name="Auto_Missing",
    index=False
)

duplicates.to_excel(
    writer,
    sheet_name="Auto_Duplicates",
    index=False
)

dates.to_excel(
    writer,
    sheet_name="Auto_Dates",
    index=False
)

negative.to_excel(
    writer,
    sheet_name="Auto_Negative",
    index=False
)

pdlgd.to_excel(
    writer,
    sheet_name="PD_LGD_Check",
    index=False
)

cibil.to_excel(
    writer,
    sheet_name="CIBIL_Check",
    index=False
)

# =============================================================================
# DPD HISTORY
# =============================================================================

print("Loading DPD History...")

dpd = load_dataset(FILES["DPD History"])

missing = check_missing_values(dpd)

dates = validate_dates(dpd)

negative = check_negative_values(dpd)

invalid_dpd = validate_dpd(dpd)

summary = pd.DataFrame([{

    "Dataset": "DPD History",

    "Rows": len(dpd),

    "Columns": len(dpd.columns),

    "Invalid DPD": len(invalid_dpd)

}])

overall_summary.append(summary)

missing.to_excel(
    writer,
    sheet_name="DPD_Missing",
    index=False
)

dates.to_excel(
    writer,
    sheet_name="DPD_Dates",
    index=False
)

negative.to_excel(
    writer,
    sheet_name="DPD_Negative",
    index=False
)

invalid_dpd.to_excel(
    writer,
    sheet_name="Invalid_DPD",
    index=False
)

# =============================================================================
# DYNAMIC LOSS
# =============================================================================

print(f"Loading {DYNAMIC_LOSS_NAME} Dataset...")

loss = load_dataset(FILES[DYNAMIC_LOSS_NAME])

missing = check_missing_values(loss)

dates = validate_dates(loss)

negative = check_negative_values(loss)

summary = pd.DataFrame([{

    "Dataset": DYNAMIC_LOSS_NAME,

    "Rows": len(loss),

    "Columns": len(loss.columns)

}])

overall_summary.append(summary)

missing.to_excel(
    writer,
    sheet_name="Loss_Missing",
    index=False
)

dates.to_excel(
    writer,
    sheet_name="Loss_Dates",
    index=False
)

negative.to_excel(
    writer,
    sheet_name="Loss_Negative",
    index=False
)

# =============================================================================
# VINTAGE
# =============================================================================

print("Loading Vintage Dataset...")

vintage = load_dataset(FILES["Vintage"])

missing = check_missing_values(vintage)

dates = validate_dates(vintage)

negative = check_negative_values(vintage)

summary = pd.DataFrame([{

    "Dataset": "Vintage",

    "Rows": len(vintage),

    "Columns": len(vintage.columns)

}])

overall_summary.append(summary)

missing.to_excel(
    writer,
    sheet_name="Vintage_Missing",
    index=False
)

dates.to_excel(
    writer,
    sheet_name="Vintage_Dates",
    index=False
)

negative.to_excel(
    writer,
    sheet_name="Vintage_Negative",
    index=False
)

# =============================================================================
# FINAL SUMMARY
# =============================================================================

summary_sheet = pd.concat(
    overall_summary,
    ignore_index=True
)

summary_sheet.to_excel(
    writer,
    sheet_name="Validation_Summary",
    index=False
)

writer.close()

print("\n" + "=" * 75)
print("VALIDATION COMPLETED SUCCESSFULLY")
print("=" * 75)

print(f"\nReport Generated:\n{OUTPUT_FILE}")

print("\nValidation Summary\n")
print(summary_sheet)

print("\nProject is ready for:")
print("✓ IFRS 9 Modelling")
print("✓ Stress Testing")
print("✓ Power BI Dashboard")
print("\nDone.")