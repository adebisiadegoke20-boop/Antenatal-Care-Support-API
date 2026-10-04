# Antenatal Care Support API

Multi-agent AI customer support API for antenatal care information and support.

Built with FastAPI, Groq, and Pydantic.


## Features

* Multi-agent AI customer support system
* AI-powered request routing
* Antenatal care information agent
* Pregnancy warning signs agent
* Antenatal appointment agent
* Customer feedback agent
* FastAPI REST API
* Groq-powered AI responses
* Lovable frontend
* Render backend deployment

## Endpoints

* `GET /` - Health check
* `POST /support` - Customer message routing and AI response
* `GET /docs` - Interactive API documentation

## Example Request

```json
{
  "message": "What should I know about antenatal appointments?"
}
```

## Response

```json
{
  "success": true,
  "category": "APPOINTMENT",
  "reply": "AI response"
}
```

## Deployment

The backend is deployed on Render and the frontend is deployed on Lovable.
## Live Demo

**Frontend:** https://antenatal-care-support.lovable.app/
**API Documentation:** https://antenatal-care-support-api.onrender.com/docs

## Healthcare Safety
This assistant provides general antenatal information and does not replace professional medical advice. If you have urgent or severe symptoms, seek appropriate medical care immediately.
