# SHL Assessment Recommender Agent

A conversational AI agent built using FastAPI and Gemini for recommending SHL assessments based on hiring requirements.

---

# Features

* Conversational assessment recommendation
* Handles vague queries with clarification
* Recommends only SHL catalog assessments
* Stateless conversation handling
* FastAPI REST API
* JSON schema compliant responses
* Supports up to 10 recommendations
* Handles refinement and conversational context

---

# Tech Stack

* Python
* FastAPI
* Gemini API
* Pydantic
* Uvicorn

---

# Project Structure

.
├── app.py
├── agent.py
├── catalog.py
├── models.py
├── requirements.txt
├── README.md
├── data/
│   └── catalog.json

---

# Setup Instructions

## 1. Create Virtual Environment

```bash
python -m venv venv
```

## 2. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the root directory.

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

# Run the Server

```bash
python -m uvicorn app:app --reload
```

Server will run at:

```text
http://127.0.0.1:8000
```

---

# API Endpoints

## 1. Health Check

### GET /health

Response:

```json
{
  "status": "ok"
}
```

---

## 2. Chat Endpoint

### POST /chat

Request:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "We are hiring a mid-level Java developer with backend development and problem solving skills"
    }
  ]
}
```

Response:

```json
{
  "reply": "Here are some recommended SHL assessments for this role.",
  "recommendations": [
    {
      "name": "Java 8 (New)",
      "url": "https://www.shl.com/",
      "test_type": "K"
    }
  ],
  "end_of_conversation": true
}
```

---

# Functionalities Implemented

* Clarifies vague queries before recommendation
* Recommends relevant SHL assessments
* Uses SHL catalog data only
* Returns valid structured JSON
* Stateless conversation handling
* URL validation through catalog
* Supports conversational refinement

---

# Notes

* Recommendations are strictly generated from the provided SHL catalog.
* Maximum recommendation count is capped at 10.
* Conversation history is passed in every request.
* The API follows the schema specified in the assignment.

---

# Author

Nikita Swain
