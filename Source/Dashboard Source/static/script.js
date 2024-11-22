function toggleChat() {
    const chatWindow = document.getElementById('chat-window');
    chatWindow.classList.toggle('active');
}

function sendMessage() {
    const inputBox = document.getElementById('chat-input-box');
    const chatMessages = document.getElementById('chat-messages');
    const message = inputBox.value.trim();

    if (message) {
        // Thêm tin nhắn của người dùng
        const userMessage = document.createElement('div');
        userMessage.className = 'chat-message user';

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = message;

        userMessage.appendChild(messageContent);
        chatMessages.appendChild(userMessage);

        inputBox.value = ''; // Reset input box

        // Hiển thị trạng thái loading trong khi chờ phản hồi
        const loadingMessage = document.createElement('div');
        loadingMessage.className = 'chat-message bot loading';
        loadingMessage.textContent = 'Bot is typing...';
        chatMessages.appendChild(loadingMessage);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Gửi tin nhắn tới backend
        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: message }),
        })
            .then(response => response.json())
            .then(data => {
                // Xóa trạng thái loading
                chatMessages.removeChild(loadingMessage);

                // Thêm phản hồi của bot
                const botMessage = document.createElement('div');
                botMessage.className = 'chat-message bot';

                const botMessageContent = document.createElement('div');
                botMessageContent.className = 'message-content';

                try {
                    // Xử lý Markdown
                    const markdownResponse = data.response || 'No response provided.';
                    const htmlContent = marked.parse(markdownResponse);
                    botMessageContent.innerHTML = htmlContent; // Chèn HTML đã chuyển đổi
                } catch (error) {
                    console.error("Error parsing Markdown:", error);
                    botMessageContent.textContent = "Error processing response.";
                }

                botMessage.appendChild(botMessageContent);
                chatMessages.appendChild(botMessage);

                // Tự động cuộn xuống cuối
                chatMessages.scrollTop = chatMessages.scrollHeight;
            })
            .catch(error => {
                console.error("Error:", error);
                chatMessages.removeChild(loadingMessage); // Xóa trạng thái loading
                const errorMessage = document.createElement('div');
                errorMessage.className = 'chat-message bot error';
                errorMessage.textContent = "Error connecting to server.";
                chatMessages.appendChild(errorMessage);
            });

        // Tự động cuộn xuống cuối sau khi thêm tin nhắn người dùng
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}



// get the enter
document.getElementById('chat-input-box').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});