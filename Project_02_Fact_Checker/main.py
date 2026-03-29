import os
import json
import requests
from dotenv import load_dotenv
from agent import Agent

# Load environment variables
load_dotenv()

LLM_URL = os.getenv("LLM_URL")  
LLM_MODEL = os.getenv("LLM_MODEL") 

# -----------------------------
# Instructions
# -----------------------------
fact_checker_instructions = """
Context:
You are a fact-checker who verifies the accuracy of statements.

Instructions:
When given a statement, carefully analyze its factual accuracy using your knowledge.

Output format STRICT:
- Start with either "✅ TRUE:" or "❌ FALSE:"
- Then give a one-line explanation only
"""


# -----------------------------
# Create Agent
# -----------------------------
fact_checker_agent = Agent(
    name="Fact Checker",
    instructions=fact_checker_instructions,
    model=LLM_MODEL
)

print(f"✅ Agent '{fact_checker_agent.name}' created successfully!")

# -----------------------------
# Run Example
# -----------------------------
statement = "The Great Wall of China is visible from space with the naked eye."

print(f"\n🔍 Checking statement:\n{statement}\n")

result = fact_checker_agent.run(statement)

print("🤖 Result:\n")
print(result)