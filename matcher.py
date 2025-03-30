
import re
import json
import nltk
import spacy
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Download required data
nltk.download("punkt")
nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    """Tokenize, clean, and lemmatize text using spaCy."""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove special characters
    return [token.lemma_ for token in nlp(text) if not token.is_stop]  # Return lemmatized words

def extract_keywords(text, top_n=10):
    """Extract top N keywords from text using TF-IDF."""
    words = clean_text(text)
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(top_n)]  # Return top keywords

def fuzzy_keyword_match(resume_tokens, keywords):
    """Find missing keywords using fuzzy matching."""
    missing = []
    for keyword in keywords:
        found = any(nltk.edit_distance(keyword, token) <= 2 for token in resume_tokens)  # Allow minor differences
        if not found:
            missing.append(keyword)
    return missing

def calculate_match(resume_text, job_description):
    """Calculate similarity using domain-specific keywords & TF-IDF."""
    resume_tokens = clean_text(resume_text)
    job_tokens = clean_text(job_description)

    # Extract domain-specific keywords from the JD
    job_keywords = extract_keywords(job_description, top_n=10)

    # Find missing keywords in the resume
    missing_keywords = fuzzy_keyword_match(resume_tokens, job_keywords)

    # Compute semantic similarity using TF-IDF + Cosine Similarity
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
    similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0] * 100  # Scale to percentage

    # Apply fuzzy keyword weighting
    fuzzy_score = 100 - (len(missing_keywords) * 5)  # Penalize missing skills
    final_score = (similarity * 0.6) + (fuzzy_score * 0.4)  # Weighted combination

    # Final recommendation
    recommendation = "Highly Fit" if final_score >= 80 else "Partially Fit" if final_score >= 50 else "Not Fit"

    return {
        "percentage_match": round(max(final_score, 0), 2),
        "missing_keywords": missing_keywords,
        "final_thoughts": f"Missing domain skills: {', '.join(missing_keywords) if missing_keywords else 'None'}",
        "recommendation": recommendation
    }

def generate_recommendation(match_result):
    """Generate recommendation based on match percentage"""
    if not match_result or "percentage_match" not in match_result or "missing_keywords" not in match_result:
        return "Error", "Invalid match result data"

    percentage = match_result["percentage_match"]
    missing = match_result["missing_keywords"]

    if percentage >= 80:
        recommendation = "Fit"
        thoughts = "Candidate is an excellent fit for the role."
    elif percentage >= 60:
        recommendation = "Potential Fit"
        thoughts = "Candidate has most required skills but may need some training."
    elif percentage >= 40:
        recommendation = "Marginal Fit"
        thoughts = "Candidate has some relevant skills but significant gaps exist."
    else:
        recommendation = "Not Fit"
        thoughts = "Candidate does not meet the basic requirements for this role."

    if missing:
        thoughts += f" Missing keywords: {', '.join(missing[:5])}" + ("..." if len(missing) > 5 else "")

    return recommendation, thoughts