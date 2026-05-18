-- =========================================================
-- E-Commerce Sales & Customer Behavior Analytics
-- SQL Business Queries
-- Dataset: Brazilian E-Commerce Public Dataset by Olist
-- =========================================================


-- 1. Total Revenue, Orders, and Customers
SELECT
    ROUND(SUM(payment_value), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_unique_id) AS total_customers
FROM ecommerce_main
WHERE order_status = 'delivered';


-- 2. Average Order Value
SELECT
    ROUND(SUM(payment_value) / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM ecommerce_main
WHERE order_status = 'delivered';


-- 3. Monthly Revenue Trend
SELECT
    order_year_month,
    ROUND(SUM(payment_value), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders
FROM ecommerce_main
WHERE order_status = 'delivered'
GROUP BY order_year_month
ORDER BY order_year_month;


-- 4. Top 10 Product Categories by Revenue
SELECT
    product_category_name_english,
    ROUND(SUM(payment_value), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders
FROM ecommerce_main
WHERE order_status = 'delivered'
  AND product_category_name_english IS NOT NULL
GROUP BY product_category_name_english
ORDER BY total_revenue DESC
LIMIT 10;


-- 5. Top 10 Customer States by Revenue
SELECT
    customer_state,
    ROUND(SUM(payment_value), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_unique_id) AS total_customers
FROM ecommerce_main
WHERE order_status = 'delivered'
GROUP BY customer_state
ORDER BY total_revenue DESC
LIMIT 10;


-- 6. Payment Method Distribution
SELECT
    payment_type,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(payment_value), 2) AS total_revenue
FROM ecommerce_main
WHERE order_status = 'delivered'
GROUP BY payment_type
ORDER BY total_orders DESC;


-- 7. Review Score Distribution
SELECT
    ROUND(review_score, 0) AS review_score,
    COUNT(DISTINCT order_id) AS total_orders
FROM ecommerce_main
WHERE order_status = 'delivered'
  AND review_score IS NOT NULL
GROUP BY ROUND(review_score, 0)
ORDER BY review_score;


-- 8. Delivery Performance
SELECT
    CASE 
        WHEN is_late_delivery = 1 THEN 'Late'
        ELSE 'On Time / Early'
    END AS delivery_status,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(review_score), 2) AS avg_review_score,
    ROUND(AVG(delivery_time_days), 2) AS avg_delivery_time_days
FROM ecommerce_main
WHERE order_status = 'delivered'
GROUP BY is_late_delivery;


-- 9. Customer Segment Summary
SELECT
    customer_segment,
    total_customers,
    ROUND(avg_recency, 2) AS avg_recency,
    ROUND(avg_frequency, 2) AS avg_frequency,
    ROUND(avg_monetary, 2) AS avg_monetary,
    ROUND(avg_rfm_score, 2) AS avg_rfm_score
FROM customer_segment_summary
ORDER BY total_customers DESC;


-- 10. High Value Customers
SELECT
    customer_unique_id,
    recency,
    frequency,
    ROUND(monetary, 2) AS monetary,
    R_score,
    F_score,
    M_score,
    RFM_total_score,
    customer_segment
FROM customer_rfm_analysis
WHERE customer_segment = 'High Value Customer'
ORDER BY monetary DESC
LIMIT 20;


-- 11. At Risk Customers
SELECT
    customer_unique_id,
    recency,
    frequency,
    ROUND(monetary, 2) AS monetary,
    RFM_total_score,
    customer_segment
FROM customer_rfm_analysis
WHERE customer_segment = 'At Risk Customer'
ORDER BY monetary DESC
LIMIT 20;


-- 12. Revenue Contribution by Product Category and State
SELECT
    customer_state,
    product_category_name_english,
    ROUND(SUM(payment_value), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders
FROM ecommerce_main
WHERE order_status = 'delivered'
  AND product_category_name_english IS NOT NULL
GROUP BY customer_state, product_category_name_english
ORDER BY total_revenue DESC
LIMIT 20;