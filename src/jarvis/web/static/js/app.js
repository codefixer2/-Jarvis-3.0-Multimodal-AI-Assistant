// App State
const state = {
    messages: [],
    isTyping: false,
    theme: localStorage.getItem('theme') || 'dark',
    apiKey: localStorage.getItem('apiKey') || ''
};

// DOM Elements
const elements = {
    sidebar: document.getElementById('sidebar'),
    menuBtn: document.getElementById('menuBtn'),
    sidebarToggle: document.getElementById('sidebarToggle'),
    messagesContainer: document.getElementById('messagesContainer'),
    messageInput: document.getElementById('messageInput'),
    sendBtn: document.getElementById('sendBtn'),
    welcomeScreen: document.getElementById('welcomeScreen'),
    clearChatBtn: document.getElementById('clearChatBtn'),
    exportBtn: document.getElementById('exportBtn'),
    settingsBtn: document.getElementById('settingsBtn'),
    settingsModal: document.getElementById('settingsModal'),
    closeSettings: document.getElementById('closeSettings'),
    cancelSettings: document.getElementById('cancelSettings'),
    saveSettings: document.getElementById('saveSettings'),
    themeToggle: document.getElementById('themeToggle'),
    themeIcon: document.getElementById('themeIcon'),
    themeText: document.getElementById('themeText'),
    newChatBtn: document.getElementById('newChatBtn'),
    typingIndicator: document.getElementById('typingIndicator'),
    statusText: document.getElementById('statusText'),
    suggestionChips: document.querySelectorAll('.suggestion-chip'),
    voiceBtn: document.getElementById('voiceBtn'),
    attachBtn: document.getElementById('attachBtn')
};

// Initialize App
function init() {
    applyTheme(state.theme);
    setupEventListeners();
    checkAPIHealth();
    loadChatHistory();
}

// Event Listeners
function setupEventListeners() {
    // Send message
    elements.sendBtn.addEventListener('click', sendMessage);
    elements.messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Auto-resize textarea
    elements.messageInput.addEventListener('input', () => {
        elements.messageInput.style.height = 'auto';
        elements.messageInput.style.height = elements.messageInput.scrollHeight + 'px';
    });

    // Sidebar toggle
    elements.menuBtn.addEventListener('click', () => {
        elements.sidebar.classList.toggle('active');
    });
    elements.sidebarToggle.addEventListener('click', () => {
        elements.sidebar.classList.toggle('active');
    });

    // Clear chat
    elements.clearChatBtn.addEventListener('click', clearChat);

    // Export chat
    elements.exportBtn.addEventListener('click', exportChat);

    // Settings
    elements.settingsBtn.addEventListener('click', () => {
        elements.settingsModal.classList.add('active');
        document.getElementById('apiKeyInput').value = state.apiKey;
    });
    elements.closeSettings.addEventListener('click', closeSettings);
    elements.cancelSettings.addEventListener('click', closeSettings);
    elements.saveSettings.addEventListener('click', saveSettings);

    // Theme toggle
    elements.themeToggle.addEventListener('click', toggleTheme);

    // New chat
    elements.newChatBtn.addEventListener('click', clearChat);

    // Suggestion chips
    elements.suggestionChips.forEach(chip => {
        chip.addEventListener('click', () => {
            const prompt = chip.getAttribute('data-prompt');
            elements.messageInput.value = prompt;
            sendMessage();
        });
    });

    // Voice input (placeholder)
    elements.voiceBtn.addEventListener('click', () => {
        alert('Voice input feature coming soon!');
    });

    // Attach file (placeholder)
    elements.attachBtn.addEventListener('click', () => {
        alert('File attachment feature coming soon!');
    });

    // Close modal on outside click
    elements.settingsModal.addEventListener('click', (e) => {
        if (e.target === elements.settingsModal) {
            closeSettings();
        }
    });
}

// Send Message
async function sendMessage() {
    const message = elements.messageInput.value.trim();
    if (!message || state.isTyping) return;

    // Hide welcome screen
    elements.welcomeScreen.style.display = 'none';

    // Add user message
    addMessage('user', message);
    elements.messageInput.value = '';
    elements.messageInput.style.height = 'auto';

    // Show typing indicator
    setTyping(true);

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        if (data.success) {
            addMessage('assistant', data.response, data.timestamp);
        } else {
            addMessage('assistant', `Error: ${data.error}`, new Date().toISOString());
        }
    } catch (error) {
        addMessage('assistant', `Error: ${error.message}`, new Date().toISOString());
    } finally {
        setTyping(false);
    }
}

// Add Message to UI
function addMessage(role, content, timestamp = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = role === 'user' 
        ? '<i class="fas fa-user"></i>' 
        : '<i class="fas fa-robot"></i>';

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = content;

    const messageTime = document.createElement('div');
    messageTime.className = 'message-time';
    messageTime.textContent = timestamp 
        ? formatTime(timestamp) 
        : formatTime(new Date().toISOString());

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);
    messageDiv.appendChild(messageTime);

    elements.messagesContainer.appendChild(messageDiv);
    scrollToBottom();

    // Save to state
    state.messages.push({ role, content, timestamp: timestamp || new Date().toISOString() });
    saveChatHistory();
}

// Format Time
function formatTime(isoString) {
    const date = new Date(isoString);
    return date.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

// Set Typing Indicator
function setTyping(isTyping) {
    state.isTyping = isTyping;
    elements.typingIndicator.style.display = isTyping ? 'flex' : 'none';
    elements.statusText.textContent = isTyping ? 'JARVIS is typing...' : 'JARVIS is ready';
    elements.sendBtn.disabled = isTyping;
}

// Scroll to Bottom
function scrollToBottom() {
    elements.messagesContainer.scrollTop = elements.messagesContainer.scrollHeight;
}

// Clear Chat
function clearChat() {
    if (confirm('Are you sure you want to clear the chat?')) {
        state.messages = [];
        elements.messagesContainer.innerHTML = '';
        elements.welcomeScreen.style.display = 'flex';
        localStorage.removeItem('chatHistory');
    }
}

// Export Chat
function exportChat() {
    if (state.messages.length === 0) {
        alert('No messages to export');
        return;
    }

    const chatText = state.messages.map(msg => {
        const role = msg.role === 'user' ? 'You' : 'JARVIS';
        const time = formatTime(msg.timestamp);
        return `[${time}] ${role}: ${msg.content}`;
    }).join('\n\n');

    const blob = new Blob([chatText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `jarvis-chat-${new Date().toISOString().split('T')[0]}.txt`;
    a.click();
    URL.revokeObjectURL(url);
}

// Settings
function closeSettings() {
    elements.settingsModal.classList.remove('active');
}

function saveSettings() {
    const apiKey = document.getElementById('apiKeyInput').value.trim();
    if (apiKey) {
        state.apiKey = apiKey;
        localStorage.setItem('apiKey', apiKey);
    }
    closeSettings();
    alert('Settings saved! Note: API key should be set via environment variable for production.');
}

// Theme Toggle
function toggleTheme() {
    const newTheme = state.theme === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);
    state.theme = newTheme;
    localStorage.setItem('theme', newTheme);
}

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    elements.themeIcon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    elements.themeText.textContent = theme === 'dark' ? 'Light Mode' : 'Dark Mode';
}

// Check API Health
async function checkAPIHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        if (!data.api_configured) {
            elements.statusText.textContent = 'Warning: API key not configured';
            elements.statusText.style.color = 'var(--warning-color)';
        }
    } catch (error) {
        console.error('Health check failed:', error);
    }
}

// Chat History
function saveChatHistory() {
    localStorage.setItem('chatHistory', JSON.stringify(state.messages));
}

function loadChatHistory() {
    const saved = localStorage.getItem('chatHistory');
    if (saved) {
        try {
            state.messages = JSON.parse(saved);
            if (state.messages.length > 0) {
                elements.welcomeScreen.style.display = 'none';
                state.messages.forEach(msg => {
                    addMessage(msg.role, msg.content, msg.timestamp);
                });
            }
        } catch (error) {
            console.error('Failed to load chat history:', error);
        }
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', init);



