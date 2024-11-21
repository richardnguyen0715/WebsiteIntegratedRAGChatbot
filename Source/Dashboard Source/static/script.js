function toggleChat() {
    const chatWindow = document.getElementById('chat-window');
    chatWindow.classList.toggle('active');
}

function sendMessage() {
    const inputBox = document.getElementById('chat-input-box');
    const chatMessages = document.getElementById('chat-messages');
    const message = inputBox.value.trim();

    if (message) {
        // user chat
        const userMessage = document.createElement('div');
        userMessage.className = 'chat-message user';

        const userIcon = document.createElement('div');
        userIcon.className = 'user-icon';
        userIcon.innerHTML = '<i class="fas fa-user"></i>';

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = message;

        userMessage.appendChild(userIcon);
        userMessage.appendChild(messageContent);

        chatMessages.appendChild(userMessage);

        inputBox.value = '';

        // chat bot response
        setTimeout(() => {
            const botMessage = document.createElement('div');
            botMessage.className = 'chat-message bot';

            const botIcon = document.createElement('div');
            botIcon.className = 'bot-icon';
            botIcon.innerHTML = '<i class="fas fa-robot"></i>';

            const botMessageContent = document.createElement('div');
            botMessageContent.className = 'message-content';
            botMessageContent.textContent = `This is a response to "${message}"`;

            botMessage.appendChild(botIcon);
            botMessage.appendChild(botMessageContent);

            chatMessages.appendChild(botMessage);

            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 1000);
    }
}



// get the enter
document.getElementById('chat-input-box').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});