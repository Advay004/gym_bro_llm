"""Configuration settings"""
import os

# Dataset settings
DATASET_PATH = "rishitmurarka/gym-exercises-dataset"
VECTORSTORE_PATH = "./vectorstore"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Valid muscle groups
VALID_MUSCLES = ['Neck', 'Shoulder', 'Upper Arms', 'Forearm', 'Back', 'Chest', 'Hips', 'Thighs', 'Calves']

# Query settings
DEFAULT_NUM_EXERCISES = 5
FUZZY_MATCH_THRESHOLD = 80