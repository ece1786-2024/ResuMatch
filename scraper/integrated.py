import csv
import json
import pandas as pd
from resume_parser.resume_parser import ResumeParser
from matching_agent.matching_agent import MatchingAgent
from jobspy import scrape_jobs

# PATH_TO_RESUME = r"G:\job applications\Karanbir.s.brar.pdf"

parser = ResumeParser()
resume_path = r"G:\job applications\Karanbir.s.brar.pdf" # load your resume here
formatted_data, resume_text = parser.parse(resume_path)
print("Extracted features:", formatted_data)



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
    #print(f"Found {len(jobs)} jobs")
    #print(jobs.head())
    jobs.to_csv("jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
else:
    print("No jobs found.")

df=pd.read_csv('jobs.csv')
print(df.columns)

ma = MatchingAgent(name="Job Fit Determination", sys_prompt="evaluate if the job descripton a potential match based on resume_text",model="gpt-4o")
ma.match_jobs(resume_text,df)
