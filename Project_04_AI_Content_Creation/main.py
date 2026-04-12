from ollama_client.ollama_client import OllamaClient
from agents.planner_agent import PlannerAgent
from agents.researcher_agent import ResearchAgent
from agents.writer_agent import WriterAgent
from agents.reviewer_agent import ReviewerAgent

# planner = PlannerAgent()
# research = ResearchAgent()
# writer = WriterAgent()
# reviewer = ReviewerAgent()


def main():
    topic = input("Enter topic: ")

    planner = PlannerAgent()
    researcher = ResearchAgent()
    writer = WriterAgent()
    reviewer = ReviewerAgent()

    print("\n🧠 Planning...\n")
    outline = planner.run(topic)
    print(outline)

    print("\n🔍 Researching...\n")
    research = researcher.run(topic, outline)
    print(research)

    print("\n✍️ Writing...\n")
    blog = writer.run(topic, research)
    print(blog)

    print("\n🧪 Reviewing...\n")
    final_output = reviewer.run(blog)
    print("\n✅ Final Output:\n")
    print(final_output)


if __name__ == "__main__":
    main()