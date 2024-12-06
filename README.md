# ResuMatch

Welcome to ResuMatch, your one-stop job matching tool! This is an agentic system designed to help in job searching. It uses only your resume which cuts out all the secret LinkedIn algorithms which think they can serve you the most fit jobs.

# To use ResuMatch

## Create venv environment and install requirements

### Step 1) Create the virtual environment - from python3.10
```
python3.10 -m venv venv
```


### Step 2) Activate the venv
```
source venv/bin/activate 
```

### Step 3) Install all our requirements
```
pip install -r requirements.txt
```

## OpenAI setup

### OpenAI API KEY

In the base dir (where this README is located), create a file, .env and paste in

```
OPENAI_API_KEY=YOUR_API_KEY
```
This will make sure all the agents are able to work!


## Running ResuMatch

You should be good to go after the above steps

Make sure you're in the `ECE1786-ResuMatch` directory and run the following

```
python main.py
```

This should print out

```
* Running on local URL:  http://127.0.0.1:7860
* Running on public URL: https://87420aa599faae7683.gradio.live
```

Which runs the Graadio UI in the browswer at localhost, just click on the link to get job matching!


# Agent Evaluation

Though not needed to run the main system, here's some helpful functionality we built into the software so we could test each agent in a quick and modular way.

These modules import out data from the `/datasets/local_datasets` folder and performs full evaluation on the respective datasets. With overall accuracy reporting and confusion matrix generation.

## For evluating the matching_agent
```
python -m  matching_agent.agent_evaluation
```

## For evluating the feature_extraction_agent
```
python -m feature_extraction_agent.evaluate_agent
```


