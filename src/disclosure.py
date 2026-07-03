"""
disclosure.py
Extracts text from an uploaded sustainability/ESG report PDF and scores it
against RBI's four disclosure pillars (Governance, Strategy, Risk Management,
Metrics & Targets), per the Draft Disclosure Framework on Climate-related
Financial Risks, 2024.

Scoring is rule-based: keyword presence per pillar, normalized to a 0-100
score. This is a simplification — a real assessment would require expert
judgment on disclosure *quality*, not just presence of relevant language.
"""

import fitz  # PyMuPDF

PILLAR_KEYWORDS = {
    "Governance": [
        "board oversight", "board of directors", "governance structure",
        "climate governance", "risk committee", "senior management",
        "oversight of climate", "accountability",
    ],
    "Strategy": [
        "climate strategy", "transition plan", "scenario analysis",
        "climate scenario", "business strategy", "net zero", "decarbonization",
        "low-carbon transition", "climate opportunities",
    ],
    "Risk Management": [
        "risk identification", "risk assessment", "physical risk",
        "transition risk", "risk management process", "materiality assessment",
        "risk mitigation", "climate risk integration",
    ],
    "Metrics and Targets": [
        "scope 1", "scope 2", "scope 3", "ghg emissions", "emissions target",
        "carbon intensity", "sustainability metrics", "science based target",
        "financed emissions",
    ],
}


def extract_text_from_pdf(pdf_file):
    """Extract all text from a PDF file (accepts a file path or file-like object)."""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf") if hasattr(pdf_file, "read") else fitz.open(pdf_file)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.lower()


def score_pillar(text, keywords):
    """Count how many distinct keywords from a pillar appear in the text."""
    found = [kw for kw in keywords if kw in text]
    score = round((len(found) / len(keywords)) * 100, 1)
    return score, found


def score_disclosure(text):
    """Score all four pillars and return a summary dict."""
    results = {}
    for pillar, keywords in PILLAR_KEYWORDS.items():
        score, found = score_pillar(text, keywords)
        results[pillar] = {"score": score, "keywords_found": found}

    overall_score = round(
        sum(r["score"] for r in results.values()) / len(results), 1
    )
    return results, overall_score


if __name__ == "__main__":
    sample_text = """
    Our board of directors provides oversight of climate governance.
    We have developed a net zero transition plan and conduct scenario analysis.
    Our risk assessment process identifies physical risk and transition risk.
    We disclose scope 1 and scope 2 ghg emissions.
    """.lower()

    results, overall = score_disclosure(sample_text)
    for pillar, data in results.items():
        print(f"{pillar}: {data['score']}% ({len(data['keywords_found'])} keywords found)")
    print(f"\nOverall Disclosure Score: {overall}%")