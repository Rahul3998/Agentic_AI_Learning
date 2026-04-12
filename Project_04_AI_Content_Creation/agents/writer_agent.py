from ollama_client.ollama_client import OllamaClient


class WriterAgent:

    def __init__(self):
        self.llm = OllamaClient()

    def run(self, topic, research):
        prompt = f"""
You are the Writer Agent in a multi-agent system.

Your job:
- Convert research into a blog
- Do NOT add new facts
- Only use provided research

Topic: {topic}
Research:
{research}

Make it engaging and well-structured.
Limit blog to 300-400 words.
"""
        return self.llm.call_ollama(prompt)