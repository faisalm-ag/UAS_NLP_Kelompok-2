const chatArea = document.getElementById("chatArea");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const userStatus = document.getElementById("userStatus");
const inputShadow = document.getElementById("inputShadow");

let selectedUserType = "";
const API_URL = "https://faisalm-ag-mindschedule.hf.space/api/chat";

/**
 * Pemilihan User & Inisialisasi
 */
function selectUser(type) {
    selectedUserType = type;
    document.getElementById("loginOverlay").style.display = "none";
    
    let profileName = "";
    let statusColor = "";

    if (type === 'faisal') {
        profileName = 'Faisal Ghani';
        statusColor = "text-red-400";
    } else if (type === 'padat') {
        profileName = 'Kevin Nurachman';
        statusColor = "text-yellow-400";
    } else {
        profileName = 'Tuti Maesaroh';
        statusColor = "text-green-400";
    }

    userStatus.textContent = `MODE: ${profileName.toUpperCase()}`;
    userStatus.className = `text-[10px] mt-1 uppercase tracking-widest font-bold ${statusColor}`;
    
    // Sambutan pertama dengan animasi mengetik
    const welcome = `🧠 **Halo ${profileName}!** Saya MindSchedule AI. Saya melihat profil jadwalmu dan siap membantumu mengatur waktu atau mendengarkan keluh kesahmu. Apa yang bisa saya bantu?`;
    addMessage("", "ai", welcome);
}

async function typeWriter(element, text) {
    element.classList.add("typing-cursor");
    const words = text.split(" ");
    let displayedText = "";
    
    for (let i = 0; i < words.length; i++) {
        displayedText += words[i] + " ";
        element.innerHTML = parseMarkdown(displayedText);
        chatArea.scrollTop = chatArea.scrollHeight;
        // Kecepatan mengetik (30ms per kata agar terasa natural)
        await new Promise(resolve => setTimeout(resolve, 35));
    }
    element.classList.remove("typing-cursor");
}

function parseMarkdown(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') 
        .replace(/\*(.*?)\*/g, '<em>$1</em>')            
        .replace(/^\s*[\-\*]\s+(.*)/gm, '• $1')          
        .replace(/\n/g, '<br>');
}

function addMessage(text, sender, fullTextAI = "") {
    const bubble = document.createElement("div");
    bubble.className = sender === "user" ? "chat-user" : "chat-ai";
    chatArea.appendChild(bubble);

    if (sender === "user") {
        bubble.innerHTML = parseMarkdown(text);
    } else {
        // Animasi mengetik untuk AI
        typeWriter(bubble, fullTextAI || text);
    }
    chatArea.scrollTop = chatArea.scrollHeight;
}

userInput.addEventListener("input", function() {
    this.style.height = "auto";
    let newHeight = this.scrollHeight;
    this.style.height = newHeight + "px";

    // Batas maksimal 4-5 baris (sekitar 115px)
    if (newHeight > 115) {
        this.style.overflowY = "auto";
        inputShadow.classList.remove("hidden");
    } else {
        this.style.overflowY = "hidden";
        inputShadow.classList.add("hidden");
    }
});

/**
 * Fungsi Kirim Pesan ke API
 */
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message || selectedUserType === "") return;

    // Tampilkan pesan user & reset input
    addMessage(message, "user");
    userInput.value = "";
    userInput.style.height = "56px";
    inputShadow.classList.add("hidden");

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

        const data = await response.json();
        removeTyping();

        if (data.chatbot_response) {
            addMessage("", "ai", data.chatbot_response);
        } else {
            addMessage("⚠️ Gagal mendapatkan balasan dari AI.", "ai");
        }
    } catch (error) {
        removeTyping();
        addMessage("⚠️ **Kesalahan Koneksi.** Pastikan Backend aktif.", "ai");
        console.error(error);
    }
}

/**
 * UI Helpers
 */
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

// Event Listeners
sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});