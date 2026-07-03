"""
synthetic_data.py
Generates a synthetic loan portfolio for testing the climate risk engine.
Sector risk weights are illustrative, loosely informed by relative
carbon-intensity and RBI's physical/transition risk framing.
"""
import pandas as pd
import random
from faker import Faker

fake = Faker("en_IN")

# Transition risk: how exposed is this sector to carbon pricing,
# regulatory tightening, and the shift to a low-carbon economy?
# Scale: 1 (low) to 5 (high)
SECTOR_TRANSITION_RISK = {
    "Thermal Power": 5,
    "Cement": 5,
    "Steel & Metals": 5,
    "Oil & Gas": 5,
    "Textiles": 3,
    "Agriculture": 3,
    "Real Estate & Construction": 3,
    "Manufacturing (General)": 3,
    "Automotive": 3,
    "Renewable Energy": 1,
    "IT & Software Services": 1,
    "Healthcare": 1,
    "Financial Services": 1,
}
# Physical risk: flood, heat, and water-stress exposure by region.
# Scale: 1 (low) to 5 (high). Illustrative — a real version would draw on
# CWC flood atlases, IMD heat data, or CGWB groundwater stress indices.
REGION_PHYSICAL_RISK = {
    "Uttar Pradesh": 4,      # Ganga-Ghaghra floodplain exposure
    "Bihar": 5,              # Kosi/Ganga flood-prone
    "Assam": 5,              # Brahmaputra flood-prone
    "Kerala": 4,             # 2018-style flood exposure
    "Rajasthan": 4,          # water stress / heat
    "Maharashtra": 3,
    "Gujarat": 3,
    "Tamil Nadu": 3,
    "Karnataka": 2,
    "Delhi NCR": 3,          # heat stress
    "Punjab": 3,             # groundwater depletion
    "West Bengal": 4,        # delta/flood exposure
}

# Approximate state/region centroid coordinates (lat, lon), for mapping.
REGION_COORDINATES = {
    "Uttar Pradesh": (26.8467, 80.9462),
    "Bihar": (25.0961, 85.3131),
    "Assam": (26.2006, 92.9376),
    "Kerala": (10.8505, 76.2711),
    "Rajasthan": (27.0238, 74.2179),
    "Maharashtra": (19.7515, 75.7139),
    "Gujarat": (22.2587, 71.1924),
    "Tamil Nadu": (11.1271, 78.6569),
    "Karnataka": (15.3173, 75.7139),
    "Delhi NCR": (28.7041, 77.1025),
    "Punjab": (31.1471, 75.3412),
    "West Bengal": (22.9868, 87.8550),
}

if __name__ == "__main__":
    print("--- Transition Risk by Sector ---")
    for sector, risk in SECTOR_TRANSITION_RISK.items():
        print(f"{sector}: transition risk = {risk}")

    print("\n--- Physical Risk by Region ---")
    for region, risk in REGION_PHYSICAL_RISK.items():
        print(f"{region}: physical risk = {risk}")

def generate_borrower():
    """Generate a single synthetic borrower with sector, region, and loan details."""
    sector = random.choice(list(SECTOR_TRANSITION_RISK.keys()))
    region = random.choice(list(REGION_PHYSICAL_RISK.keys()))
    lat, lon = REGION_COORDINATES[region]

    borrower = {
        "borrower_name": fake.company(),
        "sector": sector,
        "region": region,
        "loan_value_inr": round(random.uniform(5_00_000, 5_00_00_000), 2),
        "transition_risk": SECTOR_TRANSITION_RISK[sector],
        "physical_risk": REGION_PHYSICAL_RISK[region],
        "lat": lat,
        "lon": lon,
    }
    return borrower

if __name__ == "__main__":
    print("--- Sample Borrower ---")
    print(generate_borrower())

def generate_portfolio(n=200, seed=42):
    """Generate a synthetic loan portfolio of n borrowers as a DataFrame."""
    random.seed(seed)
    Faker.seed(seed)
    borrowers = [generate_borrower() for _ in range(n)]
    return pd.DataFrame(borrowers)


if __name__ == "__main__":
    portfolio = generate_portfolio(n=200)
    print(portfolio.head())
    print(f"\nGenerated {len(portfolio)} borrowers.")

    portfolio.to_csv("data/synthetic_loan_portfolio.csv", index=False)
    print("Saved to data/synthetic_loan_portfolio.csv")