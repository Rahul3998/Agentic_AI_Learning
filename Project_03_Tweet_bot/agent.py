import json
import os
from dotenv import load_dotenv
import requests

load_dotenv()

class Agent:
    def __init__(self, name, instructions, model):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.url = os.getenv("LLM_URL")

        if not self.url:
            raise ValueError("LLM_URL is not set in environment variables")

    def run(self, user_input):
        prompt = f"{self.instructions}\n\nTopic: {user_input}\nNow Generate tweet..."

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(self.url, json=payload)
        except Exception as e:
            return f"❌ Error connecting to LLM: {e}"

        if response.status_code != 200:
            return f"❌ API Error: {response.text}"

        # Handle multiple JSON lines (Ollama format)
        output = ""
        for line in response.text.splitlines():
            if line.strip():
                try:
                    data = json.loads(line)
                    output += data.get("response", "")
                except json.JSONDecodeError:
                    continue

        return output.strip()