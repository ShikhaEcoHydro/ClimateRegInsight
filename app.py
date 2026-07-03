import streamlit as st
import pandas as pd

st.title("ClimateReg Insight")
st.write("Climate-related financial risk scoring for loan portfolios")

df = pd.read_csv("data/scored_portfolio.csv")

# --- Summary metrics ---
total_exposure = df["loan_value_inr"].sum()
high_risk_exposure = df[df["risk_band"] == "High"]["loan_value_inr"].sum()
high_risk_pct = (high_risk_exposure / total_exposure) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Total Portfolio Value", f"₹{total_exposure/1e7:.1f} Cr")
col2.metric("High-Risk Exposure", f"₹{high_risk_exposure/1e7:.1f} Cr")
col3.metric("High-Risk % of Portfolio", f"{high_risk_pct:.1f}%")

st.subheader("Portfolio Overview")
st.dataframe(df)