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
    page_title="TravelPro AI Assistant",
    page_icon="✈️",
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
        background-image: radial-gradient(circle at 50% 50%, #151f38 0%, #0e1525 100%);
    }
    
    /* Chat interface */
    .chat-interface {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        padding: 0;
        background-color: transparent;
        position: relative;
        padding-bottom: 80px; /* Space for input area */
    }
    
    /* Messages container */
    .messages-container {
        flex: 1;
        overflow-y: auto;
        padding: 10px 20px 100px 20px;
        display: flex;
        flex-direction: column;
        gap: 15px;
        max-width: 900px;
        margin: 0 auto;
        width: 100%;
        scroll-behavior: smooth;
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
    
    /* Input area - fixed to bottom with improved design */
    .input-area {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 15px 20px 20px 20px;
        background: #0f1624;
        z-index: 100;
        border-top: 1px solid rgba(59, 130, 246, 0.1);
        box-shadow: 0 -5px 20px rgba(0, 0, 0, 0.4);
    }
    
    /* Form styling improvements */
    form[data-testid="stForm"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        max-width: 900px !important;
        margin: 0 auto !important;
    }
    
    /* Input container styling */
    .input-container {
        display: flex;
        align-items: center;
        background-color: #1b2435;
        border-radius: 8px;
        padding: 6px 5px 6px 15px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
        margin: 0 auto;
        width: 100%;
        height: 42px;
        transition: all 0.2s ease;
        border: 1px solid rgba(59, 130, 246, 0.1);
    }
    
    .input-container:focus-within {
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
        border: 1px solid rgba(59, 130, 246, 0.3);
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
    
    /* Send button improvements for perfect match */
    button[kind="primary"] {
        background: #f43f5e !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        width: 38px !important;
        height: 38px !important;
        padding: 0px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
        min-width: unset !important;
        margin: 0 !important;
        font-size: 0 !important;
    }
    
    button[kind="primary"]:hover {
        background: #e11d48 !important;
        transform: translateY(-1px) !important;
    }
    
    .stButton button::before {
        content: "↑";
        font-size: 22px;
        font-weight: bold;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: -2px;
    }
    
    /* Welcome container - made simpler without title */
    .welcome-container {
        text-align: center;
        padding: 40px 20px;
        color: #94a3b8;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: calc(100vh - 180px);
        margin-top: -20px;
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
    
    /* Footer info in chat input - minimal and centered */
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

    /* Travel banner styling */
    .travel-banner {
        background: linear-gradient(135deg, #9333ea, #7e22ce);
        color: white;
        border-radius: 12px;
        padding: 25px 30px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        animation: fadeIn 0.5s ease-out;
        text-align: left;
    }

    .travel-banner h1 {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .travel-banner p {
        font-size: 16px;
        opacity: 0.9;
        line-height: 1.5;
    }

    /* Suggestion buttons */
    .suggestion-title {
        color: #f8fafc;
        font-size: 16px;
        margin: 5px 0 15px 0;
    }

    .suggestion-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 20px;
    }

    .suggestion-button {
        background-color: #1e293b;
        color: #e2e8f0;
        border-radius: 30px;
        padding: 8px 15px;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.2s;
        border: 1px solid rgba(255, 255, 255, 0.1);
        display: inline-block;
        text-align: center;
    }

    .suggestion-button:hover {
        background-color: #2d3c50;
        transform: translateY(-2px);
    }

    /* Divider line */
    .divider {
        height: 1px;
        background: linear-gradient(to right, rgba(255,255,255,0.05), rgba(255,255,255,0.2), rgba(255,255,255,0.05));
        margin: 20px 0;
        width: 100%;
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
        # Define travel-themed rule patterns
        st.session_state.rules = [
            {
                'patterns': [r'hello|hi|hey|greetings', r'^hi$'],
                'responses': ["👋 Hello, travel enthusiast! How can I help plan your next adventure?", "👋 Hi there! Ready to explore new destinations?", "👋 Hey traveler! Where are you thinking of going next?"]
            },
            {
                'patterns': [r'who are you|what are you|tell me about yourself'],
                'responses': ["🧳 I'm TravelPro, your AI travel assistant created by Nandesh Kalashetti. I can help with destinations, itineraries, budgets, and travel tips!"]
            },
            {
                'patterns': [r'bye|goodbye|see you|farewell'],
                'responses': ["✈️ Bon voyage! Happy travels!", "🌍 Safe travels! Come back when you need more travel advice!", "👋 Enjoy your journey! See you next time!"]
            },
            {
                'patterns': [r'thank you|thanks'],
                'responses': ["🏝️ You're welcome! Enjoy your travels!", "🗺️ Happy to help with your travel plans! Anything else you need?"]
            },
            {
                'patterns': [r'what can you do|help|capabilities'],
                'responses': ["🧳 I can recommend destinations, help plan itineraries, suggest travel budgets, provide packing tips, and answer questions about attractions, accommodations, and local customs!"]
            },
            {
                'patterns': [r'weather|temperature|climate'],
                'responses': ["🌦️ Weather is a crucial factor in travel planning! I can give you general climate info for destinations, though I don't have real-time weather data."]
            },
            {
                'patterns': [r'best time|when to visit|season'],
                'responses': ["🗓️ The best time to visit depends on what you're looking for - lower prices in off-season, good weather, or special festivals. I can help you decide!"]
            },
            {
                'patterns': [r'budget|cost|expensive|cheap'],
                'responses': ["💰 Travel budgets vary widely based on destination, accommodation type, dining preferences, and activities. I can help you plan for any budget level!"]
            },
            {
                'patterns': [r'flight|airplane|airport|booking'],
                'responses': ["✈️ For the best flight deals, I recommend booking 1-3 months in advance for domestic and 2-6 months for international flights. Flexible dates often yield better prices!"]
            },
            {
                'patterns': [r'hotel|stay|accommodation|hostel'],
                'responses': ["🏨 Your accommodation choice can make or break a trip! From luxury hotels to budget hostels, I can suggest options based on your preferences and budget."]
            },
            {
                'patterns': [r'food|eat|restaurant|cuisine'],
                'responses': ["🍽️ Trying local cuisine is one of the best parts of traveling! I can recommend signature dishes and dining experiences for destinations worldwide."]
            },
            {
                'patterns': [r'safety|safe|danger'],
                'responses': ["🛡️ Safety is paramount when traveling. Research local laws, get travel insurance, keep digital copies of documents, and register with your embassy when visiting foreign countries."]
            },
            {
                'patterns': [r'pack|packing|suitcase|luggage'],
                'responses': ["🧳 Smart packing is an art! Make a list, pack versatile clothing, roll don't fold, and always leave some space for souvenirs!"]
            },
            {
                'patterns': [r'itinerary|plan|schedule|days'],
                'responses': ["📅 A good itinerary balances sightseeing with downtime. I recommend not overpacking your schedule - leave room for spontaneous discoveries!"]
            },
            {
                'patterns': [r'india|indian|mumbai|delhi|goa|jaipur'],
                'responses': ["🇮🇳 India offers incredible diversity - from the beaches of Goa to the Taj Mahal in Agra, bustling Mumbai to serene Kerala backwaters. What part are you interested in exploring?"]
            }
        ]

# Function to match user input with rule patterns - improved for faster response
def find_response(user_input):
    user_input = user_input.lower().strip()
    
    # Try to match with simple rules first for faster responses
    for rule in st.session_state.rules:
        for pattern in rule['patterns']:
            if re.search(pattern, user_input):
                return random.choice(rule['responses'])
    
    # If no simple rule matches, use Groq API for more complex responses
    return get_ai_response(user_input)

# Function to get response from Groq API
def get_ai_response(query):
    try:
        # Empty spinner for better UX
        with st.spinner(""):
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are TravelPro, a helpful AI travel assistant created by Nandesh Kalashetti. Provide concise, informative travel advice about destinations, itineraries, budgets, accommodations, attractions, local customs, and travel tips. Use emojis to make your responses engaging. Focus on being practical and specific with travel recommendations. If asked about an Indian destination, provide especially detailed information. Format important details in bold when helpful."},
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
        return "🧳 I'm having trouble connecting to my travel database right now. Please try again in a moment."

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
        
        # Get bot response
        response = find_response(user_message)
        
        # Add bot response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})
        
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
            <h4 style="color: #f8fafc; font-size: 14px; margin-bottom: 5px;">✈️ Destination Advice</h4>
            <p style="color: #94a3b8; font-size: 12px;">Recommendations for your next journey</p>
        </div>
        
        <div class="feature-card">
            <h4 style="color: #f8fafc; font-size: 14px; margin-bottom: 5px;">🗓️ Itinerary Planning</h4>
            <p style="color: #94a3b8; font-size: 12px;">Optimized travel schedules</p>
        </div>
        
        <div class="feature-card">
            <h4 style="color: #f8fafc; font-size: 14px; margin-bottom: 5px;">💰 Budget Tips</h4>
            <p style="color: #94a3b8; font-size: 12px;">Travel within your means</p>
        </div>
        
        <div class="feature-card">
            <h4 style="color: #f8fafc; font-size: 14px; margin-bottom: 5px;">🧳 Packing Lists</h4>
            <p style="color: #94a3b8; font-size: 12px;">Never forget essentials</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tech stack
        st.markdown("<h3 style='color: #f8fafc; font-size: 15px; margin: 20px 0 5px;'>Powered By</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div style="display: flex; flex-wrap: wrap; gap: 5px;">
            <span class="tech-badge">Python</span>
            <span class="tech-badge">Streamlit</span>
            <span class="tech-badge">Groq API</span>
            <span class="tech-badge">LLaMA 3</span>
            <span class="tech-badge">Travel Data</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content - TravelPro UI design
    st.markdown('<div class="chat-interface">', unsafe_allow_html=True)

    # TravelPro banner at the top
    st.markdown("""
    <div class="travel-banner">
        <h1>TravelPro AI Assistant</h1>
        <p>Ask me anything about travel planning, destinations, budgets, or itineraries! I'm here to help make your next journey unforgettable.</p>
    </div>
    """, unsafe_allow_html=True)

    # Suggestions for travel questions
    st.markdown('<p class="suggestion-title">Need inspiration? Try asking:</p>', unsafe_allow_html=True)
    st.markdown('<div class="suggestion-container">', unsafe_allow_html=True)

    # Create suggestion buttons with JavaScript to set input value
    suggestions = [
        "What's the best time to visit Goa?",
        "What are must-see attractions in Mumbai?",
        "How much should I budget for a week in Delhi?",
        "Suggest a 3-day itinerary for Jaipur"
    ]

    for suggestion in suggestions:
        suggestion_escaped = suggestion.replace("'", "\\'")
        st.markdown(f"""
        <div class="suggestion-button" onclick="document.querySelector('input[aria-label=Message]').value='{suggestion_escaped}'; document.querySelector('input[aria-label=Message]').dispatchEvent(new Event('input', {{ bubbles: true }}));">
            {suggestion}
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Divider line
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Messages container 
    st.markdown('<div class="messages-container">', unsafe_allow_html=True)
    
    # Display welcome message if no messages yet - TravelPro themed
    if not st.session_state.messages:
        st.markdown("""
        <div class="welcome-container">
            <img src="https://img.icons8.com/fluency/96/000000/globe.png" style="width: 80px; margin-bottom: 15px;" alt="Travel Icon">
            <p style="color: #f8fafc; font-size: 16px; margin-bottom: 8px;">Your AI travel companion is ready to help!</p>
            <p style="color: #94a3b8; font-size: 14px;">Ask any travel-related question using the box below</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display chat messages with emojis and better formatting
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="message user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            # Add emojis to make responses more engaging
            content = message["content"]
            # Only add emoji if not already present
            if not any(char in content[:2] for char in ['😊', '👋', '🤖', '💡', '🚀', '📊', '⚠️', '🤔', '👍', '✨', '🙏', '😄']):
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
                
            st.markdown(f'<div class="message bot-message">{content}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area with fully integrated footer - TravelPro style
    st.markdown('<div class="input-area">', unsafe_allow_html=True)

    # Using a form to handle Enter key press
    with st.form(key="message_form", clear_on_submit=True):
        cols = st.columns([30, 1])
        
        with cols[0]:
            st.markdown('<div class="input-container">', unsafe_allow_html=True)
            # Text input with travel-themed placeholder
            user_input = st.text_input(
                "Message",
                key="user_input",
                placeholder="Type your travel question here...",
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with cols[1]:
            # Send button with upward arrow
            submitted = st.form_submit_button("", type="primary", help="Send message")
        
        # Simple, unobtrusive footer
        st.markdown("""
        <div class="footer-info">
            © 2025 Nandesh Kalashetti | AI Travel Assistant
        </div>
        """, unsafe_allow_html=True)
    
    # Handle form submission
    if submitted and user_input and user_input.strip():
        # Add to chat history
        add_to_chat_history(user_input)
        
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get bot response
        response = find_response(user_input)
        
        # Add bot response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun to update the UI
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close chat-interface

if __name__ == "__main__":
    main()
