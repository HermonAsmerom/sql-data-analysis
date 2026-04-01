-- Query 4: Revenue by Product Category
-- Business question: Which category drives the most revenue?

SELECT
    p.category,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(p.price * oi.quantity), 2) AS total_revenue,
    ROUND(AVG(p.price * oi.quantity), 2) AS avg_order_value
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY p.category
ORDER BY total_revenue DESC;
