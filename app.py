# app.py
import streamlit as st
import re
import os
import time
import random
from dotenv import load_dotenv
from groq import Groq

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
        padding-right: calc(100vw - 100%); /* Prevent scrollbar jumping */
    }
    
    /* Messages container with proper scroll area */
    .messages-container {
        flex: 1;
        overflow-y: auto;
        padding: 0px 20px 100px 20px;
        display: flex;
        flex-direction: column;
        gap: 15px;
        max-width: 900px;
        margin: 0 auto;
        width: 100%;
        scroll-behavior: smooth;
        height: calc(100vh - 200px);
        margin-bottom: 90px;
    }
    
    /* Message styles */
    .message {
        padding: 15px 20px;
        margin-bottom: 15px;
        border-radius: 15px;
        max-width: 80%;
        animation: fadeIn 0.3s ease-out;
        word-wrap: break-word;
        line-height: 1.5;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        position: relative;
    }
    
    .user-message {
        background: linear-gradient(135deg, #3b82f6, #1e40af);
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
        position: relative;
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
    
    /* Input area - fixed to bottom with improved positioning */
    .input-area {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 15px 15px 10px 15px;
        background: #0e1525;
        z-index: 100;
        border-top: 1px solid rgba(59, 130, 246, 0.2);
        box-shadow: 0 -5px 20px rgba(0, 0, 0, 0.3);
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
        border-radius: 12px;
        padding: 8px 8px 8px 15px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        margin: 0 auto;
        width: 100%;
        max-width: 850px;
        height: 48px;
        transition: all 0.2s ease;
        border: 1px solid rgba(59, 130, 246, 0.2);
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
    
    /* Welcome container - better size and placement */
    .welcome-container {
        text-align: center;
        padding: 60px 20px;
        color: #94a3b8;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: calc(100vh - 280px);
        min-height: 300px;
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
    
    /* Footer info in chat input - clean and minimal */
    .footer-info {
        text-align: center;
        color: #64748b;
        font-size: 10px;
        margin-top: 6px;
        opacity: 0.6;
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
        background: linear-gradient(135deg, #1e293b, #0f172a);
        color: white;
        border-radius: 8px;
        padding: 16px 20px;
        margin: 10px 15px 15px 15px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
        animation: fadeIn 0.5s ease-out;
        text-align: left;
        border-left: 3px solid #3b82f6;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }

    .welcome-banner h1 {
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 6px;
    }

    .welcome-banner p {
        font-size: 14px;
        opacity: 0.9;
        line-height: 1.4;
    }

    /* Pattern examples section */
    .patterns-section {
        background-color: #1e293b;
        border-radius: 8px;
        padding: 14px 16px;
        margin: 0 15px 15px 15px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border-left: 2px solid #3b82f6;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
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
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
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

# Function to match user input with rule patterns
def find_response(user_input):
    user_input = user_input.lower().strip()
    
    # Try to match with simple rules first 
    for rule in st.session_state.rules:
        for pattern in rule['patterns']:
            if re.search(pattern, user_input):
                response = random.choice(rule['responses'])
                # Add indicator that this was a rule-based match
                return {"content": response, "matched": True, "pattern": pattern}
    
    # If no simple rule matches, use Groq API for more complex responses
    ai_response = get_ai_response(user_input)
    return {"content": ai_response, "matched": False, "pattern": None}

# Function to get response from Groq API
def get_ai_response(query):
    try:
        # Empty spinner for better UX
        with st.spinner(""):
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a rule-based AI assistant created by Nandesh Kalashetti. Your primary function is pattern matching, but you can handle complex queries too. Keep answers concise and informative (under 100 words). Use emojis occasionally to make responses engaging. Format important information in bold. Remember that users are testing a pattern-matching chatbot, so you might reference the pattern-matching capability in your responses when appropriate."},
                    {"role": "user", "content": query}
                ],
                model="llama3-8b-8192",  # Efficient model
                max_tokens=500,  # Reduced for faster responses
                temperature=0.7,  # Good creativity balance
                top_p=0.95,  # Better quality without sacrificing speed
                stream=False,  # Not streaming for faster complete responses
                timeout=10  # Set timeout to ensure fast responses
            )
            return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error connecting to Groq API: {str(e)}")
        return "😕 I'm having trouble connecting right now. Please try again in a moment."

# Function to add to chat history
def add_to_chat_history(query):
    if query not in [item[0] for item in st.session_state.chat_history]:
        st.session_state.chat_history.insert(0, (query, time.time()))
        # Keep only the most recent 15 queries
        if len(st.session_state.chat_history) > 15:
            st.session_state.chat_history = st.session_state.chat_history[:15]

# Function to handle message submission
def handle_submit():
    if st.session_state.user_input:
        user_message = st.session_state.user_input
        
        # Add to chat history
        add_to_chat_history(user_message)
        
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_message})
        
        # Clear input
        st.session_state.user_input = ""
        
        # Get bot response - now includes pattern info
        response_data = find_response(user_message)
        
        # Add bot response to chat with pattern info
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response_data["content"],
            "matched": response_data["matched"],
            "pattern": response_data["pattern"]
        })
        
        # Rerun to update UI
        st.rerun()

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

    # Display welcome message if no messages yet - focused on rule-based functionality
    if not st.session_state.messages:
        st.markdown("""
        <div class="welcome-container">
            <img src="https://img.icons8.com/fluency/96/000000/chatbot.png" style="width: 80px; margin-bottom: 15px;" alt="Chatbot Icon">
            <p style="color: #f8fafc; font-size: 16px; margin-bottom: 8px;">Rule-Based AI Assistant Ready!</p>
            <p style="color: #94a3b8; font-size: 14px;">Ask me predefined questions or try more complex queries</p>
        </div>
        """, unsafe_allow_html=True)
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

    # Display chat messages with pattern indicators for rule-based responses
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
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
            if message.get("matched", False):
                pattern = message.get("pattern", "")
                if pattern:
                    pattern_indicator = f'<div style="margin-top: 8px; font-size: 12px; color: #93c5fd;"><span class="pattern-indicator">rule</span> Matched pattern: <code>{pattern}</code></div>'
            
            # Add AI indicator for non-rule responses
            elif "matched" in message and not message["matched"]:
                pattern_indicator = '<div style="margin-top: 8px; font-size: 12px; color: #93c5fd;"><span class="pattern-indicator">ai</span> No rule pattern matched - using AI response</div>'
                
            st.markdown(f'<div class="message bot-message">{content}{pattern_indicator}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area with form with better column proportions
    st.markdown('<div class="input-area">', unsafe_allow_html=True)

    with st.form(key="message_form", clear_on_submit=True):
        col1, col2 = st.columns([15, 1])
        
        with col1:
            st.markdown('<div class="input-container">', unsafe_allow_html=True)
            # Text input with hint for rule-based queries
            user_input = st.text_input(
                "Message",
                key="user_input",
                placeholder="Ask me a question (try: 'hello', 'who are you', 'tell me a joke')",
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # Send button with upward arrow
            submitted = st.form_submit_button("", type="primary", help="Send message")
        
        # Footer info fully integrated with chat input
        st.markdown("""
        <div class="footer-info">
            © 2025 Nandesh Kalashetti | Rule-Based Chatbot with AI Capabilities
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # Close input-area div

    # Handle form submission
    if submitted and user_input and user_input.strip():
        # Add to chat history
        add_to_chat_history(user_input)
        
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get bot response with pattern data
        response_data = find_response(user_input)
        
        # Add bot response to chat with proper data structure
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response_data["content"],
            "matched": response_data["matched"],
            "pattern": response_data["pattern"]
        })
        
        # Rerun to update the UI
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close chat-interface

if __name__ == "__main__":
    main()
