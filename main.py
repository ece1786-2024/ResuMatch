import csv
import json
import pandas as pd
from resume_parser.resume_parser import ResumeParser
from matching_agent.matching_agent import MatchingAgent
from jobspy import scrape_jobs
from system_ui.ui import UI
from datasets.data import ResumeFeaturesDataset, JobResumeMatchesDataset, LocationValidationDataset, ResumeValidationDataset

model = "gpt-4o"

ui = UI()
def handle_pdf_location_input(pdf_file, location_filter):
    try:
        pdf_file_path = pdf_file.name
        parser = ResumeParser()
        formatted_data = parser.parse(pdf_file_path)
        print("Extracted features:", formatted_data)

        resume_text = parser._extract_text_from_pdf(pdf_file_path)

        formatted_data = json.loads(formatted_data)
        industry = formatted_data.get("industry", "general")
        experience_level = formatted_data.get("experience level", "entry-level")
        location = location_filter.strip()  # Use the provided location filter

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
            country_indeed="USA",
        )

        # Save and display the results
        if jobs is not None and not jobs.empty:
            jobs.to_csv("jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
        else:
            return "No jobs found for the given criteria."

        df = pd.read_csv("jobs.csv")
        print("Job DataFrame Columns:", df.columns)

        # Matching agent to match jobs with the resume
        ma = MatchingAgent(name="Job Fit Determination")
        matches = ma.match_jobs(resume_text, df)

        if matches:
            links = [
                f'<a href="{match["Application_link"]}" target="_blank">{match["Title"]}</a>'
                for match in matches
                if "Application_link" in match and "Title" in match
            ]
            return "<br>".join(links)
        else:
            return "No matching jobs found."
    except Exception as e:
        print(f"Error: {e}")
        return f"An error occurred: {e}"

ui.process_inputs = handle_pdf_location_input
ui.run()
