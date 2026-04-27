import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Retail Sales Performance Dashboard",
    page_icon="📊",
    layout="wide"
)


# ---------------------------------------------------------
# Load and prepare data
# ---------------------------------------------------------
@st.cache_data
def load_data():
    """Load and prepare the retail sales dataset."""
    df = pd.read_csv("data/retail_sales.csv")

    # Convert date columns
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])

    # Create useful time variables
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["Year"] = df["Order Date"].dt.year

    # Create profit margin variable
    df["Profit Margin"] = np.where(
        df["Sales"] != 0,
        df["Profit"] / df["Sales"],
        0
    )

    return df


df = load_data()


# ---------------------------------------------------------
# Dashboard title and introduction
# ---------------------------------------------------------
st.title("📊 Retail Sales Performance Dashboard")

st.markdown(
    """
    This interactive dashboard helps small business users explore retail sales performance.
    Users can filter the dataset by date range, region, product category, and customer segment.
    The dashboard shows key business indicators, sales trends, product performance, and regional profit differences.
    """
)


# ---------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------
st.sidebar.header("Dashboard Filters")

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

selected_date_range = st.sidebar.date_input(
    "Select Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Handle cases where the user selects only one date
if isinstance(selected_date_range, tuple) and len(selected_date_range) == 2:
    start_date = pd.to_datetime(selected_date_range[0])
    end_date = pd.to_datetime(selected_date_range[1])
else:
    start_date = pd.to_datetime(min_date)
    end_date = pd.to_datetime(max_date)

regions = sorted(df["Region"].dropna().unique())
categories = sorted(df["Category"].dropna().unique())
segments = sorted(df["Segment"].dropna().unique())

selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=regions,
    default=regions
)

selected_categories = st.sidebar.multiselect(
    "Select Product Category",
    options=categories,
    default=categories
)

selected_segments = st.sidebar.multiselect(
    "Select Customer Segment",
    options=segments,
    default=segments
)


# ---------------------------------------------------------
# Apply filters
# ---------------------------------------------------------
filtered_df = df[
    (df["Order Date"] >= start_date) &
    (df["Order Date"] <= end_date) &
    (df["Region"].isin(selected_regions)) &
    (df["Category"].isin(selected_categories)) &
    (df["Segment"].isin(selected_segments))
].copy()


if filtered_df.empty:
    st.warning("No data available for the selected filters. Please adjust the filter settings.")
    st.stop()


# ---------------------------------------------------------
# Key performance indicators
# ---------------------------------------------------------
st.subheader("Key Performance Indicators")

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_quantity = filtered_df["Quantity"].sum()
total_orders = filtered_df["Order ID"].nunique()
average_profit_margin = filtered_df["Profit Margin"].mean()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Quantity", f"{total_quantity:,.0f}")
col4.metric("Average Profit Margin", f"{average_profit_margin:.2%}")
col5.metric("Total Orders", f"{total_orders:,.0f}")


st.markdown("---")


# ---------------------------------------------------------
# Monthly sales trend
# ---------------------------------------------------------
st.subheader("Monthly Sales Trend")

monthly_sales = (
    filtered_df.groupby("Month")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Month")
)

monthly_sales["Month Date"] = pd.to_datetime(monthly_sales["Month"])

fig_monthly_sales = px.line(
    monthly_sales,
    x="Month Date",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

fig_monthly_sales.update_layout(
    xaxis_title="Month",
    yaxis_title="Sales",
    hovermode="x unified"
)

st.plotly_chart(fig_monthly_sales, use_container_width=True)

st.markdown(
    """
    **Insight:** This chart helps users identify how sales change over time.
    It can be used to observe stronger or weaker sales periods and possible seasonal patterns.
    """
)


# ---------------------------------------------------------
# Category and regional analysis
# ---------------------------------------------------------
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Sales by Product Category")

    category_summary = (
        filtered_df.groupby("Category")[["Sales", "Profit"]]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    fig_category_sales = px.bar(
        category_summary,
        x="Category",
        y="Sales",
        title="Sales by Product Category",
        text_auto=".2s"
    )

    fig_category_sales.update_layout(
        xaxis_title="Product Category",
        yaxis_title="Sales"
    )

    st.plotly_chart(fig_category_sales, use_container_width=True)

    st.markdown(
        """
        **Insight:** This chart compares sales across product categories.
        It helps users identify which categories contribute most to total revenue.
        """
    )


with right_col:
    st.subheader("Profit by Region")

    region_summary = (
        filtered_df.groupby("Region")[["Sales", "Profit"]]
        .sum()
        .reset_index()
        .sort_values("Profit", ascending=False)
    )

    fig_region_profit = px.bar(
        region_summary,
        x="Region",
        y="Profit",
        title="Profit by Region",
        text_auto=".2s"
    )

    fig_region_profit.update_layout(
        xaxis_title="Region",
        yaxis_title="Profit"
    )

    st.plotly_chart(fig_region_profit, use_container_width=True)

    st.markdown(
        """
        **Insight:** This chart compares profitability across regions.
        It helps users understand whether some regions perform better than others.
        """
    )


# ---------------------------------------------------------
# Top sub-category analysis
# ---------------------------------------------------------
st.markdown("---")
st.subheader("Top 10 Sub-Categories by Sales")

top_subcategories = (
    filtered_df.groupby("Sub-Category")[["Sales", "Profit"]]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)
    .head(10)
)

fig_top_subcategories = px.bar(
    top_subcategories,
    x="Sub-Category",
    y="Sales",
    color="Profit",
    title="Top 10 Sub-Categories by Sales",
    text_auto=".2s"
)

fig_top_subcategories.update_layout(
    xaxis_title="Sub-Category",
    yaxis_title="Sales"
)

st.plotly_chart(fig_top_subcategories, use_container_width=True)

st.markdown(
    """
    **Insight:** This chart identifies the sub-categories with the highest sales.
    The colour also shows profit differences, which helps users see whether high-sales sub-categories are also profitable.
    """
)


# ---------------------------------------------------------
# Summary tables
# ---------------------------------------------------------
st.markdown("---")
st.subheader("Summary Tables")

tab1, tab2, tab3 = st.tabs(["Category Summary", "Region Summary", "Filtered Data"])

with tab1:
    st.dataframe(
        category_summary.style.format({
            "Sales": "${:,.2f}",
            "Profit": "${:,.2f}"
        }),
        use_container_width=True
    )

with tab2:
    st.dataframe(
        region_summary.style.format({
            "Sales": "${:,.2f}",
            "Profit": "${:,.2f}"
        }),
        use_container_width=True
    )

with tab3:
    st.dataframe(filtered_df, use_container_width=True)


# ---------------------------------------------------------
# Automatically generated key findings
# ---------------------------------------------------------
st.markdown("---")
st.subheader("Automatically Generated Key Findings")

best_month = monthly_sales.sort_values("Sales", ascending=False).iloc[0]
best_category_sales = category_summary.sort_values("Sales", ascending=False).iloc[0]
best_category_profit = category_summary.sort_values("Profit", ascending=False).iloc[0]
best_region_profit = region_summary.sort_values("Profit", ascending=False).iloc[0]
top_subcategory_sales = top_subcategories.sort_values("Sales", ascending=False).iloc[0]

st.markdown(
    f"""
    Based on the current filters:

    - The highest sales month is **{best_month['Month']}**, with total sales of **${best_month['Sales']:,.2f}**.
    - The top product category by sales is **{best_category_sales['Category']}**, with sales of **${best_category_sales['Sales']:,.2f}**.
    - The top product category by profit is **{best_category_profit['Category']}**, with profit of **${best_category_profit['Profit']:,.2f}**.
    - The most profitable region is **{best_region_profit['Region']}**, with profit of **${best_region_profit['Profit']:,.2f}**.
    - The top sub-category by sales is **{top_subcategory_sales['Sub-Category']}**, with sales of **${top_subcategory_sales['Sales']:,.2f}**.
    """
)


# ---------------------------------------------------------
# Limitations
# ---------------------------------------------------------
st.markdown("---")
st.subheader("Limitations")

st.markdown(
    """
    This dashboard is designed for educational and exploratory analysis.
    The dataset appears to be a sample retail dataset rather than real-time company data.
    The analysis is mainly descriptive and does not include advanced forecasting or causal modelling.
    External factors such as marketing campaigns, economic conditions, competitor behaviour, and holiday effects are not included in the dataset.
    """
)


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.caption(
    "ACC102 Mini Assignment | Track 4: Interactive Data Analysis Tool | Built with Python, pandas, Plotly, and Streamlit"
)