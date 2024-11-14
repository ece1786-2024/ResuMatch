import os
import pandas as pd
from datasets.FeatureDataClass import IndustryData, ExperienceLevelData

def get_resume_features_dataset():
    """
    Returns pandas dataframe with resume text column and feature columns:
        1. resume_text: Has resume text
        2...n feature1, feature2, ..., featuren

        Current Features:
            1. Industry: Has industry-like feature (eg: Accountant, Mechanical Engineer, etc)
            2. ExperienceLevel: One of {Entry, Junior, Mid, Senior, Executive}
    """

    df = pd.read_csv(os.path.join('datasets', 'local_datasets', 'ResumeFeatures.csv'))
    
    return df

def get_resume_job_match_dataset(train_or_test="train"):
    """
    Returns pandas dataframe with three columns:
        1. resume_text: Has resume text
        2. job_description_text: Has job description text
        3. label: One of {No Fit, Good Fit, Potential Fit}, whether resume and job description are a fit
    """

    splits = {'train': 'train.csv', 'test': 'test.csv'}
    df = pd.read_csv("hf://datasets/cnamuangtoun/resume-job-description-fit/" + splits[train_or_test])

    return df
