# resumatch


# Create venv environment

## Step 1) Create the virtual environment - from python3.10
```
python3.10 -m venv venv
```


## Step 2) Activate the venv
```
source venv/bin/activate 
```


## Step 3) Install all our requirements
```
pip install -r requirements.txt
```

# OpenAI API KEY

In the base dir, create a file, .env and paste in

```
OPENAI_API_KEY=YOUR_API_KEY
```



# For Resume Parsing
```
python -m resume_parser.main
```

# For evluating the matching_agent

```
source venv/bin/activate 
```

```
pip install -r requirements.txt
```

```
python -m  matching_agent.agent_evaluation
```

# For evluating the feature_extraction_agent
```
python -m feature_extraction_agent.evaluate_agent
```


