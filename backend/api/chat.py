from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.core.chatbot import chatbot_core

router = APIRouter()

# Struktur data yang diterima dari Frontend (script.js)
class ChatRequest(BaseModel):
    message: str
    user_type: str = "biasa"  # Default ke biasa jika tidak dikirim

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not request.message:
        raise HTTPException(status_code=400, detail="Pesan tidak boleh kosong")
    
    try:
        # PENTING: Nama parameter harus 'user_type' sesuai dengan definisi di chatbot.py
        result = chatbot_core.chat(
            user_message=request.message, 
            user_type=request.user_type
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))