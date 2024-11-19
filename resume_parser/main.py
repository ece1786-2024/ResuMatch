from resume_parser.resume_parser import ResumeParser

PATH_TO_RESUME = ""

parser = ResumeParser()
resume_path = "C:/Users/Rafay/Downloads/rafay_kalim_fin.pdf" # load your resume here
formatted_data = parser.parse(resume_path)
print("Extracted features:", formatted_data)
