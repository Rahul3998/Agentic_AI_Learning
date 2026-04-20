from agents.classifier import ClassifierAgent
from agents.decision_engine import DecisionEngine
from agents.resolution_agent import ResolutionAgent
from ollama_agent.ollama_client import OllamaClient
from agents.escalation_agent import EscalationAgent
from utils.email_sender import EmailSender
import json
import os
from dotenv import load_dotenv

load_dotenv()


# 🔹 Initialize components
ollama_client = OllamaClient()
classifier = ClassifierAgent(ollama_client)
decision_engine = DecisionEngine()
resolution_agent = ResolutionAgent(ollama_client)
# escalation_agent = EscalationAgent(ollama_client)
email_sender = EmailSender(
    sender_email=os.getenv("USER_EMAIL"),
    sender_password=os.getenv("USER_PASSWORD")
)

escalation_agent = EscalationAgent(
    llm_client=ollama_client,
    email_sender=email_sender,
    admin_email=os.getenv("RECEVIER_EMAIL")
)


# 🔹 State variables
waiting_for_feedback = False
last_classification = None
original_query = None
clarify_count = 0

while True:
    raw_input = input("Query :: ").strip()
    user_query = raw_input.lower()

    if user_query == "exit":
        break

    # ✅ STEP 1: Handle feedback FIRST
    if waiting_for_feedback:
        if user_query in ["yes", "y"]:
            print("\nGlad your issue is resolved! If you need further help, feel free to reach out.\n")
            waiting_for_feedback = False
            clarify_count = 0
            continue

        elif user_query in ["no", "n"]:
            ticket, message = escalation_agent.run(original_query, last_classification)

            print("\n=== ESCALATION ===")
            print(message)

            waiting_for_feedback = False
            clarify_count = 0
            continue

        elif user_query in ["partial", "partially"]:
            ticket, message = escalation_agent.run(original_query, last_classification)

            print("\n=== ESCALATION ===")
            print(message)

            waiting_for_feedback = False
            clarify_count = 0
            continue

        else:
            print("\nPlease respond with: yes / no / partially\n")
            continue

    # 🔹 Store original query for escalation
    original_query = raw_input

    # ✅ STEP 2: Classification
    classification = classifier.run(user_query)

    print("\n=== CLASSIFICATION ===")
    print(json.dumps(classification, indent=2))

    # ✅ STEP 3: Decision
    decision = decision_engine.decide(classification, user_query)

    print("\n=== DECISION ===")
    print(json.dumps(decision, indent=2))

    # ✅ STEP 4: Action Handling

    # 🔹 RESOLVE
    if decision["action"] == "RESOLVE":
        solution = resolution_agent.run(classification, user_query)

        print("\n=== SOLUTION ===")
        print(solution)

        waiting_for_feedback = True
        last_classification = classification
        clarify_count = 0

    # 🔹 ESCALATE (Direct)
    elif decision["action"] == "ESCALATE":
        ticket, message = escalation_agent.run(raw_input, classification)

        print("\n=== ESCALATION ===")
        print(message)

        clarify_count = 0

    # 🔹 CLARIFY
    elif decision["action"] == "CLARIFY":
        clarify_count += 1

        if clarify_count >= 2:
            print("\nI will proceed with the best possible solution based on the provided information.\n")

            solution = resolution_agent.run(classification, user_query)

            print("\n=== SOLUTION ===")
            print(solution)

            waiting_for_feedback = True
            last_classification = classification
            clarify_count = 0
        else:
            print("\nI need a bit more information to help you better. Could you please provide more details about the issue?\n")

    print("================\n")