from agent.agent import Agent
import json
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import pandas as pd

class MatchingAgent(Agent):
    def __init__(self, 
                 name,
                 model="gpt-4o", 
                 max_tokens=2500,
                 response_format={"type": "json_object"},
                 temperature=0.15):
        
        super().__init__(name, model, max_tokens, response_format, temperature)
        
        self.match_categories = ["Good Fit", "Potential Fit", "No fit"]

        # ### Experiment 2        
        # self.sys_prompt = """Please respond in JSON format {'result' : 'PREDICTION'}.
        
        #                 You are a fantastic freelance recruiter and you specialize in finding the right fit for resumes and jobs.
                        
        #                 I'll provide you with a Resume and Job Description.
        #                 Determine if the resume is a Good Fit, Potential Fit, or No Fit. 
                        
        #                 A Good Fit is one where the resume and experience closely align and have many matching skills and experiences.
        #                 A Potential Fit is one where there are some matching traits, but not as many as a Good Fit.
        #                 No Fit is one where there are not a lot of matching traits, if at all, not suited for the role.
                        
                        
        #                 Only output one of, Good Fit, Potential Fit, or No Fit """
        
        ### Experiment 3
        # self.sys_prompt = """Please respond in JSON format {'result' : 'PREDICTION'}.

        #         You are a fantastic freelance recruiter and you specialize in finding the right fit for resumes and jobs.
                
        #         I'll provide you with a Resume and Job Description.
        #         Determine if the resume is a Good Fit, Potential Fit, or No Fit for the job description. 
                
        #         1. Good Fit:
        #         A "Good Fit" indicates that the candidate's qualifications, skills, and experiences closely align with the requirements of the job description. The resume showcases relevant work experience, education, and skills that match the job's key responsibilities and desired qualifications. The candidate demonstrates a strong potential to excel in the role and contribute positively to the organization.
                
        #         2. Potential Fit:
        #         A "Potential Fit" suggests that the candidate possesses some relevant skills and experiences that align with the job description, but there are notable gaps or less direct relevance. The resume may include transferable skills or experiences that could be beneficial, but the candidate may lack specific qualifications or experience that are critical for the role. This category indicates that the candidate could be trained or developed into a suitable candidate with the right support.
                
        #         3. No Fit:
        #         A "No Fit" means that the candidate's qualifications, skills, and experiences do not align with the job description. The resume lacks relevant experience, education, or skills that are necessary for the role. There may be significant discrepancies between what the job requires and what the candidate offers, indicating that the candidate is unlikely to succeed in the position without substantial retraining or a change in career direction.
                
        #         Only output one of, Good Fit, Potential Fit, or No Fit """
        
        ### Experiemnt 4 (7)
        # self.sys_prompt = """Please respond in JSON format {'result' : 'PREDICTION'}.

        #         You are a fantastic freelance recruiter and you specialize in finding the right fit for resumes and jobs. You excel at finding if resumes are good fits for job descriptions. 
        #         You are able to determine if there's overlap indicating a good fit. If there's some overlap indicating a potential fit. And if there's absolutely no overlap indicating no fit.
                
        #         I'll provide you with a Resume and Job Description.
        #         Determine if the resume is a Good Fit, Potential Fit, or No Fit for the job description. 
                
        #         1. Good Fit:
        #         A "Good Fit" indicates that the candidate aligns with the job description. 
        #         Output "Good Fit" if theres some overlapping traits between the resume and job description.
                
        #         2. Potential Fit:
        #         A "Potential Fit" suggests that the candidate possesses some relevant skills and experiences that align with the job description, but there are notable gaps or less direct relevance.
        #         Output "Potential Fit" if there's some relation between the resume and job description.
                
        #         3. No Fit:
        #         A "No Fit" means that the candidate's qualifications, skills, and experiences do not align with the job description. 
        #         Only output "No Fit" if the resume has absolutely nothing to do with the job description.
                
        #         Only output one of, Good Fit, Potential Fit, or No Fit """
                
        
        # ### Experiemnt 5 (8)
        # self.sys_prompt = """Please respond in JSON format {'result' : 'PREDICTION'}.

        #         You are a fantastic freelance recruiter and you specialize in finding the right fit for resumes and jobs. You excel at finding if resumes are good fits for job descriptions. 
        #         You are able to determine if there's overlap indicating a good fit. If there's some overlap indicating a potential fit. And if there's absolutely no overlap indicating no fit.
                
        #         I'll provide you with a Resume and Job Description.
        #         Determine if the resume is a Good Fit, Potential Fit, or No Fit for the job description. 
                
        #         1. Good Fit:
        #         A "Good Fit" indicates that the candidate aligns with the job description. 
        #         Output "Good Fit" if half or more than half the job description is covered by the resume
                
        #         2. Potential Fit:
        #         A "Potential Fit" suggests that the resume somewhat aligns with the job description, but there's some gaps.
        #         Output "Potential Fit" if about half or less of the job description is covered by the resume.
                
        #         3. No Fit:
        #         A "No Fit" means that the candidate's qualifications, skills, and experiences do not align with the job description. 
        #         Output "No Fit" if there's near no items in the job description covered by the resume.
                
        #         Only output one of, Good Fit, Potential Fit, or No Fit """
        
        ## Experiment 6, (9)
        self.sys_prompt = """Please respond in JSON format {'result' : 'PREDICTION'}.

                You are a fantastic freelance recruiter and you specialize in finding the right fit for resumes and jobs. You excel at finding if resumes are good fits for job descriptions. 
                You are able to determine if there's overlap indicating a good fit. If there's some overlap indicating a potential fit. And if there's absolutely no overlap indicating no fit.
                
                I'll provide you with a Resume and Job Description.
                Determine if the resume is a Good Fit, Potential Fit, or No Fit for the job description. 
                
                1. Good Fit:
                A "Good Fit" indicates that the candidate aligns with the job description. 
                Output "Good Fit" if theres some overlapping traits between the resume and job description.
                
                2. Potential Fit:
                A "Potential Fit" suggests that the candidate possesses some relevant skills and experiences that align with the job description, but there are notable gaps or less direct relevance.
                Output "Potential Fit" if there's some relation between the resume and job description.
                
                3. No Fit:
                A "No Fit" means that the candidate's qualifications, skills, and experiences do not align with the job description. 
                Only output "No Fit" if the resume has absolutely nothing to do with the job description.
                
                Only output one of, Good Fit, Potential Fit, or No Fit """

    def evaluate_match(self, resume_text, job_description):
        """
        Evaluate if a resume is a good match for a job description.
        
        :param resume_text: The text content of the resume
        :param job_description: The text content of the job description
        :return: Dictionary containing the match evaluation
        """
        # Summarize the resume text
        resume_summary = self.generate_response([{"role": "user", "content": f"Please breifly summarize the following resume in JSON format:\n{resume_text}"}])
        
        # # Summarize the job description text
        job_description_summary = self.generate_response([{"role": "user", "content": f"Please breifly summarize the following job description in JSON format:\n{job_description}"}])


        # print(resume_summary)
        
        # print(job_description_summary)        
        # Prepare the prompt for the main evaluation
        prompt = f"Here's the  Resume:\n{resume_summary}\n\nHere's the  Job Description:\n{job_description_summary}"

        messages = [
            {"role": "system", "content": self.sys_prompt},  # You can keep this if needed for the main evaluation
            {"role": "user", "content": prompt}
        ]
        
        response = self.generate_response(messages)
        
        return response

    def evaluate_dataset(self, df):
        """
        Evaluate the matching predictions on a test dataset.
        Assumes first column is resume_text, second is job_description, 
        and third column is the fit label.

        :param df: DataFrame with columns ['resume_text', 'job_description', 'fit']
        :return: Success rate as a percentage
        """
        correct_predictions = 0
        total = len(df)

        true_labels = []
        predicted_labels = []

        for index, row in df.iterrows():
            print(index)
            resume_text = row['resume_text']
            job_description = row['job_description_text']
            expected_fit = row['label']
            
            match_result = self.evaluate_match(resume_text, job_description)

            json_response = json.loads(match_result)
            print(json_response)
            
            # Collect true and predicted labels
            true_labels.append(expected_fit)
            predicted_labels.append(json_response['result'])
            
            if json_response['result'] == expected_fit:
                correct_predictions += 1
            
            

        success_rate = (correct_predictions / total) * 100 if total > 0 else 0
        print(f"Success rate: {success_rate:.2f}%")
        
        # Create the confusion matrix
        cm = confusion_matrix(true_labels, predicted_labels, labels=["Good Fit", "Potential Fit", "No Fit"])

        # Convert to DataFrame for better visualization
        cm_df = pd.DataFrame(cm, index=["Good Fit", "Potential Fit", "No Fit"], columns=["Good Fit", "Potential Fit", "No Fit"])

        # Print the confusion matrix
        print("\nJob Fit Agent Predictive power:")
        print(cm_df)

        # Display the confusion matrix using matplotlib
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Good Fit", "Potential Fit", "No Fit"])
        disp.plot(cmap=plt.cm.Blues)
        plt.title("Job Fit Agent Predictive power")
        plt.show()

        print(f"True labels {true_labels}")
        print(f"Predicted labels {predicted_labels}")
        return success_rate
    
    def match_jobs(self,resume_text,df):
        matches=[]
        match_scores = {"Good Fit": 3, "Potential Fit": 2, "No fit": 1}
        for index, row in df.iterrows():
            job_description = row['description']
            match_result = self.evaluate_match(resume_text, job_description)
            match_result = json.loads(match_result)
            if match_result['result']== "Good Fit":
                matches.append({
                    "Title": row["title"],
                    "Application_link": row["job_url"],
                    "Fit": match_result['result']
                })

        for job in matches:
            print(f"application_link: {job['Application_link']}, Score: {job['Fit']}\n")
        return matches
