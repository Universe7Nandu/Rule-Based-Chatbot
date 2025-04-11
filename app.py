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
    page_title="RuleBot - Rule-Based Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Configure Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Define CSS styles for glassmorphism
def load_css():
    st.markdown("""
    <style>
    /* Glassmorphism Base Style */
    .glass-container {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.12);
        padding: 20px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    /* Dark Mode Theme */
    .dark-theme {
        background-color: #121212;
        color: #e0e0e0;
    }
    
    /* Light Mode Theme */
    .light-theme {
        background-color: #f0f2f6;
        color: #121212;
    }
    
    /* Neumorphic Button */
    .neumorphic-btn {
        background: #f0f0f0;
        border-radius: 10px;
        box-shadow: 5px 5px 10px #d9d9d9, -5px -5px 10px #ffffff;
        padding: 10px 15px;
        border: none;
        color: #333;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .neumorphic-btn:hover {
        box-shadow: inset 5px 5px 10px #d9d9d9, inset -5px -5px 10px #ffffff;
    }
    
    /* Card Style */
    .card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
        transition: transform 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
    }
    
    /* Custom Table Style */
    .styled-table {
        width: 100%;
        backdrop-filter: blur(10px);
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        overflow: hidden;
    }
    
    .styled-table th {
        background: rgba(255, 255, 255, 0.1);
        padding: 10px;
    }
    
    .styled-table td {
        padding: 8px 10px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Gradient Progress Bar */
    .progress-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        height: 10px;
        width: 100%;
        overflow: hidden;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #12c2e9, #c471ed, #f64f59);
        height: 100%;
        border-radius: 20px;
        transition: width 0.5s ease;
    }
    
    /* Custom Message Styles */
    .user-message {
        background: rgba(114, 137, 218, 0.2);
        backdrop-filter: blur(10px);
        padding: 10px 15px;
        border-radius: 10px 10px 0 10px;
        margin: 10px 0;
        float: right;
        clear: both;
        max-width: 80%;
    }
    
    .bot-message {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 10px 15px;
        border-radius: 10px 10px 10px 0;
        margin: 10px 0;
        float: left;
        clear: both;
        max-width: 80%;
    }
    
    /* Page Transition Animation */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .main-content {
        animation: fadeIn 0.5s ease-in-out;
    }
    
    div[data-testid="stVerticalBlock"] {
        animation: fadeIn 0.5s ease-in-out;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state variables
def init_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    if 'rules' not in st.session_state:
        # Define simple rule patterns
        st.session_state.rules = [
            {
                'patterns': [r'hello|hi|hey|greetings', r'^hi$'],
                'responses': ["Hello! How can I help you today?", "Hi there! What can I assist you with?"]
            },
            {
                'patterns': [r'who are you|what are you|tell me about yourself'],
                'responses': ["I'm a rule-based chatbot with AI capabilities. I can answer your questions based on predefined patterns and use AI for more complex queries."]
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
                'responses': ["I can answer simple questions, provide information, and use AI to help with more complex queries."]
            },
            {
                'patterns': [r'weather|temperature'],
                'responses': ["I'm sorry, I don't have access to real-time weather data."]
            },
            {
                'patterns': [r'your name'],
                'responses': ["I'm RuleBot, your friendly rule-based chatbot with AI capabilities."]
            },
            {
                'patterns': [r'how are you'],
                'responses': ["I'm doing well, thank you! How about you?", "I'm functioning properly, thanks for asking!"]
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
                    {"role": "system", "content": "You are a helpful, friendly assistant called RuleBot. Keep your answers concise and informative."},
                    {"role": "user", "content": query}
                ],
                model="llama3-8b-8192",
                max_tokens=800
            )
            return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error connecting to Groq API: {str(e)}")
        return "I'm having trouble connecting to my AI capabilities right now. Please try again later."

# Toggle dark/light mode
def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

# Custom spinner with progress bar
def custom_spinner(message):
    progress_placeholder = st.empty()
    for percent in range(101):
        progress_placeholder.markdown(f"""
        <div class="progress-container">
            <div class="progress-bar" style="width: {percent}%;"></div>
        </div>
        <p style="text-align: center;">{message} {percent}%</p>
        """, unsafe_allow_html=True)
        time.sleep(0.01)
    progress_placeholder.empty()

# Main app function
def main():
    load_css()
    init_session_state()
    
    # Remove the set_page_config from here since it's now at the top
    st.title("🤖 RuleBot - Your AI Assistant")
    
    # Apply theme
    theme_class = "dark-theme" if st.session_state.dark_mode else "light-theme"
    st.markdown(f"""
    <div class="{theme_class}">
        <script>
            document.body.className = "{theme_class}";
        </script>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.title("🤖 RuleBot")
        st.markdown("A rule-based chatbot with AI capabilities")
        
        # Theme toggle
        theme_toggle = st.button("🌓 Toggle Light/Dark Mode")
        if theme_toggle:
            toggle_theme()
            st.experimental_rerun()
        
        # About section
        st.markdown("### About")
        st.markdown("""
        RuleBot is a simple rule-based chatbot that can:
        - Answer predefined questions
        - Use pattern matching for simple queries
        - Leverage Groq API for complex questions
        """)
        
        # GitHub link
        st.markdown("### Project")
        st.markdown("[GitHub Repository](https://github.com/yourusername/Rule-Based-Chatbot)")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Main content
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Chat", "About", "Settings"])
    
    with tab1:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.header("Chat with RuleBot")
        
        # Display chat messages
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)
        
        # Chat input
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_input("Type your message:", key="user_input")
            submit_button = st.form_submit_button("Send")
            
        if submit_button and user_input:
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Get bot response
            response = find_response(user_input)
            
            # Add bot response to chat
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Rerun to update the UI
            st.experimental_rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.header("About RuleBot")
        
        # Display information in cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Features")
            st.markdown("""
            - Rule-based pattern matching
            - AI-powered responses for complex queries
            - Modern glassmorphism UI design
            - Dark/Light theme toggle
            - Session history
            """)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Technologies")
            st.markdown("""
            - Streamlit for the web interface
            - Regular expressions for pattern matching
            - Groq API for complex query handling
            - CSS for modern UI design
            - Git & GitHub for version control
            """)
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("How It Works")
        st.markdown("""
        RuleBot uses a two-tier approach to answer questions:
        1. **Pattern Matching**: For simple queries, it uses predefined regex patterns to match questions and provide answers.
        2. **AI Integration**: For complex questions, it leverages the Groq API to generate more sophisticated responses.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.header("Settings")
        
        # Rule display
        st.subheader("Current Rule Patterns")
        
        # Show rules in a table format
        rule_data = []
        for i, rule in enumerate(st.session_state.rules):
            pattern_text = " | ".join(rule['patterns'])
            response_text = " | ".join(rule['responses'])
            rule_data.append([i+1, pattern_text, response_text])
        
        st.markdown("""
        <table class="styled-table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Patterns</th>
                    <th>Possible Responses</th>
                </tr>
            </thead>
            <tbody>
        """, unsafe_allow_html=True)
        
        for row in rule_data:
            st.markdown(f"""
            <tr>
                <td>{row[0]}</td>
                <td>{row[1]}</td>
                <td>{row[2]}</td>
            </tr>
            """, unsafe_allow_html=True)
            
        st.markdown("""
            </tbody>
        </table>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
