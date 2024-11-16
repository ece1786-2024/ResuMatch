from openai import OpenAI

# Replace 'YOUR_API_KEY' with your actual OpenAI API key
client = OpenAI(api_key="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")

class Agent:
    def __init__(self, 
                 name,  
                 model="gpt-4", 
                 max_tokens=100,
                 response_format={"type": "json_object"},
                 temperature=0.5):
        
        self.name = name
        self.model = model
        self.max_tokens = max_tokens
        self.response_format = response_format
        self.temperature = temperature

    def generate_response(self, messages):
        
        # Send the messages to the API
        completion = client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format=self.response_format,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )

        # Extract the reply
        return completion.choices[0].message.content