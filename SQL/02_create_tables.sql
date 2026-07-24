/*==========================================================
 Project : Securitisation Risk Analytics Platform
 File    : 02_create_tables.sql
==========================================================*/

USE securitisation_risk_analytics;

-- =====================================================
-- FACT TABLE : AUTO LOANS
-- =====================================================

DROP TABLE IF EXISTS fact_auto_loans;

CREATE TABLE fact_auto_loans (

LoanID                     VARCHAR(100) PRIMARY KEY,

PoolID                     VARCHAR(100),
BorrowerID                 VARCHAR(100),
ServicerID                 VARCHAR(100),
ServicerName               VARCHAR(100),

OriginationDate            DATE,
CutoffDate                 DATE,
MaturityDate               DATE,

OriginalLoanAmount         DECIMAL(18,2),
CurrentBalance             DECIMAL(18,2),
MonthlyEMI                 DECIMAL(18,2),
InterestRate               DECIMAL(8,4),

LTV_Current                DECIMAL(8,4),
DTI_Ratio                  DECIMAL(8,4),

CIBIL_Score_Current        INT,

DelinquencyDays            INT,
DelinquencyStatus          VARCHAR(50),

IFRS9_Stage                VARCHAR(20),

PD_Estimate                DECIMAL(10,6),
LGD_Estimate               DECIMAL(10,6),
EAD                        DECIMAL(18,2),
ECL_Provision              DECIMAL(18,2),

RecoveryRate               DECIMAL(8,4),

CurrentPropertyValue       DECIMAL(18,2),

AnnualIncome_INR           DECIMAL(18,2),

EmploymentType             VARCHAR(100),

Region                     VARCHAR(100),

State                      VARCHAR(100),

City                       VARCHAR(100),

VehicleType                VARCHAR(100),

VehicleAge                 INT,

VehicleManufacturer        VARCHAR(100),

FuelType                   VARCHAR(50),

LoanStatus                 VARCHAR(50)

);

-- =====================================================
-- FACT TABLE : DPD HISTORY
-- =====================================================

DROP TABLE IF EXISTS fact_dpd_history;

CREATE TABLE fact_dpd_history (

SnapshotID                 INT AUTO_INCREMENT PRIMARY KEY,

LoanID                     VARCHAR(100),

SnapshotDate               DATE,

DPD_Days                   INT,

DPD_Bucket                 VARCHAR(50),

DPD_Bucket_Prior           VARCHAR(50),

TransitionType             VARCHAR(100),

CurrentBalance             DECIMAL(18,2),

CONSTRAINT fk_dpd_loan
FOREIGN KEY (LoanID)
REFERENCES fact_auto_loans(LoanID)

);

-- =====================================================
-- FACT TABLE : DYNAMIC LOSS
-- =====================================================

DROP TABLE IF EXISTS fact_dynamic_loss;

CREATE TABLE fact_dynamic_loss (

ReportingDate              DATE PRIMARY KEY,

CollectionsTotal           DECIMAL(18,2),

Recoveries_ThisMonth       DECIMAL(18,2),

GrossLoss_ThisMonth        DECIMAL(18,2),

NetLoss_ThisMonth          DECIMAL(18,2),

CollectionEfficiency       DECIMAL(8,4),

CPR_Annualised             DECIMAL(8,4),

CDR_Annualised             DECIMAL(8,4),

ExcessSpread_Monthly       DECIMAL(8,4),

ScheduledAmort             DECIMAL(18,2),

EOP_Balance                DECIMAL(18,2)

);

-- =====================================================
-- FACT TABLE : VINTAGE
-- =====================================================

DROP TABLE IF EXISTS fact_vintage;

CREATE TABLE fact_vintage (

VintageID                  VARCHAR(100),

MonthsOnBook               INT,

PoolFactor                 DECIMAL(10,6),

RemainingPoolBalance       DECIMAL(18,2),

CumulativeNetLossRate      DECIMAL(10,6),

CumulativeDefaultRate      DECIMAL(10,6),

PRIMARY KEY (VintageID, MonthsOnBook)

);

-- =====================================================
-- INDEXES
-- =====================================================

CREATE INDEX idx_pool
ON fact_auto_loans(PoolID);

CREATE INDEX idx_servicer
ON fact_auto_loans(ServicerName);

CREATE INDEX idx_stage
ON fact_auto_loans(IFRS9_Stage);

CREATE INDEX idx_dpd
ON fact_auto_loans(DelinquencyStatus);

CREATE INDEX idx_snapshot
ON fact_dpd_history(SnapshotDate);

CREATE INDEX idx_reporting
ON fact_dynamic_loss(ReportingDate);

CREATE INDEX idx_vintage
ON fact_vintage(VintageID);

-- =====================================================
-- VERIFY TABLES
-- =====================================================

SHOW TABLES;