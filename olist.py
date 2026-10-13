
from sqlalchemy import create_engine
import pandas as pd
engine = create_engine("mysql+pymysql://root:Akh#17rysh@localhost:3307/olist_db")


orders = pd.read_sql("SELECT * from orders",engine)
customers = pd.read_sql("SELECT * from customers",engine)
products = pd.read_sql("SELECT *  from products",engine)
order_payments = pd.read_sql("SELECT * from order_payments",engine)
order_items = pd.read_sql("SELECT * from order_items",engine)
order_reviews = pd.read_sql("SELECT * from order_review",engine)
seller = pd.read_sql("SELECT * from seller",engine)
cateogary_translation = pd.read_sql("SELECT * from cateogory_translation",engine)
geolocation = pd.read_sql("SELECT * from geolocation",engine)


print("Orders:", orders.shape)
print("Customers:", customers.shape)
print("Payments:", order_payments.shape)
print("Order items:", order_items.shape)
print("Order reviews:", order_reviews.shape)
print("Seller:", seller.shape)
print("Products:", products.shape)
print("Category Translation:", cateogary_translation.shape)
print("Geolocation:", geolocation.shape)


df = orders.merge(customers, on="customer_id", how="left")
payment_totals = order_payments.groupby("order_id")["payment_value"].sum().reset_index()
df = df.merge(payment_totals, on="order_id", how="left")
print(df.shape)

print(df['order_status'].value_counts())

df_delivered = df[df['order_status'] == 'delivered'].copy()
print(df_delivered.shape)
df_delivered['order_purchase_timestamp'] = pd.to_datetime(df_delivered['order_purchase_timestamp'])
# Set a reference date — typically the day after the last order in the dataset
reference_date = df_delivered['order_purchase_timestamp'].max() + pd.Timedelta(days=1)

rfm = df_delivered.groupby('customer_unique_id').agg(
    recency=('order_purchase_timestamp', lambda x: (reference_date - x.max()).days),
    frequency=('order_id', 'nunique'),
    monetary=('payment_value', 'sum')
).reset_index()

print(rfm.shape)
print(rfm.head())
print(rfm.describe())

# Define churn threshold — e.g., no purchase in last 180 days is "churned"
churn_threshold = 180

rfm['churned'] = rfm['recency'] > churn_threshold

print(rfm['churned'].value_counts())
print(rfm['churned'].value_counts(normalize=True) * 100)

rfm['CLV'] = rfm['frequency'] * rfm['monetary']

rfm['CLV'] = rfm['frequency'] * rfm['monetary']

print(rfm[['recency','frequency','monetary','churned','CLV']].describe())
print(rfm.sort_values('CLV', ascending=False).head(10))
rfm.to_csv("rfm_clv_churn.csv", index=False)
print("Saved successfully")

orders.to_csv("orders_clean.csv", index=False)
order_items.to_csv("order_items_clean.csv", index=False)
products.to_csv("products_clean.csv", index=False)
cateogary_translation.to_csv("cateogary_translation_clean.csv", index=False)
seller.to_csv("sellers_clean.csv", index=False)
order_payments.to_csv("order_payments_clean.csv", index=False)
order_reviews.to_csv("order_review_clean.csv", index=False)
customers.to_csv("customers_clean.csv", index=False)
geolocation.to_csv("geolocation_clean.csv", index=False)

#CORRELATION
correlation = rfm[['recency','frequency','monetary']].corr()
print(correlation.round(2))

correlation.to_csv('correlation.csv',index=True)


# REGRESSION

orders.columns = orders.columns.str.strip()

orders['order_purchase_timestamp'] = pd.to_datetime(
    orders['order_purchase_timestamp'], errors='coerce'
)

orders['order_delivered_customer_date'] = pd.to_datetime(
    orders['order_delivered_customer_date'], errors='coerce'
)

orders['delivery_days'] = (
    orders['order_delivered_customer_date'] -
    orders['order_purchase_timestamp']
).dt.days



                                                                         

print(orders[['delivery_days']].head())
data=orders.merge(order_reviews[['order_id','review_score']],
                  on='order_id',
                  how = 'inner'
                  )

data = data.dropna(subset=['delivery_days','review_score'])
data=data[data['delivery_days']>=0]

x=data['delivery_days']
y=data['review_score']

correlation=x.corr(y)


scatter_data = data[['delivery_days', 'review_score']].copy()

scatter_data.to_csv(
    'delivery_review_scatter.csv',
    index=False
)

print("Delivery and review data exported successfully!")

slope = correlation * (y.std()/x.std())
intercept = y.mean() -slope *x.mean()
predicted = intercept + slope * x
r_squared =1-((y-predicted)**2).sum()/((y-y.mean())**2).sum()
print("R-squared",r_squared)

regression_results = pd.DataFrame({
    'Metric':['Slope','Intercept','R_Squared'],
    'Value':[slope,intercept,r_squared]
})
regression_results.to_csv('regression_result.csv',index=False)

#HYPOTHESIS TESTING
print(orders.columns.tolist())
print(order_reviews.columns.tolist())

print("SLOPE:",slope)
print("INTERCEPT:",intercept)



print("All tables exported")

import pandas as pd

orders['order_delivered_customer_date'] = pd.to_datetime(
    orders['order_delivered_customer_date'], errors='coerce'
)

orders['order_estimated_delivery_date'] = pd.to_datetime(
    orders['order_estimated_delivery_date'], errors='coerce'
)

data = orders.merge(
    order_reviews[['order_id', 'review_score']],
    on='order_id',
    how='inner'
)

data = data.dropna(subset=[
    'order_delivered_customer_date',
    'order_estimated_delivery_date',
    'review_score'
])

data['late_delivery'] = (
    data['order_delivered_customer_date'] >
    data['order_estimated_delivery_date']
)

print(data[['late_delivery', 'review_score']].head())
print(data['late_delivery'].value_counts())
on_time = data[data['late_delivery'] == False]['review_score']
late = data[data['late_delivery'] == True]['review_score']

print("Average review score - On-time:", round(on_time.mean(), 2))
print("Average review score - Late:", round(late.mean(), 2))
print("Difference:", round(on_time.mean() - late.mean(), 2))


import math

# Null hypothesis (H0): Both groups have equal average scores
# Alternative hypothesis (H1): Late deliveries have lower scores

difference = on_time.mean() - late.mean()

standard_error = math.sqrt(
    on_time.var(ddof=1) / len(on_time) +
    late.var(ddof=1) / len(late)
)

z_score = difference / standard_error

# Approximate one-sided p-value
p_value = 0.5 * math.erfc(z_score / math.sqrt(2))

print("Difference in means:", round(difference, 4))
print("Z-score:", round(z_score, 4))
print("P-value:", p_value)

if p_value < 0.05:
    print("Result: Statistically significant")
    print("Reject the null hypothesis.")
else:
    print("Result: Not statistically significant")
    print("Fail to reject the null hypothesis.")

hypothesis_results = pd.DataFrame({
    'Metric':[
        'On-Time Average Score',
        'Late Average Score',
        'Score Difference',
        'Z Score',
        'P Value'
    ],
    'Value':[
        on_time.mean(),
        late.mean(),
        on_time.mean()-late.mean(),
        z_score,
        p_value
    ]
})
hypothesis_results.to_csv('hypothesis_result.csv',index=False)
print("Statistcal Results exported successfully!")