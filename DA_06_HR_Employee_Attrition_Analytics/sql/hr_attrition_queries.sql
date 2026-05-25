-- =========================================================
-- HR Employee Attrition & Workforce Analytics
-- SQL Business Queries
-- Dataset: IBM HR Analytics Employee Attrition & Performance
-- =========================================================

-- Notes:
-- These queries assume the cleaned dataset is stored in a table named:
-- hr_attrition_cleaned
--
-- Main columns:
-- EmployeeNumber
-- Attrition
-- attrition_flag
-- Department
-- JobRole
-- OverTime
-- Age
-- age_group
-- MonthlyIncome
-- income_group
-- JobSatisfaction
-- WorkLifeBalance
-- YearsAtCompany
-- risk_segment


-- 1. Total Employees, Total Attrition, and Attrition Rate
SELECT
    COUNT(DISTINCT EmployeeNumber) AS total_employees,
    SUM(attrition_flag) AS total_attrition,
    ROUND(SUM(attrition_flag) * 1.0 / COUNT(DISTINCT EmployeeNumber), 4) AS attrition_rate
FROM hr_attrition_cleaned;


-- 2. Average Employee Profile
SELECT
    ROUND(AVG(Age), 2) AS avg_age,
    ROUND(AVG(MonthlyIncome), 2) AS avg_monthly_income,
    ROUND(AVG(YearsAtCompany), 2) AS avg_years_at_company,
    ROUND(AVG(JobSatisfaction), 2) AS avg_job_satisfaction,
    ROUND(AVG(WorkLifeBalance), 2) AS avg_work_life_balance
FROM hr_attrition_cleaned;


-- 3. Attrition by Department
SELECT
    Department,
    COUNT(DISTINCT EmployeeNumber) AS total_employees,
    SUM(attrition_flag) AS total_attrition,
    ROUND(SUM(attrition_flag) * 1.0 / COUNT(DISTINCT EmployeeNumber), 4) AS attrition_rate
FROM hr_attrition_cleaned
GROUP BY Department
ORDER BY attrition_rate DESC;


-- 4. Attrition by Job Role
SELECT
    JobRole,
    COUNT(DISTINCT EmployeeNumber) AS total_employees,
    SUM(attrition_flag) AS total_attrition,
    ROUND(SUM(attrition_flag) * 1.0 / COUNT(DISTINCT EmployeeNumber), 4) AS attrition_rate
FROM hr_attrition_cleaned
GROUP BY JobRole
ORDER BY attrition_rate DESC;


-- 5. Attrition by OverTime
SELECT
    OverTime,
    COUNT(DISTINCT EmployeeNumber) AS total_employees,
    SUM(attrition_flag) AS total_attrition,
    ROUND(SUM(attrition_flag) * 1.0 / COUNT(DISTINCT EmployeeNumber), 4) AS attrition_rate
FROM hr_attrition_cleaned
GROUP BY OverTime
ORDER BY attrition_rate DESC;


-- 6. Attrition by Age Group
SELECT
    age_group,
    COUNT(DISTINCT EmployeeNumber) AS total_employees,
    SUM(attrition_flag) AS total_attrition,
    ROUND(SUM(attrition_flag) * 1.0 / COUNT(DISTINCT EmployeeNumber), 4) AS attrition_rate
FROM hr_attrition_cleaned
GROUP BY age_group
ORDER BY attrition_rate DESC;


-- 7. Attrition by Income Group
SELECT
    income_group,
    COUNT(DISTINCT EmployeeNumber) AS total_employees,
    SUM(attrition_flag) AS total_attrition,
    ROUND(SUM(attrition_flag) * 1.0 / COUNT(DISTINCT EmployeeNumber), 4) AS attrition_rate
FROM hr_attrition_cleaned
GROUP BY income_group
ORDER BY attrition_rate DESC;


-- 8. Attrition by Job Satisfaction
SELECT
    JobSatisfaction,
    COUNT(DISTINCT EmployeeNumber) AS total_employees,
    SUM(attrition_flag) AS total_attrition,
    ROUND(SUM(attrition_flag) * 1.0 / COUNT(DISTINCT EmployeeNumber), 4) AS attrition_rate
FROM hr_attrition_cleaned
GROUP BY JobSatisfaction
ORDER BY JobSatisfaction;


-- 9. Attrition by Work Life Balance
SELECT
    WorkLifeBalance,
    COUNT(DISTINCT EmployeeNumber) AS total_employees,
    SUM(attrition_flag) AS total_attrition,
    ROUND(SUM(attrition_flag) * 1.0 / COUNT(DISTINCT EmployeeNumber), 4) AS attrition_rate
FROM hr_attrition_cleaned
GROUP BY WorkLifeBalance
ORDER BY WorkLifeBalance;


-- 10. Risk Segment Summary
SELECT
    risk_segment,
    COUNT(DISTINCT EmployeeNumber) AS total_employees,
    SUM(attrition_flag) AS total_attrition,
    ROUND(AVG(MonthlyIncome), 2) AS avg_monthly_income,
    ROUND(AVG(Age), 2) AS avg_age,
    ROUND(AVG(YearsAtCompany), 2) AS avg_years_at_company,
    ROUND(SUM(attrition_flag) * 1.0 / COUNT(DISTINCT EmployeeNumber), 4) AS attrition_rate
FROM hr_attrition_cleaned
GROUP BY risk_segment
ORDER BY attrition_rate DESC;


-- 11. Top High-Risk Job Roles
SELECT
    JobRole,
    COUNT(DISTINCT EmployeeNumber) AS total_employees,
    SUM(attrition_flag) AS total_attrition,
    ROUND(SUM(attrition_flag) * 1.0 / COUNT(DISTINCT EmployeeNumber), 4) AS attrition_rate
FROM hr_attrition_cleaned
GROUP BY JobRole
HAVING COUNT(DISTINCT EmployeeNumber) >= 20
ORDER BY attrition_rate DESC
LIMIT 5;


-- 12. Overtime and Job Satisfaction Analysis
SELECT
    OverTime,
    JobSatisfaction,
    COUNT(DISTINCT EmployeeNumber) AS total_employees,
    SUM(attrition_flag) AS total_attrition,
    ROUND(SUM(attrition_flag) * 1.0 / COUNT(DISTINCT EmployeeNumber), 4) AS attrition_rate
FROM hr_attrition_cleaned
GROUP BY OverTime, JobSatisfaction
ORDER BY OverTime, JobSatisfaction;


-- 13. Overtime and Work Life Balance Analysis
SELECT
    OverTime,
    WorkLifeBalance,
    COUNT(DISTINCT EmployeeNumber) AS total_employees,
    SUM(attrition_flag) AS total_attrition,
    ROUND(SUM(attrition_flag) * 1.0 / COUNT(DISTINCT EmployeeNumber), 4) AS attrition_rate
FROM hr_attrition_cleaned
GROUP BY OverTime, WorkLifeBalance
ORDER BY OverTime, WorkLifeBalance;


-- 14. Monthly Income by Attrition Status
SELECT
    Attrition,
    COUNT(DISTINCT EmployeeNumber) AS total_employees,
    ROUND(AVG(MonthlyIncome), 2) AS avg_monthly_income,
    ROUND(MIN(MonthlyIncome), 2) AS min_monthly_income,
    ROUND(MAX(MonthlyIncome), 2) AS max_monthly_income
FROM hr_attrition_cleaned
GROUP BY Attrition;


-- 15. Business Recommendation Query
SELECT
    risk_segment,
    COUNT(DISTINCT EmployeeNumber) AS total_employees,
    SUM(attrition_flag) AS total_attrition,
    ROUND(SUM(attrition_flag) * 1.0 / COUNT(DISTINCT EmployeeNumber), 4) AS attrition_rate,
    CASE
        WHEN ROUND(SUM(attrition_flag) * 1.0 / COUNT(DISTINCT EmployeeNumber), 4) >= 0.30
            THEN 'Priority retention action required'
        WHEN ROUND(SUM(attrition_flag) * 1.0 / COUNT(DISTINCT EmployeeNumber), 4) >= 0.20
            THEN 'Monitor and improve engagement'
        ELSE 'Maintain current retention strategy'
    END AS recommendation
FROM hr_attrition_cleaned
GROUP BY risk_segment
ORDER BY attrition_rate DESC;