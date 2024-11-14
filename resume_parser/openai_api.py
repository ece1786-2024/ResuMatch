from openai import OpenAI

class OpenAIAPI:
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    def format_text_to_json(self, text: str, json_structure: dict) -> dict:       
        client = OpenAI(
            api_key = self.api_key,
        )
        system_message = "You are a helpful assistant for parsing resume."
        prompt = f"Extract the following information from the text and format it into the specified JSON, four options for eperience level are entry, junior, senior, executive. The industry should reflect where their expertise and capabilities are most applicable or valuable, instead of the industry the company is in" \
                 f" structure:\n\nText: {text}\n\nExpected JSON Structure: {json_structure}"

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.5,
            max_tokens=1500
        )

        return response.choices[0].message.content
