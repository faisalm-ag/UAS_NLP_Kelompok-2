import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.chat import router as chat_router

app = FastAPI(title="MindSchedule AI Backend")

# PENTING: Konfigurasi CORS agar Frontend bisa mengakses API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Menghubungkan rute API
app.include_router(chat_router, prefix="/api")

@app.get("/")
def home():
    return {
        "status": "Online",
        "message": "Server MindSchedule AI aktif dan siap melayani!"
    }

if __name__ == "__main__":
    # Mengambil port dari Environment Variable (penting untuk Deploy)
    # Jika di laptop, defaultnya 8000
    port = int(os.environ.get("PORT", 8000))
    
    # Host 0.0.0.0 agar bisa diakses secara publik di server cloud
    # Reload=True hanya aktif jika kita menjalankan di localhost secara manual
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)