-- =========================================================
-- Marketing A/B Testing Campaign Analysis
-- SQL Business Queries
-- Dataset: Control Campaign vs Test Campaign
-- =========================================================

-- Notes:
-- These queries assume the cleaned dataset is stored in a table named:
-- ab_testing_cleaned
--
-- Main columns:
-- group
-- spend
-- impressions
-- reach
-- website_clicks
-- searches
-- view_content
-- add_to_cart
-- purchase
-- ctr
-- purchase_conversion_rate
-- cart_to_purchase_rate
-- cost_per_click
-- cost_per_purchase


-- =========================================================
-- 1. Total Campaign Performance by Group
-- =========================================================

SELECT
    "group",
    SUM(spend) AS total_spend,
    SUM(impressions) AS total_impressions,
    SUM(reach) AS total_reach,
    SUM(website_clicks) AS total_website_clicks,
    SUM(add_to_cart) AS total_add_to_cart,
    SUM(purchase) AS total_purchase
FROM ab_testing_cleaned
GROUP BY "group";


-- =========================================================
-- 2. CTR by Campaign Group
-- CTR = website clicks / impressions
-- =========================================================

SELECT
    "group",
    ROUND(SUM(website_clicks) * 1.0 / SUM(impressions), 4) AS ctr
FROM ab_testing_cleaned
GROUP BY "group";


-- =========================================================
-- 3. Purchase Conversion Rate by Campaign Group
-- Purchase Conversion Rate = purchase / website clicks
-- =========================================================

SELECT
    "group",
    ROUND(SUM(purchase) * 1.0 / SUM(website_clicks), 4) AS purchase_conversion_rate
FROM ab_testing_cleaned
GROUP BY "group";


-- =========================================================
-- 4. Cart to Purchase Rate by Campaign Group
-- Cart to Purchase Rate = purchase / add to cart
-- =========================================================

SELECT
    "group",
    ROUND(SUM(purchase) * 1.0 / SUM(add_to_cart), 4) AS cart_to_purchase_rate
FROM ab_testing_cleaned
GROUP BY "group";


-- =========================================================
-- 5. Cost per Click by Campaign Group
-- Cost per Click = spend / website clicks
-- =========================================================

SELECT
    "group",
    ROUND(SUM(spend) * 1.0 / SUM(website_clicks), 2) AS cost_per_click
FROM ab_testing_cleaned
GROUP BY "group";


-- =========================================================
-- 6. Cost per Purchase by Campaign Group
-- Cost per Purchase = spend / purchase
-- =========================================================

SELECT
    "group",
    ROUND(SUM(spend) * 1.0 / SUM(purchase), 2) AS cost_per_purchase
FROM ab_testing_cleaned
GROUP BY "group";


-- =========================================================
-- 7. Daily Purchase Trend by Campaign Group
-- =========================================================

SELECT
    date,
    "group",
    purchase
FROM ab_testing_cleaned
ORDER BY date, "group";


-- =========================================================
-- 8. Daily Spend Trend by Campaign Group
-- =========================================================

SELECT
    date,
    "group",
    spend
FROM ab_testing_cleaned
ORDER BY date, "group";


-- =========================================================
-- 9. Marketing Funnel Summary
-- =========================================================

SELECT
    "group",
    SUM(impressions) AS impressions,
    SUM(reach) AS reach,
    SUM(website_clicks) AS website_clicks,
    SUM(searches) AS searches,
    SUM(view_content) AS view_content,
    SUM(add_to_cart) AS add_to_cart,
    SUM(purchase) AS purchase
FROM ab_testing_cleaned
GROUP BY "group";


-- =========================================================
-- 10. Funnel Drop-off Rate: Impressions to Clicks
-- =========================================================

SELECT
    "group",
    SUM(impressions) AS total_impressions,
    SUM(website_clicks) AS total_clicks,
    ROUND(
        1 - (SUM(website_clicks) * 1.0 / SUM(impressions)),
        4
    ) AS impression_to_click_dropoff_rate
FROM ab_testing_cleaned
GROUP BY "group";


-- =========================================================
-- 11. Funnel Drop-off Rate: Clicks to Purchase
-- =========================================================

SELECT
    "group",
    SUM(website_clicks) AS total_clicks,
    SUM(purchase) AS total_purchase,
    ROUND(
        1 - (SUM(purchase) * 1.0 / SUM(website_clicks)),
        4
    ) AS click_to_purchase_dropoff_rate
FROM ab_testing_cleaned
GROUP BY "group";


-- =========================================================
-- 12. Campaign Efficiency Summary
-- =========================================================

SELECT
    "group",
    SUM(spend) AS total_spend,
    SUM(purchase) AS total_purchase,
    ROUND(SUM(website_clicks) * 1.0 / SUM(impressions), 4) AS ctr,
    ROUND(SUM(purchase) * 1.0 / SUM(website_clicks), 4) AS purchase_conversion_rate,
    ROUND(SUM(spend) * 1.0 / SUM(website_clicks), 2) AS cost_per_click,
    ROUND(SUM(spend) * 1.0 / SUM(purchase), 2) AS cost_per_purchase
FROM ab_testing_cleaned
GROUP BY "group";


-- =========================================================
-- 13. Best Campaign Based on CTR
-- =========================================================

SELECT
    "group",
    ROUND(SUM(website_clicks) * 1.0 / SUM(impressions), 4) AS ctr
FROM ab_testing_cleaned
GROUP BY "group"
ORDER BY ctr DESC
LIMIT 1;


-- =========================================================
-- 14. Best Campaign Based on Purchase Conversion Rate
-- =========================================================

SELECT
    "group",
    ROUND(SUM(purchase) * 1.0 / SUM(website_clicks), 4) AS purchase_conversion_rate
FROM ab_testing_cleaned
GROUP BY "group"
ORDER BY purchase_conversion_rate DESC
LIMIT 1;


-- =========================================================
-- 15. Best Campaign Based on Cost per Purchase
-- Lower cost per purchase is better
-- =========================================================

SELECT
    "group",
    ROUND(SUM(spend) * 1.0 / SUM(purchase), 2) AS cost_per_purchase
FROM ab_testing_cleaned
GROUP BY "group"
ORDER BY cost_per_purchase ASC
LIMIT 1;


-- =========================================================
-- 16. Uplift: Test Campaign vs Control Campaign
-- =========================================================

WITH campaign_metrics AS (
    SELECT
        "group",
        ROUND(SUM(website_clicks) * 1.0 / SUM(impressions), 6) AS ctr,
        ROUND(SUM(purchase) * 1.0 / SUM(website_clicks), 6) AS purchase_conversion_rate,
        ROUND(SUM(purchase) * 1.0 / SUM(add_to_cart), 6) AS cart_to_purchase_rate,
        ROUND(SUM(spend) * 1.0 / SUM(website_clicks), 6) AS cost_per_click,
        ROUND(SUM(spend) * 1.0 / SUM(purchase), 6) AS cost_per_purchase,
        SUM(purchase) AS total_purchase
    FROM ab_testing_cleaned
    GROUP BY "group"
),
control AS (
    SELECT * FROM campaign_metrics WHERE "group" = 'Control'
),
test AS (
    SELECT * FROM campaign_metrics WHERE "group" = 'Test'
)

SELECT
    'CTR' AS metric,
    control.ctr AS control_value,
    test.ctr AS test_value,
    ROUND((test.ctr - control.ctr) * 100.0 / control.ctr, 2) AS uplift_percent
FROM control, test

UNION ALL

SELECT
    'Purchase Conversion Rate' AS metric,
    control.purchase_conversion_rate AS control_value,
    test.purchase_conversion_rate AS test_value,
    ROUND((test.purchase_conversion_rate - control.purchase_conversion_rate) * 100.0 / control.purchase_conversion_rate, 2) AS uplift_percent
FROM control, test

UNION ALL

SELECT
    'Cart to Purchase Rate' AS metric,
    control.cart_to_purchase_rate AS control_value,
    test.cart_to_purchase_rate AS test_value,
    ROUND((test.cart_to_purchase_rate - control.cart_to_purchase_rate) * 100.0 / control.cart_to_purchase_rate, 2) AS uplift_percent
FROM control, test

UNION ALL

SELECT
    'Cost per Click' AS metric,
    control.cost_per_click AS control_value,
    test.cost_per_click AS test_value,
    ROUND((test.cost_per_click - control.cost_per_click) * 100.0 / control.cost_per_click, 2) AS uplift_percent
FROM control, test

UNION ALL

SELECT
    'Cost per Purchase' AS metric,
    control.cost_per_purchase AS control_value,
    test.cost_per_purchase AS test_value,
    ROUND((test.cost_per_purchase - control.cost_per_purchase) * 100.0 / control.cost_per_purchase, 2) AS uplift_percent
FROM control, test

UNION ALL

SELECT
    'Total Purchase' AS metric,
    control.total_purchase AS control_value,
    test.total_purchase AS test_value,
    ROUND((test.total_purchase - control.total_purchase) * 100.0 / control.total_purchase, 2) AS uplift_percent
FROM control, test;


-- =========================================================
-- 17. Business Decision Query
-- Campaign recommendation based on purchase conversion rate
-- =========================================================

WITH conversion_summary AS (
    SELECT
        "group",
        ROUND(SUM(purchase) * 1.0 / SUM(website_clicks), 6) AS purchase_conversion_rate,
        ROUND(SUM(spend) * 1.0 / SUM(purchase), 2) AS cost_per_purchase
    FROM ab_testing_cleaned
    GROUP BY "group"
)

SELECT
    "group",
    purchase_conversion_rate,
    cost_per_purchase,
    CASE
        WHEN purchase_conversion_rate = (
            SELECT MAX(purchase_conversion_rate)
            FROM conversion_summary
        )
        THEN 'Recommended for purchase conversion'
        ELSE 'Needs optimization'
    END AS recommendation
FROM conversion_summary;