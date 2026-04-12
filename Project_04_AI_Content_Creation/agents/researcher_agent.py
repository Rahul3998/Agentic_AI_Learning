from ollama_client.ollama_client import OllamaClient


class ResearchAgent:

    def __init__(self):
        self.llm = OllamaClient()

    def run(self, topic, outline):
        prompt = f"""
You are a research assistant.

Generate key points for each section.

Topic: {topic}
Outline:
{outline}

Give only 2-3 key points per section. Keep it concise.
"""
        return self.llm.call_ollama(prompt)