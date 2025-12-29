const chatArea = document.getElementById("chatArea");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const userStatus = document.getElementById("userStatus");

let selectedUserType = "";

/**
 * Fungsi untuk menangani pemilihan profil di awal (Login Overlay)
 */
function selectUser(type) {
    selectedUserType = type;
    
    // Sembunyikan overlay pemilihan user
    document.getElementById("loginOverlay").style.display = "none";
    
    // Tentukan nama profil untuk tampilan
    const profileName = type === 'padat' ? 'User Padat' : 'User Biasa';
    
    // Update status di header
    userStatus.textContent = `MODE: ${profileName.toUpperCase()}`;
    userStatus.classList.replace("text-slate-500", "text-blue-400");
    
    // Kirim pesan sambutan pertama dari AI secara otomatis
    // Menggunakan nama profil pilihan sebagai sapaan
    addMessage(`🧠 **Halo ${profileName}!** Saya sudah siap mendampingimu. Apa ada kendala jadwal atau perasaan stres yang ingin kamu ceritakan hari ini?`, "ai");
}

/**
 * Fungsi untuk menambahkan gelembung chat ke layar
 * Dilengkapi dengan Markdown Parser sederhana (Bold, Italic, Bullet)
 */
function addMessage(text, sender) {
    const bubble = document.createElement("div");
    bubble.className = sender === "user" ? "chat-user" : "chat-ai";
    
    // Logic untuk mengubah teks Markdown menjadi tag HTML
    let formattedText = text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Mengubah **teks** jadi tebal
        .replace(/\*(.*?)\*/g, '<em>$1</em>')            // Mengubah *teks* jadi miring
        .replace(/^\s*[\-\*]\s+(.*)/gm, '• $1')          // Mengubah tanda - atau * di awal baris jadi bullet point
        .replace(/\n/g, '<br>');                         // Mengubah baris baru (enter) menjadi tag <br>

    bubble.innerHTML = formattedText;
    chatArea.appendChild(bubble);
    
    // Otomatis scroll ke pesan paling bawah
    chatArea.scrollTop = chatArea.scrollHeight;
}

/**
 * Fungsi untuk menampilkan indikator sedang mengetik
 */
function showTyping() {
    const typing = document.createElement("div");
    typing.className = "chat-ai opacity-50 italic text-sm flex items-center";
    typing.id = "typingIndicator";
    typing.innerHTML = `<span class="mr-2 animate-bounce">🧠</span> MindSchedule sedang menganalisis...`;
    chatArea.appendChild(typing);
    chatArea.scrollTop = chatArea.scrollHeight;
}

/**
 * Fungsi untuk menghapus indikator sedang mengetik
 */
function removeTyping() {
    const typing = document.getElementById("typingIndicator");
    if (typing) typing.remove();
}

/**
 * Fungsi utama untuk mengirim pesan ke Backend FastAPI
 */
async function sendMessage() {
    const message = userInput.value.trim();
    
    // Validasi agar tidak mengirim pesan kosong atau jika user belum dipilih
    if (!message || selectedUserType === "") return;

    // Tampilkan pesan user di layar
    addMessage(message, "user");
    userInput.value = ""; // Kosongkan input
    showTyping();

    try {
        // Request ke backend menggunakan Fetch API
        const response = await fetch("http://127.0.0.1:8000/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: message,
                user_type: selectedUserType
            })
        });

        if (!response.ok) throw new Error("Server bermasalah");

        const data = await response.json();
        removeTyping();

        if (data.chatbot_response) {
            addMessage(data.chatbot_response, "ai");
        } else {
            addMessage("⚠️ Maaf, sistem tidak memberikan respon valid.", "ai");
        }

    } catch (error) {
        removeTyping();
        addMessage("⚠️ **Gagal terhubung ke server.** Pastikan terminal Python sudah menjalankan `python -m backend.main`.", "ai");
        console.error("Error Detail:", error);
    }
}

// Event Listeners
sendBtn.addEventListener("click", sendMessage);

userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        sendMessage();
    }
});