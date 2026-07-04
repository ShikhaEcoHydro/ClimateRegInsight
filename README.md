# ClimateReg Insight

A Python/Streamlit tool for assessing climate-related financial risk in a loan
portfolio and scoring corporate sustainability disclosures against recognised
frameworks (TCFD / BRSR-aligned indicators).

Built as a portfolio project to demonstrate skills relevant to climate risk
and sustainable finance roles: portfolio-level physical & transition risk
scoring, disclosure assessment, geospatial exposure mapping, and automated
reporting.

## ⚠️ Data disclaimer

This project uses **synthetic data** generated to resemble a realistic loan
portfolio (borrower sector, location, loan value, sector emissions intensity)
and does not represent any real institution's data. The scoring methodology
is a simplified, rule-based implementation loosely inspired by public
frameworks (TCFD physical/transition risk categories; RBI's draft climate
risk disclosure framework for Indian banks).

## Project structure

\`\`\`
ClimateRegInsight/
├── app.py                 # Streamlit entry point (Module 3)
├── src/
│   ├── risk_engine.py      # Climate risk scoring logic (Module 2)
│   ├── disclosure.py       # PDF disclosure analyzer (Module 5)
│   └── report.py           # PDF report generation (Module 6)
├── utils/
│   └── synthetic_data.py   # Synthetic loan portfolio generator (Module 2)
├── data/
├── notebooks/
├── outputs/
├── requirements.txt
└── README.md
\`\`\`

## Roadmap

- [x] Module 1 — Project setup & repo
- [x] Module 2 — Climate risk scoring engine
- [x] Module 3 — Streamlit dashboard
- [x] Module 4 — Geospatial exposure map
- [x] Module 5 — Disclosure analyzer
- [x] Module 6 — Supervisory report generator
- [x] Module 7 — Polish & deploy

## Setup

\`\`\`bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
\`\`\`

## Author

Deepshikha Srivastava — Applied Ecohydrology (Erasmus Mundus), Applied Geology (Central University of Karnataka).

🔗 **Live app:** [climatereginsight.streamlit.app](https://climatereginsight.streamlit.app)