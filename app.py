import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

st.title("ClimateReg Insight")
st.write("Climate-related financial risk scoring for loan portfolios")
st.caption("⚠️ Built on synthetic data for demonstration purposes. Methodology inspired by RBI's Draft Disclosure Framework on Climate-related Financial Risks, 2024.")

df = pd.read_csv("data/scored_portfolio.csv")

# --- Sidebar filters ---
st.sidebar.header("Filters")

sectors = st.sidebar.multiselect(
    "Sector", options=sorted(df["sector"].unique()), default=sorted(df["sector"].unique())
)
regions = st.sidebar.multiselect(
    "Region", options=sorted(df["region"].unique()), default=sorted(df["region"].unique())
)
bands = st.sidebar.multiselect(
    "Risk Band", options=["Low", "Medium", "High"], default=["Low", "Medium", "High"]
)

filtered_df = df[
    df["sector"].isin(sectors) & df["region"].isin(regions) & df["risk_band"].isin(bands)
]

# --- Summary metrics (now based on filtered data) ---
total_exposure = filtered_df["loan_value_inr"].sum()
high_risk_exposure = filtered_df[filtered_df["risk_band"] == "High"]["loan_value_inr"].sum()
high_risk_pct = (high_risk_exposure / total_exposure * 100) if total_exposure > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Portfolio Value", f"₹{total_exposure/1e7:.1f} Cr")
col2.metric("High-Risk Exposure", f"₹{high_risk_exposure/1e7:.1f} Cr")
col3.metric("High-Risk % of Portfolio", f"{high_risk_pct:.1f}%")

st.subheader(f"Portfolio Overview ({len(filtered_df)} borrowers)")
st.dataframe(filtered_df, hide_index=True)

st.subheader("Risk Distribution")

col_a, col_b = st.columns(2)

with col_a:
    exposure_by_band = filtered_df.groupby("risk_band")["loan_value_inr"].sum().reset_index()
    fig_bar = px.bar(
        exposure_by_band,
        x="risk_band",
        y="loan_value_inr",
        color="risk_band",
        color_discrete_map={"Low": "#4CAF50", "Medium": "#FFA726", "High": "#E53935"},
        category_orders={"risk_band": ["Low", "Medium", "High"]},
        title="Exposure (₹) by Risk Band",
        labels={"loan_value_inr": "Loan Exposure (₹)", "risk_band": "Risk Band"},
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_b:
    count_by_sector = filtered_df["sector"].value_counts().reset_index()
    count_by_sector.columns = ["sector", "count"]
    fig_pie = px.pie(
        count_by_sector,
        names="sector",
        values="count",
        title="Borrower Count by Sector",
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.subheader("Geographic Exposure")

# Aggregate by region so we get one marker per state, not 200 overlapping ones
region_summary = filtered_df.groupby(["region", "lat", "lon"]).agg(
    total_exposure=("loan_value_inr", "sum"),
    borrower_count=("borrower_name", "count"),
).reset_index()

m = folium.Map(location=[22.5, 80], zoom_start=5, tiles="CartoDB positron")

for _, row in region_summary.iterrows():
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=max(5, row["total_exposure"] / 5e7),  # scale circle size by exposure
        popup=f"{row['region']}<br>Exposure: ₹{row['total_exposure']/1e7:.1f} Cr<br>Borrowers: {row['borrower_count']}",
        tooltip=row["region"],
        color="#2E7D5B",
        fill=True,
        fill_color="#2E7D5B",
        fill_opacity=0.6,
    ).add_to(m)

st_folium(m, use_container_width=True, height=500)