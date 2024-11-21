import pandas as pd
from agent.agent import Agent
import ast
import pickle
import os
from tqdm import tqdm
import json

class ResumeValidationAgent(Agent):
    def __init__(self, name, model="gpt-4o"):        
        super().__init__(name, model=model)

    def validate(self, resume_text):
        prompt = f"Please tell me if the following text is from a resume (1) or not (0). Format this in a JSON with the key 'resume_decision' and variable is the 1 or 0 with your decision. Do not say anything except your JSON response: {resume_text}"
        
        messages=[
                {"role": "user", "content": prompt}
        ]
        
        response = json.loads(self.generate_response(messages))
        return int(response['resume_decision'])


    def evaluate_dataset(self, df):
        """
        Evaluate the feature extraction on a given DataFrame for multiple features.
        Assumes first column is resume_text and all subsequent columns are features.

        :param df: DataFrame with columns ['resume_text', feature1, feature2, ...]
        :return: Dictionary with success rates for each feature
        """
        
        # Put resume_text first
        df = df[['resume_text'] + [col for col in df.columns if col != 'resume_text']]

        # Get all columns except the first one (resume_text)
        label = df['label']

        successes = 0
        true_labels = []
        pred_labels = []
        
        total = len(df)

        for index, row in tqdm(df.iterrows()):
            resume_text = row['resume_text']  # Get resume text from first column
            
            pred_label = self.validate(resume_text)
            true_label = row['label']

            if pred_label == true_label:
                successes += 1
            
            true_labels.append(true_label)
            pred_labels.append(pred_label)

        # Calculate success rate for each feature
        success_rate = (successes / total) * 100 if total > 0 else 0
        print(f"Success rate: {success_rate:.2f}%")

        with open(os.path.join('resume_validation_agent', 'evaluation_results', 'success'), 'wb') as f:
            pickle.dump(success_rate, f)

        with open(os.path.join('resume_validation_agent', 'evaluation_results', 'true_labels'), 'wb') as f:
            pickle.dump(true_labels, f)

        with open(os.path.join('resume_validation_agent', 'evaluation_results', 'pred_labels'), 'wb') as f:
            pickle.dump(pred_labels, f)

        return success_rate
