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


# # Example JSON string
# formatted_data = '{"industry": "Data analytics and machine learning", "experience level": "junior"}'

# formatted_data = json.loads(formatted_data)


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
matches=[]
match_scores = {"Good Fit": 3, "Potential Fit": 2, "No fit": 1}
job_agent = MatchingAgent(name="JobMatcher", sys_prompt="Match resumes with job descriptions.",model="gpt-4o")
for index, row in df.iterrows():
    job_description = row["description"]
    #apllication_link = row[""]
    # Get match result from agent
    match_result = job_agent.evaluate_match(resume_text, job_description)
    match_category = match_result["fit"]  # Extract the match category
    
    # Append job with its score
    matches.append({
        "Application_link": row["job_url"],
        "match_category": match_category,
        "score": match_scores.get(match_category, 0)
    })

# Sort matches by score in descending order
top_matches = sorted(matches, key=lambda x: x["score"], reverse=True)[:5]

for job in top_matches:
    print(f"Match Category: {job['match_category']}, Score: {job['score']}")
    print(f"application_link: {job['Application_link']}\n")
