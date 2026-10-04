
import os
import json
from dotenv import load_dotenv
from groq import Groq


load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
print("API Client Ready")

# Input Guardrail
class InputGuard:
    # Validates user input before sending it to the LLM
    PROHIBITED_TOPICS = ["hack", "exploit", "illegal", "malware", "password"]
    MAX_LENGTH = 2000
    MIN_LENGTH = 10

    @classmethod
    def validate(cls, user_input):
        if not user_input or len(user_input.strip()) < cls.MIN_LENGTH:
            return {"valid": False, "reason": "Input too short. Minimum" + str(cls.MIN_LENGTH) + "characters."}
        if len(user_input) > cls.MAX_LENGTH:
            return {"valid": False, "reason": "Input too long. Maximum" + str(cls.MAX_LENGTH) + "characters."}
        lower = user_input.lower()
        for topic in cls.PROHIBITED_TOPICS:
            if topic in lower:
                return {"valid": False, "reason": "Prohibited topic detected:" + topic}
        return {"valid": True, "reason": None}
    

# Test Input Guard
print()
print("Testing Input Guard")
print("-" * 40)
tests = [
    "hi", #too short
    "What should I know about antenatal appointments?", # Valid
    "How do I hack into the system?", # Prohibited
    "x" * 3000 # Too long
    ]
for test_input in tests:
    result = InputGuard.validate(test_input)
    status = "PASS" if result["valid"] else "REJECT"
    reason = result["reason"] or "No issue"
    print(" " + status + ":" + test_input[:50] + "...")
    print(" " + reason)
    print ()

# Output Guardrail
class OutputGuard:
    # Validates LLM output before showing it to the user
    PROHIBITED_PHRASES = ["I guarantee", "I promise", "100%", "definitely"]
    MAX_RESPONSE_LENGTH = 2000

    @classmethod
    def validate(cls, ai_response, expected_format=None):
        if not ai_response:
            return {"valid": False, "reason": "Empty response"}
        if len(ai_response) > cls.MAX_RESPONSE_LENGTH:
            return {"valid": False, "reason": "Response too long:" + str(len(ai_response)) + "characters"}
        for phrase in cls.PROHIBITED_PHRASES:
            if phrase.lower() in ai_response.lower():
                return {"valid": False, "reason": "Prohibited phrase found: " + phrase}
        if expected_format == "json":
            try:
                json.loads(ai_response)
            except json.JSONDecodeError:
                return {"valid": False, "reason": "Response is not valid JSON"}
        return {"valid": True, "reason": None}

# Test Output Guard
print()
print("Testing Output Guard")
print("-" * 40)
valid_output = "Antenatal appointments help monitor the health of the mother and baby."
invalid_output = "I guarantee you will have no complications during pregnancy. It is 100% safe."

check1 = OutputGuard.validate(valid_output)
print("Valid Response:", check1["valid"])

check2 = OutputGuard.validate(invalid_output)
print("Response with prohibited phrases:", check2["valid"])
print("Reason:", check2["reason"])

# Cost Tracker
class CostTracker:
    def __init__(self, daily_budget=1.00):
        self.daily_budget = daily_budget
        self.daily_spend = 0.0
        self.total_tokens = 0
        self.calls = 0

    def track(self, usage):
        if usage:
            self.total_tokens += usage.total_tokens or 0
        self.calls += 1

    def summary(self):
        return {
            "calls": self.calls,
            "tokens": self.total_tokens,
            "budget_status": "free tier - no cost"
        }
tracker = CostTracker()

print()
print("Cost Tracker Ready")
print("-" * 40)
print("Model: openai/gpt-oss-120b via Groq")
print("Cost: Free tier")
print("Daily budget tracking still important for production")

# Safe AI Function
def safe_ai_call(user_input, system_prompt):
    # Layer 1: Input Guardrail
    input_check = InputGuard.validate(user_input)
    if not input_check["valid"]:
        return {
            "success": False,
            "error": input_check["reason"],
            "response": None
        }

    # Layer 2: LLM Call
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.3,
            max_tokens=500
        )

        tracker.track(response.usage)
        ai_text = response.choices[0].message.content

        # Layer 3: Output Guardrail
        output_check = OutputGuard.validate(ai_text)
        if not output_check["valid"]:
            return {
                "success": False,
                "error": "Response failed validation:" + output_check['reason'],
                "response": None
            }

        return {
            "success": True,
            "response": ai_text,
            "tokens": response.usage.total_tokens,
            "tracker": tracker.summary()
        }

    except Exception as e:
        return {
            "success": False,
            "error": "API Error:" + str(e),
            "response": None
        }

# Testing Safe AI Function
print()
print("Testing Safe AI Function")
print("-" * 40)

system_prompt = ("You are a helpful antenatal care knowledge assistant"
                               "Answer questions using the available knowledge base"
                                "Do not invent medical information"
                        "If the information is not available, clearly state that you do not have enough information"
                        "Do not provide guarantees or make claims of certainty"
          "For urgent pregnancy warning signs, advise the user to seek appropriate professional medical care.")

# Valid input
print()
print("Testing Valid Input")
result = safe_ai_call("What should I know about antenatal appointments?", system_prompt)
print(json.dumps(result, indent=2, default=str))

# Invalid input
print()
print("Testing Invalid Input")
result = safe_ai_call("hi", system_prompt )
print(json.dumps(result, indent=2, default=str))

# Prohibited topic
print()
print("Testing Prohibited Topic")
result = safe_ai_call("How do I hack into the admin panel?", system_prompt)
print(json.dumps(result, indent=2, default=str))
