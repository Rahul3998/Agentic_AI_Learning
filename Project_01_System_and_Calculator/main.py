import os
import requests
from math_agent import MathAgent
from system_agent import SystemAgent
from dotenv import load_dotenv

load_dotenv()

LLM_URL = os.getenv("LLM_URL")

def call_llm(query:str):
  payload = {
      "model": os.getenv("LLM_MODEL"),
      "prompt": query,
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

  return response.json()["response"]

def user_prompt(query:str):
  return f"""
You are an intelligent query router.

User Query:
{query}

Your task is to understand the user's intent and respond in a strict, structured format based on the category of the query.

### Instructions:

1. **Mathematical Queries**

   * If the user asks for any mathematical calculation (e.g., "solve 5*10", "what is 11/11", "calculate sin 30"):
   * Convert the query into the predefined operation format:

     * add a b
     * sub a b
     * mul a b
     * div a b
     * pow a b
     * sqrt a
     * log a
     * log10 a
     * sin a
     * cos a
     * tan a
     * fact a
   * Examples:

     * "Solve 5*10" → mul 5 10
     * "What is 11/11" → div 11 11
     * "Square root of 25" → sqrt 25

2. **System Information Queries**

   * If the user asks about system-related information:

     * OS → respond: os
     * CPU → respond: cpu
     * RAM / Memory → respond: ram
     * Disk → respond: disk
     * Network → respond: network
     * Full system info → respond: system

   * Examples:

     * "What is my system config?" → system
     * "Check RAM usage" → ram
     * "Show CPU details" → cpu

3. **Other Queries**

   * If the query is not related to math or system info:
   * Respond normally as an AI assistant with a helpful answer.

### Rules:

* Do NOT explain your reasoning.
* Do NOT add extra text for math/system queries.
* Output ONLY the final formatted answer.
* Keep responses concise and accurate.

"""

def reasoning(query:str, tool_output:str):
   return f"""

You are a helpful AI assistant.

You have already received a processed result from a tool/agent (like math agent or system agent).

User Query:
{query}

Tool/Agent Output:
{tool_output}

Your task is to explain the answer clearly to the user.

### Instructions:

1. Use **very simple English** (easy to understand for anyone).
2. Explain the answer with **step-by-step reasoning** when needed.
3. Keep the explanation **short and clear** (do not over-explain).
4. If it is a math result:

   * Briefly explain how the answer was calculated.
5. If it is system information:

   * Explain what each value means in simple words.
6. If it is general AI response:

   * Answer normally in a helpful way.

### Rules:

* Do NOT mention tools, agents, or internal processing.
* Do NOT repeat the question unnecessarily.
* Keep the tone friendly and clear.
* Focus on helping the user understand the answer.

### Output Style:

* 2–5 lines maximum
* Simple sentences
* No complex words

Now generate the final answer.

"""

def main():
  math_agent = MathAgent()
  system_agent = SystemAgent()

  while True:
    user_input = input(">> ")
    if "exit" in user_input.lower():
       break
    input_prompt = user_prompt(user_input)
    llm_ans = call_llm(input_prompt)

    print("LLM ANS :: ",llm_ans)

    if any(word in llm_ans.lower() for word in ["add", "sub", "mul", "div", "sqrt", "sin", "cos", "tan", "log"]):
        result = math_agent.handle(llm_ans)
    elif any(word in llm_ans.lower() for word in ["cpu", "ram", "memory", "disk", "os", "system", "network"]):
        result = system_agent.handle(llm_ans)
    else:
      result = llm_ans

    print(f"RESULT :: {result}")
    llm_reasoning_prompt = reasoning(user_input, result)
    final_output = call_llm(llm_reasoning_prompt)

    print("Final Answer ::\n",final_output)
  
  

if __name__=="__main__":
  main()