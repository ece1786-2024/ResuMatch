from openai import OpenAI

# Replace 'YOUR_API_KEY' with your actual OpenAI API key
client = OpenAI(api_key ="")

class Agent:
    def __init__(self, name, sys_prompt, model="gpt-4", max_tokens=100):
        self.name = name
        self.sys_prompt = sys_prompt
        self.model = model
        self.max_tokens = max_tokens

    def generate_response(self, additional_prompts=None):
        # Update system prompt
        sys_prompt = self.sys_prompt

        # Build the messages list
        messages = [{"role": "system", "content": sys_prompt}]
        
        # Add additional prompts if provided
        if additional_prompts:
            messages.extend(additional_prompts)

        # Send the messages to the API
        completion = client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens
        )

        # Extract the reply
        reply_content = completion.choices[0].message.content.strip()
        reply = {"role": "assistant", "name": self.name, "content": reply_content}
        return reply