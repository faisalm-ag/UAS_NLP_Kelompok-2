import streamlit as st
import requests

# Konfigurasi Halaman
st.set_page_config(page_title="MindSchedule AI", page_icon="🧠")

# URL API Hugging Face kamu (Gunakan URL yang sama dengan script.js)
API_URL = "https://faisalm-ag-mindschedule.hf.space/api/chat"

st.title("🧠 MindSchedule AI Assistant")
st.markdown("---")

# 1. Pilihan Profil (Simulasi Login)
if "user_type" not in st.session_state:
    st.subheader("Pilih Profil Anda")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("User Biasa (Kuliah Saja)"):
            st.session_state.user_type = "biasa"
            st.rerun()
    with col2:
        if st.button("User Padat (Kuliah + Kerja)"):
            st.session_state.user_type = "padat"
            st.rerun()
else:
    # Tampilan Chat jika sudah pilih profil
    st.sidebar.info(f"Mode: {st.session_state.user_type.upper()}")
    if st.sidebar.button("Reset Profil"):
        del st.session_state.user_type
        st.session_state.messages = []
        st.rerun()

    # Inisialisasi Riwayat Pesan
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Tampilkan Riwayat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input User
    if prompt := st.chat_input("Tanya jadwal atau ceritakan kendalamu..."):
        # Tampilkan pesan user
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Kirim ke Backend Hugging Face
        with st.chat_message("assistant"):
            with st.spinner("MindSchedule sedang menganalisis..."):
                try:
                    payload = {
                        "message": prompt,
                        "user_type": st.session_state.user_type
                    }
                    response = requests.post(API_URL, json=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        full_response = data.get("chatbot_response", "Maaf, respon kosong.")
                        st.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                    else:
                        st.error("Gagal terhubung ke API.")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")