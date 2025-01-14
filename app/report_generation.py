from app.data_generation import ThreatIntelligenceGenerator
import pandas as pd
from datetime import datetime
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf_report(df):
    """Generate a detailed PDF report from the threat data."""
    
    # Create reports directory if it doesn't exist
    os.makedirs('reports', exist_ok=True)
    
    filename = f"reports/threat_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    
    # Add title and timestamp
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Cyber Threat Intelligence Report", styles['Title']))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                            styles['Normal']))
    
    # Add summary statistics
    elements.append(Paragraph("Summary Statistics", styles['Heading1']))
    stats = [
        f"Total Threats: {len(df)}",
        f"High/Critical Severity Threats: {len(df[df['severity'].isin(['High', 'Critical'])])}",
        f"Average Risk Score: {df['risk_score'].mean():.2f}",
        f"Top Threat Categories: {', '.join(df['threat_category'].value_counts().nlargest(3).index)}"
    ]
    for stat in stats:
        elements.append(Paragraph(stat, styles['Normal']))
    
    # Add threat distribution table
    elements.append(Paragraph("Threat Distribution by Category", styles['Heading1']))
    threat_dist = df['threat_category'].value_counts().reset_index()
    threat_dist.columns = ['Threat Category', 'Count']
    
    # Convert DataFrame to list of lists for the table
    table_data = [threat_dist.columns.tolist()] + threat_dist.values.tolist()
    
    # Create and style the table
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    
    # Build the PDF
    doc.build(elements)
    
    return filename

def generate_csv_report(df):
    """Generate a CSV report from the threat data."""
    
    # Create reports directory if it doesn't exist
    os.makedirs('reports', exist_ok=True)
    
    filename = f"reports/threat_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    # Add additional calculated fields
    df['report_generated'] = datetime.now()
    df['threat_level'] = df.apply(calculate_threat_level, axis=1)
    
    # Save to CSV
    df.to_csv(filename, index=False)
    
    return filename

def calculate_threat_level(row):
    """Calculate overall threat level based on multiple factors."""
    severity_scores = {
        'Low': 1,
        'Medium': 2,
        'High': 3,
        'Critical': 4
    }
    
    # Calculate base score
    base_score = severity_scores.get(row['severity'], 1) * row['risk_score'] / 25
    
    # Adjust based on confidence score
    adjusted_score = base_score * row['confidence_score']
    
    # Categorize
    if adjusted_score >= 12:
        return 'Critical'
    elif adjusted_score >= 8:
        return 'High'
    elif adjusted_score >= 4:
        return 'Medium'
    else:
        return 'Low'

if __name__ == '__main__':
    # Test report generation
    from data_generation import generate_threat_data
    df = generate_threat_data(10)
    pdf_file = generate_pdf_report(df)
    csv_file = generate_csv_report(df)
    print(f"Generated reports: {pdf_file}, {csv_file}") 