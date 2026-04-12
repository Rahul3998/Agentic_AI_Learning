# =========================
# CREWAI + OLLAMA (GEMMA)
# =========================

from crewai import Agent, Task, Crew

# =========================
# AGENT DEFINITION
# =========================
assistant = Agent(
    role="AI Assistant",
    goal="Answer user queries clearly and accurately",
    backstory="You are a helpful AI assistant working locally using Ollama.",
    
    # 🔥 THIS IS THE KEY FIX
    llm="ollama/gemma3:4b",

    verbose=True
)

# =========================
# TASK DEFINITION
# =========================
task = Task(
    description="Explain what CrewAI is in simple and easy language.",
    agent=assistant,
    expected_output="A beginner-friendly explanation of CrewAI."
)

# =========================
# CREW SETUP
# =========================
crew = Crew(
    agents=[assistant],
    tasks=[task],
    verbose=True
)

# =========================
# EXECUTION
# =========================
if __name__ == "__main__":
    print("\n🚀 Running CrewAI with Ollama...\n")
    
    result = crew.kickoff()
    
    print("\n✅ FINAL OUTPUT:\n")
    print(result)