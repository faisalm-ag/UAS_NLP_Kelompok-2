import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Ambil dari .env
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    # Path untuk model ML lokal
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_PATH = os.path.join(BASE_DIR, "../model/intent_model.pkl")
    VECTORIZER_PATH = os.path.join(BASE_DIR, "../model/tfidf_vectorizer.pkl")

settings = Settings()