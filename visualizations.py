"""Data visualization utilities"""
import matplotlib.pyplot as plt
import seaborn as sns
from data_processor import GymDataProcessor

class GymDataVisualizer:
    def __init__(self):
        self.processor = GymDataProcessor()
    
    def plot_missing_values(self):
        """Create heatmap of missing values"""
        data = self.processor.clean_data()
        
        plt.figure(figsize=(12, 8))
        ax = plt.axes()
        sns.heatmap(data.isna().transpose(), cbar=False, ax=ax)
        plt.xlabel("Columns")
        plt.ylabel("Missing Values")
        plt.title("Missing Values Heatmap")
        plt.show()
    
    def plot_muscle_distribution(self):
        """Plot distribution of exercises by muscle group"""
        data = self.processor.clean_data()
        
        plt.figure(figsize=(12, 6))
        muscle_counts = data['Main_muscle'].value_counts()
        muscle_counts.plot(kind='bar')
        plt.title("Exercise Distribution by Muscle Group")
        plt.xlabel("Muscle Group")
        plt.ylabel("Number of Exercises")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()