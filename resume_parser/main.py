from resume_parser.resume_parser import ResumeParser

PATH_TO_RESUME = ""

<<<<<<< HEAD
parser = ResumeParser(api_key=api_key, model=model)
resume_path = "C:/Users/Rafay/Downloads/rafay_kalim_fin-2.pdf" # load your resume here
formatted_data = parser.parse(resume_path)
=======
parser = ResumeParser()

formatted_data = parser.parse(PATH_TO_RESUME)
>>>>>>> d12163b8a1f69f69f2397a7b63bc17f25d75a7d0
print("Extracted features:", formatted_data)
