/*==========================================================
 Project : Securitisation Risk Analytics Platform
 File    : 01_create_database.sql
 Author  : Garvit Mehta
==========================================================*/

-- Remove old database if it exists
DROP DATABASE IF EXISTS securitisation_risk_analytics;

-- Create new database
CREATE DATABASE securitisation_risk_analytics
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Use the database
USE securitisation_risk_analytics;

-- Verify that the correct database is selected
SELECT DATABASE() AS CurrentDatabase;