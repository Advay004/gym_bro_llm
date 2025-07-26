"""Query parsing and processing"""
import re
import spacy
from rapidfuzz import process
from config import VALID_MUSCLES, DEFAULT_NUM_EXERCISES, FUZZY_MATCH_THRESHOLD

class QueryProcessor:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Warning: spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
    
    def correct_muscle_name(self, user_input, threshold=FUZZY_MATCH_THRESHOLD):
        """Correct misspelled muscle names using fuzzy matching"""
        match, score, _ = process.extractOne(user_input, VALID_MUSCLES)
        return match if score >= threshold else None
    
    def parse_query(self, query: str):
        """Parse user query to extract number of exercises and target muscles"""
        # Extract number
        number_match = re.search(r'(\d+)', query)
        num_exercises = int(number_match.group(1)) if number_match else DEFAULT_NUM_EXERCISES
        
        found_muscles = set()
        
        if self.nlp:
            # Use spaCy for better parsing
            doc = self.nlp(query.lower())
            for token in doc:
                corrected = self.correct_muscle_name(token.text.capitalize())
                if corrected:
                    found_muscles.add(corrected)
        else:
            # Fallback: simple word matching
            words = query.lower().split()
            for word in words:
                corrected = self.correct_muscle_name(word.capitalize())
                if corrected:
                    found_muscles.add(corrected)
        
        return num_exercises, list(found_muscles)