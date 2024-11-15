# Datasets Used

1. `JobResumeMatches.csv`: This contains a resume, job description, and a label of {Good Fit, No Fit, Potential Fit}. Data source: hf://datasets/cnamuangtoun/resume-job-description-fit/.
2. `ResumeFeatures.csv`: This contains a resume, Industry, Experience Level. Industry is from Huggingface (https://huggingface.co/datasets/ahmedheakl/resume-atlas). We sampled 150 rows from this dataset. Experience Level is made by us.
3. `Locations.csv`: This contains a text and a label of {1, 0} where 1 means it is a location, 0 means it is not a location. This is made by us.
4. `Resumes.csv`: This contains a text and a label of {1, 0} where 1 means it is a resume, 0 means it is not a location. The label-1 data is from `ResumeFeatures.csv`, the label-0 data are IMDB movie reviews.
