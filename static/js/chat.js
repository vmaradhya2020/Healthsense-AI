// Mobile Navigation Toggle
const navbarToggle = document.getElementById('navbarToggle');
const navbarLinks = document.getElementById('navbarLinks');

if (navbarToggle) {
    navbarToggle.addEventListener('click', () => {
        navbarLinks.classList.toggle('active');
    });
}

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const typingIndicator = document.getElementById('typingIndicator');
const welcomeMessage = document.getElementById('welcomeMessage');
const newChatBtn = document.getElementById('newChatBtn');
const chatSidebar = document.getElementById('chatSidebar');
const mobileSidebarBtn = document.getElementById('mobileSidebarBtn');
const sidebarOverlay = document.getElementById('sidebarOverlay');

// State
let conversationHistory = [];
let isWaitingForResponse = false;

// Initialize
function init() {
    setupEventListeners();
    setupMobileDetection();
    setupQuickActions();

    // Check for query parameter
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('q');
    if (query) {
        chatInput.value = query;
        sendMessage();
    }
}

// Setup Event Listeners
function setupEventListeners() {
    // Send button
    sendBtn.addEventListener('click', sendMessage);

    // Enter key to send (Shift+Enter for new line)
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Auto-resize textarea
    chatInput.addEventListener('input', () => {
        chatInput.style.height = 'auto';
        chatInput.style.height = Math.min(chatInput.scrollHeight, 150) + 'px';
    });

    // New chat button
    newChatBtn.addEventListener('click', startNewChat);

    // Mobile sidebar
    if (mobileSidebarBtn) {
        mobileSidebarBtn.addEventListener('click', toggleSidebar);
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', closeSidebar);
    }
}

// Setup Mobile Detection
function setupMobileDetection() {
    function checkMobile() {
        if (window.innerWidth <= 768) {
            if (mobileSidebarBtn) {
                mobileSidebarBtn.style.display = 'block';
            }
        } else {
            if (mobileSidebarBtn) {
                mobileSidebarBtn.style.display = 'none';
            }
            closeSidebar();
        }
    }

    checkMobile();
    window.addEventListener('resize', checkMobile);
}

// Setup Quick Actions
function setupQuickActions() {
    document.querySelectorAll('.quick-action-card').forEach(card => {
        card.addEventListener('click', () => {
            const action = card.dataset.action;
            switch (action) {
                case 'hospitals':
                    window.location.href = 'hospitals.html';
                    break;
                case 'doctors':
                    window.location.href = 'doctors.html';
                    break;
                case 'tests':
                    window.location.href = 'tests.html';
                    break;
                case 'emergency':
                    window.location.href = 'emergency.html';
                    break;
            }
        });
    });
}

// Toggle Mobile Sidebar
function toggleSidebar() {
    chatSidebar.classList.toggle('active');
    sidebarOverlay.classList.toggle('active');
}

function closeSidebar() {
    chatSidebar.classList.remove('active');
    sidebarOverlay.classList.remove('active');
}

// Send Message
async function sendMessage() {
    const message = chatInput.value.trim();

    if (!message || isWaitingForResponse) {
        return;
    }

    // Hide welcome message
    if (welcomeMessage) {
        welcomeMessage.style.display = 'none';
    }

    // Add user message
    addMessage(message, 'user');

    // Clear input
    chatInput.value = '';
    chatInput.style.height = 'auto';

    // Update state
    isWaitingForResponse = true;
    sendBtn.disabled = true;

    // Show typing indicator
    typingIndicator.classList.add('active');
    scrollToBottom();

    // Add to conversation history
    conversationHistory.push({
        role: 'user',
        content: message
    });

    try {
        // Call backend API
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                history: conversationHistory
            })
        });

        if (!response.ok) {
            throw new Error('Failed to get response from server');
        }

        const data = await response.json();

        // Hide typing indicator
        typingIndicator.classList.remove('active');

        // Add assistant response
        const assistantMessage = data.response || data.message || 'I apologize, but I encountered an error. Please try again.';
        addMessage(assistantMessage, 'assistant');

        // Update conversation history
        conversationHistory.push({
            role: 'assistant',
            content: assistantMessage
        });

    } catch (error) {
        console.error('Error:', error);

        // Hide typing indicator
        typingIndicator.classList.remove('active');

        // Show mock response for demo
        setTimeout(() => {
            const mockResponse = generateMockResponse(message);
            addMessage(mockResponse, 'assistant');

            conversationHistory.push({
                role: 'assistant',
                content: mockResponse
            });
        }, 500);
    } finally {
        isWaitingForResponse = false;
        sendBtn.disabled = false;
        chatInput.focus();
    }
}

// Add Message to Chat
function addMessage(content, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = type === 'user' ? '👤' : '🤖';

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';

    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = content;

    const time = document.createElement('div');
    time.className = 'message-time';
    time.textContent = formatTime(new Date());

    messageContent.appendChild(bubble);
    messageContent.appendChild(time);

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);

    chatMessages.appendChild(messageDiv);

    scrollToBottom();
}

// Format Time
function formatTime(date) {
    return date.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
}

// Scroll to Bottom
function scrollToBottom() {
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 100);
}

// Start New Chat
function startNewChat() {
    conversationHistory = [];
    chatMessages.innerHTML = '';

    // Re-add welcome message
    const welcomeDiv = document.createElement('div');
    welcomeDiv.className = 'welcome-message';
    welcomeDiv.id = 'welcomeMessage';
    welcomeDiv.innerHTML = `
        <div class="welcome-icon">🤖</div>
        <h2 class="welcome-title">Hello! I'm your AI Health Assistant</h2>
        <p class="welcome-text">
            I can help you find hospitals, book doctor appointments, search for lab tests,
            and answer general health questions. Try asking me something below!
        </p>

        <div class="sample-questions">
            <div class="sample-question" onclick="askSampleQuestion('What are the symptoms of diabetes?')">
                <div class="sample-question-icon">🍬</div>
                <div class="sample-question-text">What are the symptoms of diabetes?</div>
            </div>

            <div class="sample-question" onclick="askSampleQuestion('Find cardiologists near me')">
                <div class="sample-question-icon">💓</div>
                <div class="sample-question-text">Find cardiologists near me</div>
            </div>

            <div class="sample-question" onclick="askSampleQuestion('What lab tests do I need for a health checkup?')">
                <div class="sample-question-icon">🔬</div>
                <div class="sample-question-text">What lab tests do I need for a health checkup?</div>
            </div>

            <div class="sample-question" onclick="askSampleQuestion('Compare hospitals for heart surgery')">
                <div class="sample-question-icon">🏥</div>
                <div class="sample-question-text">Compare hospitals for heart surgery</div>
            </div>
        </div>
    `;

    chatMessages.appendChild(welcomeDiv);

    // Re-add typing indicator
    const typingDiv = document.createElement('div');
    typingDiv.className = 'typing-indicator';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="typing-bubble">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    `;
    chatMessages.appendChild(typingDiv);

    chatInput.focus();
    closeSidebar();
}

// Ask Sample Question
window.askSampleQuestion = function(question) {
    chatInput.value = question;
    sendMessage();
};

// Generate Mock Response (for demo when backend is unavailable)
function generateMockResponse(userMessage) {
    const message = userMessage.toLowerCase();

    // Hospital queries
    if (message.includes('hospital') || message.includes('compare')) {
        return "I can help you find and compare hospitals! I found several options:\n\n" +
               "🏥 NewYork-Presbyterian Hospital (4.8★)\n" +
               "🏥 Mount Sinai Hospital (4.7★)\n" +
               "🏥 NYU Langone Health (4.9★)\n\n" +
               "Would you like to see detailed comparisons? You can also visit our Hospital Comparison page for more filters and options.";
    }

    // Doctor queries
    if (message.includes('doctor') || message.includes('cardiologist') || message.includes('appointment')) {
        return "I can help you find doctors! Here are some available cardiologists:\n\n" +
               "👨‍⚕️ Dr. Sarah Johnson (Cardiology, 4.9★, $250)\n" +
               "👨‍⚕️ Dr. Michael Chen (Neurology, 4.8★, $275)\n\n" +
               "Would you like to book an appointment? Visit our Doctor Booking page to see availability and schedule online.";
    }

    // Lab test queries
    if (message.includes('test') || message.includes('lab') || message.includes('blood') || message.includes('checkup')) {
        return "For a comprehensive health checkup, I recommend:\n\n" +
               "🔬 Complete Blood Count (CBC) - $25\n" +
               "🔬 Lipid Profile - $35\n" +
               "🔬 Blood Sugar (Fasting) - $15\n" +
               "🔬 Thyroid Profile - $65\n\n" +
               "We also have health screening packages starting at $99! Visit our Lab Tests page to see all options and prices.";
    }

    // Diabetes queries
    if (message.includes('diabetes') || message.includes('sugar')) {
        return "Common symptoms of diabetes include:\n\n" +
               "• Increased thirst and frequent urination\n" +
               "• Extreme hunger\n" +
               "• Unexplained weight loss\n" +
               "• Fatigue\n" +
               "• Blurred vision\n" +
               "• Slow-healing sores\n\n" +
               "I recommend getting tested with:\n" +
               "🔬 Blood Sugar (Fasting) - $15\n" +
               "🔬 HbA1c Test - $45\n\n" +
               "Would you like to book these tests?";
    }

    // Emergency queries
    if (message.includes('emergency') || message.includes('urgent') || message.includes('911')) {
        return "⚠️ For life-threatening emergencies, please CALL 911 immediately!\n\n" +
               "For non-emergency urgent care, I can help you find:\n" +
               "🚨 Nearest emergency rooms\n" +
               "🚨 Ambulance services\n" +
               "🚨 24/7 urgent care centers\n\n" +
               "Visit our Emergency Services page for detailed information and locations.";
    }

    // Default response
    return "I'm your AI health assistant powered by HealthSense AI. I can help you:\n\n" +
           "🏥 Find and compare hospitals\n" +
           "👨‍⚕️ Search for doctors and book appointments\n" +
           "🔬 Browse lab tests and prices\n" +
           "🚨 Locate emergency services\n" +
           "💊 Answer general health questions\n\n" +
           "What would you like to know more about?";
}

// Initialize on page load
window.addEventListener('load', init);
