
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.ai import get_ai_response


app = FastAPI(
    title="Sarang AI API",
    description="Intelligent Guitar Shopping Assistant",
    version="1.0.0"
)


# Frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Conversation history model
class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(max_length=4000)


# Incoming chat request
class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    conversation_history: list[ChatMessage] = Field(default_factory=list)


# Home endpoint
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

app.frontend("/", directory=str(BASE_DIR / "frontend"))

# Health endpoint
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# Main chatbot endpoint
@app.post("/api/chat")
def chat(request: ChatRequest):

    try:
        history = [
            item.model_dump()
            for item in request.conversation_history[-10:]
        ]

        response = get_ai_response(
            user_message=request.message,
            conversation_history=history
        )

        return {
            "response": response,
            "status": "success"
        }

    except Exception as error:
        print("Chat endpoint error:", error)

        raise HTTPException(
            status_code=500,
            detail="Something went wrong. Please try again."
        )
