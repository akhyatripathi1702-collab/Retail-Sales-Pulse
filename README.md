# Sales Retail Pulse — Olist E-Commerce Analysis

An end-to-end analysis of the Brazilian Olist e-commerce dataset, covering sales performance, customer segmentation, churn risk, and statistical analysis — built using a SQL → Python → Power BI pipeline.

## Overview

This project analyzes approximately 99K orders from the Olist marketplace to answer three core business questions:

1. **How is the business performing?** — Revenue trends, top categories, payment behavior, and seller/state performance.
2. **Which customers are at risk of churn, and how valuable are they?** — Using RFM (Recency, Frequency, Monetary) segmentation and CLV estimation.
3. **How does delivery performance relate to customer satisfaction?** — Using correlation, regression analysis, and hypothesis testing.

## Pipeline

**1. MySQL** — Loaded the raw Olist tables (orders, customers, products, order items, payments, reviews, sellers, geolocation, and category translations) and performed initial data cleaning, including duplicate and missing-value handling.

**2. Python (pandas)** — Connected to the cleaned MySQL tables and performed:
- Table merging for orders, customers, payments, and reviews.
- Filtering to delivered orders for reliable RFM calculations.
- Customer-level RFM aggregation using `groupby().agg()`.
- CLV estimation and churn-risk classification based on a recency threshold.
- Correlation analysis to examine relationships between Recency, Frequency, and Monetary metrics.
- Simple linear regression to investigate the relationship between delivery time and review scores.
- Hypothesis testing to compare average review scores for late and on-time deliveries.

**3. Power BI** — Developed an interactive dashboard with three analytical pages:

- **Page 1 — Sales Overview:** Total revenue, total orders, average order value, monthly revenue trends, orders by state, order status breakdown, revenue by product category, payment type distribution, and seller revenue by city.
- **Page 2 — Churn & Customer Value:** Churn rate, CLV distribution, RFM table, active vs. churned customer split, and Recency vs. CLV scatter plot.
- **Page 3 — Statistical Analysis:** Comparison of review scores by delivery status, RFM correlation matrix, regression performance (R²), hypothesis-testing results, and key statistical insights.

## Key Metrics

- **96K** total customers
- **99K** total orders
- **₹16M** total revenue
- **₹161.02** average order value
- **59.18%** churn rate, based on the project's recency threshold

### Statistical Analysis Findings

- **On-time deliveries:** Average review score of 4.29/5.
- **Late deliveries:** Average review score of 2.57/5.
- **Review score difference:** Approximately 1.73 points lower for late-delivered orders.
- **Regression R²:** Approximately 11.13% for the delivery-time and review-score model.
- **Hypothesis testing:** The difference in average review scores was statistically significant (p < 0.001).

**Business insight:** Late-delivered orders are associated with substantially lower average customer review scores. Delivery performance may therefore be an important factor to investigate when improving customer satisfaction.

*Note: Statistical significance does not establish causation. R² describes the explanatory power of the fitted regression model, not the percentage of customers satisfied or dissatisfied.*

## Tools Used

`MySQL` · `Python` · `pandas` · `SQLAlchemy` · `Power BI`

## Dataset

[Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — Kaggle. The dataset is not included in this repository due to its size; download it directly from the source.

## Dashboard Preview

### Sales Overview

![Sales Overview](images/sales-overview.png)

### Churn & Customer Value (RFM/CLV)

![Churn Analysis](images/churn-analysis.png)

### Statistical Analysis

![Statistical Analysis](images/statistical-analysis.png)

*Place your dashboard screenshots in the repository's `images` folder using the filenames shown above.*

## How to Reproduce

1. Download the Olist dataset from Kaggle.
2. Load the CSV files into MySQL.
3. Run `sql/cleaning_queries.sql` to perform the documented cleaning operations.
4. Run `python/olist_rfm_clv.py` to generate the RFM and CLV analysis.
5. Run the statistical analysis script to reproduce the correlation, regression, and hypothesis-testing results.
6. Open `powerbi/olist_dashboard.pbix` and configure the database connection.
7. Explore the three dashboard pages to review sales performance, customer value, and statistical findings.
