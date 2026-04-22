document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById("chatbot-toggle-btn");
    const container = document.getElementById("chatbot-container");
    const closeBtn = document.getElementById("chatbot-close-btn");
    const inputField = document.getElementById("chatbot-input-field");
    const sendBtn = document.getElementById("chatbot-send-btn");
    const messagesDiv = document.getElementById("chatbot-messages");

    let sessionId = null;

    // 開關 UI 邏輯
    toggleBtn.addEventListener("click", () => {
        container.classList.remove("chatbot-hidden");
        toggleBtn.style.display = "none";
    });

    closeBtn.addEventListener("click", () => {
        container.classList.add("chatbot-hidden");
        toggleBtn.style.display = "flex";
    });

    // 協助函數：新增訊息到畫面
    const addMessage = (text, isUser = false) => {
        const msgDiv = document.createElement("div");
        msgDiv.className = isUser ? "message user-message" : "message bot-message";
        
        const avatar = document.createElement("div");
        avatar.className = "msg-avatar";
        avatar.innerHTML = isUser ? "" : '<i class="ri-robot-2-fill"></i>';

        const bubble = document.createElement("div");
        bubble.className = "msg-bubble";
        const p = document.createElement("p");
        p.textContent = text;
        bubble.appendChild(p);

        msgDiv.appendChild(avatar);
        msgDiv.appendChild(bubble);

        messagesDiv.appendChild(msgDiv);
        
        // 滾動到最底部
        setTimeout(() => {
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }, 50);
        return msgDiv;
    };

    // 協助函數：加入打字中的動畫
    const addTypingIndicator = () => {
        const ind = document.createElement("div");
        ind.className = "message bot-message";
        
        const avatar = document.createElement("div");
        avatar.className = "msg-avatar";
        avatar.innerHTML = '<i class="ri-robot-2-fill"></i>';

        const bubble = document.createElement("div");
        bubble.className = "msg-bubble typing-indicator";
        bubble.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';

        ind.appendChild(avatar);
        ind.appendChild(bubble);
        messagesDiv.appendChild(ind);
        
        setTimeout(() => {
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }, 50);
        return ind;
    };

    // 發送訊息邏輯
    const sendMessage = async () => {
        const text = inputField.value.trim();
        if (!text) return;

        // 1. 顯示使用者文字
        addMessage(text, true);
        inputField.value = "";

        // 2. 顯示 AI 正在輸入的動畫
        const indicator = addTypingIndicator();

        try {
            // 3. 打往後端 FastAPI
            const res = await fetch("/api/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    session_id: sessionId,
                    message: text
                })
            });

            if (!res.ok) throw new Error("API request failed");

            const data = await res.json();
            
            // 將伺服器分派的 session_id 儲存下來
            sessionId = data.session_id; 

            // 4. 移除打字動畫，並加入 AI 實際的回覆
            messagesDiv.removeChild(indicator);
            addMessage(data.reply, false);

        } catch (error) {
            console.error(error);
            messagesDiv.removeChild(indicator);
            addMessage("系統錯誤，無法回覆。請稍後再試。", false);
        }
    };

    // 綁定點擊事件與 Enter 鍵
    sendBtn.addEventListener("click", sendMessage);
    inputField.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            sendMessage();
        }
    });
});
