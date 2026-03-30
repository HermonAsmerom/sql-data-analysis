-- Query 2: Top Performing Products
-- Business question: Which products generate the most revenue?

SELECT
    p.name AS product_name,
    p.category,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(p.price * oi.quantity), 2) AS total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY p.product_id
ORDER BY total_revenue DESC
LIMIT 5;
