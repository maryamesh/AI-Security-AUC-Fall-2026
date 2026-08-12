from uuid import uuid4

from fastapi import FastAPI

from app.agent import respond
from app.models import ChatRequest, ChatResponse


app = FastAPI(
    title="MedSynth — Breaking the Assistant",
    description=(
        "Controlled direct prompt-injection lab using entirely fictional data."
    ),
    version="1.0.0",
)


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(
        response=respond(request.message),
        request_id=f"MED-{uuid4().hex[:8].upper()}",
    )
