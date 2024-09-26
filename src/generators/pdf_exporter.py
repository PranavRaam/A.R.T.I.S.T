from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListItem, ListFlowable
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def export_to_pdf(resume_data, file_path="resume.pdf"):
    """
    Export structured resume data to a PDF file using ReportLab.
    :param resume_data: Dictionary containing resume content.
    :param file_path: Path where the PDF will be saved.
    """

    # Create a PDF document
    doc = SimpleDocTemplate(file_path, pagesize=LETTER, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
    # Define elements to hold the resume content
    elements = []
    
    # Set up basic styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    title_style.alignment = TA_CENTER
    section_heading_style = styles['Heading2']
    section_heading_style.alignment = TA_LEFT
    normal_style = styles['Normal']
    
    # Add Header (Name, Email, Phone)
    header = f"{resume_data['name']}\n{resume_data['email']} | {resume_data['phone']}"
    elements.append(Paragraph(header, title_style))
    elements.append(Spacer(1, 12))
    
    # Add Career Summary
    if 'career_summary' in resume_data:
        elements.append(Paragraph("Career Summary", section_heading_style))
        elements.append(Paragraph(resume_data['career_summary'], normal_style))
        elements.append(Spacer(1, 12))
    
    # Add Work Experience
    if 'experience' in resume_data:
        elements.append(Paragraph("Work Experience", section_heading_style))
        for job in resume_data['experience']:
            job_info = f"{job['role']} at {job['company']} ({job['start_date']} - {job['end_date']})"
            elements.append(Paragraph(job_info, normal_style))
            if 'description' in job and job['description']:
                description_paragraph = Paragraph(job['description'], normal_style)
                elements.append(description_paragraph)
            elements.append(Spacer(1, 8))
        elements.append(Spacer(1, 12))
    
    # Add Education
    if 'education' in resume_data:
        elements.append(Paragraph("Education", section_heading_style))
        for edu in resume_data['education']:
            education_paragraph = f"{edu['degree']} from {edu['institution']} ({edu['graduation_year']})"
            elements.append(Paragraph(education_paragraph, normal_style))
        elements.append(Spacer(1, 12))
    
    # Add Skills
    if 'skills' in resume_data:
        elements.append(Paragraph("Skills", section_heading_style))
        skills_list = ListFlowable(
            [ListItem(Paragraph(skill, normal_style), leftIndent=12) for skill in resume_data['skills']],
            bulletType='bullet',
            start='circle',
        )
        elements.append(skills_list)
        elements.append(Spacer(1, 12))
    
    # Build PDF document
    try:
        doc.build(elements)
        print(f"Resume PDF saved at {file_path}")
    except Exception as e:
        print(f"Error building PDF: {e}")

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
