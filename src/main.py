import os
import json
import logging
from src.generators.input_parser import parse_resume_input, ValidationError
from src.generators.resume_generator import ResumeGenerator
from src.generators.pdf_exporter import export_to_pdf
from src.models.llm_inference import LLMInference
from src.services.resume_ranking_service import ResumeRankingService
from src.utils.scoring_utils import score_resume
from src.utils.template_renderer import TemplateRenderer
from dotenv import load_dotenv

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        # Step 1: Parse the Input Data
        logging.info("Parsing input data...")
        input_file_path = os.path.join("data", "sample_input.json")
        
        # Load the input file as a dictionary
        with open(input_file_path, 'r') as file:
            input_data = json.load(file)

        # Validate the loaded data
        user_data = parse_resume_input(input_data)

        # Step 2: Generate Resume
        logging.info("Generating resume content...")
        template_name = "modern_resume.tex"
        resume_gen = ResumeGenerator(user_input=user_data, template_name=template_name)
        resume_gen.generate()

        # Verify parsed_data before rendering template
        if resume_gen.parsed_data is None:
            raise ValueError("Parsed data is None. Please check resume generation logic.")
        elif not isinstance(resume_gen.parsed_data, dict):
            raise ValueError("Parsed data is not a dictionary. It should be in key-value format.")
        
        logging.info(f"Parsed Data: {resume_gen.parsed_data}")

        # Step 3: Invoke LLM for Enhancements (optional)
        logging.info("Enhancing content with LLM...")
        api_key = os.getenv("LLM_API_KEY")
        if not api_key:
            raise ValueError("API key for LLM not set")
        llm_infer = LLMInference(api_key=api_key)

        # Step 4: Render LaTeX Template
        logging.info("Rendering resume template...")
        template_dir = "/home/thelone/Projects/Artist/src/templates/basic"  # Update the path as needed
        template_renderer = TemplateRenderer(template_dir=template_dir)

        # Rendering LaTeX template with the parsed data from the resume generator
        rendered_resume = template_renderer.render_template(template_name, context=resume_gen.parsed_data)

        # Step 5: Export to PDF
        logging.info("Exporting resume to PDF...")
        pdf_exporter = export_to_pdf(rendered_resume)
        pdf_file_path = pdf_exporter.export("generated_resume.pdf")

        # Step 6: Rank the Resume
        logging.info("Ranking the resume...")
        ranking_service = ResumeRankingService()
        score = ranking_service.rank_resume(pdf_file_path)

        # Step 7: Display Results
        logging.info(f"Resume successfully generated and exported to {pdf_file_path}")
        logging.info(f"Resume score: {score}/100")

        # Optional: Apply additional scoring utilities
        calculated_score = score_resume(score, user_data)
        logging.info(f"Adjusted Resume Score: {calculated_score}/100")
    
    except ValidationError as ve:
        logging.error(f"Validation error: {ve}")
    except Exception as e:
        logging.exception("An unexpected error occurred")

if __name__ == "__main__":
    main()
