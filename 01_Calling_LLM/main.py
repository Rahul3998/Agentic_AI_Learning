import requests
import os

LLM_URL = "http://127.0.0.1:11434/api/generate"

payload = {
    "model": "gemma3:4b",
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
# print(LLM_URL)
# print(os.getenv("LLM_MODEL"))
response = requests.post(LLM_URL, json=payload)

print(response.json()["response"])