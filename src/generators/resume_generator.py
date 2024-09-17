import json
import os
from jinja2 import Environment, FileSystemLoader
from input_parser import parse_resume_input  
from resume_templates import templates      
from pdf_exporter import export_to_pdf       
from llm_inference import expand_content    
from language_support import translate_text  
from resume_score import score_resume        
from ats_optimization import optimize_for_ats  
from version_control import save_version, load_version   

class ResumeGenerator:
    def __init__(self, user_input: dict, template_name: str, language: str = 'en', optimize_ats: bool = True):
        self.user_input = user_input
        self.template_name = template_name
        self.language = language
        self.optimize_ats = optimize_ats
        self.parsed_data = None
        self.final_resume = None
        self.env = Environment(loader=FileSystemLoader('templates'))

    def parse_input(self):
        """
        Parse and validate user input
        """
        self.parsed_data = parse_resume_input(self.user_input)
        if not self.parsed_data:
            raise ValueError("Invalid input data")
    
    def select_template(self):
        """
        Load the selected resume template
        """
        if self.template_name not in templates:
            raise ValueError(f"Template {self.template_name} not found")
        return templates[self.template_name]
    
    def apply_llm(self):
        """
        Use LLM to expand brief inputs (like job responsibilities) into full sentences
        """
        sections = ['work_experience', 'career_summary', 'skills']
        for section in sections:
            if section in self.parsed_data:
                self.parsed_data[section] = expand_content(self.parsed_data[section])
    
    def apply_language_support(self):
        """
        Translate the resume content into the selected language
        """
        if self.language != 'en': 
            for key, value in self.parsed_data.items():
                if isinstance(value, str):
                    self.parsed_data[key] = translate_text(value, target_lang=self.language)
                elif isinstance(value, list):
                    self.parsed_data[key] = [translate_text(item, target_lang=self.language) for item in value]
    
    def optimize_for_ats(self):
        """
        Optimize the resume for ATS systems
        """
        if self.optimize_ats:
            self.parsed_data = optimize_for_ats(self.parsed_data)
    
    def render_resume(self):
        """
        Render the resume with the selected template and parsed data
        """
        template = self.select_template()
        template = self.env.get_template(template['file'])  
        self.final_resume = template.render(self.parsed_data)
    
    def score_resume(self):
        """
        Score the resume and provide feedback
        """
        score = score_resume(self.final_resume)
        print(f"Resume score: {score}/100")
        return score
    
    def save_version(self, version_name: str):
        """
        Save the current resume version for later use
        """
        save_version(version_name, self.final_resume)
    
    def load_version(self, version_name: str):
        """
        Load a saved version of the resume
        """
        self.final_resume = load_version(version_name)
    
    def export_resume(self, export_format='pdf'):
        """
        Export the resume to the desired format (PDF)
        """
        if export_format == 'pdf':
            export_to_pdf(self.final_resume)
        else:
            with open(f'resume.{export_format}', 'w') as file:
                file.write(self.final_resume)
    
    def preview_resume(self):
        """
        Provide a real-time preview of the resume
        """
        print(self.final_resume)
    
    def generate(self):
        """
        Full generation process
        """
        try:
            self.parse_input()
            self.apply_llm()  
            self.apply_language_support()  
            self.optimize_for_ats()  
            self.render_resume()  
            self.score_resume()  
        except Exception as e:
            print(f"Error generating resume: {e}")
    
if __name__ == "__main__":
    sample_input = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone_number": "+1234567890",
        "work_experience": ["Developed software", "Led a team of engineers"],
        "education": ["Bachelor of Computer Science"],
        "skills": ["Python", "Machine Learning"],
        "career_summary": "Experienced software engineer",
    }
    
    # Generate a resume
    generator = ResumeGenerator(user_input=sample_input, template_name="modern", language="en")
    generator.generate()  
    generator.export_resume()  
