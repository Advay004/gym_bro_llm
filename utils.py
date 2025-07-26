import re
from difflib import get_close_matches

MUSCLE_LIST = [
    "Neck", "Shoulder", "Upper Arms", "Forearm", "Back",
    "Chest", "Hips", "Thighs", "Calves"
]

def simple_tokenize(text):
    return re.findall(r'\w+', text.lower())

def correct_muscles_from_query(query):
    tokens = simple_tokenize(query)
    corrected = []
    for token in tokens:
        match = get_close_matches(token.title(), MUSCLE_LIST, n=1, cutoff=0.7)
        if match:
            corrected.append(match[0])
    return list(set(corrected))  # remove duplicates

def extract_number_from_query(query):
    match = re.search(r'\b(\d+)\b', query)
    return int(match.group(1)) if match else 5  # Default to 5
