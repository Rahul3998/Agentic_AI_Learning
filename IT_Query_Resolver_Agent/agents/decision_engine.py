class DecisionEngine:
    def __init__(self):
        self.severity_priority_map = {
            "low": "LOW",
            "medium": "MEDIUM",
            "high": "HIGH",
            "critical": "URGENT"
        }

        self.confidence_threshold = 0.75

    def decide(self, classification_output, user_query):
        # Basic validation
        if "error" in classification_output:
            return {
                "action": "ESCALATE",
                "priority": "MEDIUM",
                "reason": "Invalid classification output"
            }

        severity = classification_output.get("severity")
        resolvable = classification_output.get("resolvable")
        confidence = classification_output.get("confidence")

        priority = self.severity_priority_map.get(severity, "MEDIUM")

        # Rule 1: Low confidence → CLARIFY
        # if confidence < self.confidence_threshold:
        #     return {
        #         "action": "CLARIFY",
        #         "priority": "LOW",
        #         "reason": "Low confidence in classification"
        #     }
        
        # if confidence is None:
        #   return {
        #       "action": "CLARIFY",
        #       "priority": "LOW",
        #       "reason": "Missing confidence value"
        #   }

        query = user_query.lower()

        # Rule 1: Low or missing confidence → CLARIFY
        if confidence is None or confidence < self.confidence_threshold:
            return {
                "action": "CLARIFY",
                "priority": "LOW",
                "reason": "Low or missing confidence in classification"
            }

        # Rule 2: Critical → Immediate escalation (always highest priority)
        if severity == "critical":
            return {
                "action": "ESCALATE",
                "priority": "URGENT",
                "reason": "Critical issue"
            }

        # Rule 3: User already tried (only medium/high)
        # if ("tried" in query or "still" in query) and severity in ["medium", "high"]:
        if any(word in query for word in ["tried", "still", "already", "not working", "again"]):
            return {
                "action": "ESCALATE",
                "priority": priority,
                "reason": "User already attempted troubleshooting; requires support"
            }

        # Rule 4: Not resolvable → escalate
        if resolvable is False:
            return {
                "action": "ESCALATE",
                "priority": priority,
                "reason": "Requires admin/support intervention"
            }

        # Rule 5: High severity but resolvable
        if severity == "high" and resolvable:
            return {
                "action": "RESOLVE",
                "priority": "HIGH",
                "reason": "Attempt immediate self-resolution; escalate if not resolved"
            }

        # Default
        return {
            "action": "RESOLVE",
            "priority": priority,
            "reason": "User can resolve using guided steps"
        }