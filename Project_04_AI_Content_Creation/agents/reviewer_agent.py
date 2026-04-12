from ollama_client.ollama_client import OllamaClient


class ReviewerAgent:

    def __init__(self):
        self.llm = OllamaClient()

    def run(self, blog):
        prompt = f"""
You are the Reviewer Agent.

Your job:
- Improve clarity
- Do NOT change meaning
- Keep content concise

Blog:
{blog}
"""
        return self.llm.call_ollama(prompt)