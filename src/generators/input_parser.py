import re
from email_validator import validate_email, EmailNotValidError
import phonenumbers
from datetime import datetime

class ValidationError(Exception):
    """Custom exception class for input validation errors"""
    pass

def validate_email_address(email: str) -> str:
    """
    Validate email format using email-validator library
    """
    try:
        valid = validate_email(email)
        return valid.email
    except EmailNotValidError as e:
        raise ValidationError(f"Invalid email format: {str(e)}")

def validate_phone_number(phone: str) -> str:
    """
    Validate phone number format using phonenumbers library
    """
    try:
        phone_obj = phonenumbers.parse(phone, None)
        if not phonenumbers.is_valid_number(phone_obj):
            raise ValidationError("Invalid phone number")
        return phonenumbers.format_number(phone_obj, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    except phonenumbers.NumberParseException:
        raise ValidationError("Invalid phone number format")

def validate_date(date_str: str, date_format: str = "%Y-%m") -> str:
    """
    Validate date format (default: YYYY-MM)
    """
    try:
        datetime.strptime(date_str, date_format)
        return date_str
    except ValueError:
        raise ValidationError(f"Invalid date format for {date_str}, expected {date_format}")

def sanitize_input(data: str) -> str:
    """
    Sanitize input to remove unwanted characters and trim spaces
    """
    return data.strip()

def parse_experience(experience_list):
    """
    Parse and validate work experience fields
    """
    parsed_experience = []
    for exp in experience_list:
        if not all(key in exp for key in ("company", "role", "start_date")):
            raise ValidationError("Work experience requires 'company', 'role', and 'start_date'")
        company = sanitize_input(exp["company"])
        role = sanitize_input(exp["role"])
        start_date = validate_date(exp["start_date"])
        end_date = exp.get("end_date", "Present")
        if end_date != "Present":
            end_date = validate_date(end_date)
        parsed_experience.append({
            "company": company,
            "role": role,
            "start_date": start_date,
            "end_date": end_date
        })
    return parsed_experience

def parse_education(education_list):
    """
    Parse and validate education fields
    """
    parsed_education = []
    for edu in education_list:
        if not all(key in edu for key in ("institution", "degree", "graduation_year")):
            raise ValidationError("Education requires 'institution', 'degree', and 'graduation_year'")
        institution = sanitize_input(edu["institution"])
        degree = sanitize_input(edu["degree"])
        graduation_year = validate_date(edu["graduation_year"], date_format="%Y")
        parsed_education.append({
            "institution": institution,
            "degree": degree,
            "graduation_year": graduation_year
        })
    return parsed_education

def parse_resume_input(data: dict) -> dict:
    """
    Main function to parse and validate the entire resume input data
    """
    required_fields = ["personal_information", "work_experience", "education"]
    
    # Check if all required fields are present
    for field in required_fields:
        if field not in data:
            raise ValidationError(f"Missing required field: {field}")
    
    # Extract and validate personal information
    personal_info = data.get("personal_information", {})
    name = sanitize_input(personal_info.get("full_name", ""))
    email = validate_email_address(sanitize_input(personal_info.get("email", "")))
    phone = validate_phone_number(sanitize_input(personal_info.get("phone_number", "")))
    
    # Parse work experience
    work_experience = []
    for exp in data.get("work_experience", []):
        if not all(key in exp for key in ("job_title", "company_name", "start_date")):
            raise ValidationError("Work experience requires 'job_title', 'company_name', and 'start_date'")
        job_title = sanitize_input(exp["job_title"])
        company_name = sanitize_input(exp["company_name"])
        start_date = validate_date(exp["start_date"], date_format="%B %Y")
        end_date = exp.get("end_date", "Present")
        if end_date != "Present":
            end_date = validate_date(end_date, date_format="%B %Y")
        work_experience.append({
            "job_title": job_title,
            "company_name": company_name,
            "start_date": start_date,
            "end_date": end_date,
            "responsibilities": [sanitize_input(res) for res in exp.get("responsibilities", [])],
            "achievements": [sanitize_input(ach) for ach in exp.get("achievements", [])]
        })

    # Parse education
    education = data.get("education", {})
    institution = sanitize_input(education.get("institution_name", ""))
    degree = sanitize_input(education.get("degree", ""))
    graduation_year = validate_date(education.get("graduation_date", ""), date_format="%B %Y")
    
    parsed_education = {
        "institution": institution,
        "degree": degree,
        "graduation_year": graduation_year
    }

    # Optional fields handling
    skills = {
        "technical_skills": [sanitize_input(skill) for skill in data.get("skills", {}).get("technical_skills", [])],
        "soft_skills": [sanitize_input(skill) for skill in data.get("skills", {}).get("soft_skills", [])],
        "tools": [sanitize_input(tool) for tool in data.get("skills", {}).get("tools", [])]
    }
    career_summary = sanitize_input(data.get("career_objective", "Not Provided"))
    hobbies = [sanitize_input(hobby) for hobby in data.get("interests_hobbies", [])]
    
    # Return structured and validated data
    processed_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "work_experience": work_experience,
        "education": parsed_education,
        "skills": skills,
        "career_summary": career_summary,
        "hobbies": hobbies
    }
    
    return processed_data


if __name__ == "__main__":
    sample_input = {
        "personal_information": {
            "full_name": "John Doe",
            "email": "john.doe@gmail.com",
            "phone_number": "+911288234586"
        },
        "work_experience": [
            {
                "job_title": "Software Engineer",
                "company_name": "ABC Corp",
                "start_date": "January 2020",
                "end_date": "Present",
                "responsibilities": ["Developed software", "Led a team of engineers"],
                "achievements": ["Improved code efficiency", "Reduced deployment time"]
            }
        ],
        "education": {
            "institution_name": "XYZ University",
            "degree": "Bachelor of Computer Science",
            "graduation_date": "June 2018"
        },
        "skills": {
            "technical_skills": ["Python", "Machine Learning"],
            "soft_skills": ["Communication", "Teamwork"],
            "tools": ["Git", "Docker"]
        },
        "career_objective": "To work as a software engineer in a challenging environment.",
        "interests_hobbies": ["Reading", "Coding"]
    }

    parsed_data = parse_resume_input(sample_input)
    print(parsed_data)


