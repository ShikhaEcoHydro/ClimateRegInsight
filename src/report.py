"""
report.py
Generates a downloadable PDF summarizing portfolio climate risk exposure
and (optionally) disclosure assessment results.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from datetime import date


def generate_report(exposure_summary, total_exposure, high_risk_pct, disclosure_results=None, overall_disclosure=None):
    """
    Build a PDF report in memory and return the bytes, suitable for
    st.download_button in Streamlit.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle("TitleStyle", parent=styles["Title"], fontSize=20)
    story.append(Paragraph("ClimateReg Insight - Supervisory Summary", title_style))
    story.append(Paragraph(f"Generated: {date.today().strftime('%d %B %Y')}", styles["Normal"]))
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph(
        "This report is based on synthetic data for demonstration purposes. "
        "Methodology loosely informed by RBI's Draft Disclosure Framework on "
        "Climate-related Financial Risks, 2024.",
        styles["Italic"]
    ))
    story.append(Spacer(1, 1*cm))

    story.append(Paragraph("Portfolio Risk Summary", styles["Heading2"]))
    story.append(Paragraph(f"Total Portfolio Value: Rs. {total_exposure/1e7:.1f} Cr", styles["Normal"]))
    story.append(Paragraph(f"High-Risk Exposure: {high_risk_pct:.1f}% of portfolio", styles["Normal"]))
    story.append(Spacer(1, 0.5*cm))

    table_data = [["Risk Band", "Borrower Count", "Exposure (Rs. Cr)", "% of Portfolio"]]
    for band, row in exposure_summary.iterrows():
        table_data.append([
            band,
            str(int(row["borrower_count"])),
            f"{row['total_exposure_inr']/1e7:.1f}",
            f"{row['pct_of_portfolio']:.1f}%",
        ])

    table = Table(table_data, colWidths=[4*cm, 4*cm, 4*cm, 4*cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E7D5B")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    story.append(table)
    story.append(Spacer(1, 1*cm))

    if disclosure_results is not None:
        story.append(Paragraph("Disclosure Assessment", styles["Heading2"]))
        story.append(Paragraph(f"Overall Disclosure Score: {overall_disclosure}%", styles["Normal"]))
        story.append(Spacer(1, 0.3*cm))

        disc_table_data = [["Pillar", "Score"]]
        for pillar, data in disclosure_results.items():
            disc_table_data.append([pillar, f"{data['score']}%"])

        disc_table = Table(disc_table_data, colWidths=[8*cm, 4*cm])
        disc_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E7D5B")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        story.append(disc_table)

    doc.build(story)
    buffer.seek(0)
    return buffer