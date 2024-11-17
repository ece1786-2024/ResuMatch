from openai import OpenAI

# Replace 'YOUR_API_KEY' with your actual OpenAI API key
with open('api-key.txt', 'r') as f:
  api_key = f.read()

client = OpenAI(api_key=api_key)

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