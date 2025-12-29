class ScheduleManager:
    def __init__(self):
        # Jadwal Dasar Kuliah (Sesuai list Anda)
        self.base_college = {
            "Senin": ["Machine Learning"],
            "Selasa": ["Pengembangan Aplikasi Mobile"],
            "Rabu": ["NLP", "Etika Profesi"],
            "Kamis": ["Kerja Praktik"],
            "Jumat": ["Kosong / Mandiri"],
            "Sabtu": ["Data Mining", "RPL Spesifik Domain"]
        }

        # Tambahan kegiatan untuk User Padat
        self.busy_activities = {
            "Senin": ["07:00 - Rapat Organisasi", "19:00 - Freelance Project"],
            "Rabu": ["16:00 - Kursus Bahasa Inggris"],
            "Kamis": ["19:00 - Evaluasi KP"],
            "Sabtu": ["08:00 - Workshop Online"]
        }

    def get_summary(self, user_type="biasa"):
        summary = "Jadwal Kamu:\n"
        for day, classes in self.base_college.items():
            daily_list = classes.copy()
            
            # Jika user padat, tambahkan kegiatan tambahan
            if user_type == "padat" and day in self.busy_activities:
                daily_list += self.busy_activities[day]
                
            summary += f"- {day}: {', '.join(daily_list)}\n"
        return summary

schedule_manager = ScheduleManager()