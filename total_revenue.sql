-- Query 3: Customer Retention
-- Business question: How many customers came back and made more than one order?

SELECT
    CASE
        WHEN order_count = 1 THEN 'One-time buyer'
        WHEN order_count BETWEEN 2 AND 3 THEN 'Returning buyer'
        ELSE 'Loyal buyer'
    END AS customer_segment,
    COUNT(*) AS number_of_customers,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) AS percentage
FROM (
    SELECT customer_id, COUNT(order_id) AS order_count
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
) AS customer_orders
GROUP BY customer_segment
ORDER BY number_of_customers DESC;
