from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from chatbot_can import ask_bot

app = FastAPI(
    title="CAN 2025 Chatbot API",
    description="API FastAPI pour l’assistant intelligent CAN 2025",
    version="1.0.0"
)

# Autoriser le frontend HTML
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # en prod → restreindre
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------- MODELE DE DONNEES ---------
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str


# --------- ENDPOINT ---------
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    answer = ask_bot(req.message)
    return {"response": answer}


# --------- TEST ---------
@app.get("/")
def root():
    return {"status": "CAN 2025 Chatbot API running"}
