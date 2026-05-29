import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config------------------------------------------------------------------

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load Data------------------------------------------------------------------

df = pd.read_csv("../data/processed/processed_superstore.csv")

# Header------------------------------------------------------------------

st.title("Sales Dashboard")

st.markdown("""
Analyze sales performance, profitability, regional trends,
and product performance using interactive filters.
""")

# Sidebar Filters------------------------------------------------------------------

st.sidebar.header("Filters")

region = st.sidebar.selectbox(
    "Region",
    ["All"] + sorted(df["region"].unique().tolist())
)

category = st.sidebar.selectbox(
    "Category",
    ["All"] + sorted(df["category"].unique().tolist())
)

# Apply Filters------------------------------------------------------------------

filtered_df = df.copy()

if region != "All":
    filtered_df = filtered_df[
        filtered_df["region"] == region
    ]

if category != "All":
    filtered_df = filtered_df[
        filtered_df["category"] == category
    ]

# KPI Calculations------------------------------------------------------------------

total_sales = filtered_df["sales"].sum()
total_profit = filtered_df["profit"].sum()
total_orders = filtered_df["order_id"].nunique()
profit_margin = (total_profit / total_sales) * 100

# KPI Cards------------------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Orders", f"{total_orders:,}")
col4.metric("Profit Margin", f"{profit_margin:.2f}%")

st.divider()

# Sales Trend------------------------------------------------------------------

sales_trend = (
    filtered_df
    .groupby("month_year", as_index=False)["sales"]
    .sum()
)

fig_sales_trend = px.line(
    sales_trend,
    x="month_year",
    y="sales",
    title="Sales Trend"
)

st.plotly_chart(
    fig_sales_trend,
    use_container_width=True
)

# Region & Category Charts------------------------------------------------------------------

region_sales = (
    filtered_df
    .groupby("region", as_index=False)["sales"]
    .sum()
    .sort_values("sales", ascending=False)
)

category_sales = (
    filtered_df
    .groupby("category", as_index=False)["sales"]
    .sum()
    .sort_values("sales", ascending=False)
)

col1, col2 = st.columns(2)

with col1:
    fig_region = px.bar(
        region_sales,
        x="region",
        y="sales",
        title="Regional Sales"
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True
    )

with col2:
    fig_category = px.bar(
        category_sales,
        x="category",
        y="sales",
        title="Category Sales"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

# Top Products------------------------------------------------------------------

top_products = (
    filtered_df
    .groupby("product_name", as_index=False)["sales"]
    .sum()
    .sort_values("sales", ascending=False)
    .head(10)
)

fig_products = px.bar(
    top_products.sort_values("sales"),
    x="sales",
    y="product_name",
    orientation="h",
    title="Top 10 Products by Sales"
)

st.plotly_chart(
    fig_products,
    use_container_width=True
)

# Correlation Heatmap------------------------------------------------------------------

st.subheader("Correlation Heatmap")

corr_cols = ["sales", "profit", "quantity", "discount"]

corr_matrix = filtered_df[corr_cols].corr()

fig_heatmap = px.imshow(
    corr_matrix,
    text_auto=".2f",
    aspect="auto",
    title="Correlation Matrix"
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True
)

# Raw Data------------------------------------------------------------------

with st.expander("View Data"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )