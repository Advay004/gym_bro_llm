"""Data loading and preprocessing"""
import pandas as pd
import kagglehub
import os
from config import DATASET_PATH

class GymDataProcessor:
    def __init__(self):
        self.data = None
        self.processed_data = None
    
    def download_and_load_data(self):
        """Download and load the gym dataset"""
        if self.data is not None:
            return self.data
            
        path = kagglehub.dataset_download(DATASET_PATH)
        print(f"Dataset downloaded to: {path}")
        
        self.data = pd.read_csv(f"{path}/gym_exercise_dataset.csv")
        return self.data
    
    def clean_data(self):
        """Clean and preprocess the data"""
        if self.data is None:
            self.download_and_load_data()
        
        # Drop unnecessary columns
        columns_to_drop = ['Stabilizer_Muscles', 'Antagonist_Muscles', 'parent_id', 'Dynamic_Stabilizer_Muscles']
        self.processed_data = self.data.drop(columns_to_drop, axis=1)
        
        return self.processed_data
    
    def generate_exercise_descriptions(self):
        """Generate LLM-ready descriptions for exercises"""
        if self.processed_data is None:
            self.clean_data()
        
        def _generate_description(row):
            return f"""
            Exercise Name: {row['Exercise Name']}
            Equipment: {row['Equipment']}
            Variation: {row['Variation']}
            Utility: {row['Utility']}
            Mechanics: {row['Mechanics']}
            Force: {row['Force']}
            Preparation: {row['Preparation']}
            Execution: {row['Execution']}
            Difficulty (1-5): {row['Difficulty (1-5)']}
            Main Muscle: {row['Main_muscle']}
            Synergist Muscles: {row['Synergist_Muscles']}
            Secondary Muscles: {row['Secondary Muscles']}
            """
        
        self.processed_data['llm_entry'] = self.processed_data.apply(_generate_description, axis=1)
        return self.processed_data