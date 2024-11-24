import pandas as pd
from openai import OpenAI
import os
import re
# Get the directory of the current script (categorize_industries.py)
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the full relative path to the 'api-key.txt' file
api_key_path = os.path.join(script_dir, '..', 'api-key.txt')
with open(api_key_path, 'r') as f:
  api_key = f.read()
client = OpenAI(api_key=api_key)
#def categorize_industries(df):
def categorize_industries(industry_counts):
    # Extract the industries (index of the Series)
    industries = industry_counts.index.tolist()

    prompt = """
    I have provided a list of industries. Please categorize them into exactly 20 broader categories based on their domain or similarity. The category names need to be consice.
    For each category, list the industries that belong to it. Then, generate a mapping where each industry is mapped to its broader category. 
    Do **not** include the list of industries themselves in the output. Only generate the mapping in the following format:

    'category1': [industry1', 'industry1'],
    'category2': ['industry3', 'industry4'...]
    ...
    'category20': ['industry', 'industry'...]

    Please provide the mapping only, no additional explanation or listing of industries.
    """
    # Get a list of industries from the dataframe
    #industries = df['Industry'].unique().tolist()
    # Combine the list of industries into a string to pass to the model
    industries_text = "\n".join(industries)
    
    #print(industries_text)
    prompt = prompt + "\n" + industries_text

    response = client.chat.completions.create(
            model="gpt-4o", 
            max_tokens=1000,
            messages=[
                {"role": "system", "content": f"{prompt}"},
                #{"role": "user", "content": f"{prompt}"}
            ]
        )

    categories = response.choices[0].message.content
    print(categories)
    
    #return response

def update_industry(ind):
    # Define role mappings using a dictionary
    industry_roles = {
        'Engineering': ['Mechanical Engineer', 'Electrical Engineering', 'Civil Engineer', 'Architecture'],
        'IT':['DevOps', 'ETL Developer', 'Web Designing', 'Database', 'Network Security Engineer','Testing', 'Blockchain'],
        'Consulting': ['Consultant', 'Business Analyst'],
        'Sales and Marketing': ['Sales', 'Public Relations'],
        'Management': ['Management', 'Operations Manager', 'PMO'],
        'HR': ['Human Resources'],
        'Finance': ['Accountant', 'Finance', 'Banking'],
        'Software Development': ['Java Developer', 'DotNet Developer', 'SQL Developer', 'SAP Developer', 'Python Developer', 'React Developer'],
        'Construction': ['Building and Construction'],
        'Aviation': ['Aviation'],
        'Healthcare': ['Health and Fitness'],
        'Arts and Media': ['Arts', 'Designing', 'Digital Media'],
        'Apparel': ['Apparel'],
        'Automotive': ['Automobile'],
        'Food Services': ['Food and Beverages'],
        'Legal': ['Advocate'],
        'Agriculture': ['Agriculture'],
        'Customer Service': ['BPO']
    }

    # Iterate through the dictionary and update the 'Industry' column
    for industry, roles in industry_roles.items():
        ind.loc[ind['Industry'].isin(roles), 'Industry'] = industry

    # Return the updated DataFrame
    return ind

