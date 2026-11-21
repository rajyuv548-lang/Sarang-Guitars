
// ======================================
// SARANG AI - CHATBOT FUNCTIONALITY
// ======================================

const API_URL = "/api/chat";

const chatForm = document.getElementById("chatForm");
const userInput = document.getElementById("userInput");
const chatMessages = document.getElementById("chatMessages");
const sendButton = document.getElementById("sendButton");

// Store conversation history
let conversationHistory = [];


// ======================================
// ADD MESSAGE TO CHAT
// ======================================

function addMessage(message, sender) {
    const messageElement = document.createElement("div");

    messageElement.classList.add("message");

    if (sender === "user") {
        messageElement.classList.add("user-message");
    } else {
        messageElement.classList.add("bot-message");
    }

    messageElement.textContent = message;

    chatMessages.appendChild(messageElement);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}


// ======================================
// TYPING INDICATOR
// ======================================

function showTypingIndicator() {
    const typing = document.createElement("div");

    typing.classList.add("message", "bot-message");
    typing.id = "typingIndicator";
    typing.textContent = "Sarang AI is thinking...";

    chatMessages.appendChild(typing);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}


function removeTypingIndicator() {
    const typing = document.getElementById("typingIndicator");

    if (typing) {
        typing.remove();
    }
}


// ======================================
// SEND MESSAGE TO FASTAPI
// ======================================

async function sendMessage(message) {

    const cleanMessage = message.trim();

    if (!cleanMessage || sendButton.disabled) return;

    // Display customer message
    addMessage(cleanMessage, "user");

    userInput.value = "";

    sendButton.disabled = true;
    sendButton.textContent = "...";

    showTypingIndicator();

    try {

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: cleanMessage,
                conversation_history: conversationHistory
            })

        });


        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }


        const data = await response.json();

        if (!data.response) {
            throw new Error("Invalid response from Sarang AI.");
        }

        // Save conversation context
        conversationHistory.push(
            { role: "user", content: cleanMessage },
            { role: "assistant", content: data.response }
        );

        // Keep only recent messages
        conversationHistory = conversationHistory.slice(-10);

        removeTypingIndicator();

        addMessage(data.response, "bot");

    }

    catch (error) {

        console.error("Sarang AI Error:", error);

        removeTypingIndicator();

        addMessage(
            "I'm having trouble connecting right now. Please check that the Sarang AI server is running and try again.",
            "bot"
        );

    }

    finally {

        sendButton.disabled = false;
        sendButton.textContent = "Send ↑";

        userInput.focus();

    }

}


// ======================================
// FORM SUBMISSION
// ======================================

chatForm.addEventListener("submit", function(event) {

    event.preventDefault();

    sendMessage(userInput.value);

});


// ======================================
// SUGGESTED PROMPTS
// ======================================

const suggestionButtons = document.querySelectorAll(".suggestion");

suggestionButtons.forEach(button => {

    button.addEventListener("click", function() {

        sendMessage(button.textContent);

    });

});


console.log("Sarang AI frontend connected to FastAPI!");
