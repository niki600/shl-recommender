# main.py
# Ye FastAPI server hai - assignment ka main entry point

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import ChatRequest, ChatResponse, Recommendation
from agent import process_conversation

# FastAPI app banao
app = FastAPI(
    title="SHL Assessment Recommender",
    description="Conversational agent for SHL assessment recommendations",
    version="1.0.0"
)

# CORS middleware - bahar se calls allow karne ke liye
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---- ENDPOINT 1: Health Check ----
@app.get("/health")
def health_check():
    """
    Assignment requirement: GET /health must return {"status": "ok"} with HTTP 200
    Evaluator pehle yahi call karega check karne ke liye ki server chal raha hai
    """
    return {"status": "ok"}


# ---- ENDPOINT 2: Chat ----
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Main endpoint - conversation history lo, next reply do
    
    Assignment ke rules:
    - Max 8 turns (user + assistant combined)
    - 30 second timeout
    - Schema EXACTLY as defined in assignment
    """
    
    # Validation: messages empty nahi hone chahiye
    if not request.messages:
        raise HTTPException(status_code=400, detail="Messages cannot be empty")
    
    # Turn limit check (8 turns max)
    if len(request.messages) > 8:
        return ChatResponse(
            reply="We've reached the maximum conversation length. Based on our discussion, here are my final recommendations. Thank you!",
            recommendations=[],
            end_of_conversation=True
        )
    
    # Messages ko dict format mein convert karo agent ke liye
    messages = [
        {"role": msg.role, "content": msg.content}
        for msg in request.messages
    ]
    
    # Agent se response lo
    result = process_conversation(messages)
    
    # Response banao (exact schema jo assignment mein diya hai)
    recommendations = [
        Recommendation(
            name=rec["name"],
            url=rec["url"],
            test_type=rec["test_type"]
        )
        for rec in result.get("recommendations", [])
    ]
    
    return ChatResponse(
        reply=result["reply"],
        recommendations=recommendations,
        end_of_conversation=result.get("end_of_conversation", False)
    )


# Local testing ke liye
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
