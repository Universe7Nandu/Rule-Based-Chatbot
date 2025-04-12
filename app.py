# app.py
import streamlit as st
import re
import os
import time
import random
import json
from dotenv import load_dotenv
from groq import Groq
from datetime import datetime

# Set page config (must be first Streamlit command)
st.set_page_config(
    page_title="Rule-Based AI Assistant | Nandesh Kalashetti",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Configure Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Define CSS styles for modern UI
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Base styling */
    body {
        background-color: #0e1525;
        color: #f8fafc;
        background-image: radial-gradient(circle at 50% 50%, #131c31 0%, #0e1525 100%);
    }
    
    /* Chat interface */
    .chat-interface {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        display: flex;
        flex-direction: column;
        padding: 0;
        background-color: transparent;
        overflow: hidden;
        max-width: 100%;
    }
    
    /* Messages container with proper scroll area */
    .messages-container {
        flex: 1;
        overflow-y: auto;
        padding: 0px 20px 80px 20px;
        display: flex;
        flex-direction: column;
        gap: 12px;
        max-width: 850px;
        margin: 0 auto;
        width: 100%;
        scroll-behavior: smooth;
        height: calc(100vh - 160px);
        margin-bottom: 70px;
    }
    
    /* Message styles */
    .message {
        padding: 14px 18px;
        margin-bottom: 12px;
        border-radius: 14px;
        max-width: 80%;
        animation: fadeIn 0.3s ease-out;
        word-wrap: break-word;
        line-height: 1.5;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.12);
        position: relative;
    }
    
    .user-message {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        align-self: flex-end;
        border-radius: 18px 18px 0 18px;
        margin-right: 15px;
    }
    
    .bot-message {
        background-color: #1e293b;
        color: #f1f5f9;
        align-self: flex-start;
        border-radius: 18px 18px 18px 0;
        border-left: 3px solid #3b82f6;
        margin-left: 15px;
    }
    
    /* Message avatars */
    .user-message::before {
        content: "";
        position: absolute;
        bottom: -10px;
        right: -15px;
        width: 35px;
        height: 35px;
        background-image: url('https://img.icons8.com/color/96/000000/user-male-circle--v1.png');
        background-size: cover;
        border-radius: 50%;
        border: 2px solid #1d4ed8;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }
    
    .bot-message::before {
        content: "";
        position: absolute;
        bottom: -10px;
        left: -15px;
        width: 35px;
        height: 35px;
        background-image: url('https://img.icons8.com/fluency/96/000000/chatbot.png');
        background-size: cover;
        border-radius: 50%;
        border: 2px solid #3b82f6;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }
    
    /* Input area - professional design */
    .input-area {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 12px 15px;
        background: #0e1525;
        z-index: 100;
        border-top: 1px solid rgba(59, 130, 246, 0.15);
        box-shadow: 0 -4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Form styling improvements */
    form[data-testid="stForm"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Input container improved */
    .input-container {
        display: flex;
        align-items: center;
        background-color: #1e293b;
        border-radius: 10px;
        padding: 8px 8px 8px 15px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        margin: 0 auto;
        width: 100%;
        max-width: 850px;
        height: 45px;
        transition: all 0.2s ease;
        border: 1px solid rgba(59, 130, 246, 0.15);
    }
    
    .input-container:focus-within {
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
        border: 1px solid rgba(59, 130, 246, 0.6);
        transform: translateY(-3px);
    }
    
    /* Fix for Streamlit inputs */
    .input-container .stTextInput {
        flex-grow: 1;
    }
    
    .input-container .stTextInput > div {
        background-color: transparent !important;
    }
    
    .input-container .stTextInput > div > div > input {
        background-color: transparent !important;
        color: #f8fafc !important;
        border: none !important;
        padding: 12px 0 !important;
        font-size: 16px !important;
        width: 100% !important;
        margin: 0 !important;
        height: 40px !important;
    }
    
    /* Hide form label */
    label[data-testid="stText"] {
        display: none;
    }
    
    /* Column spacing fixes */
    div[data-testid="column"] {
        padding: 0 !important;
    }
    
    /* Reset stForm padding */
    div[data-testid="stForm"] > div:first-child {
        padding-bottom: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Fix form button spacing */
    div[data-testid="stForm"] button {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }
    
    /* Send button improvements for perfect positioning */
    button[kind="primary"] {
        background: #ef4444 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        width: 38px !important;
        height: 38px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15) !important;
        min-width: unset !important;
        margin-top: 5px !important;
    }
    
    button[kind="primary"]:hover {
        background: #dc2626 !important;
        transform: translateY(-1px) !important;
    }
    
    .stButton button::before {
        content: "↑";
        font-size: 20px;
        font-weight: bold;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Welcome container */
    .welcome-container {
        text-align: center;
        padding: 30px 20px;
        color: #94a3b8;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 250px;
        margin-top: 20px;
    }
    
    .welcome-container img {
        width: 70px;
        height: 70px;
        margin-bottom: 20px;
        filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
    }
    
    /* Sidebar styling */
    .sidebar .stMarkdown {
        color: #f8fafc !important;
    }
    
    .sidebar-content {
        background-color: #1e293b;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    /* Chat history in sidebar */
    .history-item {
        background-color: #334155;
        border-radius: 8px;
        padding: 10px 15px;
        margin: 8px 0;
        font-size: 13px;
        color: #e2e8f0;
        cursor: pointer;
        transition: all 0.2s;
        border-left: 3px solid transparent;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    
    .history-item:hover {
        background-color: #3b4a63;
        border-left-color: #3b82f6;
    }
    
    .history-container {
        max-height: 300px;
        overflow-y: auto;
        padding-right: 5px;
        margin-top: 10px;
    }
    
    /* Feature cards */
    .feature-card {
        background-color: #334155;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 12px;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    header {display:none;}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #64748b;
    }
    
    /* Logo styling */
    .logo-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .logo-container img {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #3b82f6;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    
    /* Tech badges */
    .tech-badge {
        display: inline-block;
        background-color: #334155;
        color: #94a3b8;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        margin: 0 5px 5px 0;
    }
    
    /* Connect links */
    .connect-links {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin: 15px 0;
    }
    
    .connect-link {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 36px;
        background-color: #334155;
        border-radius: 50%;
        transition: all 0.3s ease;
    }
    
    .connect-link:hover {
        transform: translateY(-3px);
        background-color: #3b82f6;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .message {
            max-width: 90%;
            font-size: 14px;
            padding: 12px 15px;
        }
        
        .user-message::before,
        .bot-message::before {
            width: 30px;
            height: 30px;
        }
        
        .user-message {
            margin-right: 10px;
        }
        
        .bot-message {
            margin-left: 10px;
        }
        
        .input-container {
            padding: 5px 5px 5px 15px;
            height: 50px;
        }
        
        .input-container .stTextInput > div > div > input {
            font-size: 14px !important;
        }
        
        .stButton button {
            width: 36px;
            height: 36px;
        }
        
        .welcome-container {
            padding: 20px 10px;
            height: calc(100vh - 150px);
        }
        
        .welcome-container img {
            width: 60px;
        }
        
        .sidebar-content {
            padding: 15px;
        }
        
        .logo-container img {
            width: 60px;
            height: 60px;
        }
        
        .history-container {
            max-height: 200px;
        }
        
        .messages-container {
            padding: 0px 10px 100px 10px;
        }
    }

    /* Welcome banner styling */
    .welcome-banner {
        background: linear-gradient(135deg, #1e293b, #111827);
        color: white;
        border-radius: 8px;
        padding: 15px 18px;
        margin: 10px auto 12px auto;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.12);
        animation: fadeIn 0.5s ease-out;
        text-align: left;
        border-left: 3px solid #3b82f6;
        max-width: 850px;
        width: 100%;
    }

    .welcome-banner h1 {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 5px;
    }

    .welcome-banner p {
        font-size: 13px;
        opacity: 0.9;
        line-height: 1.4;
    }

    /* Pattern examples section */
    .patterns-section {
        background-color: #1e293b;
        border-radius: 8px;
        padding: 12px 15px;
        margin: 0 auto 12px auto;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        border-left: 2px solid #3b82f6;
        max-width: 850px;
        width: 100%;
    }

    /* Responsive fixes */
    @media (min-width: 992px) {
        .welcome-banner, .patterns-section, .messages-container, .input-container {
            max-width: 850px;
        }
    }

    @media (min-width: 1200px) {
        .welcome-banner, .patterns-section, .messages-container, .input-container {
            max-width: 900px;
        }
    }

    /* Rule pattern indicators */
    .pattern-indicator {
        display: inline-block;
        background-color: rgba(59, 130, 246, 0.15);
        border: 1px solid rgba(59, 130, 246, 0.3);
        color: #93c5fd;
        border-radius: 4px;
        padding: 1px 5px;
        font-size: 11px;
        margin-right: 5px;
        font-family: monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state variables
def init_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'first_prompt' not in st.session_state:
        st.session_state.first_prompt = True
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []  # For keeping track of recent conversations
    if 'rules' not in st.session_state:
        # Define rule patterns with improved responses and emojis
        st.session_state.rules = [
            {
                'patterns': [r'hello|hi|hey|greetings', r'^hi$'],
                'responses': ["👋 Hello! How can I help you today?", "👋 Hi there! What can I assist you with?", "👋 Hey! I'm here to help. What's on your mind?"]
            },
            {
                'patterns': [r'who are you|what are you|tell me about yourself'],
                'responses': ["🤖 I'm an advanced AI assistant created by Nandesh Kalashetti. I combine rule-based capabilities with AI to provide helpful responses to your questions!"]
            },
            {
                'patterns': [r'bye|goodbye|see you|farewell'],
                'responses': ["👋 Goodbye! Have a great day!", "✨ See you later! Take care!", "👋 Farewell! Come back soon!"]
            },
            {
                'patterns': [r'thank you|thanks'],
                'responses': ["😊 You're welcome! Anything else you need help with?", "🙏 Happy to help! Let me know if you need anything else."]
            },
            {
                'patterns': [r'what can you do|help|capabilities'],
                'responses': ["🚀 I can answer questions, provide information, assist with various tasks, and engage in natural conversations. Just ask me anything!"]
            },
            {
                'patterns': [r'weather|temperature'],
                'responses': ["🌦️ I'm sorry, I don't have access to real-time weather data, but I'd be happy to help with other questions!"]
            },
            {
                'patterns': [r'your name'],
                'responses': ["🤖 I'm your AI assistant, created by Nandesh Kalashetti. You can call me Assistant!"]
            },
            {
                'patterns': [r'how are you'],
                'responses': ["😊 I'm doing well, thank you! How about you?", "🌟 I'm functioning perfectly! How can I brighten your day?"]
            },
            {
                'patterns': [r'who (is|made) (you|this)|creator|developer'],
                'responses': ["👨‍💻 I was created by Nandesh Kalashetti, a talented full-stack developer specializing in MERN stack, React.js, TypeScript, PHP, and MySQL."]
            },
            {
                'patterns': [r'project|about this chatbot'],
                'responses': ["🚀 This is an advanced AI chatbot with rule-based intelligence. I use pattern matching for quick responses and AI capabilities for complex questions!"]
            },
            {
                'patterns': [r'joke|tell me a joke|make me laugh'],
                'responses': ["😄 Why don't scientists trust atoms? Because they make up everything!", 
                             "😂 Why did the JavaScript developer wear glasses? Because he couldn't C#!",
                             "🤣 Why do programmers prefer dark mode? Because light attracts bugs!"]
            },
            {
                'patterns': [r'time|what time|date|what date'],
                'responses': ["⏰ I don't have access to the current time or date, but your device should show that information!"]
            }
        ]

# Function to get response based on pattern matching rules
def get_response(user_input):
    user_input = user_input.lower().strip()
    
    # More sophisticated patterns with variations
    patterns = {
        r"\b(hi|hello|hey|hola|namaste|greetings)\b": {
            "responses": [
                "Hello! How can I assist you today?",
                "Hi there! What can I help you with?",
                "Greetings! How may I be of service?",
                "Hello! It's nice to meet you. What brings you here today?"
            ],
            "pattern_display": "hello"
        },
        r"\b(who are you|tell me about yourself|what are you|your identity)\b": {
            "responses": [
                "I'm an AI assistant designed to provide helpful responses based on rule patterns. I can answer questions, have conversations, and assist with various tasks.",
                "I'm your digital assistant, built to help answer questions and provide information through pattern-based responses.",
                "I'm an AI chatbot created to assist users through natural language interactions. My responses are based on predefined patterns that I match with your questions."
            ],
            "pattern_display": "who are you"
        },
        r"\b(how are you|how do you feel|how are you doing|how are you feeling)\b": {
            "responses": [
                "I'm functioning well, thank you for asking! How about you?",
                "I'm doing great! Always ready to help. How can I assist you today?",
                "I'm operating at optimal levels! Thanks for checking. What can I help you with?"
            ],
            "pattern_display": "how are you"
        },
        r"\b(joke|tell me a joke|make me laugh|something funny)\b": {
            "responses": [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the scarecrow win an award? Because he was outstanding in his field!",
                "I told my wife she was drawing her eyebrows too high. She looked surprised!",
                "What do you call a fake noodle? An impasta!"
            ],
            "pattern_display": "tell me a joke"
        },
        r"\b(thank you|thanks|thx|ty)\b": {
            "responses": [
                "You're welcome! Is there anything else I can help with?",
                "Happy to help! Let me know if you need anything else.",
                "Anytime! Feel free to ask if you have more questions."
            ],
            "pattern_display": "thank you"
        },
        r"\b(bye|goodbye|see you|farewell)\b": {
            "responses": [
                "Goodbye! Feel free to return whenever you need assistance.",
                "Farewell! Have a great day!",
                "Until next time! Take care!"
            ],
            "pattern_display": "goodbye"
        },
        r"\b(help|assistance|guide me|i need help)\b": {
            "responses": [
                "I'm here to help! You can ask me questions, request information, or just chat. Try asking about myself, a joke, or any general questions you might have.",
                "I'd be happy to assist you. You can try phrases like 'hello', 'who are you', 'tell me a joke', or ask questions about various topics.",
                "How can I assist you today? Feel free to ask questions or just chat with me."
            ],
            "pattern_display": "help"
        },
        r"\b(time|what time|current time|now)\b": {
            "responses": [
                f"The current time is {datetime.now().strftime('%H:%M:%S')}.",
                f"Right now, it's {datetime.now().strftime('%I:%M %p')}.",
                f"It's currently {datetime.now().strftime('%H:%M')} hours."
            ],
            "pattern_display": "what time is it"
        },
        r"\b(weather|temperature|forecast)\b": {
            "responses": [
                "I'm sorry, I don't have real-time weather data. You would need to integrate a weather API for that functionality.",
                "I don't have access to current weather information. You could check a weather service for accurate forecasts.",
                "I don't have the capability to check weather conditions yet. That would require integration with a weather service API."
            ],
            "pattern_display": "weather"
        }
    }
    
    # Look for matching patterns
    for pattern, data in patterns.items():
        if re.search(pattern, user_input):
            return {
                "response": random.choice(data["responses"]),
                "matched_pattern": data["pattern_display"],
                "is_pattern_match": True
            }
    
    # Handle unknown inputs more intelligently
    if len(user_input) < 5:
        return {
            "response": "I need a bit more information. Could you please elaborate on your question?",
            "matched_pattern": None,
            "is_pattern_match": False
        }
    elif "?" in user_input:
        return {
            "response": "That's an interesting question. I'm constantly learning, but I don't have a specific rule to answer that yet. Could you try asking something else?",
            "matched_pattern": None,
            "is_pattern_match": False
        }
    else:
        responses = [
            "I don't have a specific answer for that query. Could you try rephrasing or asking something else?",
            "I'm not sure I understand what you're asking. Could you provide more details or try a different question?",
            "I don't have that information in my knowledge base yet. Is there something else I can help with?",
            "I'm still learning, and I don't have a pattern that matches your question. Could you try asking differently?"
        ]
        return {
            "response": random.choice(responses),
            "matched_pattern": None,
            "is_pattern_match": False
        }

# Add message to chat history
def add_message(role, content, matched_pattern=None):
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "matched_pattern": matched_pattern,
        "timestamp": datetime.now().strftime("%H:%M")
    })

# Add function to update chat history in sidebar
def add_to_chat_history(query):
    # Get current timestamp for the chat history entry
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # Add to the beginning of the list (most recent first)
    st.session_state.chat_history.insert(0, (query, timestamp))
    
    # Limit history to last 10 conversations
    if len(st.session_state.chat_history) > 10:
        st.session_state.chat_history = st.session_state.chat_history[:10]

# Main app function
def main():
    load_css()
    init_session_state()
    
    # Sidebar
    with st.sidebar:
        # Developer info with profile picture
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown("""
        <div class="logo-container">
            <img src="https://nandeshkalashetti.netlify.app/img/person.jpg" alt="Nandesh Kalashetti">
            <h2 style="margin-top: 10px; color: #f8fafc; font-size: 18px;">Nandesh Kalashetti</h2>
            <p style="color: #94a3b8; font-size: 13px;">Full-Stack Developer</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Connect links
        st.markdown("<h3 style='color: #f8fafc; font-size: 15px; margin: 15px 0 10px;'>Connect With Me</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div class="connect-links">
            <a href="https://github.com/Universe7Nandu" target="_blank" class="connect-link">
                <img src="https://img.icons8.com/fluent/24/000000/github.png" width="18" />
            </a>
            <a href="https://www.linkedin.com/in/nandesh-kalashetti-333a78250/" target="_blank" class="connect-link">
                <img src="https://img.icons8.com/color/24/000000/linkedin.png" width="18" />
            </a>
            <a href="https://twitter.com/UniverseMath25" target="_blank" class="connect-link">
                <img src="https://img.icons8.com/color/24/000000/twitter--v1.png" width="18" />
            </a>
            <a href="https://www.instagram.com/nandesh_kalshetti/" target="_blank" class="connect-link">
                <img src="https://img.icons8.com/fluency/24/000000/instagram-new.png" width="18" />
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # Chat history in sidebar
        if st.session_state.chat_history:
            st.markdown("<h3 style='color: #f8fafc; font-size: 15px; margin: 20px 0 5px;'>Recent Chats</h3>", unsafe_allow_html=True)
            st.markdown('<div class="history-container">', unsafe_allow_html=True)
            
            for i, (query, timestamp) in enumerate(st.session_state.chat_history):
                # Fix the SyntaxError by using double quotes and escaping properly
                safe_query = query.replace('"', '&quot;')
                st.markdown(f"""
                <div class="history-item" onclick="document.getElementById('user-input').value='{safe_query}'; document.getElementById('user-input').focus();">
                    {query[:40] + '...' if len(query) > 40 else query}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Feature cards
        st.markdown("<h3 style='color: #f8fafc; font-size: 15px; margin: 20px 0 5px;'>Features</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-card">
            <h4 style="color: #f8fafc; font-size: 14px; margin-bottom: 5px;">🧠 Pattern Matching</h4>
            <p style="color: #94a3b8; font-size: 12px;">Rule-based responses to predefined questions</p>
        </div>
        
        <div class="feature-card">
            <h4 style="color: #f8fafc; font-size: 14px; margin-bottom: 5px;">⚙️ Regular Expressions</h4>
            <p style="color: #94a3b8; font-size: 12px;">Advanced pattern recognition</p>
        </div>
        
        <div class="feature-card">
            <h4 style="color: #f8fafc; font-size: 14px; margin-bottom: 5px;">🤖 AI Fallback</h4>
            <p style="color: #94a3b8; font-size: 12px;">For complex questions outside patterns</p>
        </div>
        
        <div class="feature-card">
            <h4 style="color: #f8fafc; font-size: 14px; margin-bottom: 5px;">📊 Unit Testing</h4>
            <p style="color: #94a3b8; font-size: 12px;">Ensuring response reliability</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tech stack
        st.markdown("<h3 style='color: #f8fafc; font-size: 15px; margin: 20px 0 5px;'>Tech Stack</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div style="display: flex; flex-wrap: wrap; gap: 5px;">
            <span class="tech-badge">Python</span>
            <span class="tech-badge">Streamlit</span>
            <span class="tech-badge">Groq API</span>
            <span class="tech-badge">PyTest</span>
            <span class="tech-badge">Git</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content - rule-based AI assistant
    st.markdown('<div class="chat-interface">', unsafe_allow_html=True)

    # Simple welcome banner highlighting rule-based functionality
    st.markdown("""
    <div class="welcome-banner">
        <h1>Rule-Based AI Assistant</h1>
        <p>Pattern matching chatbot with predefined responses and AI capabilities for complex queries</p>
    </div>
    """, unsafe_allow_html=True)

    # Add pattern examples section
    st.markdown("""
    <div class="patterns-section">
        <div style="color: #e2e8f0; font-size: 13px; margin-bottom: 8px;">Try these pattern examples:</div>
        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
            <span class="pattern-indicator">hello</span>
            <span class="pattern-indicator">who are you</span>
            <span class="pattern-indicator">tell me a joke</span>
            <span class="pattern-indicator">thank you</span>
            <span class="pattern-indicator">capabilities</span>
            <span class="pattern-indicator">bye</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Messages container
    st.markdown('<div class="messages-container">', unsafe_allow_html=True)

    # Display welcome message if no messages yet - focused on rule-based functionality
    if not st.session_state.messages:
        st.markdown("""
        <div class="welcome-container">
            <img src="https://img.icons8.com/fluency/96/000000/chatbot.png" style="width: 80px; margin-bottom: 15px;" alt="Chatbot Icon">
            <p style="color: #f8fafc; font-size: 16px; margin-bottom: 8px;">Rule-Based AI Assistant Ready!</p>
            <p style="color: #94a3b8; font-size: 14px;">Ask me predefined questions or try more complex queries</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display chat messages with pattern indicators for rule-based responses
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="message user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            # Get content
            content = message.get("content", "")
            
            # Only add emoji if content exists and doesn't already have an emoji
            emoji_list = ['😊', '👋', '🤖', '💡', '🚀', '📊', '⚠️', '🤔', '👍', '✨', '🙏', '😄']
            if content and not any(emoji in content[:4] for emoji in emoji_list):
                # Add relevant emojis based on content
                if "hello" in content.lower() or "hi" in content.lower():
                    content = "👋 " + content
                elif "thank" in content.lower():
                    content = "😊 " + content
                elif "sorry" in content.lower():
                    content = "😔 " + content
                elif "help" in content.lower() or "assist" in content.lower():
                    content = "🤝 " + content
                elif "created" in content.lower() or "developer" in content.lower():
                    content = "👨‍💻 " + content
                elif "capabilities" in content.lower() or "can you" in content.lower():
                    content = "🚀 " + content
                elif any(word in content.lower() for word in ["data", "weather", "temperature"]):
                    content = "📊 " + content
                elif "error" in content.lower() or "trouble" in content.lower():
                    content = "⚠️ " + content
                elif "?" in content:
                    content = "🤔 " + content
                elif any(word in content.lower() for word in ["yes", "sure", "correct", "right"]):
                    content = "👍 " + content
                elif any(word in content.lower() for word in ["welcome", "please", "glad"]):
                    content = "🙏 " + content
                elif any(word in content.lower() for word in ["joke", "funny", "laugh"]):
                    content = "😄 " + content
                elif any(word in content.lower() for word in ["awesome", "amazing", "excellent", "great"]):
                    content = "✨ " + content
                else:
                    content = "💡 " + content
            
            # Check if this was a rule-based match and add the pattern indicator
            pattern_indicator = ""
            if message.get("matched_pattern", None):
                pattern_indicator = f'<div style="margin-top: 8px; font-size: 12px; color: #93c5fd;"><span class="pattern-indicator">rule</span> Matched pattern: <code>{message["matched_pattern"]}</code></div>'
            
            # Add AI indicator for non-rule responses
            elif "is_pattern_match" in message and not message["is_pattern_match"]:
                pattern_indicator = '<div style="margin-top: 8px; font-size: 12px; color: #93c5fd;"><span class="pattern-indicator">ai</span> No rule pattern matched - using AI response</div>'
                
            st.markdown(f'<div class="message bot-message">{content}{pattern_indicator}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area with form with better column proportions
    st.markdown('<div class="input-area">', unsafe_allow_html=True)

    with st.form(key="message_form", clear_on_submit=True):
        col1, col2 = st.columns([20, 1])
        
        with col1:
            st.markdown('<div class="input-container">', unsafe_allow_html=True)
            # Text input with clearer hint
            user_input = st.text_input(
                "Message",
                key="user_input",
                placeholder="Type your message here...",
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # Send button with upward arrow
            submitted = st.form_submit_button("", type="primary", help="Send message")
        
    st.markdown('</div>', unsafe_allow_html=True)  # Close input-area div

    # Handle form submission
    if submitted and user_input and user_input.strip():
        # Add user message to chat
        add_message("user", user_input)
        
        # Add to sidebar chat history
        add_to_chat_history(user_input)
        
        # Get and display response
        response_data = get_response(user_input)
        
        # Add assistant response to chat with pattern information if applicable
        add_message(
            "assistant", 
            response_data["response"], 
            response_data.get("matched_pattern") if response_data.get("is_pattern_match", False) else None
        )
        
        # Rerun to update the UI
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close chat-interface

# Improved method to check if a message has an emoji
def has_emoji(message):
    content = message.get("content", "")
    if not content:
        return False
    
    # Check for common emoji patterns (both Unicode and text-based)
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251" 
        "]+"
    )
    
    # Check for Unicode emojis
    if emoji_pattern.search(content):
        return True
    
    # Check for text-based emojis
    text_emojis = [':)', ':(', ':D', ':P', ':/', ':|', ';)', '<3', 'XD', '=)']
    for emoji in text_emojis:
        if emoji in content:
            return True
            
    return False

if __name__ == "__main__":
    main()
