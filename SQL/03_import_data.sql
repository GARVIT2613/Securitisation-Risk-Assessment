SELECT
'fact_auto_loans' AS TableName,
COUNT(*) AS Records
FROM fact_auto_loans

UNION ALL

SELECT
'fact_dpd_history',
COUNT(*)
FROM fact_dpd_history

UNION ALL

SELECT
'fact_dynamic_loss',
COUNT(*)
FROM fact_dynamic_loss

UNION ALL

SELECT
'fact_vintage',
COUNT(*)
FROM fact_vintage;