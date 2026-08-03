# Sales Retail Pulse — Olist E-Commerce Analysis

An end-to-end analysis of the Brazilian Olist e-commerce dataset, covering sales
performance, customer segmentation, and churn risk — built using a SQL → Python →
Power BI pipeline.

## Overview

This project analyzes ~99K orders from the Olist marketplace to answer two core
business questions:
1. **How is the business performing?** — revenue trends, top categories, payment
   behavior, seller/state performance
2. **Which customers are at risk of churn, and how valuable are they?** — using
   RFM (Recency, Frequency, Monetary) segmentation and CLV estimation

## Pipeline

**1. MySQL** — Loaded the raw Olist tables (orders, customers, products, order
items, payments, reviews, sellers, geolocation, category translations) and
performed initial data cleaning: null removal and duplicate removal across
tables before further analysis.

**2. Python (pandas)** — Connected to the cleaned MySQL tables and performed:
- Table merges (orders + customers + payments)
- Filtered to delivered orders for reliable RFM calculation
- Built an RFM (Recency, Frequency, Monetary) table per customer using
  `groupby().agg()`
- Calculated Customer Lifetime Value (CLV) and flagged churned customers based
  on recency thresholds

**3. Power BI** — Built a 2-page interactive dashboard:
- **Page 1 — Sales Overview:** total revenue, total orders, average order
  value, revenue trend by month, orders by state, order status breakdown,
  revenue by product category, payment type distribution, seller revenue by
  city
- **Page 2 — Churn & Customer Value:** churn rate, CLV distribution, RFM table,
  active vs. churned customer split, recency vs. CLV scatter plot

## Key Metrics (from dashboard)
- 96K total customers
- 99K total orders
- ₹16M total revenue
- ₹161.02 average order value
- 59.18% churn rate (based on recency threshold)

## Tools Used
`MySQL` · `Python (pandas, SQLAlchemy)` · `Power BI`

## Dataset
[Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
(Kaggle) — not included in this repo due to size; download directly from the
source above.

## Dashboard Preview

### Sales Overview
![Sales Overview]("C:\Users\akhya\OneDrive\Pictures\Screenshots\Screenshot (135).png")

### Churn & Customer Value (RFM/CLV)
![Churn Analysis]("C:\Users\akhya\OneDrive\Pictures\Screenshots\Screenshot (136).png")

## How to Reproduce
1. Download the Olist dataset from Kaggle (link above)
2. Load CSVs into a MySQL database
3. Run `sql/cleaning_queries.sql` to clean nulls/duplicates
4. Run `python/olist_rfm_clv.py` to generate the RFM/CLV table
5. Open `powerbi/olist_dashboard.pbix` and point it to your MySQL connection
