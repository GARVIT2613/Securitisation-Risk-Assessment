# 📊 Securitisation Risk Analytics Platform

<p align="center">
  <b>Enterprise-grade Banking Risk Analytics | Power BI • Python • SQL • IFRS 9</b>
</p>

<p align="center">
<img src="https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi">
<img src="https://img.shields.io/badge/Python-3.12-blue?logo=python">
<img src="https://img.shields.io/badge/MySQL-Database-4479A1?logo=mysql">
<img src="https://img.shields.io/badge/IFRS9-ECL-success">
<img src="https://img.shields.io/badge/License-MIT-green">
</p>

---

## 🚀 Overview

**Securitisation Risk Analytics Platform** is an end-to-end banking analytics project that simulates how financial institutions monitor securitised auto-loan portfolios. It combines **SQL, Python, and Microsoft Power BI** to automate data validation, IFRS 9 Expected Credit Loss (ECL) calculations, macroeconomic stress testing, and executive reporting.

The solution follows a modern analytics workflow—from raw portfolio data to business-ready dashboards—and is designed as a portfolio-quality demonstration of banking risk analytics and business intelligence.

---

## ✨ Key Features

- Automated data validation pipeline
- IFRS 9 Expected Credit Loss (ECL) calculations
- Delinquency (DPD) & portfolio risk monitoring
- Static Pool Vintage analysis
- Dynamic Loss tracking
- Cash Flow Waterfall reporting
- Macroeconomic stress testing
- Executive KPI dashboards
- Investor reporting
- SQL reporting views & stored procedures

---

## 🏗️ Project Architecture

```text
CSV Datasets
      │
      ▼
Python Validation Engine
      │
      ▼
IFRS 9 ECL Engine
      │
      ▼
Stress Testing Engine
      │
      ▼
MySQL Database
      │
      ▼
Power BI Dashboards
      │
      ▼
Business Insights
```

---

## 🛠️ Tech Stack

| Layer | Technologies |
|-------|--------------|
| Visualization | Microsoft Power BI |
| Programming | Python |
| Database | MySQL |
| Analytics | DAX, Power Query |
| Libraries | Pandas, NumPy, OpenPyXL |
| Version Control | Git & GitHub |

---

## 📁 Project Structure

```text
Securitisation-Risk-Analytics/
├── Datasets/
├── SQL/
├── Python/
├── PowerBI/
├── Documentation/
├── README.md
├── LICENSE
└── .gitignore
```

---

## 📈 Dashboards

- Executive Summary
- Portfolio Overview
- IFRS 9 Analytics
- DPD & Roll Rate
- Vintage Analysis
- Dynamic Loss
- Waterfall Analysis
- Stress Testing
- Investor Reporting

> Add screenshots in `/Documentation/Dashboard_Screenshots/` and embed them here for maximum impact.

---

## ⚙️ Python Modules

### `data_validation.py`
Validates datasets by checking missing values, duplicates, invalid dates, negative balances, PD/LGD ranges, and CIBIL scores.

### `ifrs9_model.py`
Calculates Expected Credit Loss using:

```text
ECL = PD × LGD × EAD
```

Generates portfolio-level and stage-wise summaries.

### `stress_testing.py`
Applies multiple macroeconomic scenarios:
- Base
- Mild Recession
- Severe Recession
- Financial Crisis
- Pandemic Shock

---

## 🗄️ SQL Components

- Database creation
- Normalized schema
- Data import scripts
- Analytical Views
- Stored Procedures

---

## 📊 Business Value

This project demonstrates practical implementation of:

- Credit Risk Analytics
- IFRS 9 Provisioning
- Portfolio Monitoring
- Banking Business Intelligence
- Stress Testing
- Financial Reporting

---

## 🚀 Getting Started

```bash
git clone <repository-url>
cd Securitisation-Risk-Analytics

pip install -r Python/requirements.txt
```

Run:

```bash
python Python/data_validation.py
python Python/ifrs9_model.py
python Python/stress_testing.py
```

Open the Power BI report to explore interactive dashboards.

---

## 📌 Future Improvements

- Automated ETL pipelines
- Cloud deployment
- ML-based Probability of Default models
- Real-time dashboard refresh
- CI/CD workflow

---

## 👨‍💻 Author

**Garvit Mehta**

If you found this project useful, consider giving it a ⭐ on GitHub.
