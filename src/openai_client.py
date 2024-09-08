# openai_client.py
import openai

class OpenAIClient:
    def __init__(self, api_key):
        openai.api_key = api_key

    def fetch_response(self, prompt):
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()