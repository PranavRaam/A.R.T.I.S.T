import logging
from huggingface_hub import InferenceClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LLMInference:
    def __init__(self, api_key, model_id=None):
        """
        Initialize the LLM inference model using Hugging Face InferenceClient.
        
        :param api_key: API key for Hugging Face Inference API.
        :param model_id: (Optional) The specific model ID on Hugging Face.
        """
        self.api_key = api_key
        self.model_id = model_id or "mistralai/Mistral-7B-Instruct-v0.3"

        if not self.api_key:
            raise ValueError("API key for Hugging Face API is required.")

        # Initialize Hugging Face InferenceClient
        self.client = InferenceClient(token=self.api_key)

    def _send_request(self, prompt, model_id=None, temperature=0.7):
        """
        Sends a request to the Hugging Face Inference API for text generation.
        
        :param prompt: The prompt to send to the model.
        :param model_id: (Optional) Specific model ID to override the default one.
        :param temperature: Controls randomness in generation.
        :return: Generated text or None in case of error.
        """
        selected_model = model_id or self.model_id
        logging.info(f"Sending request to Hugging Face model {selected_model}...")

        try:
            # Sending the text generation request
            response = self.client.text_generation(prompt, model=selected_model, temperature=temperature)
            
            # Check if the response is a string or dictionary
            if isinstance(response, dict):
                # If it's a dictionary, extract the 'generated_text'
                generated_text = response.get('generated_text', '').strip()
                if generated_text:
                    logging.info("Response received from Hugging Face.")
                    return generated_text
                else:
                    logging.error("No response or empty result from Hugging Face.")
                    return None
            elif isinstance(response, str):
                # If the response is a string, log it and return the string itself
                logging.info("Response is a string, returning the raw response.")
                return response.strip()
            else:
                # Handle unexpected response types
                logging.error(f"Unexpected response type: {type(response)}")
                return None
        except Exception as e:
            logging.error(f"Error during Hugging Face inference: {str(e)}")
            return None


    def generate_text(self, prompt, model_id=None, temperature=0.7):
        """
        Public method to generate text using the Hugging Face model.
        
        :param prompt: The text prompt.
        :param model_id: Optional, if you want to specify another model for this call.
        :param max_length: Maximum text length.
        :param temperature: The randomness of text generation.
        :return: Generated text.
        """
        return self._send_request(prompt, model_id=model_id, temperature=temperature)

    def refine_resume_section(self, section_name, input_data):
        """
        Generate or refine a specific section of a resume using LLM.
        
        :param section_name: The section name (e.g., 'summary', 'experience', 'skills').
        :param input_data: Raw data relevant to the section.
        :return: Refined text for the resume section.
        """
        prompt = f"Generate a {section_name} for a resume based on the following information:\n{input_data}"
        return self.generate_text(prompt)

# Helper function for generating a professional summary
def generate_professional_summary(llm_instance, resume_data):
    """
    Generate a professional summary for a resume using LLM.
    
    :param llm_instance: Instance of the LLMInference class.
    :param resume_data: Structured dictionary with resume info.
    :return: Generated professional summary text.
    """
    name = resume_data.get("name", "Unknown Candidate")
    job_title = resume_data.get("current_job_title", "Professional")
    years_of_experience = resume_data.get("years_of_experience", 0)
    key_skills = ', '.join(resume_data.get("skills", []))

    prompt = (f"Write a professional summary for {name}, who is a {job_title} with {years_of_experience} years of experience. "
              f"The candidate is skilled in {key_skills}.")
    return llm_instance.generate_text(prompt)

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
    llm_inference = LLMInference(api_key="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")

    # Generate a professional summary
    professional_summary = generate_professional_summary(llm_inference, resume_data)
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
