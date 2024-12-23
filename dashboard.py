import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_top_product_df(df):
    top_product_df = df.groupby(by="product_category_name_english").order_id.nunique().sort_values(ascending=False).reset_index()
    top_product_df.rename(columns={
        "order_id": "order_count"
    }, inplace=True)
    
    return top_product_df

def create_hourly_orders_df(df):
    hourly_orders_df = df.groupby(by="order_hour").order_id.nunique().reset_index()
    hourly_orders_df.rename(columns={
        "order_id": "order_count"
    }, inplace=True)
    
    return hourly_orders_df

# Load cleaned data
merged_df = pd.read_csv("https://raw.githubusercontent.com/eko31rj/proyek_analisis_data_dicoding_eko31rj/refs/heads/main/cleaned_data/merged_data_cleaned.csv")

# Convert to datetime
datetime_columns = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
merged_df.sort_values(by="order_purchase_timestamp", inplace=True)
merged_df.reset_index(inplace=True)
 
for column in datetime_columns:
    merged_df[column] = pd.to_datetime(merged_df[column])

min_date = merged_df["order_purchase_timestamp"].min()
max_date = merged_df["order_purchase_timestamp"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data
main_df = merged_df[(merged_df["order_purchase_timestamp"] >= str(start_date)) & 
                (merged_df["order_purchase_timestamp"] <= str(end_date))]

# Menyiapkan berbagai dataframe
top_product_df = create_top_product_df(main_df)
hourly_orders_df = create_hourly_orders_df(main_df)

# Header
st.header('E-Commerce Dashboard :sparkles:')

# Top_Products
st.subheader('Top Products')
fig, ax = plt.subplots(figsize=(35, 15))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
        x="order_count", 
        y="product_category_name_english",
        data=top_product_df.head(10),
        palette=colors,
        ax=ax
    )
ax.set_title("Top Products", loc="center", fontsize=50)
ax.set_ylabel('Kategori Produk', fontsize=12)
ax.set_xlabel('Jumlah Order', fontsize=12)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

# Hourly order
st.subheader('Hourly Order')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    hourly_orders_df["order_hour"],
    hourly_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.caption('Copyright (c) eko31rj 2024')



