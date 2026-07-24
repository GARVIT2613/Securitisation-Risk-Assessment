"""
===============================================================================
Project : Securitisation Risk Analytics Platform
File    : stress_testing.py
Author  : Garvit Mehta

Purpose
-------
Perform macroeconomic stress testing using IFRS 9 Expected Credit Loss (ECL).

Formula
-------
Stress ECL = EAD × (PD × PD Multiplier) × (LGD × LGD Multiplier)

Outputs
-------
Stress_Test_Output.xlsx
===============================================================================
"""

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET = BASE_DIR / "Datasets" / "auto_loan_securitisation_data.csv"
OUTPUT = BASE_DIR / "Python" / "Stress_Test_Output.xlsx"

df = pd.read_csv(DATASET)

required = [
    "LoanID","PD_Estimate","LGD_Estimate","EAD",
    "CurrentBalance","IFRS9_Stage","ECL_Provision"
]

missing = [c for c in required if c not in df.columns]
if missing:
    raise Exception(f"Missing columns: {missing}")

for c in ["PD_Estimate","LGD_Estimate","EAD","CurrentBalance","ECL_Provision"]:
    df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

SCENARIOS = {
    "Base": (1.00,1.00),
    "Mild Recession": (1.25,1.10),
    "Severe Recession": (1.50,1.30),
    "Financial Crisis": (2.00,1.50),
    "Pandemic Shock": (2.25,1.60)
}

summary = []

with pd.ExcelWriter(OUTPUT, engine="openpyxl") as writer:

    for name,(pd_mult,lgd_mult) in SCENARIOS.items():

        temp = df.copy()

        temp["Stress_PD"] = (temp["PD_Estimate"]*pd_mult).clip(upper=1)
        temp["Stress_LGD"] = (temp["LGD_Estimate"]*lgd_mult).clip(upper=1)

        temp["Stress_ECL"] = (
            temp["Stress_PD"]*
            temp["Stress_LGD"]*
            temp["EAD"]
        ).round(2)

        temp["ECL_Change"] = (
            temp["Stress_ECL"]-
            temp["ECL_Provision"]
        ).round(2)

        stage = (
            temp.groupby("IFRS9_Stage")
            .agg(
                Loan_Count=("LoanID","count"),
                Portfolio_Balance=("CurrentBalance","sum"),
                Exposure=("EAD","sum"),
                Existing_ECL=("ECL_Provision","sum"),
                Stress_ECL=("Stress_ECL","sum")
            )
            .reset_index()
        )

        stage.to_excel(
            writer,
            sheet_name=name[:31],
            index=False
        )

        summary.append({
            "Scenario":name,
            "PD Multiplier":pd_mult,
            "LGD Multiplier":lgd_mult,
            "Portfolio Balance":temp["CurrentBalance"].sum(),
            "Exposure":temp["EAD"].sum(),
            "Existing ECL":temp["ECL_Provision"].sum(),
            "Stress ECL":temp["Stress_ECL"].sum(),
            "Increase":temp["Stress_ECL"].sum()-temp["ECL_Provision"].sum()
        })

        if name=="Financial Crisis":
            top20 = (
                temp.sort_values("Stress_ECL",ascending=False)
                .head(20)
            )
            top20.to_excel(
                writer,
                sheet_name="Top20_High_Risk",
                index=False
            )

    pd.DataFrame(summary).to_excel(
        writer,
        sheet_name="Scenario Summary",
        index=False
    )

print("="*70)
print("STRESS TESTING COMPLETED")
print("="*70)
print(pd.DataFrame(summary))
print(f"\nOutput saved to:\n{OUTPUT}")
