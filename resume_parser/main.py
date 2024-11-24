from .resume_parser import ResumeParser

PATH_TO_RESUME = ""

parser = ResumeParser()
resume_path = "C:/Users/bartc/Desktop/job app/Resume_Cui,W.pdf" # load your resume here
formatted_data = parser.parse(resume_path)
print("Extracted features:", formatted_data)
