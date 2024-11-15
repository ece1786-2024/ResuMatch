from resume_parser.core import ResumeParser

api_key = ""
model = "gpt-4o"

parser = ResumeParser(api_key=api_key, model=model)
resume_path = "C:/Users/Rafay/Downloads/rafay_kalim_fin.pdf" # load your resume here
formatted_data = parser.parse(resume_path)
print("Extracted features:", formatted_data)
