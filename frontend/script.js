const chatArea = document.getElementById("chatArea");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const userStatus = document.getElementById("userStatus");

let selectedUserType = "";

// URL Backend Hugging Face kamu
const API_URL = "https://faisalm-ag-mindschedule.hf.space/api/chat";

/**
 * Fungsi untuk menangani pemilihan profil di awal
 */
function selectUser(type) {
    selectedUserType = type;
    
    // Sembunyikan overlay pemilihan user
    document.getElementById("loginOverlay").style.display = "none";
    
    const profileName = type === 'padat' ? 'User Padat' : 'User Biasa';
    
    // Update status di header
    userStatus.textContent = `MODE: ${profileName.toUpperCase()}`;
    userStatus.classList.replace("text-slate-500", "text-blue-400");
    
    // Kirim pesan sambutan pertama
    addMessage(`🧠 **Halo ${profileName}!** Saya sudah siap mendampingimu. Apa ada kendala jadwal atau perasaan stres yang ingin kamu ceritakan hari ini?`, "ai");
}

/**
 * Fungsi untuk menambahkan gelembung chat
 */
function addMessage(text, sender) {
    const bubble = document.createElement("div");
    bubble.className = sender === "user" ? "chat-user" : "chat-ai";
    
    // Markdown Parser sederhana
    let formattedText = text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') 
        .replace(/\*(.*?)\*/g, '<em>$1</em>')            
        .replace(/^\s*[\-\*]\s+(.*)/gm, '• $1')          
        .replace(/\n/g, '<br>');                         

    bubble.innerHTML = formattedText;
    chatArea.appendChild(bubble);
    chatArea.scrollTop = chatArea.scrollHeight;
}

function showTyping() {
    const typing = document.createElement("div");
    typing.className = "chat-ai opacity-50 italic text-sm flex items-center";
    typing.id = "typingIndicator";
    typing.innerHTML = `<span class="mr-2 animate-bounce">🧠</span> MindSchedule sedang menganalisis...`;
    chatArea.appendChild(typing);
    chatArea.scrollTop = chatArea.scrollHeight;
}

function removeTyping() {
    const typing = document.getElementById("typingIndicator");
    if (typing) typing.remove();
}

/**
 * Fungsi utama untuk mengirim pesan ke Backend Hugging Face
 */
async function sendMessage() {
    const message = userInput.value.trim();
    
    if (!message || selectedUserType === "") return;

    addMessage(message, "user");
    userInput.value = ""; 
    showTyping();

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: message,
                user_type: selectedUserType
            })
        });

        if (!response.ok) throw new Error("Server Hugging Face bermasalah");

        const data = await response.json();
        removeTyping();

        if (data.chatbot_response) {
            addMessage(data.chatbot_response, "ai");
        } else {
            addMessage("⚠️ Maaf, sistem tidak memberikan respon valid.", "ai");
        }

    } catch (error) {
        removeTyping();
        addMessage("⚠️ **Gagal terhubung ke AI.** Pastikan backend di Hugging Face statusnya masih 'Running'.", "ai");
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