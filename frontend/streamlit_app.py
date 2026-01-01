import streamlit as st
import requests

# Konfigurasi Halaman
st.set_page_config(page_title="MindSchedule AI", page_icon="🧠", layout="centered")

# URL API (Sesuaikan jika sudah dideploy ke Hugging Face)
API_URL = "https://faisalm-ag-mindschedule.hf.space/api/chat"

st.title("🧠 MindSchedule")
st.caption("Asisten Manajemen Jadwal & Kesehatan Mental Mahasiswa")
st.markdown("---")

# 1. Pilihan Profil (Simulasi Login dengan 3 User)
if "user_type" not in st.session_state:
    st.subheader("Silakan Login / Pilih Profil Mahasiswa")
    
    # Membuat 3 kolom untuk 3 profil berbeda
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("https://api.dicebear.com/7.x/avataaars/svg?seed=Tuti", width=100)
        if st.button("Tuti Maesaroh"):
            st.session_state.user_type = "tuti"
            st.session_state.user_name = "Tuti Maesaroh"
            st.rerun()
        st.caption("Jadwal: Normal")

    with col2:
        st.image("https://api.dicebear.com/7.x/avataaars/svg?seed=Kevin", width=100)
        if st.button("Kevin Nurachman"):
            st.session_state.user_type = "kevin"
            st.session_state.user_name = "Kevin Nurachman"
            st.rerun()
        st.caption("Jadwal: Padat")

    with col3:
        st.image("https://api.dicebear.com/7.x/avataaars/svg?seed=Faisal", width=100)
        if st.button("Faisal Ghani"):
            st.session_state.user_type = "faisal"
            st.session_state.user_name = "Faisal Ghani"
            st.rerun()
        st.caption("Jadwal: Super Padat")

else:
    # --- SIDEBAR INFO ---
    st.sidebar.title("Profil Aktif")
    st.sidebar.markdown(f"**Nama:** {st.session_state.user_name}")
    
    # Indikator Visual Kepadatan Jadwal
    if st.session_state.user_type == "faisal":
        st.sidebar.error("Status: SUPER PADAT (High Burnout Risk)")
    elif st.session_state.user_type == "kevin":
        st.sidebar.warning("Status: PADAT (Organisasi aktif)")
    else:
        st.sidebar.success("Status: NORMAL (Fokus Kuliah)")

    if st.sidebar.button("Logout / Reset Profil"):
        del st.session_state.user_type
        del st.session_state.user_name
        st.session_state.messages = []
        st.rerun()

    # --- CHAT INTERFACE ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Tampilkan Riwayat Chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input User
    if prompt := st.chat_input("Tanya jadwal atau bicarakan perasaanmu hari ini..."):
        # Tampilkan pesan user
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Kirim ke Backend
        with st.chat_message("assistant"):
            with st.spinner("MindSchedule sedang berpikir..."):
                try:
                    payload = {
                        "message": prompt,
                        "user_type": st.session_state.user_type
                    }
                    response = requests.post(API_URL, json=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        # Pastikan key 'chatbot_response' sesuai dengan return dari backend/core/chatbot.py
                        full_response = data.get("chatbot_response", "Maaf, sistem tidak memberikan jawaban.")
                        st.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                    else:
                        st.error(f"Gagal terhubung ke API (Status: {response.status_code})")
                except Exception as e:
                    st.error(f"Koneksi backend gagal: {e}")