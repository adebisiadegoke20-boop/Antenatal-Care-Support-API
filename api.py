from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from httpx import request
from pydantic import BaseModel
from groq import Groq
import os
from dotenv import load_dotenv


load_dotenv()
client = Groq(api_key= os.environ.get ("GROQ_API_KEY"))

app = FastAPI(title= "Antenatal Care Support API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

print("API Client Ready")

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

# Api Models
class Customermessage(BaseModel):
    message: str

# API Endpoints
@app.post("/support")
async def handle_customer_message(request: Customermessage):
    try:
        # Classify
        category = router_agent.run("Classify this message: " + request.message).strip().upper()
        
    # Route to specialized agent 
        if category == "ANTENATAL":
            response = antenatal_agent.run(request.message)
        elif category == "WARNING":
            response = warning_agent.run(request.message)
        elif category == "APPOINTMENT":
            response = appointment_agent.run(request.message)
        elif category == "FEEDBACK":
            response = feedback_agent.run(request.message)
        else:
            response = "I'm sorry, I couldn't classify your request. Please provide more details."

        return {
            "success": True,
            "category": category,
            "reply": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/")
async def root():
    return {"status": "Antenatal Care Support API is running."}
