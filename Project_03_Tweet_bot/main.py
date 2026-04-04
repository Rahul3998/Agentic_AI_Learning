from prompt import Prompt
from agent import Agent
import os
from dotenv import load_dotenv

load_dotenv()

# Gettinng Env Data
# print(os.getenv("LLM_URL"))
# print(os.getenv("LLM_MODEL"))

# Checking Prompt
# print(Prompt.tweet_prompt("Scary"))


instruction = Prompt.tweet_prompt()
tweet_bot_agent = Agent(name="Tweet Bot", instructions=instruction, model=os.getenv("LLM_MODEL"))

# print(tweet_bot_agent.name)

topic = "Heartbroken boy living in his old memories with girlfriend"

print("Generating tweet....")

result = tweet_bot_agent.run(topic)

print(f"Agent Response\n\n{result}")