import json
import os

class ResolutionAgent:
    def __init__(self, llm_client, kb_path="knowledge_base.json", model="mistral:latest"):
        self.llm = llm_client
        self.model = model

        base_dir = os.path.dirname(__file__)
        kb_full_path = os.path.join(base_dir, kb_path)

        with open(kb_full_path, "r") as f:
            self.kb = json.load(f)

    # 🔍 Step 1: Retrieve best match
    def retrieve(self, issue_type, user_query):
      query = user_query.lower()

      candidates = [item for item in self.kb if item["issue_type"] == issue_type]

      best_match = None
      best_score = 0

      for item in candidates:
          score = 0

          title = item["title"].lower()
          if title in query:
              score += 5

          for keyword in item["keywords"]:
              keyword = keyword.lower()

              # Exact match (strong)
              if keyword in query:
                  score += 3

              # Partial word match
              else:
                  keyword_words = keyword.split()
                  match_count = sum(1 for word in keyword_words if word in query)
                  score += match_count

          if score > best_score:
              best_score = score
              best_match = item

      if best_score == 0:
        return None

      return best_match


    def fallback_solution(self, user_query):
      prompt = f"""
  You are an IT support assistant.

  Provide general troubleshooting steps for the issue below.

  Keep it simple, safe, and practical.
  Limit to 4-6 steps.

  Issue:
  {user_query}
  """
      return self.llm.call_ollama(prompt, self.model)


    # 🤖 Step 2: Generate steps using LLM
    def generate_steps(self, context, user_query):
        steps_text = "\n".join([f"- {step}" for step in context["steps"]])

        prompt = f"""
You are an IT support assistant.

Use ONLY the provided context to answer.

Do NOT add extra steps.
Do NOT hallucinate.

Context:
{steps_text}

User Query:
{user_query}

Return step-by-step solution in numbered format.
"""

        response = self.llm.call_ollama(prompt, self.model)
        return response.strip()

    # 🚀 Step 3: Main run function
    def run(self, classification_output, user_query):
      issue_type = classification_output.get("issue_type")

      match = self.retrieve(issue_type, user_query)

      # ✅ Handle no match → fallback
      if not match:
          solution = self.fallback_solution(user_query)

          return f"""
  I couldn't find an exact match for your issue.

  Here are some general troubleshooting steps:

  {solution}

  Did this resolve your issue? (yes / no / partially)
  """.strip()

      steps = match["steps"]

      # ✅ Handle both formats (list or dict)
      if isinstance(steps, dict):
          all_steps = steps.get("basic", []) + steps.get("advanced", [])
      else:
          all_steps = steps

      # ✅ Convert to numbered steps
      steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(all_steps)])

      # ✅ Friendly message mapping
      issue_messages = {
          "software": "application-related issue",
          "network": "network connectivity issue",
          "account": "account or login issue",
          "hardware": "hardware-related issue",
          "access": "access or permission issue"
      }

      msg = issue_messages.get(issue_type, "technical issue")

      return f"""
  It looks like you're facing a {msg}.

  You can try the following steps:

  {steps_text}

  If the issue is still not resolved after trying these steps, please let me know.

  Did this resolve your issue? (yes / no / partially)
  """.strip()