import uuid
from datetime import datetime

class EscalationAgent:
    def __init__(self, llm_client, email_sender, admin_email, model="mistral:latest"):
        self.llm = llm_client
        self.model = model
        self.email_sender = email_sender
        self.admin_email = admin_email

    def generate_ticket_id(self):
        return f"TICKET-{str(uuid.uuid4())[:8].upper()}"

    def create_ticket(self, user_query, classification_output):
        return {
            "ticket_id": self.generate_ticket_id(),
            "issue_type": classification_output.get("issue_type"),
            "severity": classification_output.get("severity"),
            "description": user_query,
            "status": "OPEN",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    # 🔥 Email Prompt
    def build_email_prompt(self, user_query, classification_output, ticket):
        return f"""
You are an IT support system.

Generate a professional email for the admin/support team.

STRICT RULES:
- Keep it concise and structured
- DO NOT add greetings like "I hope you are doing well"
- DO NOT hallucinate any user details
- DO NOT add fields not provided

Details:
Ticket ID: {ticket['ticket_id']}
Issue Type: {classification_output.get("issue_type")}
Severity: {classification_output.get("severity")}
User Query: {user_query}

OUTPUT FORMAT:

Subject: [{classification_output.get("severity").upper()}] {classification_output.get("issue_type").capitalize()} Issue ({ticket['ticket_id']})

Body:

Hello Team,

A new IT issue has been reported.

Issue Details:
- Ticket ID: {ticket['ticket_id']}
- Issue Type: {classification_output.get("issue_type")}
- Severity: {classification_output.get("severity")}
- Description: {user_query}

Action Required:
Please investigate and resolve this issue at the earliest.

Regards,
IT Support System
"""

    # 🔥 Parse Subject + Body
    def parse_email(self, email_content):
        lines = email_content.split("\n")
        subject = ""
        body_lines = []

        for line in lines:
            if line.lower().startswith("subject:"):
                subject = line.replace("Subject:", "").strip()
            else:
                body_lines.append(line)

        body = "\n".join(body_lines).strip()
        return subject, body

    # 🤖 Generate Email
    def generate_email(self, user_query, classification_output, ticket):
        prompt = self.build_email_prompt(user_query, classification_output, ticket)
        response = self.llm.call_ollama(prompt, self.model)

        subject, body = self.parse_email(response)
        return subject, body

    # 📩 Format User Message
    def format_user_message(self, ticket):
        return f"""
Your issue has been successfully escalated to the IT support team.

🆔 Ticket ID: {ticket['ticket_id']}
📌 Issue Type: {ticket['issue_type']}
⚠️ Severity: {ticket['severity']}

Our team will review your issue and get back to you shortly.
"""

    # 🚀 Main Run
    def run(self, user_query, classification_output):
        ticket = self.create_ticket(user_query, classification_output)

        subject, body = self.generate_email(user_query, classification_output, ticket)

        print("\n=== EMAIL (TO ADMIN) ===")
        print(f"Subject: {subject}")
        print(body)

        # 🔥 SEND EMAIL HERE
        self.email_sender.send_email(
            to_email=self.admin_email,
            subject=subject,
            body=body
        )

        user_message = self.format_user_message(ticket)

        return ticket, user_message