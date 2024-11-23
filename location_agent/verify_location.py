import pandas as pd
from agent.agent import Agent

class verify_location(Agent):
    def __init__(self, 
                 name, 
                #  sys_prompt, 
                 model="gpt-4", 
                 max_tokens=30,
                 response_format={"type": "json_object"},
                 temperature=1.0):
        
        super().__init__(name, model, max_tokens, response_format, temperature)
        self.json_structure = {
            "industry": "",
            "experience_level": ""
        }