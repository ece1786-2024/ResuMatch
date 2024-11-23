from agent.agent import Agent
import json
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import pandas as pd

class MatchingAgent(Agent):
    def __init__(self, 
                 name,
                 model="gpt-4o", 
                 max_tokens=15,
                 response_format={"type": "json_object"},
                 temperature=0.5):
        
        super().__init__(name, model, max_tokens, response_format, temperature)
        
        self.match_categories = ["Good Fit", "Potential Fit", "No fit"]
        self.sys_prompt = "Please respond in JSON format {'result' : 'PREDICTION'}. Determine if the resume is a Good Fit, Potential Fit, or No Fit. Determing if the resume is a Good Fit, Potential Fit, or No Fit. Only output one of, Good Fit, Potential Fit, or No Fit"

    def evaluate_match(self, resume_text, job_description):
        """
        Evaluate if a resume is a good match for a job description.
        
        :param resume_text: The text content of the resume
        :param job_description: The text content of the job description
        :return: Dictionary containing the match evaluation
        """
        prompt = f"Here's the Resume:{resume_text}           Here's the Job Description:{job_description}"

        messages=[
                {"role": "system", "content": self.sys_prompt},
                {"role": "user", "content": prompt}
            ]
        response = self.generate_response(messages)
        
        # Process the response to determine the match category
        # match_result = self._process_response(response)
        return response

    # def _process_response(self, response):
    #     """
    #     Process the GPT response to extract the match category
    #     """
    #     # Could be additional logic for processing the output, though the output format
    #     # "Good Fit", "Potential Fit", "No fit" should be straight forward for gpt
    #     return {"fit": response["content"]}

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
