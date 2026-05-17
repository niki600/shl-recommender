# models.py
# Ye file define karti hai - API mein kya aayega (request) aur kya jaayega (response)

from pydantic import BaseModel
from typing import List, Optional


# ---- REQUEST MODELS ----

class Message(BaseModel):
    """Ek message - either user ka ya assistant ka"""
    role: str          # "user" ya "assistant"
    content: str       # actual message text


class ChatRequest(BaseModel):
    """Jo POST /chat mein aayega"""
    messages: List[Message]   # poori conversation history


# ---- RESPONSE MODELS ----

class Recommendation(BaseModel):
    """Ek assessment recommendation"""
    name: str        # assessment ka naam
    url: str         # SHL catalog link
    test_type: str   # "K" = Knowledge, "P" = Personality, "A" = Ability, "S" = Simulation


class ChatResponse(BaseModel):
    """Jo POST /chat return karega - YE SCHEMA BADALNA NAHI HAI"""
    reply: str                              # agent ka text reply
    recommendations: List[Recommendation]  # assessments list (empty ya 1-10 items)
    end_of_conversation: bool               # kya conversation khatam ho gayi?
