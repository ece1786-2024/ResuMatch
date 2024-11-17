from agent.agent import Agent

class MatchingAgent(Agent):
    def __init__(self, name, sys_prompt, model="gpt-4o", max_tokens=15):
        super().__init__(name, sys_prompt, model, max_tokens)
        self.match_categories = ["Good Fit", "Potential Fit", "No fit"]

    def evaluate_match(self, resume_text, job_description):
        """
        Evaluate if a resume is a good match for a job description.
        
        :param resume_text: The text content of the resume
        :param job_description: The text content of the job description
        :return: Dictionary containing the match evaluation
        """
        prompt = f"Resume:\n{resume_text}\n\nJob Description:\n{job_description}"
        additional_prompts = [{"role": "user", "content": prompt}]
        response = self.generate_response(additional_prompts)
        
        # Process the response to determine the match category
        match_result = self._process_response(response)
        return match_result

    def _process_response(self, response):
        """
        Process the GPT response to extract the match category
        """
        # Could be additional logic for processing the output, though the output format
        # "Good Fit", "Potential Fit", "No fit" should be straight forward for gpt
        return {"fit": response["content"]}

    def evaluate_dataset(self, df):
        """
        Evaluate the matching predictions on a test dataset.
        Assumes first column is resume_text, second is job_description, 
        and third column is the fit label.

        :param df: DataFrame with columns ['resume_text', 'job_description', 'fit']
        :return: Success rate as a percentage
        """
        correct_predictions = 0
        total = len(df)

        for index, row in df.iterrows():
            resume_text = row[df.columns[0]]
            job_description = row[df.columns[1]]
            expected_fit = row[df.columns[2]]
            
            match_result = self.evaluate_match(resume_text, job_description)
            
            if match_result['fit'] == expected_fit:
                correct_predictions += 1

        success_rate = (correct_predictions / total) * 100 if total > 0 else 0
        print(f"Success rate: {success_rate:.2f}%")
        
        return success_rate