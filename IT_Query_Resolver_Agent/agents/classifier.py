import json

class ClassifierAgent:
    def __init__(self, llm_client, model="mistral:latest"):
        self.llm = llm_client
        self.model = model

        self.required_keys = ["category", "issue_type", "severity", "resolvable", "confidence"]

        self.valid_issue_types = ["network", "access", "hardware", "software", "account", "other"]
        self.valid_severity = ["low", "medium", "high", "critical"]

    def build_prompt(self, user_input):
        return f"""
You are an IT support issue classifier.

Your task is to analyze the user query and classify it into a structured JSON format.

Rules:
- Only respond in valid JSON.
- Do not add explanations.
- Do not add extra text.
- Always include all fields.
- If the request is about permissions, approvals, or enabling access → classify as "access" and resolvable = false
- VPN issues are usually resolvable unless explicitly stated otherwise.

Definitions:

Issue Types:
- network: VPN, WiFi, internet issues
- access: permissions, login failures
- hardware: laptop, keyboard, physical device issues
- software: application errors, crashes
- account: password reset, account lock
- other: anything unclear

Severity Levels:
- low: minor inconvenience
- medium: affecting work but not blocked
- high: blocking work
- critical: urgent or system-wide issue

Severity Rules:
- Password issues, minor login problems → low
- Account locked, repeated login failures → medium
- Unable to work due to issue → high
- System-wide outages, server down → critical

Resolvable:
- true: user can likely fix with steps
- false: requires admin/support team

Confidence:
- value between 0 and 1

Confidence Rules:
- Clear and specific issues → 0.8 to 0.95
- Ambiguous issues → below 0.7
- Never return 1.0 unless absolutely certain

Access Rules:
- Requests to enable ports, grant permissions, provide admin rights, or access systems → MUST be classified as "access"
- These are NOT resolvable by the user → resolvable = false

Output format:
{{
  "category": "IT",
  "issue_type": "...",
  "severity": "...",
  "resolvable": true,
  "confidence": 0.0
}}

Example:
User: "Enable port 8080 for my application"
Output:
{{
  "category": "IT",
  "issue_type": "access",
  "severity": "medium",
  "resolvable": false,
  "confidence": 0.9
}}

User Query:
\"\"\"{user_input}\"\"\"
"""

    def validate_response(self, data):
        # Check required keys
        for key in self.required_keys:
            if key not in data:
                return False, f"Missing key: {key}"

        # Validate values
        if data["issue_type"] not in self.valid_issue_types:
            return False, "Invalid issue_type"

        if data["severity"] not in self.valid_severity:
            return False, "Invalid severity"

        if not isinstance(data["resolvable"], bool):
            return False, "Invalid resolvable value"

        if not (0 <= data["confidence"] <= 1):
            return False, "Invalid confidence"

        return True, "Valid"

    def run(self, user_input):
        prompt = self.build_prompt(user_input)

        # First attempt
        response = self.llm.call_ollama(prompt, self.model)
        # print(f"RESPONSE :: {response}")
        try:
            parsed = json.loads(response)
        except:
            # Retry once if JSON fails
            response = self.llm.call_ollama(prompt, self.model)
            try:
                parsed = json.loads(response)
            except:
                return {"error": "Invalid JSON from model"}

        # Validate schema
        is_valid, message = self.validate_response(parsed)

        if not is_valid:
            return {"error": message, "raw": parsed}

        return parsed
    


    