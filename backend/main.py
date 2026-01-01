import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.chat import router as chat_router
from scalar_fastapi import get_scalar_api_reference

# Inisialisasi FastAPI
app = FastAPI(
    title="MindSchedule AI Backend",
    description="Backend API untuk asisten jadwal mahasiswa menggunakan Gemini AI",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
)

# Konfigurasi CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Menghubungkan rute API (Endpoint: /api/chat)
app.include_router(chat_router, prefix="/api")

# Endpoint Dokumentasi Modern (Scalar)
@app.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
        dark_mode=True, # Mengaktifkan tema Dark Mode
    )

@app.get("/")
def home():
    """Endpoint untuk mengecek apakah server sudah berjalan"""
    return {
        "status": "Online",
        "message": "Server MindSchedule AI aktif!",
        "platform": "Hugging Face Spaces",
        "documentation": "/docs" # Memberikan petunjuk link docs baru
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port)