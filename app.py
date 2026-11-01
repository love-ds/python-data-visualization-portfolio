import streamlit as st
import pandas as pd
import numpy as np


@st.cache_data
def load_csv(file):
    return pd.read_csv(file)


uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)


# ============================================================
# DATA LOADING
# ============================================================

if uploaded_file is not None:

    # Load uploaded CSV
    df = load_csv(uploaded_file)

    # Required columns
    required_columns = [
        "Category",
        "Region",
        "Segment",
        "Product",
        "Sales",
        "Profit",
        "Order_Date",
        "Shipping_Mode",
        "Payment_Method",
        "Quantity",
        "Discount"
    ]

    # Find missing columns
    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    # Stop if required columns are missing
    if missing_columns:
        st.error(
            "Uploaded file is missing required columns: "
            + ", ".join(missing_columns)
        )
        st.stop()


else:

    # ========================================================
    # SYNTHETIC DATA
    # ========================================================

    np.random.seed(42)
    n = 5000

    df = pd.DataFrame({
        "Order_ID": [
            f"ORD-{i:05d}" for i in range(1, n + 1)
        ],

        "Order_Date": pd.date_range(
            "2023-01-01",
            periods=n,
            freq="6h"
        ),

        "Customer": np.random.choice(
            [
                "Aarav", "Vivaan", "Aditya", "Arjun", "Rohan",
                "Ananya", "Diya", "Ishita", "Meera", "Aanya"
            ],
            n
        ),

        "Segment": np.random.choice(
            ["Consumer", "Corporate", "Home Office"],
            n
        ),

        "Region": np.random.choice(
            ["North", "South", "East", "West"],
            n
        ),

        "State": np.random.choice(
            [
                "Delhi", "Maharashtra", "Karnataka",
                "Tamil Nadu", "Gujarat", "Rajasthan",
                "Haryana", "West Bengal"
            ],
            n
        ),

        "Category": np.random.choice(
            ["Technology", "Furniture", "Office Supplies"],
            n
        ),

        "Product": np.random.choice(
            [
                "Laptop", "Phone", "Monitor", "Chair", "Table",
                "Binder", "Paper", "Storage", "Keyboard", "Mouse"
            ],
            n
        ),

        "Quantity": np.random.randint(1, 10, n),

        "Sales": np.random.uniform(
            500, 100000, n
        ).round(2),

        "Discount": np.random.choice(
            [0, 0.05, 0.10, 0.15, 0.20, 0.30],
            n
        ),

        "Shipping_Mode": np.random.choice(
            [
                "Standard",
                "Second Class",
                "First Class",
                "Same Day"
            ],
            n
        ),

        "Payment_Method": np.random.choice(
            [
                "UPI",
                "Credit Card",
                "Debit Card",
                "Net Banking",
                "Cash"
            ],
            n
        )
    })

    df["Profit"] = (
        df["Sales"] * np.random.uniform(0.05, 0.25, n)
        - df["Sales"] * df["Discount"] * 0.5
    ).round(2)


# ============================================================
# DATA VALIDATION & DATE FEATURES
# ============================================================

try:

    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"]
    )

    df["Sales"] = pd.to_numeric(
        df["Sales"]
    )

    df["Profit"] = pd.to_numeric(
        df["Profit"]
    )

    df["Quantity"] = pd.to_numeric(
        df["Quantity"]
    )

    df["Discount"] = pd.to_numeric(
        df["Discount"]
    )

except (ValueError, TypeError):

    st.error(
        "Invalid data format. "
        "Order_Date must contain valid dates, "
        "and Sales, Profit, Quantity and Discount "
        "must contain numbers."
    )

    st.stop()


# Create date-related columns

df["Year"] = df["Order_Date"].dt.year

df["Quarter"] = df["Order_Date"].dt.quarter

df["Month"] = df["Order_Date"].dt.month

df["Year-Month"] = (
    df["Order_Date"]
    .dt.to_period("M")
    .astype(str)
)

df["Month_Name"] = (
    df["Order_Date"].dt.month_name()
)

df["Day_Name"] = (
    df["Order_Date"].dt.day_name()
)


# Create Profit Margin

df["Profit_Margin"] = (
    df["Profit"] / df["Sales"] * 100
).round(2)



# =======================================================================================================================================================================
# =======================================================================================================================================================================
# =======================================================================================================================================================================

st.title("Sales Dashboard")

if "selected_product" not in st.session_state:
    st.session_state.selected_product = None

def product_changed(message):
    st.session_state.product_message = message

if "product_message" not in st.session_state:
    st.session_state.product_message = ""

# ------------------------------------------------------------------------------------------------------------------------------------
#                                            Form for filtering the data
# ------------------------------------------------------------------------------------------------------------------------------------

with st.sidebar.form("filter_form"):

    category = st.multiselect(
        "Select Category(s)",
        df["Category"].unique(),
        placeholder="All Categories"
    )

    region = st.multiselect(
        "Select Region(s)",
        df["Region"].unique()
    )

    segment = st.multiselect(
        "Select Segment(s)",
        df["Segment"].unique()
    )

    shipping = st.multiselect(
        "Select Shipping Mode(s)",
        df["Shipping_Mode"].unique()
    )

    payment = st.multiselect(
        "Select Payment Method(s)",
        df["Payment_Method"].unique(),
        placeholder="All Payment Methods"
    )

    min_sales = st.slider(
        "Minimum Sales",
        min_value=0,
        max_value=int(df["Sales"].max()),
        value=0,
        step=1000
    )

    date_range = st.date_input(
        "Select Date Range",
        value=(
            df["Order_Date"].min().date(),
            df["Order_Date"].max().date()
        )
    )

    product = st.multiselect(
        "Select Products",
        df["Product"].unique(),
        placeholder="All Products"
    )

    apply_filters = st.form_submit_button(
        "Apply Filters"
    )

    if apply_filters:
        st.sidebar.success("Filters applied successfully!")



# Start filtering from the original dataframe
filtered_df = df.copy()

# Category
if category:
    filtered_df = filtered_df[
        filtered_df["Category"].isin(category)
    ]

# Region
if region:
    filtered_df = filtered_df[
        filtered_df["Region"].isin(region)
    ]

# Segment
if segment:
    filtered_df = filtered_df[
        filtered_df["Segment"].isin(segment)
    ]

# Shipping Mode
if shipping:
    filtered_df = filtered_df[
        filtered_df["Shipping_Mode"].isin(shipping)
    ]

# Payment Method
if payment:
    filtered_df = filtered_df[
        filtered_df["Payment_Method"].isin(payment)
    ]

# Product
if product:
    filtered_df = filtered_df[
        filtered_df["Product"].isin(product)
    ]

# Minimum Sales
filtered_df = filtered_df[
    filtered_df["Sales"] >= min_sales
]

# Date Range
if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df["Order_Date"].dt.date >= start_date) &
        (filtered_df["Order_Date"].dt.date <= end_date)
    ]


# ---------------------------------------------------------------------------------------------
if filtered_df.empty:
    st.warning("No data found for the selected filters.")
    st.stop()


csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Filtered Data",
    data=csv_data,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)
# ---------------------------------------------------------------------------------------------

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = len(filtered_df)
profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0
    else 0
)

with st.container(border=True):

    st.subheader("Key Performance Indicators (KPIs)")

    col1,col2 = st.columns(2)
    col3,col4 = st.columns(2)

    col1.metric("Total Sales",f"₹{total_sales:,.0f}")
    col2.metric("Total Profit",f"₹{total_profit:,.0f}")
    col3.metric("Total Orders",f"{total_orders}")
    col4.metric("Profit Margin",f"{profit_margin:.2f}%")
# ----------------------------------------------------------------------------------------------

import plotly.express as px

tab1, tab2 = st.tabs([
    "📊 Overview",
    "💰 Profit Analysis"
])

# ============================================================
# TAB 1 — OVERVIEW
# ============================================================

with tab1:

    st.subheader("Sales Analysis")

    chart_type = st.selectbox(
        "Choose Analysis",
        [
            "Sales by Product",
            "Sales by Region",
            "Sales by Segment"
        ]
    )

    if chart_type == "Sales by Product":

        product_sales = (
            filtered_df
            .groupby("Product", as_index=False)
            .agg(
                Sales=("Sales", "sum"),
                Profit=("Profit", "sum"),
                Quantity=("Quantity", "sum")
            )
            .sort_values("Sales", ascending=False)
        )


        fig_dynamic = px.bar(
            product_sales,
            x="Product",
            y="Sales",
            color="Product",
            title="Sales by Product",
            hover_data={
                "Sales": ":,.2f",
                "Profit": ":,.2f",
                "Quantity": True
            }
        )

        

    elif chart_type == "Sales by Region":

        region_sales = (
            filtered_df
            .groupby("Region")["Sales"]
            .sum()
            .reset_index()
            .sort_values("Sales", ascending=False)
        )

        fig_dynamic = px.bar(
            region_sales,
            x="Region",
            y="Sales",
            color="Region",
            title="Sales by Region"
        )

    elif chart_type == "Sales by Segment":

        segment_sales = (
            filtered_df
            .groupby("Segment")["Sales"]
            .sum()
            .reset_index()
            .sort_values("Sales", ascending=False)
        )

        fig_dynamic = px.bar(
            segment_sales,
            x="Segment",
            y="Sales",
            color="Segment",
            title="Sales by Segment"
        )

    fig_dynamic.update_layout(
        showlegend=False,
        xaxis_title="",
        yaxis_title="Sales"
    )

    plot_event = st.plotly_chart(
        fig_dynamic,
        use_container_width=True,
        on_select="rerun"
    )

    selected_df = filtered_df.copy()

    selected_value = None


    st.write(
        "Remembered Product:",
        st.session_state.selected_product
    )

    def clear_selection():
        st.session_state.selected_product = None


    st.button(
        "Clear Selection",
        on_click=clear_selection
    )



    if plot_event.selection.points:

        selected_point = plot_event.selection.points[0]

        if chart_type == "Sales by Product":
            st.session_state.selected_product = selected_point["x"]

        elif chart_type == "Sales by Region":
            selected_value = selected_point["x"]

        elif chart_type == "Sales by Segment":
            selected_value = selected_point["x"]


    # Get the remembered product from Session State
    if chart_type == "Sales by Product":
        selected_value = st.session_state.selected_product


    if selected_value:

        st.subheader(f"Details for {selected_value}")

        if chart_type == "Sales by Product":
            selected_df = filtered_df[
                filtered_df["Product"] == selected_value
            ]

        elif chart_type == "Sales by Region":
            selected_df = filtered_df[
                filtered_df["Region"] == selected_value
            ]

        elif chart_type == "Sales by Segment":
            selected_df = filtered_df[
                filtered_df["Segment"] == selected_value
            ]

        selected_sales = selected_df["Sales"].sum()
        selected_profit = selected_df["Profit"].sum()
        selected_orders = len(selected_df)

        selected_margin = (
            selected_profit / selected_sales * 100
            if selected_sales != 0
            else 0
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Sales", f"₹{selected_sales:,.0f}")
        col2.metric("Profit", f"₹{selected_profit:,.0f}")
        col3.metric("Orders", f"{selected_orders:,}")
        col4.metric("Profit Margin", f"{selected_margin:.2f}%")


    # ---------------------------------------------------------------------------------------------

    ##############################
    ##############################

    # ---------------------------------------------------------------------------------------------

    if selected_value:

        monthly_df = selected_df.copy()

    else:

        monthly_df = filtered_df.copy()


    monthly_sales = (
        monthly_df
        .groupby(["Year", "Month", "Month_Name"])["Sales"]
        .sum()
        .reset_index()
    )

    monthly_sales["Month_Year"] = (
        monthly_sales["Month_Name"] + " " +
        monthly_sales["Year"].astype(str)
    )

    monthly_sales["Date"] = pd.to_datetime(
        monthly_sales["Year"].astype(str)
        + "-"
        + monthly_sales["Month"].astype(str)
        + "-01"
    )

    monthly_sales = monthly_sales.sort_values("Date")




    fig3 = px.line(
        monthly_sales,
        x="Date",
        y="Sales",
        markers=True,
        title="Sales Trend Over Time"
    )

    fig3.update_layout(
        xaxis_title="Month-Year",
        yaxis_title="Sales",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )


# ============================================================
# TAB 2 — PROFIT ANALYSIS
# ============================================================

with tab2:

    st.subheader("Profit Performance")

    profit_kpi1, profit_kpi2 = st.columns(2)
    profit_kpi3, profit_kpi4 = st.columns(2)

    avg_profit = filtered_df["Profit"].mean()
    profitable_orders = (filtered_df["Profit"] > 0).sum()

    profit_kpi1.metric(
        "Total Profit",
        f"₹{total_profit:,.0f}"
    )

    profit_kpi2.metric(
        "Profit Margin",
        f"{profit_margin:.2f}%"
    )

    profit_kpi3.metric(
        "Avg Profit / Order",
        f"₹{avg_profit:,.0f}"
    )

    profit_kpi4.metric(
        "Profitable Orders",
        f"{profitable_orders:,}"
    )


    product_profit = (
        filtered_df
        .groupby("Product", as_index=False)["Profit"]
        .sum()
        .sort_values("Profit", ascending=False)
    )

# ----------------------------------------------------------------------------


    fig_profit_product = px.bar(
        product_profit,
        x="Product",
        y="Profit",
        title="Total Profit by Product",
        template="plotly_white"
    )

    fig_profit_product.update_layout(
        title_x=0.5,
        xaxis_title="Product",
        yaxis_title="Profit"
    )

    profit_event = st.plotly_chart(
        fig_profit_product,
        use_container_width=True,
        key="profit_by_product_chart",
        on_select="rerun"
    )

    if "selected_profit_product" not in st.session_state:
        st.session_state.selected_profit_product = None


    if profit_event.selection.points:
        st.session_state.selected_profit_product = (
            profit_event.selection.points[0]["x"]
        )

    selected_profit_product = (
        st.session_state.selected_profit_product
    )

    if selected_profit_product:

        selected_product_df = filtered_df[
            filtered_df["Product"] == selected_profit_product
        ]

        selected_profit = selected_product_df["Profit"].sum()
        selected_sales = selected_product_df["Sales"].sum()

        selected_profit_margin = (
            selected_profit / selected_sales * 100
            if selected_sales != 0
            else 0
        )

        st.subheader(
            f"Profit Details — {selected_profit_product}"
        )

        detail_col1, detail_col2, detail_col3 = st.columns(3)

        detail_col1.metric(
            "Total Profit",
            f"₹{selected_profit:,.0f}"
        )

        detail_col2.metric(
            "Average Profit",
            f"₹{selected_product_df['Profit'].mean():,.0f}"
        )

        detail_col3.metric(
            "Profit Margin",
            f"{selected_profit_margin:.2f}%"
        )

        if st.button("Clear Product Selection"):
            st.session_state.selected_profit_product = None
            st.rerun()
# ----------------------------------------------------------------------------


    if selected_profit_product:
        monthly_profit_df = filtered_df[
            filtered_df["Product"] == selected_profit_product
        ]
    else:
        monthly_profit_df = filtered_df

    monthly_profit = (
        monthly_profit_df
        .groupby("Year-Month", as_index=False)["Profit"]
        .sum()
        .sort_values("Year-Month")
    )

    fig_monthly_profit = px.line(
        monthly_profit,
        x="Year-Month",
        y="Profit",
        markers=True,
        title="Monthly Profit Trend",
        template="plotly_white"
    )

    fig_monthly_profit.update_layout(
        title_x=0.5,
        xaxis_title="Month",
        yaxis_title="Profit"
    )

    st.plotly_chart(
        fig_monthly_profit,
        use_container_width=True
    )



    fig_sales_vs_profit = px.scatter(
        filtered_df,
        x="Profit",
        y="Sales",
        color="Product",
        size="Quantity",
        hover_data=[
            "Product",
            "Quantity",
            "Discount",
            "Profit_Margin"
        ],
        title="Sales vs Profit by Product"
    )

    fig_sales_vs_profit.update_layout(
        title_x=0.5,
        xaxis_title="Profit",
        yaxis_title="Sales"
    )

    st.plotly_chart(
        fig_sales_vs_profit,
        use_container_width=True
    )

    # ------------------------------------------------------------
    # Profitability by Region and Segment
    # ------------------------------------------------------------

    region_profit = (
        filtered_df
        .groupby("Region", as_index=False)["Profit"]
        .sum()
        .sort_values("Profit", ascending=False)
    )

    segment_profit = (
        filtered_df
        .groupby("Segment", as_index=False)["Profit"]
        .sum()
        .sort_values("Profit", ascending=False)
    )

    col1, col2 = st.columns(2)

    with col1:

        fig_region_profit = px.bar(
            region_profit,
            x="Region",
            y="Profit",
            title="Profit by Region",
            template="plotly_white"
        )

        fig_region_profit.update_layout(
            title_x=0.5,
            xaxis_title="Region",
            yaxis_title="Profit"
        )

        st.plotly_chart(
            fig_region_profit,
            use_container_width=True,
            key="profit_by_region"
        )

    with col2:

        fig_segment_profit = px.bar(
            segment_profit,
            x="Segment",
            y="Profit",
            title="Profit by Segment",
            template="plotly_white"
        )

        fig_segment_profit.update_layout(
            title_x=0.5,
            xaxis_title="Segment",
            yaxis_title="Profit"
        )

        st.plotly_chart(
            fig_segment_profit,
            use_container_width=True,
            key="profit_by_segment"
        )

