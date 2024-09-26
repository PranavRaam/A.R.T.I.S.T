def score_resume(resume_content: str) -> int:
    """
    Scores the resume based on various factors like length, keyword usage, formatting, etc.
    :param resume_content: The rendered resume content as a string.
    :return: A score between 0 and 100.
    """
    # Example scoring logic: 
    score = 0
    
    # Rule 1: Ensure resume has some key sections
    if "Work Experience" in resume_content:
        score += 20
    if "Education" in resume_content:
        score += 20
    if "Skills" in resume_content:
        score += 20

    # Rule 2: Penalize if resume is too long or too short
    word_count = len(resume_content.split())
    if 400 <= word_count <= 800:
        score += 20
    else:
        score -= 10
    
    # Rule 3: Bonus for including certain keywords (for example, "Python", "Machine Learning", etc.)
    keywords = ["Python", "Machine Learning", "Team Leadership"]
    for keyword in keywords:
        if keyword in resume_content:
            score += 5

    # Rule 4: Deduct points for missing contact information
    if "Phone" not in resume_content or "Email" not in resume_content:
        score -= 20

    # Ensure score is between 0 and 100
    score = max(0, min(100, score))

    return score
