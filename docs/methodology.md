# Methodology

## Overview

ClimateReg Insight is a rule-based tool for two related tasks a climate risk
function at a regulated entity would need: (1) scoring a loan portfolio's
climate risk exposure, and (2) screening a counterparty's sustainability
disclosures for topical coverage. Both are built on **synthetic data** and
simplified logic, deliberately designed to be transparent and explainable
rather than statistically sophisticated — the goal is to demonstrate a clear,
defensible approach to climate risk integration, not to replicate a
production-grade model.

## 1. Portfolio Risk Scoring

### Risk framework
Risk is split into two channels, following both TCFD and RBI's Draft
Disclosure Framework on Climate-related Financial Risks (2024):

- **Physical risk** — driven by a borrower's location, reflecting exposure
  to flood, heat, and water-stress events.
- **Transition risk** — driven by a borrower's sector, reflecting exposure
  to carbon pricing, tightening regulation, and demand shifts away from
  carbon-intensive activity.

Each borrower receives a physical risk score (1–5) based on their region and
a transition risk score (1–5) based on their sector, both assigned from
illustrative reference tables (`utils/synthetic_data.py`).

### Composite scoring and weighting
The two scores are combined into one composite score:

```
composite_score = (physical_risk × 0.6) + (transition_risk × 0.4)
```

**Physical risk is weighted higher (60/40)** because physical climate
impacts — floods, heat stress, water scarcity — are already materializing in
India, while transition risk (carbon pricing, stricter disclosure mandates)
is still in a phased regulatory rollout under RBI's own timeline. This
weighting is a judgment call, not an empirical calibration, and would ideally
be revisited against a real institution's loss experience and risk appetite.

### Risk bands
Composite scores are translated into Low / Medium / High bands using fixed
thresholds (< 2.5, 2.5–3.99, ≥ 4.0). These thresholds are illustrative,
splitting the 1–5 range roughly into thirds. A production deployment would
calibrate these against the actual portfolio's score distribution and the
institution's risk tolerance, rather than using a fixed a priori split.

### Known limitations
- Regional and sectoral risk scores are illustrative single numbers, not
  derived from actual hazard data (e.g. CWC flood atlases, IMD heat data) or
  sector-specific emissions intensity data.
- The model treats risk as static; it does not account for risk changing
  over the loan tenure, or second-order effects (e.g. a flood damaging a
  borrower's supply chain rather than their own site).

## 2. Disclosure Analyzer

### Approach
An uploaded sustainability/ESG report (PDF) is scored against RBI's four
disclosure pillars — Governance, Strategy, Risk Management, and Metrics and
Targets — using **keyword presence matching**. Each pillar has a fixed list
of representative phrases; the pillar score is the percentage of those
phrases found anywhere in the document text. The overall score is the
average across all four pillars.

### Known limitation (important)
This measures **topical coverage, not disclosure quality**. A report that
mentions "Scope 1 emissions" once in a footnote scores identically to one
that provides a detailed, verified emissions breakdown. The tool is a
reasonable first-pass screening signal — useful for flagging reports that
are clearly thin on a given pillar — but it cannot substitute for expert
review of disclosure depth, specificity, or data quality. A more advanced
version could use semantic similarity or LLM-based assessment to evaluate
substance rather than presence.

## 3. Geospatial Exposure Map

Borrowers are aggregated to state-level centroids (approximate coordinates,
not exact addresses, since the underlying data is synthetic and
state-level). Map markers encode two independent dimensions: **circle size**
reflects total loan exposure (₹) in that region, and **circle color**
reflects the region's average composite risk score. This lets a viewer
identify, at a glance, both where the money is concentrated and where that
money is most at risk — which are not always the same region.

## 4. Supervisory Report

The PDF report combines the portfolio risk summary and (if provided) the
disclosure assessment into a single downloadable document, intended to
resemble the kind of internal summary a risk or ESG function might produce
for management reporting.

## What Would Change With Real Data

- Sector transition risk weights would be informed by actual carbon
  intensity data (e.g. sectoral emissions per unit revenue) rather than
  illustrative 1–5 assignments.
- Regional physical risk would draw on hazard datasets (CWC flood
  hazard maps, IMD extreme heat records, CGWB groundwater stress indices)
  rather than a single illustrative score per state.
- Risk band thresholds would be calibrated against the real portfolio's
  score distribution and the institution's risk appetite, rather than a
  fixed a priori split.
- Disclosure scoring would ideally move from keyword presence to a
  quality-aware method (e.g. semantic matching, or a structured checklist
  requiring human sign-off), particularly given how consequential accurate
  disclosure assessment is for regulatory reporting.