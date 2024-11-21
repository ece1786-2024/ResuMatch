from resume_validation_agent.resume_validation_agent import ResumeValidationAgent
from datasets.data import ResumeValidationDataset

# print(ResumeFeaturesDataset.df.head())
rv_agent = ResumeValidationAgent('resume-validator')
print(ResumeValidationDataset.df.head())
print(int(rv_agent.validate('this is some random gibberish')))

rv_agent.evaluate_dataset(ResumeValidationDataset.df)
