import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
print("API Client Ready")

# Define the Agent Class
class Agent:
    def __init__(self, name, role, instructions):
        self.name = name
        self.role = role
        self.instructions = instructions

    def run(self, task):
        print(" " + self.name + " is working...")
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "You are " + self.name + ". " + self.role + ". " + self.instructions},
                {"role": "user", "content": task}
            ],
            temperature=0.3,
            max_tokens=500
        )
        result = response.choices[0].message.content
        print(self.name + " completed")
        return result

# Create Specialized Agents
antenatal_agent = Agent(
    "Antenatal Information Agent",
    "An antenatal care information assistant",
    "Answer general questions about antenatal care using the available knowledge. Do not invent medical information."
)

warning_agent = Agent(
    "Warning Signs Agent",
    "A pregnancy warning signs information assistant",
    "Provide information about pregnancy warning signs. Do not diagnose. For urgent symptoms, advise the user to seek appropriate professional medical care."
)

appointment_agent = Agent(
    "Appointment Agent",
    "An antenatal appointment specialist",
    "Answer questions about antenatal appointments, schedules, preparation, and related information using the available knowledge."
)

feedback_agent = Agent(
    "Customer Feedback Agent",
    "A customer feedback and user experience specialist",
    "Handle complaints, suggestions, ratings, and feedback. Be empathetic and professional. Acknowledge the user's concern and provide an appropriate response."
)

router_agent = Agent(
    "Router Agent",
    "A customer request dispatcher for an antenatal care knowledge system",
   "Classify the user's message into one of four categories: ANTENATAL, WARNING, APPOINTMENT, or FEEDBACK. Reply with only the category."
)
print("1. Antenatal Information Agent")
print("2. Warning Signs Agent")
print("3. Appointment Agent")
print("4. Customer Feedback Agent")
print("5. Router Agent")

# Multi-Agent Pipeline
def handle_user_message(message):
    print()
    print("-" * 50)
    print("User Message:", message)
    print("-" * 50)

    # Step 1: Classify
    print("Step 1: Classification")
    print("-" * 40)
    category = router_agent.run("Classify this message: " + message).strip().upper()
    print("Category:", category)

    # Step 2: Route to the right agent
    print()
    print("Step 2: Routing")
    print("-" * 40)

    if "WARNING" in category:
        response = warning_agent.run(message)
    elif "APPOINTMENT" in category:
        response = appointment_agent.run(message)
    elif "ANTENATAL" in category:
        response = antenatal_agent.run(message)
    elif "FEEDBACK" in category:
        response = feedback_agent.run(message)
    else:
        response = "I'm sorry, I didn't understand that. Please rephrase your question."

    print()
    print("Final Response")
    print("-" * 40)
    print(response)

    return {"category": category, "reply": response}

# Test Multi-Agent System
print()
print("Testing Multi-Agent System")
print("-" * 50)

# Test 1
handle_user_message("What should I know about antenatal care?")

# Test 2
handle_user_message("What are the warning signs I should look out for during pregnancy?")

# Test 3
handle_user_message("What should I know about my antenatal appointments?")

# Test 4
handle_user_message("I have some feedback about the antenatal care services.")