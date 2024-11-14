import pandas as pd
from agent import Agent

class FeatureExtractionAgent(Agent):
    def __init__(self, name, sys_prompt, model="gpt-4", max_tokens=15):
        super().__init__(name, sys_prompt, model, max_tokens)

    def extract_features(self, text):
        # Example method for feature extraction
        additional_prompts = [{"role": "user", "content": text}]
        response = self.generate_response(additional_prompts)
        # Process the response to extract features
        features = self._process_response(response)
        return features

    def _process_response(self, response):
        # Logic here in case we want multiple of the same feature
        return {"features": response["content"]}

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