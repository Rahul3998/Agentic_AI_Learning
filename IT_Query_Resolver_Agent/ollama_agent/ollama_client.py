from ollama import Client

class OllamaClient:
    def __init__(self):
        self.client = Client(host='http://localhost:11434')

    def call_ollama(self, prompt, llm_model):
        response = self.client.generate(
            model=llm_model,
            prompt=prompt
        )
        return response.get('response', '').strip()