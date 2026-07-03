import pandas as pd
"""
risk_engine.py
Computes composite climate risk scores for a loan portfolio, combining
physical and transition risk per RBI's Draft Disclosure Framework on
Climate-related Financial Risks, 2024 (built on TCFD's physical/transition
risk categories).


Physical risk is weighted higher (0.6) than transition risk (0.4) since
physical climate impacts are already materializing, while India's
transition-risk regulatory regime (carbon pricing, stricter disclosure)
is still in a phased rollout per RBI's timeline.
"""

PHYSICAL_WEIGHT = 0.6
TRANSITION_WEIGHT = 0.4


def compute_composite_score(physical_risk, transition_risk):
    """
    Combine physical and transition risk (each 1-5) into a single
    weighted composite score, also on a 1-5 scale.
    """
    score = (physical_risk * PHYSICAL_WEIGHT) + (transition_risk * TRANSITION_WEIGHT)
    return round(score, 2)



def get_risk_band(composite_score):
    """
    Translate a composite score (1-5) into a plain-language risk band.
    Thresholds are illustrative and would ideally be calibrated against
    a real institution's risk appetite.
    """
    if composite_score >= 4.0:
        return "High"
    elif composite_score >= 2.5:
        return "Medium"
    else:
        return "Low"
    
def score_portfolio(csv_path="data/synthetic_loan_portfolio.csv"):
    """
    Load a loan portfolio CSV, compute composite risk score and band
    for every borrower, and return the enriched DataFrame.
    """
    df = pd.read_csv(csv_path)

    df["composite_score"] = df.apply(
        lambda row: compute_composite_score(row["physical_risk"], row["transition_risk"]),
        axis=1,
    )
    df["risk_band"] = df["composite_score"].apply(get_risk_band)

    return df
    
if __name__ == "__main__":
    scored = score_portfolio()
    print(scored[["borrower_name", "sector", "region", "composite_score", "risk_band"]].head(10))
    print(f"\nRisk band distribution:\n{scored['risk_band'].value_counts()}")