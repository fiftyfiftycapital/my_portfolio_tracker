import pdfplumber
import csv
import os
from datetime import datetime
from process_data import parse_data, preformat

def process_pdf_statement(pdf_path, csv_path):
    """Process PDF statement and append data to CSV file"""
    
    # Extract text from PDF
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    
    # Parse the extracted text using existing functions
    formatted_text = preformat(text)
    parsed_data = parse_data(formatted_text)
    
    if not parsed_data:
        print(f"No data could be parsed from {pdf_path}")
        return
    
    # Check if CSV exists and get headers
    csv_exists = os.path.exists(csv_path)
    if csv_exists:
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
    else:
        headers = parsed_data[0].keys()
    
    # Append data to CSV
    with open(csv_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not csv_exists:
            writer.writeheader()
        for entry in parsed_data:
            writer.writerow(entry)
    
    print(f"Successfully processed {pdf_path} and appended data to {csv_path}")

if __name__ == "__main__":
    pdf_path = "data/ActivityStatement5805600-2025-03-07.pdf"
    csv_path = "data/brokerage_data1.csv"
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found: {pdf_path}")
    else:
        process_pdf_statement(pdf_path, csv_path)