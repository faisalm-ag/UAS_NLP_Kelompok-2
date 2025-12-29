class PromptBuilder:
    @staticmethod
    def build_prompt(user_input, intent, schedule_info=None):
        if intent == "mental_health":
            instruction = "Fokuslah memberikan dukungan emosional yang empati."
        elif intent == "academic":
            instruction = "Berikan saran akademik yang praktis."
        else:
            instruction = "Bantu mahasiswa mengelola waktunya."

        schedule_context = f"\nJadwal: {schedule_info}" if schedule_info else ""
        
        return f"Instruction: {instruction}{schedule_context}\nUser: {user_input}\nAssistant:"

# JANGAN LUPA BARIS INI:
prompt_builder = PromptBuilder()