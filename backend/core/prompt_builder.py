class PromptBuilder:
    @staticmethod
    def build_prompt(user_input, intent, schedule_info=None, user_type="tuti"):
        user_type = user_type.lower()
        
        # Logika Instruksi Berdasarkan Profil
        if user_type == "faisal":
            instruction = (
                "Anda adalah asisten kesehatan mental yang sangat protektif. "
                "User (Faisal) memiliki jadwal SUPER PADAT. Jika dia ingin menambah jadwal, "
                "TOLAK secara halus, ingatkan tentang bahaya burnout, dan sarankan untuk istirahat."
            )
        elif intent == "mental_health":
            instruction = "Berikan dukungan emosional yang empati dan menenangkan."
        else:
            instruction = "Bantu mahasiswa mengelola waktunya dengan efisien."

        schedule_context = f"\nKonteks Jadwal Aktif:\n{schedule_info}" if schedule_info else ""
        
        return (
            f"Instruction: {instruction}\n"
            f"{schedule_context}\n"
            f"User Input: {user_input}\n"
            f"Assistant Response:"
        )

prompt_builder = PromptBuilder()