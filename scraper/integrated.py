import csv
import json
import pandas as pd
from resume_parser.resume_parser import ResumeParser
from matching_agent.matching_agent import MatchingAgent
from jobspy import scrape_jobs

parser = ResumeParser()
resume_path = r"G:\job applications\Karanbir.s.brar.pdf" # load your resume here
formatted_data = parser.parse(resume_path)
print("Extracted features:", formatted_data)

resume_text= parser._extract_text_from_pdf(resume_path)

formatted_data = json.loads(formatted_data)
industry = formatted_data.get("industry")
experience_level = formatted_data.get("experience level")
location = "San Francisco, CA"  # Default location; adjust if location is available in the resume data

# Create search terms dynamically
search_term = f"{experience_level} {industry}".lower()

# Scrape jobs
jobs = scrape_jobs(
    site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor", "google"],
    search_term=search_term,
    google_search_term=f"{search_term} jobs near {location}",
    location=location,
    results_wanted=20,
    hours_old=72,
    country_indeed='USA',
)

# Save and display the results
if jobs is not None and not jobs.empty:
    jobs.to_csv("jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
else:
    print("No jobs found.")

df=pd.read_csv('jobs.csv')
print(df.columns)

ma = MatchingAgent(name="Job Fit Determination")
ma.match_jobs(resume_text,df)
