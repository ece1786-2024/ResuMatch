import pandas as pd
from agent.agent import Agent

class FeatureExtractionAgent(Agent):
    def __init__(self, 
                 name, 
                 sys_prompt, 
                 model="gpt-4o", 
                 max_tokens=15,
                 response_format={"type": "json_object"},
                 temperature=0.5):
        
        super().__init__(name, model, max_tokens, response_format, temperature)
        
        self.sys_prompt=sys_prompt

    def extract_features(self, text, json_structure):
       
        prompt = f"Extract the following information from the text and format it into the specified JSON, four options for eperience level are entry, junior, senior, executive. The industry should reflect where their expertise and capabilities are most applicable or valuable, instead of the industry the company is in" \
                 f" structure:\n\nText: {text}\n\nExpected JSON Structure: {json_structure}"

        messages=[
                {"role": "system", "content": self.sys_prompt},
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
        # Get all columns except the first one (resume_text)
        feature_columns = df.columns[1:]
        success_rates = {feature: 0 for feature in feature_columns}
        total = len(df)

        for index, row in df.iterrows():
            resume_text = row[df.columns[0]]  # Get resume text from first column
            extracted_features = self.extract_features(resume_text)

            for feature in feature_columns:
                expected_feature = row[feature]
                # Compare extracted features with expected features
                if extracted_features['features'] == expected_feature:
                    success_rates[feature] += 1

        # Calculate success rate for each feature
        for feature in feature_columns:
            success_rates[feature] = (success_rates[feature] / total) * 100 if total > 0 else 0
            print(f"Success rate for {feature}: {success_rates[feature]:.2f}%")

        return success_rates