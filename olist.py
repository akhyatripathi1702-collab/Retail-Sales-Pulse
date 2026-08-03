
from sqlalchemy import create_engine
import pandas as pd
engine = create_engine("mysql+pymysql://root:Akh#17rysh@localhost:3306/olist_db")


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


print("All tables exported")