from fpdf import FPDF
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def generate_pdf_report(df, summary, missing_fig, outlier_info, visualizations):
    """Generates a PDF report summarizing EDA results."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "Exploratory Data Analysis Report", ln=True, align='C')

    # Dataset Overview
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns", ln=True)

    # Summary
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "Dataset Summary", ln=True)
    pdf.set_font("Arial", size=12)
    for key, value in summary.items():
        pdf.cell(200, 10, f"{key}: {value}", ln=True)

    # Missing Values
    if missing_fig:
        missing_fig.savefig("missing_values.png", bbox_inches='tight')
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, "Missing Values Analysis", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.image("missing_values.png", x=10, w=190)
        os.remove("missing_values.png")

    # Outlier Detection
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "Outlier Detection", ln=True)
    pdf.set_font("Arial", size=12)
    for col, count in outlier_info.items():
        pdf.cell(200, 10, f"{col}: {count} outliers", ln=True)

    # Visualizations
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "Visualizations", ln=True)
    pdf.set_font("Arial", size=12)
    for i, fig in enumerate(visualizations):
        img_path = f"visual_{i}.png"
        fig.savefig(img_path, bbox_inches='tight')
        pdf.image(img_path, x=10, w=190)
        os.remove(img_path)

    # Save PDF
    pdf_filename = "EDA_Report.pdf"
    pdf.output(pdf_filename)
    return pdf_filename

def generate_markdown_report(df, summary, missing_info, outlier_info):
    """Generates a Markdown report summarizing EDA results."""
    md_report = "# 📝 Exploratory Data Analysis Report\n\n"
    md_report += f"## 📊 Dataset Overview\n- **Rows:** {df.shape[0]}\n- **Columns:** {df.shape[1]}\n\n"

    md_report += "## 🔍 Dataset Summary\n"
    for key, value in summary.items():
        md_report += f"- **{key}:** {value}\n"

    md_report += "\n## 📌 Missing Values\n"
    md_report += f"- {missing_info}\n"

    md_report += "\n## 🚨 Outlier Detection\n"
    for col, count in outlier_info.items():
        md_report += f"- **{col}:** {count} outliers\n"

    md_filename = "EDA_Report.md"
    with open(md_filename, "w", encoding='utf-8') as f:
        f.write(md_report)

    return md_filename
