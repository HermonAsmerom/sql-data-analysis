# SQL Data Analysis — E-Commerce Orders

## Overview
A series of SQL queries analysing e-commerce order data to surface actionable business insights around revenue, customer retention, and product performance.

## Problem
Businesses generate large volumes of transactional data but often lack the analysis to understand what's driving revenue and where customers are dropping off.

## Solution
Using a sample e-commerce dataset, I wrote structured SQL queries to answer real business questions across sales, retention, and segmentation.

## Tech Stack
- SQL (SQLite / PostgreSQL compatible)
- DB Browser for SQLite (or any SQL client)
- Optional: Python + Matplotlib for visualisation

## Queries Included

| Query | Business Question |
|---|---|
| `total_revenue.sql` | What is total revenue by month? |
| `top_products.sql` | Which products drive the most sales? |
| `customer_retention.sql` | What % of customers return after first purchase? |
| `segment_analysis.sql` | Which customer segments are most valuable? |
| `revenue_trend.sql` | How has revenue trended over time? |

## Sample Insight
> Customers who made a second purchase within 30 days had a 3x higher lifetime value than one-time buyers.

## How to Run
```bash
# Open the database
sqlite3 ecommerce.db

# Run a query
.read queries/total_revenue.sql
```


## Key Learnings
- Writing multi-table JOINs for customer and order data
- Using window functions for retention cohort analysis
- Translating SQL output into business recommendations

## Next Steps
- Connect to a live database via Python (psycopg2)
- Build a visual dashboard using Tableau or Metabase
- Add A/B test analysis queries
