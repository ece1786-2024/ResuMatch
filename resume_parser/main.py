from resume_parser.core import ResumeParser

api_key = "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"
model = "gpt-4o"

parser = ResumeParser(api_key=api_key, model=model)
resume_path = "C:/Users/Rafay/Downloads/rafay_kalim_fin-2.pdf" # load your resume here
formatted_data = parser.parse(resume_path)
print("Extracted features:", formatted_data)
