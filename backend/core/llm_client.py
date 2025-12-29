import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("❌ GEMINI_API_KEY tidak ditemukan di .env")
            
        genai.configure(api_key=api_key)
        
        # MENCARI MODEL OTOMATIS
        self.model_name = None
        try:
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if available_models:
                # Ambil yang terbaru (biasanya flash atau pro)
                self.model_name = available_models[0]
                print(f"✅ Gemini Client menggunakan model: {self.model_name}")
                self.model = genai.GenerativeModel(self.model_name)
            else:
                print("❌ Tidak ada model yang mendukung generateContent.")
        except Exception as e:
            print(f"❌ Gagal mengambil daftar model: {e}")

    def get_ai_response(self, prompt, context=""):
        if not self.model_name:
            return "⚠️ Error: Model AI tidak tersedia. Cek API Key atau koneksi."
            
        try:
            full_prompt = f"Context: {context}\n\nUser Question: {prompt}"
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"⚠️ Detail Error: {str(e)}"

llm_client = GeminiClient()