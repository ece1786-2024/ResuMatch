import pandas as pd
from agent.agent import Agent
import ast
import pickle
import os
from tqdm import tqdm

class FeatureExtractionAgent(Agent):
    def __init__(self, 
                 name, 
                #  sys_prompt, 
                 model="gpt-4o", 
                 max_tokens=30,
                 response_format={"type": "json_object"},
                 temperature=1.0):
        
        super().__init__(name, model, max_tokens, response_format, temperature)
        self.json_structure = {
            "industry": "",
            "experience_level": ""
        }
        # self.sys_prompt=sys_prompt

    def extract_features(self, text):
       
        prompt = f"Extract the following information from the text and format it into the specified JSON, four options for eperience level are entry, junior, senior, executive. The industry should reflect where their expertise and capabilities are most applicable or valuable, instead of the industry the company is in" \
                 f" structure:\n\nText: {text}\n\nExpected JSON Structure: {self.json_structure}"

        messages=[
                # {"role": "system", "content": self.sys_prompt},
                {"role": "user", "content": prompt}
            ]
        
        
        response = self.generate_response(messages)
        return response


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
        feature_columns = df.columns[1:]

        success_rates = {feature: 0 for feature in feature_columns}
        true_labels = {feature: [] for feature in feature_columns}
        predicted_labels = {feature: [] for feature in feature_columns}
        
        total = len(df)

        for index, row in tqdm(df.iterrows()):
            resume_text = row[df.columns[0]]  # Get resume text from first column
            
            extracted_features = self.extract_features(resume_text)
            extracted_features = ast.literal_eval(extracted_features)

            for feature in feature_columns:
                try:
                    extracted_feature = extracted_features[feature].lower()
                    expected_feature = row[feature].lower()

                    true_labels[feature].append(expected_feature)
                    predicted_labels[feature].append(extracted_feature)

                    # Compare extracted features with expected features
                    if extracted_feature == expected_feature:
                        success_rates[feature] += 1
                except Exception as e:
                    print(f"Error: {e}")
                    continue

        # Calculate success rate for each feature
        for feature in feature_columns:
            success_rates[feature] = (success_rates[feature] / total) * 100 if total > 0 else 0
            print(f"Success rate for {feature}: {success_rates[feature]:.2f}%")

        with open(os.path.join('feature_extraction_agent', 'evaluation_results', 'success'), 'wb') as f:
            pickle.dump(success_rates, f)

        with open(os.path.join('feature_extraction_agent', 'evaluation_results', 'true_labels'), 'wb') as f:
            pickle.dump(true_labels, f)

        with open(os.path.join('feature_extraction_agent', 'evaluation_results', 'pred_labels'), 'wb') as f:
            pickle.dump(predicted_labels, f)

        return success_rates
