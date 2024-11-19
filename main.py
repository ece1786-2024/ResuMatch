from resume_parser.resume_parser import ResumeParser
from datasets.data import ResumeFeaturesDataset, JobResumeMatchesDataset, LocationValidationDataset, ResumeValidationDataset

model = "gpt-4o"

parser = ResumeParser()
resume_path = "C:/Users/Rafay/Downloads/rafay_kalim_fin.pdf" # load your resume here
formatted_data = parser.parse(resume_path)
print("Extracted features:", formatted_data)
