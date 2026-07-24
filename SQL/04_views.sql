/*==========================================================
 Project : Securitisation Risk Analytics Platform
 File    : 04_views.sql
==========================================================*/

USE securitisation_risk_analytics;

-- =====================================================
-- VIEW 1 : Portfolio Summary
-- =====================================================

DROP VIEW IF EXISTS vw_portfolio_summary;

CREATE VIEW vw_portfolio_summary AS

SELECT

PoolID,

COUNT(*) AS TotalLoans,

SUM(CurrentBalance) AS PortfolioBalance,

SUM(ECL_Provision) AS TotalECL,

AVG(PD_Estimate) AS AvgPD,

AVG(LGD_Estimate) AS AvgLGD,

AVG(InterestRate) AS AvgInterestRate

FROM fact_auto_loans

GROUP BY PoolID;

-- =====================================================
-- VIEW 2 : IFRS 9 Summary
-- =====================================================

DROP VIEW IF EXISTS vw_ifrs9_summary;

CREATE VIEW vw_ifrs9_summary AS

SELECT

IFRS9_Stage,

COUNT(*) AS LoanCount,

SUM(CurrentBalance) AS PortfolioBalance,

SUM(EAD) AS TotalExposure,

SUM(ECL_Provision) AS TotalECL,

AVG(PD_Estimate) AS AvgPD,

AVG(LGD_Estimate) AS AvgLGD

FROM fact_auto_loans

GROUP BY IFRS9_Stage;

-- =====================================================
-- VIEW 3 : Delinquency Summary
-- =====================================================

DROP VIEW IF EXISTS vw_dpd_summary;

CREATE VIEW vw_dpd_summary AS

SELECT

DPD_Bucket,

COUNT(*) AS LoanCount,

AVG(DPD_Days) AS AvgDPD,

SUM(CurrentBalance) AS PortfolioBalance

FROM fact_dpd_history

GROUP BY DPD_Bucket;

-- =====================================================
-- VIEW 4 : Servicer Performance
-- =====================================================

DROP VIEW IF EXISTS vw_servicer_summary;

CREATE VIEW vw_servicer_summary AS

SELECT

ServicerName,

COUNT(*) AS LoanCount,

SUM(CurrentBalance) AS PortfolioBalance,

SUM(ECL_Provision) AS TotalECL,

AVG(PD_Estimate) AS AvgPD,

AVG(LGD_Estimate) AS AvgLGD

FROM fact_auto_loans

GROUP BY ServicerName;

-- =====================================================
-- VIEW 5 : Dynamic Loss Summary
-- =====================================================

DROP VIEW IF EXISTS vw_dynamic_loss_summary;

CREATE VIEW vw_dynamic_loss_summary AS

SELECT

ReportingDate,

CollectionsTotal,

Recoveries_ThisMonth,

GrossLoss_ThisMonth,

NetLoss_ThisMonth,

CollectionEfficiency,

CPR_Annualised,

CDR_Annualised,

ExcessSpread_Monthly,

EOP_Balance

FROM fact_dynamic_loss;

-- =====================================================
-- VIEW 6 : Vintage Summary
-- =====================================================

DROP VIEW IF EXISTS vw_vintage_summary;

CREATE VIEW vw_vintage_summary AS

SELECT

VintageID,

MonthsOnBook,

PoolFactor,

RemainingPoolBalance,

CumulativeDefaultRate,

CumulativeNetLossRate

FROM fact_vintage;

-- =====================================================
-- VERIFY CREATED VIEWS
-- =====================================================

SHOW FULL TABLES
WHERE Table_type='VIEW';