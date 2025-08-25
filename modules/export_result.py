import streamlit as st
import pandas as pd
import json
from fpdf import FPDF

def export_results(results, format_type):
    df = pd.DataFrame(results, columns=["Student Name", "ID/Matric", "total score", "details"])
    
    if format_type == "CSV":
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(label="Download CSV", data=csv_data, file_name="test_results.csv", mime="text/csv")
    elif format_type == "PDF":
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, "Student Test Results", ln=True, align='C')
        
        for _, row in df.iterrows():
            pdf.cell(200, 10, f"{row['Student Name']} - {row['ID/Matric']} - Score: {row['total score']} - {str(row["details"])}", ln=True)
        
        pdf_output = pdf.output(dest='S').encode("latin1")
        st.download_button(label="Download PDF", data=pdf_output, file_name="test_results.pdf", mime="application/pdf")
