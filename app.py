import streamlit as st
import pandas as pd

st.title("ClimateReg Insight")
st.write("Climate-related financial risk scoring for loan portfolios")

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
st.dataframe(filtered_df)