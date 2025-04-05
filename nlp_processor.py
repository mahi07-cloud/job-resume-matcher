import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Define key skills dictionary with weights
key_skills = {"python": 2, "nlp": 2, "flask": 2, "sql": 2, "machine learning": 2}

def extract_skills(text):
    """Extract skills/keywords from text using SpaCy and weighted key skills."""
    doc = nlp(text.lower())  # Process text with SpaCy
    skills = []
    
    # Add weighted key skills to the skills list
    for token in doc:
        if token.text in key_skills:
            skills.extend([token.text] * key_skills[token.text])  # Weight key skills
        elif token.pos_ in ["NOUN", "PROPN"] and not token.is_stop:
            skills.append(token.text)
    
    return " ".join(skills)  # Return space-separated skills

def calculate_similarity(job_desc, resume):
    """Calculate similarity between job description and resume using TF-IDF."""
    # Extract skills from both job description and resume
    job_skills = extract_skills(job_desc)
    resume_skills = extract_skills(resume)
    
    # If no skills were extracted from either job description or resume, return 0 similarity
    if not job_skills or not resume_skills:
        return 0.0
    
    # Use TF-IDF to vectorize the extracted skills
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([job_skills, resume_skills])
    
    # Compute cosine similarity between the two TF-IDF vectors
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    return round(similarity * 100, 2)  # Return similarity as a percentage
