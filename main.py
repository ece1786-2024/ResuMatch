import csv
import json
import pandas as pd
from resume_parser.resume_parser import ResumeParser
from location_agent.location_agent_verify import VerifyLocation
from matching_agent.matching_agent import MatchingAgent
from jobspy import scrape_jobs
from system_ui.ui import UI

def resumatch(pdf_file, location_filter):
    try:
        
        ### Perform Resume parsing
        pdf_file_path = pdf_file.name # Get pdf location
        
        resume_parser = ResumeParser(pdf_file_path) # Init the resume parser, which converts to text in init
        resume_text = resume_parser.text # Assign resume test
        
        formatted_data = resume_parser.extract_resume_features()
        print("Extracted features:", formatted_data)

        # Parse the resume features
        formatted_data = json.loads(formatted_data)
        
        industry = formatted_data.get("industry", "general")
        experience_level = formatted_data.get("experience level", "entry-level")
        
        # Parse location and verify via loc. verif agent
        location_agent = VerifyLocation(name="Location Verifier")
        result = location_agent.extract_city_country(location_filter.strip()) # Verify the given location
        
        
        location = result.get("location", "unknown")
        country = result.get("country", "unknown")
        
        if location == "unknown" or country == "unknown":
            print("ERROR: The provided location could not be verified or does not exist.")
        else:

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
                country_indeed=f"{country}",
            )

        # Save and display the results
        if jobs is not None and not jobs.empty:
            jobs.to_csv("jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
        else:
            return "No jobs found for the given criteria."

        df = pd.read_csv("jobs.csv")

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
    
    # If any error is encountered in the system, throw an erorr and shut down
    except Exception as e:
        print(f"Error: {e}")
        return f"An error occurred: {e}"

ui = UI()
ui.process_inputs = resumatch
ui.run()
