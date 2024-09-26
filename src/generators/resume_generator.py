import os
import logging
from jinja2 import Environment, FileSystemLoader

# Placeholder for the missing imports from your project.
from src.generators.input_parser import parse_resume_input, ValidationError
from src.generators.pdf_exporter import export_to_pdf as pdf_exporter
from src.models.llm_inference import LLMInference
from src.services.resume_ranking_service import ResumeRankingService
from src.utils.template_renderer import TemplateRenderer


class ResumeGenerator:
    def __init__(self, user_input: dict, template_name: str, language: str = 'en', optimize_ats: bool = True):
        self.user_input = user_input
        self.template_name = template_name
        self.language = language
        self.optimize_ats = optimize_ats
        self.parsed_data = None
        self.final_resume = None

    def parse_input(self):
        """
        Parse and validate user input and format it for the LaTeX template.
        """
        try:
            # Validate required fields in user input
            required_fields = [
                'name', 'email', 'phone_number', 
                'institution_name', 'degree', 'graduation_date'
            ]
            for field in required_fields:
                if field not in self.user_input.get('personal_information', {}) and field not in self.user_input.get('education', {}):
                    raise ValueError(f"Missing '{field}' in user input.")
            
            self.parsed_data = {
                'name': self.user_input['personal_information']['name'],
                'email': self.user_input['personal_information']['email'],
                'phone': self.user_input['personal_information']['phone_number'],
                'career_summary': self.user_input.get('career_objective', ''),
                'work_experience': self.user_input.get('work_experience', []),
                'education': {
                    'institution': self.user_input['education']['institution_name'],
                    'degree': self.user_input['education']['degree'],
                    'graduation_year': self.user_input['education']['graduation_date']
                },
                'skills': self.user_input.get('skills', {}),
                'hobbies': self.user_input.get('interests_hobbies', [])
            }

            # Ensure no missing keys cause issues in the template rendering
            self.parsed_data.setdefault('career_summary', '')
            self.parsed_data.setdefault('work_experience', [])
            self.parsed_data.setdefault('skills', {
                'technical_skills': [],
                'soft_skills': [],
                'tools': []
            })
            self.parsed_data.setdefault('hobbies', [])

            if not self.parsed_data:
                raise ValueError("Parsed data is None. Please check resume generation logic.")
        except KeyError as e:
            raise ValueError(f"Missing key in user input: {e}")
        except ValidationError as e:
            raise ValueError(f"Input validation error: {e}")

    def select_template(self):
        """
        Load the selected resume template.
        """
        try:
            template_dir = os.path.join("src", "templates/basic")
            env = Environment(loader=FileSystemLoader(template_dir))
            return env.get_template(self.template_name + '.tex')
        except Exception as e:
            raise ValueError(f"Template {self.template_name} not found: {str(e)}")

    def render_resume(self):
        """
        Render the resume with the selected template and parsed data.
        """
        try:
            # Select the LaTeX template
            template = self.select_template()
            
            # Render the template with parsed data
            self.final_resume = template.render(self.parsed_data)
            logging.info("Rendered resume:\n" + self.final_resume)
        except Exception as e:
            raise ValueError(f"Error rendering resume: {e}")

    def export_to_pdf(self):
        """
        Convert the rendered resume content to a PDF.
        """
        try:
            # Debugging: print the type and content of the final_resume
            print(f"Final resume type: {type(self.final_resume)}")
            print(f"Final resume content: {self.final_resume[:100]}...")  # Print first 100 characters for preview

            if not isinstance(self.final_resume, str):
                raise ValueError("final_resume must be a LaTeX string.")

            if not self.final_resume:
                raise ValueError("No resume content to export.")

            # Check if all required keys are present
            required_keys = ['name', 'email', 'phone']
            for key in required_keys:
                if key not in self.parsed_data:
                    raise ValueError(f"Parsed data missing '{key}'. Please check input data.")

            # Call to actual PDF exporter function
            pdf_exporter({
                "content": self.final_resume,
                "name": self.parsed_data['name'],
                "email": self.parsed_data['email'],
                "phone": self.parsed_data['phone']
            })
        except Exception as e:
            raise ValueError(f"Error exporting resume to PDF: {e}")

    def generate(self):
        """
        Full generation process.
        """
        try:
            self.parse_input()
            self.render_resume()
            self.export_to_pdf()
        except Exception as e:
            logging.error(f"Error generating resume: {e}")
            raise


if __name__ == "__main__":
    # Sample input data
    sample_input = {
        "personal_information": {
            "name": "John Doe",
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

    # Initialize the resume generator with the sample input and template
    generator = ResumeGenerator(user_input=sample_input, template_name="modern_resume", language="en")
    try:
        # Generate the resume
        generator.generate()
    except Exception as e:
        logging.error(f"Error: {e}")
