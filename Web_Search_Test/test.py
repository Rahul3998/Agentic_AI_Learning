import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# ==============================
# CONFIG
# ==============================
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OLLAMA_URL = os.getenv("LLM_URL")
OLLAMA_MODEL = os.getenv("LLM_MODEL")

# ==============================
# 1. SEARCH FUNCTION (Tavily)
# ==============================
def search_web(query):
    url = "https://api.tavily.com/search"
    
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        # "search_depth": "advanced",
        # "include_answer": True,
        "max_results": 5
    }

    response = requests.post(url, json=payload)
    print(f"\nRESPONSE::\n{response.json()}")
    
    if response.status_code != 200:
        raise Exception(f"Search API error: {response.text}")
    
    return response.json()

# ==============================
# 2. FORMAT SEARCH RESULTS
# ==============================
def format_results(data):
    formatted = ""

    if "answer" in data:
        formatted += f"Quick Answer:\n{data['answer']}\n\n"

    for i, result in enumerate(data.get("results", []), start=1):
        formatted += f"{i}. {result.get('title')}\n"
        formatted += f"URL: {result.get('url')}\n"
        formatted += f"Content: {result.get('content')}\n\n"

    return formatted.strip()

# ==============================
# 3. OLLAMA CALL
# ==============================
def ask_ollama(prompt):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code != 200:
        raise Exception(f"Ollama error: {response.text}")

    return response.json()["response"]

# ==============================
# 4. MAIN AGENT FUNCTION
# ==============================
def web_search_agent(user_query):
    print("\n🔍 Searching web...\n")
    
    search_data = search_web(user_query)
    print(f"\nSEARCH DATA :: \n{search_data}")
    formatted_data = format_results(search_data)
    print(f"\nFORMATTED DATA :: \n{formatted_data}")

    # Prompt for LLM
    final_prompt = f"""
You are an intelligent research assistant.

User Query:
{user_query}

Web Search Results:
{formatted_data}

Instructions:
- Analyze the results carefully
- Combine information from multiple sources
- Give a clear, structured answer
- Avoid hallucination
- If info is insufficient, say so

Final Answer:
"""

    print("🧠 Generating answer using Ollama...\n")
    
    answer = ask_ollama(final_prompt)
    return answer


# ==============================
# 5. RUN
# ==============================
if __name__ == "__main__":
    while True:
        query = input("\n💬 Enter your query (or 'exit'): ")
        if query.lower() == "exit":
            break

        try:
            result = web_search_agent(query)
            print("\n✅ Final Answer:\n")
            print(result)

        except Exception as e:
            print(f"\n❌ Error: {e}")