from backend.core.intent_classifier import classifier
from backend.core.llm_client import llm_client
from backend.core.prompt_builder import prompt_builder
from backend.core.schedule import schedule_manager

class MindScheduleChatbot:
    def chat(self, user_message, user_type="biasa"):
        try:
            # 1. Prediksi Intent menggunakan model .pkl
            intent = classifier.predict(user_message)
            
            # Print di terminal untuk memudahkan demo/debug
            print(f"--- CHAT PROCESS ---")
            print(f"User Type: {user_type}")
            print(f"Input    : {user_message}")
            print(f"Intent   : {intent}")
            
            # 2. Ambil jadwal dari schedule.py berdasarkan profil user
            schedule_info = schedule_manager.get_summary(user_type)

            # 3. Rakit prompt menggunakan prompt_builder.py
            final_prompt = prompt_builder.build_prompt(
                user_input=user_message, 
                intent=intent, 
                schedule_info=schedule_info
            )

            # 4. Kirim ke Gemini API
            ai_response = llm_client.get_ai_response(final_prompt)
            print(f"Status   : Berhasil membalas")
            print(f"--------------------")

            return {
                "intent": intent,
                "chatbot_response": ai_response,
                "user_selected": user_type,
                "status": "success"
            }
        except Exception as e:
            print(f"❌ Error in Chatbot Core: {str(e)}")
            return {
                "intent": "error",
                "chatbot_response": f"Sistem sedang mengalami gangguan teknis: {str(e)}",
                "user_selected": user_type,
                "status": "error"
            }

# Inisialisasi object agar bisa langsung di-import di api/chat.py
chatbot_core = MindScheduleChatbot()