import requests
import logging
import os
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LLMInference:
    def __init__(self, api_key=None, model_endpoint=None):
        """
        Initialize the LLM inference model with the necessary configurations.
        
        :param api_key: API key for Hugging Face Inference API.
        :param model_endpoint: The specific model endpoint URL on Hugging Face.
        """
        self.api_key = api_key or os.getenv('HUGGINGFACE_API_KEY')
        if not self.api_key:
            raise ValueError("API key for Hugging Face API is not provided. Set the HUGGINGFACE_API_KEY environment variable or pass it explicitly.")

        self.model_endpoint = model_endpoint or os.getenv('HUGGINGFACE_MODEL_ENDPOINT')
        if not self.model_endpoint:
            raise ValueError("Hugging Face model endpoint URL is not provided. Set the HUGGINGFACE_MODEL_ENDPOINT environment variable or pass it explicitly.")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_text(self, prompt):
        """
        Generate text using the Hugging Face model based on the provided prompt.
        
        :param prompt: The prompt to send to the model for text generation.
        :return: Generated text from the model.
        """
        payload = {
            "inputs": prompt,
            "parameters": {"max_length": 200, "temperature": 0.7},
        }

        try:
            logging.info(f"Sending request to Hugging Face model endpoint {self.model_endpoint}...")
            response = requests.post(self.model_endpoint, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                generated_text = response.json()[0]['generated_text'].strip()
                logging.info("Received response from Hugging Face.")
                return generated_text
            else:
                logging.error(f"Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logging.error(f"Error during Hugging Face inference: {str(e)}")
            raise

    def refine_resume_section(self, section_name, input_data):
        """
        Generate or refine a specific section of the resume using LLM.
        
        :param section_name: The section of the resume (e.g., 'summary', 'experience', 'skills').
        :param input_data: The raw input data related to the section.
        :return: Generated or refined text for the resume section.
        """
        prompt = f"Generate a {section_name} for a resume based on the following information:\n{input_data}"
        return self.generate_text(prompt)

# Example function for generating a professional summary
def generate_professional_summary(resume_data):
    """
    Generate a professional summary for the resume using LLM.
    
    :param resume_data: Dictionary containing structured resume content.
    :return: Generated professional summary text.
    """
    llm = LLMInference()

    # Construct a prompt based on input data
    name = resume_data.get("name", "Unknown Candidate")
    job_title = resume_data.get("current_job_title", "Professional")
    years_of_experience = resume_data.get("years_of_experience", 0)
    key_skills = ', '.join(resume_data.get("skills", []))

    # Create a descriptive prompt
    prompt = (f"Write a professional summary for {name}, who is a {job_title} with {years_of_experience} years of experience. "
              f"The candidate is skilled in {key_skills}.")

    return llm.generate_text(prompt)

# Example of how to use the LLMInference class in resume generation
if __name__ == "__main__":
    # Sample structured resume data
    resume_data = {
        "name": "John Doe",
        "current_job_title": "Software Engineer",
        "years_of_experience": 5,
        "skills": ["Python", "Machine Learning", "Django", "API Development"]
    }

    # Initialize the LLM inference
    llm_inference = LLMInference()

    # Generate a professional summary
    professional_summary = generate_professional_summary(resume_data)
    print("Professional Summary:")
    print(professional_summary)

    # Example of generating a specific section (e.g., experience)
    experience_data = """
    Worked as a Software Engineer at TechCorp, developing API solutions for clients. 
    Led a team of engineers to deliver high-quality software solutions.
    """
    generated_experience = llm_inference.refine_resume_section("experience", experience_data)
    print("\nRefined Experience Section:")
    print(generated_experience)
