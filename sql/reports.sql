# Orders total
SELECT
    COUNT(*) AS order_count,
    ROUND(SUM(
        o.quantity * p.price *
        (1 - COALESCE(o.discount_pct, 0) / 100.0)),2) AS total_revenue,
    ROUND(AVG(
        o.quantity * p.price *
        (1 - COALESCE(o.discount_pct, 0) / 100.0)),2
    ) AS average_order_value
FROM orders AS o
JOIN products AS p
    ON o.product_id = p.product_id;
    
# calculate orders without rating    
SELECT
    COUNT(*) AS total_orders,
    COUNT(rating) AS orders_with_rating,
    COUNT(*) - COUNT(rating) AS orders_without_rating
FROM orders;    

#Left Join

SELECT
    c.customer_id,
    c.name
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.name
HAVING COUNT(o.order_id) = 0;

#Distinct

SELECT
    customer_id,
    name
FROM customers
WHERE customer_id NOT IN (
    SELECT DISTINCT customer_id
    FROM orders
);

#Group By + Having
SELECT
    c.city,
    COUNT(*) AS total_orders,
    SUM(o.returned) AS returned_orders,
    ROUND(SUM(o.returned) * 100.0 / COUNT(*), 1) AS return_rate_pct
FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id
GROUP BY c.city
HAVING return_rate_pct > 20
ORDER BY return_rate_pct DESC;

-- Run 1: Top 5 customers by total spend
SELECT
    c.customer_id,
    c.name,
    ROUND(SUM(o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100.0)
        ), 2
    ) AS total_spend
FROM orders AS o
JOIN products AS p
    ON o.product_id = p.product_id
JOIN customers AS c
    ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spend DESC, c.customer_id ASC
LIMIT 5;

# RANKING 3-5

SELECT
    c.customer_id,
    c.name,
    ROUND(SUM(o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100.0)), 2) AS total_spend
FROM orders AS o
JOIN products AS p
    ON o.product_id = p.product_id
JOIN customers AS c
    ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spend DESC, c.customer_id ASC
LIMIT 3 OFFSET 2;

# Group By Category
SELECT
    p.category,
    COUNT(*) AS order_count,
    ROUND(
        SUM(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100.0)
        ), 2
    ) AS category_revenue
FROM orders AS o
JOIN products AS p
    ON o.product_id = p.product_id
JOIN customers AS c
    ON o.customer_id = c.customer_id
GROUP BY p.category
ORDER BY category_revenue DESC;


#Like Pattern Match
SELECT
    customer_id,
    name,
    city
FROM customers
WHERE name LIKE 'A%';

# Distinct acquisition source against all customers

SELECT DISTINCT acquisition_source
FROM customers;

#Alter Table
ALTER TABLE customers
ADD COLUMN loyalty_tier VARCHAR(10);

SET SQL_SAFE_UPDATES = 0;
#Update
UPDATE customers
SET loyalty_tier =
    CASE
        WHEN city_tier = 1 THEN 'Gold'
        ELSE 'Silver'
    END;
    
    SET SQL_SAFE_UPDATES = 1;
    select * from customers;
    
    SELECT loyalty_tier, COUNT(*)
FROM customers
GROUP BY loyalty_tier;
