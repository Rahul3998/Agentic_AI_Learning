import requests
import os

LLM_URL = os.getenv("LLM_URL")

payload = {
    "model": os.getenv("LLM_MODEL"),
    "prompt": "Explain large language models in simple terms.",
    "stream": False,
    "options": {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "repeat_penalty": 1.1,
        "num_predict": 200
    }
}

response = requests.post(LLM_URL, json=payload)

print(response.json()["response"])