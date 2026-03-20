const chatHistory = document.getElementById('chatHistory');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');

function addMessage(content, type, context = null) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', type);
    
    let innerHTML = '';
    
    if (type === 'ai-message' && content !== '...') {
        // Just text content
        innerHTML += `<div class="answer-text">${content.replace(/\n/g, '<br>')}</div>`;
        
        // Add context for transparency
        if (context && context.length > 0) {
            let contextHTML = `<div class="context-box"><strong>Transparency Context (Found ${context.length} Source Chunks)</strong><br>`;
            context.forEach((chunk, i) => {
                contextHTML += `<div class="context-chunk">
                    <strong>Source: ${chunk.source}</strong><br>
                    ${chunk.content}
                </div>`;
            });
            contextHTML += `</div>`;
            innerHTML += contextHTML;
        }
    } else if (content === '...') {
        // Loading animation
        innerHTML = `<div class="loading-message">
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
        </div>`;
        msgDiv.id = 'loadingMsg';
    } else {
        innerHTML = content;
    }

    msgDiv.innerHTML = innerHTML;
    chatHistory.appendChild(msgDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function removeLoading() {
    const loading = document.getElementById('loadingMsg');
    if (loading) {
        loading.remove();
    }
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    userInput.value = '';
    userInput.disabled = true;
    sendBtn.disabled = true;

    addMessage(text, 'user-message');
    addMessage('...', 'ai-message');

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: text })
        });

        const data = await response.json();
        removeLoading();
        
        if (response.ok) {
            addMessage(data.answer, 'ai-message', data.context);
        } else {
            addMessage('An error occurred on the server.', 'ai-message');
        }
    } catch (error) {
        removeLoading();
        addMessage(`Connection error: ${error.message}`, 'ai-message');
    }

    userInput.disabled = false;
    sendBtn.disabled = false;
    userInput.focus();
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
