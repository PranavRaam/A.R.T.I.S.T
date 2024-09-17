import json
import re
import requests
from typing import List, Dict, Any, Union
from pydantic import BaseModel, EmailStr, ValidationError, Field

# Define Pydantic models for validation
class PersonalInfo(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str = Field(..., pattern=r'^\+?1?\d{9,15}$') 
    linkedin_profile: str = None
    github_profile: str = None

class WorkExperience(BaseModel):
    job_title: str
    company: str
    start_date: str  # format: YYYY-MM
    end_date: str = None
    responsibilities: List[str]

class Education(BaseModel):
    degree: str
    institution: str
    start_year: str  # format: YYYY
    end_year: str = None
    gpa: str = None

class Skills(BaseModel):
    technical_skills: List[str]
    soft_skills: List[str]

class Certifications(BaseModel):
    certification_name: str
    issued_by: str
    issue_date: str  # format: YYYY-MM

class Projects(BaseModel):
    project_title: str
    description: str
    technologies_used: List[str]

class Languages(BaseModel):
    language: str
    proficiency: str

class ResumeInput(BaseModel):
    personal_info: PersonalInfo
    work_experience: List[WorkExperience]
    education: List[Education]
    skills: Skills
    certifications: List[Certifications] = None
    projects: List[Projects] = None
    languages: List[Languages] = None
    hobbies: List[str] = None

# Function to render input form based on a schema
def render_form(template_schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Render the input form dynamically based on the selected resume template schema.
    """
    form = {}
    for section, fields in template_schema.items():
        form[section] = {field: None for field in fields}  # Initialize form fields as empty
    return form

# Function to validate user inputs
def validate_input(input_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
    """
    Validate the form input data using Pydantic models.
    """
    try:
        resume_input = ResumeInput(**input_data)
        return resume_input.dict()
    except ValidationError as e:
        return str(e)

# Function to handle form submission
def submit_form(form_data: Dict[str, Any], api_url: str) -> Dict[str, Any]:
    """
    Submit the validated form data to the FastAPI backend for resume generation.
    """
    try:
        # Send form data as JSON to the backend
        response = requests.post(api_url, json=form_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Function for dynamic customization options (like reordering sections)
def customize_form_options(form: Dict[str, Any], customization_options: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply customizations like reordering sections or adding optional fields based on user selection.
    """
    # Example: Reordering sections based on user input
    reordered_form = {section: form[section] for section in customization_options['order']}
    
    # Add any optional fields selected by the user
    for optional_field in customization_options.get('optional_fields', []):
        reordered_form[optional_field] = None
    
    return reordered_form

# Error handling and feedback mechanism
def handle_errors(errors: Union[str, Dict[str, Any]]) -> str:
    """
    Handle and return error messages to be displayed on the frontend.
    """
    if isinstance(errors, str):
        return f"Validation Error: {errors}"
    elif "error" in errors:
        return f"API Error: {errors['error']}"
    return "Unknown error occurred."

# Example usage (workflow)
if __name__ == "__main__":
    # Mock template schema for demo purposes
    resume_template_schema = {
        "personal_info": ["full_name", "email", "phone_number", "linkedin_profile", "github_profile"],
        "work_experience": ["job_title", "company", "start_date", "end_date", "responsibilities"],
        "education": ["degree", "institution", "start_year", "end_year", "gpa"],
        "skills": ["technical_skills", "soft_skills"],
        "certifications": ["certification_name", "issued_by", "issue_date"],
        "projects": ["project_title", "description", "technologies_used"],
        "languages": ["language", "proficiency"],
        "hobbies": []
    }

    # Render form based on template schema
    form = render_form(resume_template_schema)
    
    # Example form input from the user
    user_input = {
        "personal_info": {
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "phone_number": "+12345678901",
            "linkedin_profile": "https://linkedin.com/in/johndoe",
            "github_profile": "https://github.com/johndoe"
        },
        "work_experience": [
            {
                "job_title": "Senior Software Engineer",
                "company": "ABC Corp",
                "start_date": "2018-06",
                "end_date": "Present",
                "responsibilities": ["Led development of SaaS platform", "Increased productivity by 25%"]
            }
        ],
        "education": [
            {
                "degree": "BSc Computer Science",
                "institution": "XYZ University",
                "start_year": "2012",
                "end_year": "2016",
                "gpa": "3.8/4.0"
            }
        ],
        "skills": {
            "technical_skills": ["Python", "React", "Node.js"],
            "soft_skills": ["Team leadership", "Problem-solving"]
        },
        "certifications": [
            {
                "certification_name": "AWS Certified Solutions Architect",
                "issued_by": "AWS",
                "issue_date": "2020-03"
            }
        ],
        "projects": [
            {
                "project_title": "E-commerce Platform",
                "description": "Developed an e-commerce platform using React and Node.js.",
                "technologies_used": ["React", "Node.js", "MongoDB"]
            }
        ],
        "languages": [
            {
                "language": "English",
                "proficiency": "Fluent"
            }
        ],
        "hobbies": ["Reading", "Traveling"]
    }

    # Validate user input
    validated_data = validate_input(user_input)
    if isinstance(validated_data, str):
        print(handle_errors(validated_data))
    else:
        # Submit form to the backend
        api_url = "https://your-backend-api-url.com/generate_resume"
        response = submit_form(validated_data, api_url)
        if "error" in response:
            print(handle_errors(response))
        else:
            print("Resume generated successfully!")
