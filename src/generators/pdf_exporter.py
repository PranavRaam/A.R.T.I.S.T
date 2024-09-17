from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
import os

def export_to_pdf(resume_data, file_path="resume.pdf"):
    """
    Export structured resume data to a PDF file using ReportLab.
    :param resume_data: Dictionary containing resume content.
    :param file_path: Path where the PDF will be saved.
    """

    # Create a PDF document
    doc = SimpleDocTemplate(file_path, pagesize=LETTER)
    
    # Define elements to hold the resume content
    elements = []
    
    # Set up basic styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    title_style.alignment = TA_CENTER
    normal_style = styles['Normal']
    
    # Add Header (Name, Email, Phone)
    header = f"{resume_data['name']}\n{resume_data['email']} | {resume_data['phone']}"
    elements.append(Paragraph(header, title_style))
    elements.append(Spacer(1, 12))
    
    # Add Career Summary
    if 'career_summary' in resume_data:
        elements.append(Paragraph("Career Summary", styles['Heading2']))
        elements.append(Paragraph(resume_data['career_summary'], normal_style))
        elements.append(Spacer(1, 12))
    
    # Add Work Experience
    if 'experience' in resume_data:
        elements.append(Paragraph("Work Experience", styles['Heading2']))
        experience_data = []
        for job in resume_data['experience']:
            experience_data.append([
                f"{job['role']} at {job['company']}",
                f"{job['start_date']} - {job['end_date']}"
            ])
            experience_data.append([job.get('description', '')])
        
        table = Table(experience_data, colWidths=[3*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))
    
    # Add Education
    if 'education' in resume_data:
        elements.append(Paragraph("Education", styles['Heading2']))
        for edu in resume_data['education']:
            education_paragraph = f"{edu['degree']} from {edu['institution']} ({edu['graduation_year']})"
            elements.append(Paragraph(education_paragraph, normal_style))
        elements.append(Spacer(1, 12))
    
    # Add Skills
    if 'skills' in resume_data:
        elements.append(Paragraph("Skills", styles['Heading2']))
        skills_paragraph = ", ".join(resume_data['skills'])
        elements.append(Paragraph(skills_paragraph, normal_style))
        elements.append(Spacer(1, 12))
    
    # Build PDF document
    doc.build(elements)
    print(f"Resume PDF saved at {file_path}")

# Example usage:
if __name__ == "__main__":
    sample_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "career_summary": "Experienced software engineer with expertise in Python and Machine Learning.",
        "experience": [
            {
                "company": "TechCorp",
                "role": "Software Engineer",
                "start_date": "2020-06",
                "end_date": "2023-09",
                "description": "Developed software solutions for clients and led a team of engineers."
            },
        ],
        "education": [
            {
                "institution": "XYZ University",
                "degree": "B.Sc. Computer Science",
                "graduation_year": 2020
            },
        ],
        "skills": ["Python", "Machine Learning", "Django"]
    }
    
    export_to_pdf(sample_data)
