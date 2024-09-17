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
    required_fields = ["name", "email", "phone", "experience", "education"]
    
    # Check if all required fields are present
    for field in required_fields:
        if field not in data:
            raise ValidationError(f"Missing required field: {field}")
    
    # Validate and sanitize name
    name = sanitize_input(data["name"])
    
    # Validate email
    email = validate_email_address(sanitize_input(data["email"]))
    
    # Validate phone number
    phone = validate_phone_number(sanitize_input(data["phone"]))
    
    # Parse work experience
    experience = parse_experience(data.get("experience", []))
    
    # Parse education
    education = parse_education(data.get("education", []))
    
    # Optional fields handling
    skills = [sanitize_input(skill) for skill in data.get("skills", [])]
    career_summary = sanitize_input(data.get("career_summary", "Not Provided"))
    hobbies = [sanitize_input(hobby) for hobby in data.get("hobbies", [])]
    
    # Return structured and validated data
    processed_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "experience": experience,
        "education": education,
        "skills": skills,
        "career_summary": career_summary,
        "hobbies": hobbies
    }
    
    return processed_data
