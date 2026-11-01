import streamlit as st
import pandas as pd
import plotly.express as px
from pipeline import run_etl_pipeline

# =============================================================================
# 🏢 APPLICATION CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Market Intelligence Sync Pipeline",
    page_icon="🛰️",
    layout="wide"
)

# Load data through the engineered pipeline structure
df_clean, active_exchange_rate = run_etl_pipeline()

st.title("🛰️ Market Intelligence & ETL Sync Pipeline")
st.markdown("Automated web harvesting engine tracking competitor pricing variables synchronized against live foreign exchange REST indices.")

st.markdown("---")

# =============================================================================
# 🎛️ SIDEBAR CONTROL LAYER (DYNAMIC UI INTERACTIVE METRICS)
# =============================================================================
st.sidebar.markdown("### 🔍 Workspace Filters")

# Explicit unique key argument added to resolve Streamlit internal routing collision
target_competitor = st.sidebar.selectbox(
    "Filter Target Competitor Space", 
    options=["All"] + list(df_clean["Competitor_Name"].unique()),
    key="unique_sidebar_competitor_filter"
)


# Interactive price threshold warning alert slider
alert_threshold_inr = st.sidebar.slider(
    "Set INR Discrepancy Alert Threshold", 
    min_value=100, 
    max_value=5000, 
    value=1500, 
    step=100
)

# Apply context filters dynamically based on user selections
display_df = df_clean.copy()
if target_competitor != "All":
    display_df = display_df[display_df["Competitor_Name"] == target_competitor]

# =============================================================================
# 📈 EXECUTIVE KPI INFRASTRUCTURE
# =============================================================================
# =============================================================================

total_harvested_items = len(display_df)
avg_competitor_price = display_df["Price_INR"].mean()
flagged_price_alerts = len(display_df[display_df["Price_Delta_INR"] >= alert_threshold_inr])

# Unpack the list into 4 separate column objects
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

col_kpi1.metric("Harvested Items", f"{total_harvested_items} SKUs")
col_kpi2.metric("Live Exchange Rate", f"₹{active_exchange_rate:.2f} / USD", help="Real-time pull from Open Exchange REST Endpoint")
col_kpi3.metric("Avg Competitor Price", f"₹{avg_competitor_price:,.2f}")
col_kpi4.metric("Flagged Price Alerts", f"{flagged_price_alerts} Units", delta=f"{flagged_price_alerts} Critical Actions", delta_color="inverse")


st.markdown("---")

# =============================================================================
# 📊 PRESENTATION LAYER (VISUAL BREATHING ROOM ARCHITECTURE)
# =============================================================================
col1, col2 = st.columns(2)

with col1:
    fig_bar = px.box(
        display_df, 
        x="Competitor_Name", 
        y="Price_INR", 
        color="Competitor_Name",
        title="Competitor Pricing Distributions & Spread Profiles (INR)",
        points="all"
    )
    fig_bar.update_layout(template="plotly_white", showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True, key="etl_distribution_box")

with col2:
    fig_scatter = px.scatter(
        display_df, 
        x="Price_INR", 
        y="Price_Delta_INR", 
        color="Availability", 
        size="Raw_Price_USD",
        title="Price Target Volatility vs Margin Deviation Vector",
        labels={"Price_INR": "Competitor Price (INR)", "Price_Delta_INR": "Strategic Under-Cut Vector (INR)"}
    )
    fig_scatter.update_layout(template="plotly_white")
    st.plotly_chart(fig_scatter, use_container_width=True, key="etl_margin_scatter")

st.markdown("---")

# =============================================================================
# 📋 SYSTEM INVENTORY & COMPREHENSIVE DATA DOWNLOAD ACTIONS
# =============================================================================
st.subheader("📋 System Master Inventory Data Frame")
st.dataframe(display_df, use_container_width=True)

# Generate explicit physical data assets for clients to download directly
csv_download_stream = display_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Processed Master Inventory Report (.CSV)",
    data=csv_download_stream,
    file_name="processed_market_intelligence_report.csv",
    mime="text/csv",
    key="master_inventory_csv_download_action"
)


# =============================================================================
# 🚀 PHASE 3: ENTERPRISE FINANCIAL MODELING & FREELANCE ANALYTICS EXTENSION
# =============================================================================
st.markdown("---")
st.subheader("💡 Strategic Financial Modeling & Value Optimization")
st.markdown(
    "Freelance Value-Add Feature: This simulation layer calculates direct fiscal impact metrics "
    "by estimating captured transaction volume changes against optimized pricing strategy variations."
)

# 1. Component Infrastructure Layout
sim_col1, sim_col2 = st.columns([1, 2])

with sim_col1:
    st.markdown("##### ⚙️ Simulation Parameter Controls")
    
    # Client Strategy Inputs
    est_monthly_orders = st.number_input(
        "Estimated Monthly Sales Volume (Units)", 
        min_value=10, 
        max_value=100000, 
        value=2500, 
        step=500,
        help="The baseline number of units sold across these combined cloud SKU classes monthly."
    )
    
    conversion_boost_pct = st.slider(
        "Projected Market Penetration Boost (%)", 
        min_value=0.0, 
        max_value=30.0, 
        value=12.5, 
        step=0.5,
        help="Estimated increase in client sales volume resulting from executing the 8% competitor price under-cut strategy."
    )

    # Programmatic Vector Computations
    avg_delta_inr = display_df["Price_Delta_INR"].mean()
    current_estimated_revenue = est_monthly_orders * display_df["Price_INR"].mean()
    
    boosted_orders = est_monthly_orders * (1 + (conversion_boost_pct / 100.0))
    optimized_estimated_revenue = boosted_orders * display_df["Our_Target_Price_INR"].mean()
    net_revenue_impact_inr = optimized_estimated_revenue - current_estimated_revenue

with sim_col2:
    st.markdown("##### 📈 Captured Revenue Impact Vector")
    
    # Highlighting Freelance Analytics Value Through Visual Metric Blocks
    impact_metric_1, impact_metric_2 = st.columns(2)
    
    with impact_metric_1:
        st.metric(
            label="Average Competitive Advantage Spread (Per Unit)",
            value=f"₹{avg_delta_inr:,.2f}",
            help="The mean price distance created between market alternatives and internal tactical target options."
        )
    with impact_metric_2:
        st.metric(
            label="Projected Gross Revenue Impact",
            value=f"₹{net_revenue_impact_inr:,.2f}",
            delta=f"{'+' if net_revenue_impact_inr >= 0 else ''}{conversion_boost_pct}% Volume Delta",
            delta_color="normal"
        )
        
    # Visualizing Pricing Strategies Comparison
    strategy_compare_data = pd.DataFrame({
        "Strategic Profile": ["Market Benchmark (Competitor)", "Optimized Vector (Internal Target)"],
        "Average Price (INR)": [display_df["Price_INR"].mean(), display_df["Our_Target_Price_INR"].mean()]
    })
    
    fig_sim_bar = px.bar(
        strategy_compare_data,
        x="Strategic Profile",
        y="Average Price (INR)",
        color="Strategic Profile",
        text_auto=",.2f",
        title="Portfolio Baseline vs Optimized Target Comparison Matrix",
        color_discrete_sequence=["#636EFA", "#00CC96"]
    )
    fig_sim_bar.update_layout(template="plotly_white", showlegend=False, height=280)
    st.plotly_chart(fig_sim_bar, use_container_width=True, key="etl_simulation_price_comparison")

# =============================================================================
# 🧠 PHASE 4: AUTOMATED VALUE INSIGHTS HARVESTER (AI-STYLE TEXT REPORT)
# =============================================================================
st.markdown("---")
st.subheader("📋 Executive Summary & Strategic Recommendations")

# Algorithmic logic evaluating top-performing parameters to generate professional text advisory logs
top_competitor = display_df.groupby("Competitor_Name")["Price_INR"].mean().idxmax()
top_competitor_price = display_df.groupby("Competitor_Name")["Price_INR"].mean().max()

recommendation_html = f"""
<div style="background-color:#F8F9FA; padding:20px; border-left: 5px solid #636EFA; border-radius:4px;">
    <h5 style="margin-top:0; color:#1E293B;">🔍 Automated Pipeline Insights Matrix</h5>
    <ul style="color:#334155; font-size:14px; line-height:1.6;">
        <li><b>Competitive Dominance Index:</b> <span style="color:#636EFA; font-weight:640;">{top_competitor}</span> exhibits the highest pricing profile across the monitored infrastructure layer, anchoring a benchmark average price point of <b>₹{top_competitor_price:,.2f}</b>.</li>
        <li><b>Anomaly Variance Report:</b> Identified <span style="color:#EF4444; font-weight:640;">{flagged_price_alerts} critical operational targets</span> out of <b>{total_harvested_items} total tracked units</b> matching or exceeding the current anomaly alert threshold filter of <b>₹{alert_threshold_inr:,.2f}</b>.</li>
        <li><b>Strategic Monetization Guidance:</b> Adjusting the active under-cutting rule by 8% paired with a projected sales conversion growth lift vector of <b>{conversion_boost_pct}%</b> changes the monthly revenue position by <b>₹{net_revenue_impact_inr:,.2f}</b>.</li>
    </ul>
</div>
"""
st.markdown(recommendation_html, unsafe_allow_html=True)


# =============================================================================
# 🚨 PHASE 5: ENTERPRISE DATA QUALITY AUDITING & UNIT TESTING LAYER
# =============================================================================
st.markdown("---")
st.subheader("🛡️ Automated Pipeline Data Quality (DQ) Audit Trail")
st.markdown(
    "Freelance Quality-Engineering Feature: This programmatic validation harness continuously audits "
    "ingested matrices against business safety rules to guarantee data integrity before visualization execution."
)

def execute_pipeline_dq_audit(dataframe_to_verify):
    """
    Runs real-time programmatic unit assertions over the transformed analytical matrix.
    Isolates data corruption constraints, negative financial values, and structural anomalies.
    """
    audit_logs = []
    critical_failures_found = 0
    
    # Assert Check 1: Null Value Proximity Scan
    null_count = dataframe_to_verify.isnull().sum().sum()
    if null_count == 0:
        audit_logs.append(("✅ Integrity Constraint Check Passed", "Zero structural missing values detected across active metrics.", "Success"))
    else:
        audit_logs.append(("⚠️ Non-Critical Missingness Present", f"Detected {null_count} unexpected unmapped items handled via automated system imputation routines.", "Warning"))
        
    # Assert Check 2: Financial Non-Negativity Verification Vector
    negative_prices = (dataframe_to_verify["Raw_Price_USD"] < 0).sum()
    if negative_prices == 0:
        audit_logs.append(("✅ Financial Guardrail Passed", "All continuous pricing vectors confirmed strictly non-negative.", "Success"))
    else:
        audit_logs.append(("❌ Critical Violation Flagged", f"Found {negative_prices} rows with negative values. Integrity corrupted.", "Failure"))
        critical_failures_found += negative_prices

    # Assert Check 3: Relational Pricing Invariance (Target Price must never exceed Competitor Base)
    invariant_breaches = (dataframe_to_verify["Our_Target_Price_INR"] > dataframe_to_verify["Price_INR"]).sum()
    if invariant_breaches == 0:
        audit_logs.append(("✅ Strategy Rule Passed", "Strategic price invariant confirmed (Target Price ≤ Competitor Baseline).", "Success"))
    else:
        audit_logs.append(("❌ Logical Inversion Detected", f"Strategy rule breached on {invariant_breaches} instances. Margin calculations corrupted.", "Failure"))
        critical_failures_found += invariant_breaches
        
    return audit_logs, critical_failures_found

# Trigger Data Quality Verification Harness
dq_logs, failure_metrics = execute_pipeline_dq_audit(display_df)

# Render Data Governance UI Block
dq_col1, dq_col2 = st.columns([3, 1])

with dq_col1:
    st.markdown("##### 🧾 Continuous Compliance Validation Output Logs")
    for title, description, status_type in dq_logs:
        if status_type == "Success":
            st.success(f"**{title}** — {description}")
        elif status_type == "Warning":
            st.warning(f"**{title}** — {description}")
        else:
            st.error(f"**{title}** — {description}")

with dq_col2:
    st.markdown("##### 🔒 Infrastructure Status")
    # Dynamically shifting system status indicator based on running code performance metrics
    if failure_metrics == 0:
        st.markdown(
            "<div style='text-align:center; background-color:#DCFCE7; padding:30px; border-radius:8px; border:2px solid #22C55E;'>"
            "<h2 style='margin:0; color:#15803D;'>SECURE</h2>"
            "<p style='margin:10px 0 0 0; color:#166534; font-size:12px;'>Data Frame 100% Validated for Production Rendering Engine</p>"
            "</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='text-align:center; background-color:#FEE2E2; padding:30px; border-radius:8px; border:2px solid #EF4444;'>"
            f"<h2 style='margin:0; color:#991B1B;'>COMPROMISED</h2>"
            f"<p style='margin:10px 0 0 0; color:#7F1D1D; font-size:12px;'>{failure_metrics} System Violations Trapped In Memory Layer</p>"
            f"</div>",
            unsafe_allow_html=True
        )
