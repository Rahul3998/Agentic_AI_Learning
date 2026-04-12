from ollama_client import OllamaClient
# from memory_store import MemoryStore
from memory_store import MemoryStore


def main():
    llm = OllamaClient()
    memory = MemoryStore()

    print("🤖 Agent started (type 'exit' to stop)\n")

    while True:
      user_input = input("You: ")

      if user_input.lower() == "exit":
          break

      # 🔥 Delete memory trigger
      user_input_lower = user_input.lower()
      if any(cmd in user_input_lower for cmd in [
          "delete history", "clear memory", "remove my memory"
      ]):
          memory.clear()
          print("🧹 Memory cleared successfully! I will no longer remember past conversations.\n")
          continue

      # 🧠 Get context
      context = memory.get_recent()
      if not context.strip():
        context = "No previous conversation available."

      prompt = f"""
You are a helpful AI assistant.

IMPORTANT RULES:
- Only use the conversation history provided below
- If information is not present, say: "I don't know"
- Do NOT assume or guess personal details

Conversation so far:
{context}

User: {user_input}
Assistant:
"""

      response = llm.call_ollama(prompt)

      print(f"Agent: {response}\n")

      memory.store("User", user_input)
      memory.store("Assistant", response)

if __name__ == "__main__":
    main()