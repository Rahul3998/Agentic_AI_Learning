from ollama import Client
from dotenv import load_dotenv
import os

load_dotenv()

class OllamaClient:
    def __init__(self):
        self.client = Client(host='http://localhost:11434')

    def call_ollama(self, prompt):
        response = self.client.generate(
            model=os.getenv("LLM_MODEL"),
            prompt=prompt
        )
        return response['response']
