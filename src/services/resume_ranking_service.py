import os
import logging
import json
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ResumeRankingService:
    def __init__(self, job_description=None):
        """
        Initialize the ranking service.
        
        :param job_description: Optional job description for comparing resume relevance.
        """
        self.job_description = job_description
        self.keyword_list = self.extract_keywords(job_description) if job_description else []

    def extract_keywords(self, text):
        """
        Extract keywords from a given job description.
        
        :param text: Job description or reference text.
        :return: List of extracted keywords.
        """
        if not text:
            return []

        # Tokenization and basic keyword extraction
        words = text.lower().split()
        keywords = [word.strip(string.punctuation) for word in words if len(word) > 2]
        logging.info(f"Extracted keywords: {keywords}")
        return keywords

    def score_keyword_relevance(self, resume_text):
        """
        Score how well the resume text matches the extracted keywords.
        
        :param resume_text: The text of the resume.
        :return: Relevance score based on keyword matching.
        """
        if not self.keyword_list:
            logging.warning("No job description or keywords provided for comparison.")
            return 0

        resume_words = resume_text.lower().split()
        match_count = sum(1 for word in resume_words if word in self.keyword_list)

        relevance_score = (match_count / len(self.keyword_list)) * 100 if self.keyword_list else 0
        logging.info(f"Keyword relevance score: {relevance_score}%")
        return relevance_score

    def evaluate_formatting(self, resume_text):
        """
        Evaluate the formatting of the resume.
        
        :param resume_text: The text of the resume.
        :return: Formatting score based on various heuristics.
        """
        # Heuristic for formatting: presence of sections like "Experience", "Education", etc.
        sections = ['experience', 'education', 'skills', 'projects']
        formatting_score = sum(1 for section in sections if section in resume_text.lower())

        total_possible = len(sections)
        formatting_percentage = (formatting_score / total_possible) * 100
        logging.info(f"Formatting score: {formatting_percentage}%")
        return formatting_percentage

    def evaluate_content_quality(self, resume_text):
        """
        Evaluate the content quality using TF-IDF and cosine similarity with job description.
        
        :param resume_text: The text of the resume.
        :return: Content quality score based on similarity.
        """
        if not self.job_description:
            logging.warning("No job description provided for content quality evaluation.")
            return 50  # Default score if no comparison is possible

        documents = [resume_text, self.job_description]
        tfidf_vectorizer = TfidfVectorizer().fit_transform(documents)
        cosine_sim = cosine_similarity(tfidf_vectorizer[0:1], tfidf_vectorizer[1:2])

        content_quality_score = cosine_sim[0][0] * 100
        logging.info(f"Content quality score (similarity): {content_quality_score}%")
        return content_quality_score

    def rank_resume(self, resume_text):
        """
        Rank the resume by applying various evaluation metrics.
        
        :param resume_text: The text of the resume.
        :return: A dictionary containing scores and feedback.
        """
        scores = {
            'keyword_relevance': self.score_keyword_relevance(resume_text),
            'formatting': self.evaluate_formatting(resume_text),
            'content_quality': self.evaluate_content_quality(resume_text)
        }

        # Calculate overall score as a weighted average of individual scores
        overall_score = (0.4 * scores['keyword_relevance'] +
                         0.3 * scores['formatting'] +
                         0.3 * scores['content_quality'])
        
        feedback = self.generate_feedback(scores)
        
        result = {
            'overall_score': overall_score,
            'scores': scores,
            'feedback': feedback
        }

        logging.info(f"Overall resume score: {overall_score}%")
        return result

    def generate_feedback(self, scores):
        """
        Generate feedback based on individual scores.
        
        :param scores: Dictionary containing individual scores.
        :return: Feedback as a dictionary.
        """
        feedback = {}

        if scores['keyword_relevance'] < 70:
            feedback['keyword_relevance'] = "Consider including more keywords from the job description to improve relevance."

        if scores['formatting'] < 80:
            feedback['formatting'] = "Improve the resume formatting by ensuring clear sections like 'Experience' and 'Education'."

        if scores['content_quality'] < 75:
            feedback['content_quality'] = "Work on improving the overall clarity and relevance of your resume content."

        if not feedback:
            feedback['overall'] = "Your resume is well-structured and relevant to the job description."

        return feedback


# Example of how to use ResumeRankingService
if __name__ == "__main__":
    # Sample resume text
    resume_text = """
    John Doe
    Software Engineer with 5 years of experience in Python, Django, and Machine Learning.
    Education: B.S. in Computer Science
    Experience: Developed API solutions and managed a team of engineers.
    Skills: Python, Machine Learning, API Development, Leadership
    """

    # Sample job description text
    job_description = """
    We are looking for a Software Engineer with experience in Python, Machine Learning, and leadership abilities.
    The ideal candidate should have a background in API development and team management.
    """

    # Initialize the ranking service with a job description
    ranking_service = ResumeRankingService(job_description=job_description)

    # Rank the resume and get feedback
    ranking_result = ranking_service.rank_resume(resume_text)

    # Display the results
    print("\n--- Resume Ranking Results ---")
    print(json.dumps(ranking_result, indent=4))
