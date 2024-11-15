from resume_parser.resume_parser import ResumeParser

PATH_TO_RESUME = ""

parser = ResumeParser()

formatted_data = parser.parse(PATH_TO_RESUME)
print("Extracted features:", formatted_data)
