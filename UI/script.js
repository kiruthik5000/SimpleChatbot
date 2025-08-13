document.addEventListener("DOMContentLoaded", function () {
    const sendBtn = document.getElementById("sendBtn");
    const userInput = document.getElementById("userInput");

    sendBtn.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", function (e) {
        if (e.key === "Enter") sendMessage();
    });

    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        addMessage(message, "user-message");
        userInput.value = "";

        // Call backend API for response
        try {
            const botReply = await getBotReply(message);
            addMessage(botReply, "bot-message");
        } catch (error) {
            addMessage("Error: Could not fetch reply.", "bot-message");
            console.error(error);
        }
    }

    async function getBotReply(userMessage) {
        const response = await fetch("http://127.0.0.1:8000/get_response", { // Your backend URL
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ user_message: userMessage })
        });

        if (!response.ok) {
            throw new Error("API request failed");
        }

        const data = await response.json();
        console.log(data)
        return data.response; // The backend should return { reply: "text" }
    }

    function addMessage(text, className) {
        const chatMessages = document.getElementById("chatMessages");
        const msg = document.createElement("div");
        msg.className = "message " + className;
        msg.textContent = text;
        chatMessages.appendChild(msg);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
