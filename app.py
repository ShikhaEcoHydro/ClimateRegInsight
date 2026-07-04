import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
import sys
sys.path.append("src")
from disclosure import extract_text_from_pdf, score_disclosure
from report import generate_report

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
    st.plotly_chart(fig_bar, width='stretch')

with col_b:
    count_by_sector = filtered_df["sector"].value_counts().reset_index()
    count_by_sector.columns = ["sector", "count"]
    fig_pie = px.pie(
        count_by_sector,
        names="sector",
        values="count",
        title="Borrower Count by Sector",
    )
    st.plotly_chart(fig_pie, width='stretch')

st.subheader("Geographic Exposure")

# Aggregate by region so we get one marker per state, not 200 overlapping ones
region_summary = filtered_df.groupby(["region", "lat", "lon"]).agg(
    total_exposure=("loan_value_inr", "sum"),
    borrower_count=("borrower_name", "count"),
    avg_composite_score=("composite_score", "mean"),
).reset_index()

def score_to_color(score):
    if score >= 4.0:
        return "#E53935"  # High - red
    elif score >= 2.5:
        return "#FFA726"  # Medium - orange
    else:
        return "#4CAF50"  # Low - green

m = folium.Map(location=[22.5, 80], zoom_start=5, tiles="CartoDB positron")

for _, row in region_summary.iterrows():
    color = score_to_color(row["avg_composite_score"])
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=max(5, row["total_exposure"] / 5e7),
        popup=f"{row['region']}<br>Exposure: ₹{row['total_exposure']/1e7:.1f} Cr<br>"
              f"Borrowers: {row['borrower_count']}<br>"
              f"Avg Risk Score: {row['avg_composite_score']:.2f}",
        tooltip=row["region"],
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
    ).add_to(m)

st_folium(m, width='stretch', height=500)

st.subheader("Disclosure Analyzer")
st.caption("Upload a sustainability/ESG report (PDF) to score it against RBI's four disclosure pillars.")

uploaded_pdf = st.file_uploader("Upload sustainability report", type="pdf")

if uploaded_pdf is not None:
    text = extract_text_from_pdf(uploaded_pdf)
    results, overall = score_disclosure(text)

    st.metric("Overall Disclosure Score", f"{overall}%")

    pillar_cols = st.columns(4)
    for col, (pillar, data) in zip(pillar_cols, results.items()):
        col.metric(pillar, f"{data['score']}%")

    with st.expander("See keyword matches by pillar"):
        for pillar, data in results.items():
            st.write(f"**{pillar}**: {', '.join(data['keywords_found']) if data['keywords_found'] else 'None found'}")

st.subheader("Generate Report")

exposure_summary_table = filtered_df.groupby("risk_band").agg(
    borrower_count=("borrower_name", "count"),
    total_exposure_inr=("loan_value_inr", "sum"),
)
exposure_summary_table["pct_of_portfolio"] = (
    exposure_summary_table["total_exposure_inr"] / exposure_summary_table["total_exposure_inr"].sum() * 100
)

if st.button("Generate PDF Report"):
    disclosure_results = results if uploaded_pdf is not None else None
    overall_disclosure_score = overall if uploaded_pdf is not None else None

    pdf_buffer = generate_report(
        exposure_summary_table,
        total_exposure,
        high_risk_pct,
        disclosure_results,
        overall_disclosure_score,
    )

    st.download_button(
        "Download Report (PDF)",
        data=pdf_buffer,
        file_name="climatereg_insight_report.pdf",
        mime="application/pdf",
    )

st.divider()
st.caption(
    "Built by Deepshikha Srivastava | Portfolio project demonstrating climate risk "
    "scoring and disclosure assessment for financial institutions | "
    "[GitHub](https://github.com/ShikhaEcoHydro/ClimateRegInsight)"
)