class ScheduleManager:
    def __init__(self):
        # Jadwal Dasar Kuliah (Sama untuk semua)
        self.base_college = {
            "Senin": ["Machine Learning"],
            "Selasa": ["Pengembangan Aplikasi Mobile"],
            "Rabu": ["NLP", "Etika Profesi"],
            "Kamis": ["Kerja Praktik"],
            "Jumat": ["Kosong / Mandiri"],
            "Sabtu": ["Data Mining", "RPL Spesifik Domain"]
        }

        # Tambahan kegiatan spesifik per profil
        self.user_activities = {
            "kevin": { # Jadwal Padat
                "Senin": ["17:00 - Rapat Organisasi"],
                "Rabu": ["16:00 - Kursus Bahasa Inggris"],
                "Sabtu": ["08:00 - Workshop Online"]
            },
            "faisal": { # Jadwal Super Padat
                "Senin": ["18:00 - Kerja Shift Malam", "22:00 - Belajar Mandiri Kanji"],
                "Selasa": ["19:00 - Pelatihan Bahasa Jepang"],
                "Rabu": ["18:00 - Kerja Shift Malam"],
                "Kamis": ["19:00 - Pelatihan Bahasa Jepang"],
                "Jumat": ["18:00 - Kerja Shift Malam"],
                "Sabtu": ["19:00 - Review Materi JLPT"]
            }
        }

    def get_summary(self, user_type="tuti"):
        user_type = user_type.lower()
        summary = f"Profil Jadwal: {user_type.capitalize()}\n"
        
        for day, classes in self.base_college.items():
            daily_list = classes.copy()
            
            # Tambahkan kegiatan sesuai tipe user
            if user_type in self.user_activities and day in self.user_activities[user_type]:
                daily_list += self.user_activities[user_type][day]
                
            summary += f"- {day}: {', '.join(daily_list)}\n"
        
        if user_type == "faisal":
            summary += "\nSTATUS: KRITIS. Kapasitas waktu sudah 100% terisi (Kuliah + Kerja + Jepang)."
            
        return summary

schedule_manager = ScheduleManager()