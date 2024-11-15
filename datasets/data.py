import os
import pandas as pd

class Dataset:
    def __init__(self, csv_name) -> None:
        self.df = pd.read_csv(os.path.join('datasets', 'local_datasets', f'{csv_name}.csv'))

ResumeFeaturesDataset = Dataset('ResumeFeatures')
JobResumeMatchesDataset = Dataset('JobResumeMatches')
LocationValidationDataset = Dataset('Locations')
ResumeValidationDataset = Dataset('Resumes')

