function sendMessage() {
    const inputBox = document.getElementById('chat-input-box');
    const chatMessages = document.getElementById('chat-messages');
    const fileInput = document.getElementById('image-upload');
    const clipboardDiv = document.getElementById('clipboard-upload');
    const message = inputBox.value.trim();
    const file = fileInput.files[0];
    const clipboardBlob = clipboardDiv.blob; // Get the data from Bob

    const formData = new FormData();
    let hasDataToSend = false;

    // Append Message
    if (message) {
        formData.append('message', message);
        displayUserMessage(message, chatMessages);
        hasDataToSend = true;
    }

    // Append files
    if (file) {
        formData.append('file', file);
        hasDataToSend = true;
    }

    // Append image from clipboard
    if (clipboardBlob) {
        formData.append('file', clipboardBlob, 'clipboard_image.png');
        hasDataToSend = true;
    }

    // Dont have any data
    if (!hasDataToSend) {
        console.log('No data to send');
        return;
    }

    // Sent data to backend
    sendToBackend(formData, chatMessages);

    // Reset the GUI after sent
    resetUI(inputBox, fileInput, clipboardDiv);
}

// Reset GUI
function resetUI(inputBox, fileInput, clipboardDiv) {
    inputBox.value = ''; // Reset message
    fileInput.value = ''; // Reset file

    // reset clipboard
    clipboardDiv.innerHTML = '<p>Paste an image from clipboard:</p>';
    clipboardDiv.blob = null; // Remove bob objects
    console.log('UI has been reset to the default state.');
}

document.getElementById('clipboard-upload').addEventListener('paste', function (event) {
    const clipboardItems = event.clipboardData.items;

    for (let item of clipboardItems) {
        if (item.type.startsWith('image/')) {
            const blob = item.getAsFile();
            const blobUrl = URL.createObjectURL(blob);

            // Show the image 
            displayClipboardImage(blobUrl);

            // Save bob to dataset
            document.getElementById('clipboard-upload').blob = blob; // save bob to bob attributes
            return; // Got images
        }
    }

    alert('No image found in clipboard!');
});

document.getElementById('send-button').addEventListener('click', function () {
    sendMessage();
});

// Show the image small icon
function displayClipboardImage(blobUrl) {
    const clipboardDiv = document.getElementById('clipboard-upload');
    clipboardDiv.innerHTML = ''; // Remove out dated data

    const img = document.createElement('img');
    img.src = blobUrl;
    img.style.maxWidth = '200px';
    img.style.maxHeight = '200px';
    img.style.marginTop = '10px';
    img.style.borderRadius = '8px';
    img.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.1)';
    clipboardDiv.appendChild(img);
}


// Show user message
function displayUserMessage(message, chatMessages) {
    const userMessage = document.createElement('div');
    userMessage.className = 'chat-message user';
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = message;
    userMessage.appendChild(messageContent);
    chatMessages.appendChild(userMessage);
}

function sendToBackend(formData, chatMessages) {
    console.log('Sending to backend:', Array.from(formData.entries())); // Log dữ liệu gửi

    // Loading status
    const loadingMessage = document.createElement('div');
    loadingMessage.className = 'chat-message bot loading';
    loadingMessage.textContent = 'Bot is typing...';
    chatMessages.appendChild(loadingMessage);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    fetch('/upload-image', {
            method: 'POST',
            body: formData,
        })
            .then(response => response.json())
            .then(data => {
                chatMessages.removeChild(loadingMessage);

                if (data.error) {
                    addBotMessage(`Error: ${data.error}`);
                } else {
                    if (data.response) {
                        addBotMessage(data.response); // Show the response
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                chatMessages.removeChild(loadingMessage);
                addBotMessage('Error sending message or uploading file.');
            });
}

// Markdown rendered
function displayMarkdownResponse(content, chatMessages) {
    const botMessage = document.createElement('div');
    botMessage.className = 'chat-message bot';
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    try {
        messageContent.innerHTML = marked.parse(content);
    } catch (e) {
        console.error('Error rendering Markdown:', e);
        messageContent.textContent = content; // Fallback if errors
    }
    botMessage.appendChild(messageContent);
    chatMessages.appendChild(botMessage);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Show the image ( chart )
function displayImageResponse(imageUrl, chatMessages) {
    const botMessage = document.createElement('div');
    botMessage.className = 'chat-message bot';
    const img = document.createElement('img');
    img.src = imageUrl;
    img.style.maxWidth = '100%';
    botMessage.appendChild(img);
    chatMessages.appendChild(botMessage);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

const chatInputBox = document.getElementById('chat-input-box');
chatInputBox.replaceWith(chatInputBox.cloneNode(true));

document.getElementById('chat-input-box').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        e.preventDefault(); // Enter -> Done
        sendMessage(); // Send the message
    }
});

function addBotMessage(content) {
    const chatMessages = document.getElementById('chat-messages');
    const botMessage = document.createElement('div');
    botMessage.className = 'chat-message bot';

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    try {
        messageContent.innerHTML = marked.parse(content); // Render Markdown
    } catch (e) {
        console.error('Error rendering Markdown:', e);
        messageContent.textContent = content; // Fallback
    }

    botMessage.appendChild(messageContent);
    chatMessages.appendChild(botMessage);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
