import streamlit as st
import pandas as pd

st.title("ClimateReg Insight")
st.write("Climate-related financial risk scoring for loan portfolios")

df = pd.read_csv("data/scored_portfolio.csv")

st.subheader("Portfolio Overview")
st.dataframe(df)