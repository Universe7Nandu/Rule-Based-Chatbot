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
    page_title="AI Assistant | Nandesh Kalashetti",
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
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main Container */
    .main-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #fff;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        margin-bottom: 30px;
    }
    
    /* Chat Container */
    .chat-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.18);
        min-height: 600px;
        display: flex;
        flex-direction: column;
    }
    
    /* Message Styles */
    .messages-container {
        flex: 1;
        overflow-y: auto;
        padding: 15px;
        margin-bottom: 20px;
    }
    
    .user-message {
        background: rgba(255, 255, 255, 0.25);
        color: #fff;
        padding: 12px 18px;
        border-radius: 18px 18px 0 18px;
        margin: 10px 0;
        float: right;
        clear: both;
        max-width: 70%;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .bot-message {
        background: rgba(255, 255, 255, 0.15);
        color: #fff;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 0;
        margin: 10px 0;
        float: left;
        clear: both;
        max-width: 70%;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Input Area */
    .input-area {
        display: flex;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50px;
        padding: 5px;
        box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    .stTextInput>div>div>input {
        background-color: transparent !important;
        color: white !important;
        border: none !important;
        padding: 10px 15px !important;
        font-size: 16px !important;
    }
    
    /* Send Button */
    .send-button {
        background: linear-gradient(45deg, #6e45e2, #88d3ce);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 10px 25px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .send-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 15px rgba(0, 0, 0, 0.3);
    }
    
    /* Sidebar Styling */
    .sidebar-content {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 20px;
    }
    
    /* Feature Cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 15px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .main-content {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Background with Gradient Animation */
    body {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    
    /* Custom headers */
    h1, h2, h3 {
        font-weight: 600;
        color: white;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    h1 {
        font-size: 2.5rem;
        margin-bottom: 20px;
    }
    
    /* Logo animation */
    .logo-container {
        transition: all 0.3s ease;
    }
    
    .logo-container:hover {
        transform: scale(1.05);
    }
    
    /* Typing animation */
    .typing-animation {
        overflow: hidden;
        border-right: .15em solid white;
        white-space: nowrap;
        margin: 0 auto;
        letter-spacing: .15em;
        animation: 
            typing 3.5s steps(40, end),
            blink-caret .75s step-end infinite;
    }
    
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    
    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: white; }
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state variables
def init_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'rules' not in st.session_state:
        # Define rule patterns
        st.session_state.rules = [
            {
                'patterns': [r'hello|hi|hey|greetings', r'^hi$'],
                'responses': ["Hello! How can I help you today?", "Hi there! What can I assist you with?"]
            },
            {
                'patterns': [r'who are you|what are you|tell me about yourself'],
                'responses': ["I'm an AI assistant with rule-based capabilities. I can answer your questions based on predefined patterns and use AI for more complex queries."]
            },
            {
                'patterns': [r'bye|goodbye|see you|farewell'],
                'responses': ["Goodbye! Have a great day!", "See you later! Take care!"]
            },
            {
                'patterns': [r'thank you|thanks'],
                'responses': ["You're welcome!", "Happy to help!"]
            },
            {
                'patterns': [r'what can you do|help|capabilities'],
                'responses': ["I can answer simple questions, provide information, use AI for complex queries, and help with various tasks."]
            },
            {
                'patterns': [r'weather|temperature'],
                'responses': ["I'm sorry, I don't have access to real-time weather data."]
            },
            {
                'patterns': [r'your name'],
                'responses': ["I'm your AI assistant, created by Nandesh Kalashetti."]
            },
            {
                'patterns': [r'how are you'],
                'responses': ["I'm doing well, thank you! How about you?", "I'm functioning properly, thanks for asking!"]
            },
            {
                'patterns': [r'who (is|made) (you|this)|creator|developer'],
                'responses': ["I was created by Nandesh Kalashetti, a full-stack developer specializing in MERN stack, React.js, TypeScript, PHP, and MySQL."]
            },
            {
                'patterns': [r'project|about this chatbot'],
                'responses': ["This is an advanced rule-based chatbot with AI capabilities. It uses pattern matching for simple queries and AI for more complex questions."]
            }
        ]

# Function to match user input with rule patterns
def find_response(user_input):
    user_input = user_input.lower().strip()
    
    # Try to match with simple rules first
    for rule in st.session_state.rules:
        for pattern in rule['patterns']:
            if re.search(pattern, user_input):
                return random.choice(rule['responses'])
    
    # If no simple rule matches, use Groq API for more complex responses
    return get_ai_response(user_input)

# Function to get response from Groq API
def get_ai_response(query):
    try:
        with st.spinner("Thinking..."):
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful, friendly assistant created by Nandesh Kalashetti. Keep your answers concise, informative and engaging."},
                    {"role": "user", "content": query}
                ],
                model="llama3-8b-8192",
                max_tokens=800
            )
            return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error connecting to Groq API: {str(e)}")
        return "I'm having trouble connecting to my AI capabilities right now. Please try again later."

# Animated typing effect for messages
def typing_effect(message, container):
    full_message = ""
    for char in message:
        full_message += char
        container.markdown(full_message)
        time.sleep(0.01)  # Adjust speed as needed
    return full_message

# Main app function
def main():
    load_css()
    init_session_state()
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        
        # Developer info with profile picture
        st.markdown("""
        <div class="logo-container" style="text-align: center;">
            <img src="https://nandeshkalashetti.netlify.app/img/person.jpg" style="width: 150px; border-radius: 50%; border: 3px solid white; box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);">
            <h2>Nandesh Kalashetti</h2>
            <p>Full-Stack Developer</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Connect With Me")
        
        # Social links
        st.markdown("""
        <div style="display: flex; justify-content: center; gap: 15px; margin: 15px 0;">
            <a href="https://github.com/Universe7Nandu" target="_blank" style="text-decoration: none;">
                <img src="https://img.icons8.com/fluent/48/000000/github.png" width="35" />
            </a>
            <a href="https://www.linkedin.com/in/nandesh-kalashetti-333a78250/" target="_blank" style="text-decoration: none;">
                <img src="https://img.icons8.com/color/48/000000/linkedin.png" width="35" />
            </a>
            <a href="https://nandeshkalashetti.netlify.app/" target="_blank" style="text-decoration: none;">
                <img src="https://img.icons8.com/color/48/000000/domain.png" width="35" />
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature cards
        st.markdown("### Features")
        
        st.markdown("""
        <div class="feature-card">
            <h4>🧠 Rule-Based Intelligence</h4>
            <p>Pattern matching for quick responses to common queries</p>
        </div>
        
        <div class="feature-card">
            <h4>🤖 AI Integration</h4>
            <p>Powered by Groq LLM API for complex questions</p>
        </div>
        
        <div class="feature-card">
            <h4>💬 Natural Conversations</h4>
            <p>Engaging dialogue with context awareness</p>
        </div>
        
        <div class="feature-card">
            <h4>🎨 Modern UI</h4>
            <p>Beautiful glassmorphism design with animations</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tech stack
        st.markdown("### Tech Stack")
        st.markdown("""
        <div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-top: 10px;">
            <span style="background: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 15px; font-size: 12px;">Python</span>
            <span style="background: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 15px; font-size: 12px;">Streamlit</span>
            <span style="background: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 15px; font-size: 12px;">Groq API</span>
            <span style="background: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 15px; font-size: 12px;">LLaMA 3</span>
            <span style="background: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 15px; font-size: 12px;">CSS3</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Main chat area
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Main container with title
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Animated title
    st.markdown("""
    <h1 class="typing-animation" style="text-align: center;">AI Assistant with Rule-Based Intelligence</h1>
    <p style="text-align: center; margin-bottom: 30px;">Ask any question or start a conversation</p>
    """, unsafe_allow_html=True)
    
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Welcome message if no messages yet
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align: center; padding: 50px 20px; color: rgba(255,255,255,0.7);">
            <img src="https://img.icons8.com/fluency/96/000000/chatbot.png" style="width: 80px; margin-bottom: 20px;">
            <h3>Welcome to the AI Assistant!</h3>
            <p>Start the conversation by typing a message below.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Messages container
    st.markdown('<div class="messages-container">', unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    st.markdown('<div class="input-area">', unsafe_allow_html=True)
    
    # Using columns for better layout of input and button
    col1, col2 = st.columns([5,1])
    
    with col1:
        user_input = st.text_input("", placeholder="Type your message here...", key="user_input", label_visibility="collapsed")
    
    with col2:
        send_button = st.button("Send", key="send", help="Send message")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process user input
    if send_button and user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get bot response
        response = find_response(user_input)
        
        # Add bot response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun to update the UI
        st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close chat-container
    st.markdown('</div>', unsafe_allow_html=True)  # Close main-container
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 30px; padding: 15px; font-size: 12px; color: rgba(255,255,255,0.7);">
        © 2025 Nandesh Kalashetti | Advanced Rule-Based Chatbot with AI Capabilities
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close main-content

if __name__ == "__main__":
    main()
