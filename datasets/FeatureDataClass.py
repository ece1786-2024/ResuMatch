"""
Used for pre-processing
"""

import os
import pandas as pd

class FeatureData:
    def __init__(self, data_path) -> None:
        self.data = pd.read_csv(data_path)
        self.data = self.preprocess_data()
    
    def preprocess_data(self):
        # By default just return the df
        return self.data

class IndustryData(FeatureData):
    def __init__(self) -> None:
        self.name = 'Industry'
        data_path = "hf://datasets/ahmedheakl/resume-atlas/train.csv"
        super().__init__(data_path)
    
    def preprocess_data(self):
        df = self.data
        df = df.rename(
        columns={
            'Category': 'Industry',
            'Text': 'resume_text',
            }
        )

        return df

class ExperienceLevelData(FeatureData):
    def __init__(self) -> None:
        self.name = 'ExperienceLevel'
        data_path = os.path.join('datasets', 'local_datasets', 'ExperienceLevel.csv')
        super().__init__(data_path)


