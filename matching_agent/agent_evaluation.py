from matching_agent.matching_agent import MatchingAgent
import pandas as pd

ma = MatchingAgent(name="Job Fit Determination")

df = pd.read_csv('./datasets/local_datasets/JobResumeMatches.csv')

ma.evaluate_dataset(df)
