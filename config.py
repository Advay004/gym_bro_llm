import os

# Dataset settings
DATASET_PATH = "rishitmurarka/gym-exercises-dataset"
VECTORSTORE_PATH = "./data/vectorstore"  # Changed path for better organization
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Valid muscle groups
VALID_MUSCLES = ['Neck', 'Shoulder', 'Upper Arms', 'Forearm', 'Back', 'Chest', 'Hips', 'Thighs', 'Calves']

# Query settings
DEFAULT_NUM_EXERCISES = 5
FUZZY_MATCH_THRESHOLD = 80

# Create data directory if it doesn't exist
os.makedirs(os.path.dirname(VECTORSTORE_PATH), exist_ok=True)