import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="E-commerce Sales Analytics", layout="wide")

# Load cleaned data
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_orders.csv")
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df

try:
    df = load_data()
except Exception:
    # Fallback if cleaned_orders.csv is missing
    path = "/content/sample_data/ecommerce_sales_analytics_5000.csv"
    df = pd.read_csv(path)
    df["order_date"] = pd.to_datetime(df["order_date"])

# Sidebar Filters
st.sidebar.header("Dashboard Filters")
categories = ["All"] + sorted(df["product_category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Select Product Category", categories)

regions = ["All"] + sorted(df["region"].dropna().unique().tolist())
selected_region = st.sidebar.multiselect("Select Region(s)", regions, default=["All"])

# Filter DataFrame
filtered_df = df.copy()
if selected_category != "All":
    filtered_df = filtered_df[filtered_df["product_category"] == selected_category]

if "All" not in selected_region and len(selected_region) > 0:
    filtered_df = filtered_df[filtered_df["region"].isin(selected_region)]

# App Title
st.title("🛍️ E-commerce Sales Analytics Dashboard")

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    total_revenue = filtered_df["revenue"].sum()
    st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
with col2:
    total_orders = len(filtered_df)
    st.metric(label="Total Orders", value=f"{total_orders:,}")
with col3:
    avg_rating = filtered_df["customer_rating"].mean()
    st.metric(label="Average Rating", value=f"{avg_rating:.2f} ⭐")
with col4:
    avg_delivery = filtered_df["delivery_days"].mean()
    st.metric(label="Avg Delivery Days", value=f"{avg_delivery:.1f} Days")

st.markdown("--- ")

# Charts Section
st.subheader("Visualizing Key Trends")

# Layout columns for charts
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.write("### 1. Distribution of Order Revenue")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(filtered_df["revenue"], bins=30, kde=True, ax=ax, color="skyblue")
    ax.set_title("Distribution of Order Revenue")
    ax.set_xlabel("Revenue")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

with chart_col2:
    st.write("### 2. Number of Orders by Category")
    fig, ax = plt.subplots(figsize=(8, 5))
    cat_counts = filtered_df["product_category"].value_counts()
    sns.barplot(x=cat_counts.index, y=cat_counts.values, hue=cat_counts.index, palette="viridis", legend=False, ax=ax)
    ax.set_title("Orders per Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Number of Orders")
    st.pyplot(fig)

# Chart 3: Scatter Plot
st.write("### 3. Relationship: Unit Price vs Revenue")
fig, ax = plt.subplots(figsize=(12, 6))
sns.scatterplot(
    data=filtered_df,
    x="unit_price",
    y="revenue",
    hue="product_category",
    alpha=0.7,
    ax=ax
)
ax.set_title("Unit Price vs Revenue by Product Category")
ax.set_xlabel("Unit Price")
ax.set_ylabel("Revenue")
st.pyplot(fig)

# Run instructions
# We will use localtunnel to deploy on colab
import urllib
print("External IP address to use as password for Localtunnel:")
print(urllib.request.urlopen('https://ipv4.icanhazip.com').read().decode('utf8').strip())
