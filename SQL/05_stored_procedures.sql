/*==========================================================
 Project : Securitisation Risk Analytics Platform
 File    : 05_stored_procedures.sql
==========================================================*/

USE securitisation_risk_analytics;

DELIMITER $$

-- =====================================================
-- Procedure 1 : Portfolio Summary
-- =====================================================

DROP PROCEDURE IF EXISTS sp_GetPortfolioSummary $$

CREATE PROCEDURE sp_GetPortfolioSummary()
BEGIN

    SELECT
        COUNT(*) AS TotalLoans,
        SUM(CurrentBalance) AS PortfolioBalance,
        SUM(ECL_Provision) AS TotalECL,
        AVG(PD_Estimate) AS AveragePD,
        AVG(LGD_Estimate) AS AverageLGD
    FROM fact_auto_loans;

END $$

-- =====================================================
-- Procedure 2 : IFRS 9 Summary
-- =====================================================

DROP PROCEDURE IF EXISTS sp_GetIFRS9Summary $$

CREATE PROCEDURE sp_GetIFRS9Summary()
BEGIN

    SELECT

        IFRS9_Stage,

        COUNT(*) AS LoanCount,

        SUM(CurrentBalance) AS PortfolioBalance,

        SUM(ECL_Provision) AS TotalECL,

        AVG(PD_Estimate) AS AveragePD,

        AVG(LGD_Estimate) AS AverageLGD

    FROM fact_auto_loans

    GROUP BY IFRS9_Stage

    ORDER BY IFRS9_Stage;

END $$

-- =====================================================
-- Procedure 3 : Stress Scenario
-- =====================================================

DROP PROCEDURE IF EXISTS sp_GetStressScenario $$

CREATE PROCEDURE sp_GetStressScenario(
    IN PDMultiplier DECIMAL(5,2),
    IN LGDMultiplier DECIMAL(5,2)
)

BEGIN

    SELECT

        LoanID,

        CurrentBalance,

        PD_Estimate,

        LGD_Estimate,

        ROUND(PD_Estimate * PDMultiplier,6) AS StressPD,

        ROUND(LGD_Estimate * LGDMultiplier,6) AS StressLGD,

        ROUND(
            EAD *
            (PD_Estimate * PDMultiplier) *
            (LGD_Estimate * LGDMultiplier),
        2) AS StressECL

    FROM fact_auto_loans;

END $$

DELIMITER ;