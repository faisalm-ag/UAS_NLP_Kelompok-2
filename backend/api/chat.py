from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.core.chatbot import chatbot_core

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    user_type: str = "tuti" # Default ke Tuti (Biasa)

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not request.message:
        raise HTTPException(status_code=400, detail="Pesan tidak boleh kosong")
    
    try:
        # Mengirim user_type ke chatbot_core
        result = chatbot_core.chat(
            user_message=request.message, 
            user_type=request.user_type.lower()
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))