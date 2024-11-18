from feature_extraction_agent.feature_extraction_agent import FeatureExtractionAgent
from datasets.data import ResumeFeaturesDataset

# print(ResumeFeaturesDataset.df.head())
fe_agent = FeatureExtractionAgent('feature-extractor')
fe_agent.evaluate_dataset(ResumeFeaturesDataset.df)