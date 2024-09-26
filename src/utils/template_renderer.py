import os

from jinja2 import Environment, FileSystemLoader, TemplateNotFound

class TemplateRenderer:
    def __init__(self, template_dir: str):
        """
        Initializes the Jinja2 environment and sets up the template directory.
        :param template_dir: Path to the directory where templates are stored.
        """
        if not os.path.isdir(template_dir):
            raise FileNotFoundError(f"Template directory '{template_dir}' does not exist.")
        
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template_dir = template_dir  # Store the template directory path
    
    def render_template(self, template_name: str, context: dict) -> str:
        """
        Render the given template with the provided context (data).
        :param template_name: Name of the template file (e.g., 'modern_template.tex').
        :param context: Dictionary with data to be filled into the template.
        :return: Rendered template as a string.
        """
        try:
            template = self.env.get_template(template_name)
            return template.render(context)
        except TemplateNotFound:
            raise ValueError(f"Template '{template_name}' not found in the template directory.")
        except Exception as e:
            raise RuntimeError(f"Error rendering template: {str(e)}")

    def list_available_templates(self) -> list:
        """
        Lists all available templates in the template directory.
        :return: List of template names.
        """
        template_files = os.listdir(self.template_dir)
        return [template_file for template_file in template_files if template_file.endswith('.tex')]

# Example usage:
if __name__ == "__main__":
    template_dir = "/home/thelone/Projects/Artist/src/templates/basic"  # Directory with your template
    template_name = "modern_resume.tex"  # Name of your template

    # Parsed data (replace with your actual parsed data)
    parsed_data = {
        'name': 'John Doe',
        'email': 'john.doe@gmail.com',
        'phone': '+91 1288 234 586',
        'work_experience': [
            {
                'job_title': 'Software Engineer',
                'company_name': 'ABC Corp',
                'start_date': 'January 2020',
                'end_date': 'Present',
                'responsibilities': ['Developed software', 'Led a team of engineers'],
                'achievements': ['Improved code efficiency', 'Reduced deployment time']
            }
        ],
        'education': {
            'institution': 'XYZ University',
            'degree': 'Bachelor of Computer Science',
            'graduation_year': 'June 2018'
        },
        'skills': {
            'technical_skills': ['Python', 'Machine Learning'],
            'soft_skills': ['Communication', 'Teamwork'],
            'tools': ['Git', 'Docker']
        },
        'career_summary': 'To work as a software engineer in a challenging environment.',
        'hobbies': ['Reading', 'Coding']
    }

    # Initialize the renderer
    template_renderer = TemplateRenderer(template_dir=template_dir)

    # Render the template with parsed data
    try:
        rendered_resume = template_renderer.render_template(template_name, context=parsed_data)
        print(rendered_resume)  # or save it to a file if needed
    except RuntimeError as e:
        print(f"Error: {str(e)}")
