import pandas as pd

def get_resume_industry_dataset():
    """
    Returns pandas dataframe with two columns:
        1. Industry: Has industry-like feature (eg: Accountant, Mechanical Engineer, etc)
        2. resume_text: Has resume text
    """
    df = pd.read_csv("hf://datasets/ahmedheakl/resume-atlas/train.csv")

    df = df.rename(
        columns={
            'Category': 'Industry',
            'Text': 'resume_text',
        }
    )
    
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

print(get_resume_industry_dataset())
