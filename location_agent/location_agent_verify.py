import json
from agent.agent import Agent

class VerifyLocation(Agent):
    def __init__(self, 
                 name, 
                #  sys_prompt, 
                 model="gpt-4o", 
                 max_tokens=30,
                 response_format={"type": "json_object"},
                 temperature=1.0):
        
        super().__init__(name, model, max_tokens, response_format, temperature)
        self.json_structure = {
            "location": "",
            "country": ""
        }
        self.sys_prompt = """You are a highly skilled assistant that extracts city and country information from a given address. 

Instructions:
1. If the address explicitly contains a city, state, or country, return it in the `location` field as provided. 
2. If the address is incomplete or ambiguous, make an educated guess based on the information available.
3. Always ensure the `country` field is accurate and corresponds to the inferred or provided location.
4. If the input is clearly a country or state, use it directly as the `location` and include the `country`."""

    def extract_city_country(self, address):
        """
        Extract city and country from a given address.
        """
        try:
            # Convert the json_structure to a JSON string format for prompt inclusion
            json_structure_str = json.dumps(self.json_structure)

            # Define the prompt (using triple-quotes for multi-line string)
            prompt = f"""Return the result in the following JSON format: {json_structure_str} 
Address: {address}"""

            # Send the prompt to OpenAI using the `generate_response` method of the parent `Agent` class
            messages = [{"role": "system", "content": self.sys_prompt},
                        {"role": "user", "content": prompt}]
            
            response = self.generate_response(messages)

            print(f"Raw response: {response}")

            # Parse the response into JSON if possible
            try:
                result = json.loads(response)
                return result
            except json.JSONDecodeError:
                return {"error": "Response is not in valid JSON format", "response": response}

        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}

if __name__ == "__main__":
    # Example usage
    location_agent = VerifyLocation(name="locator")
    address = "toronto"
    result = location_agent.extract_city_country(address)
    print(result)
