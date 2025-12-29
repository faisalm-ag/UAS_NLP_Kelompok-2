import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.chat import router as chat_router

# Inisialisasi FastAPI
app = FastAPI(
    title="MindSchedule AI Backend",
    description="Backend API untuk asisten jadwal mahasiswa menggunakan Gemini AI",
    version="1.0.0"
)

# Konfigurasi CORS: Sangat penting agar Frontend (HTML/Streamlit) bisa memanggil API ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Menghubungkan rute API (Endpoint: /api/chat)
app.include_router(chat_router, prefix="/api")

@app.get("/")
def home():
    """Endpoint untuk mengecek apakah server sudah berjalan"""
    return {
        "status": "Online",
        "message": "Server MindSchedule AI aktif dan siap melayani!",
        "platform": "Hugging Face Spaces"
    }

if __name__ == "__main__":
    # Hugging Face menggunakan port 7860 secara default.
    # Jika variabel PORT tidak ditemukan, maka akan menggunakan 7860.
    port = int(os.environ.get("PORT", 7860))
    
    # Menjalankan server menggunakan Uvicorn
    # host "0.0.0.0" wajib digunakan agar server bisa menerima koneksi dari luar
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port)