from ollama_client.ollama_client import OllamaClient


class PlannerAgent:

    def __init__(self):
        self.llm = OllamaClient()

    def run(self, topic):
        prompt = f"""
You are a planning expert.

Break the topic into a structured outline with 5-7 sections.

Topic: {topic}

Output only 5 concise bullet points. Keep it short.
"""
        return self.llm.call_ollama(prompt)