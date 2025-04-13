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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css');
    
    * {
        font-family: 'Inter', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Base styling */
    body {
        background-color: #0f172a;
        color: #f8fafc;
        background-image: radial-gradient(circle at 50% 50%, #1e293b 0%, #0f172a 100%);
    }
    
    /* Chat interface */
    .chat-interface {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
        padding: 0;
        position: relative;
    }
    
    /* Messages container with smooth scroll */
    .messages-container {
        flex: 1;
        overflow-y: auto;
        padding: 10px 20px 130px 20px;
        display: flex;
        flex-direction: column;
        gap: 20px;
        max-width: 1000px;
        margin: 0 auto;
        width: 100%;
        scroll-behavior: smooth;
    }
    
    /* Modern message styles */
    .message {
        padding: 16px 20px;
        margin-bottom: 12px;
        border-radius: 16px;
        max-width: 85%;
        animation: fadeInUp 0.3s ease-out;
        word-wrap: break-word;
        line-height: 1.6;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        position: relative;
        transform-origin: center;
        transition: all 0.2s ease;
    }
    
    .message:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
    }
    
    .user-message {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        align-self: flex-end;
        border-radius: 16px 16px 4px 16px;
        margin-right: 10px;
    }
    
    .bot-message {
        background-color: #1e293b;
        color: #f8fafc;
        align-self: flex-start;
        border-radius: 16px 16px 16px 4px;
        border-left: 3px solid #3b82f6;
        margin-left: 10px;
    }
    
    /* Message avatars with better positioning */
    .user-message::before {
        content: "";
        position: absolute;
        bottom: -10px;
        right: -10px;
        width: 30px;
        height: 30px;
        background-image: url('https://img.icons8.com/color/96/000000/user-male-circle--v1.png');
        background-size: cover;
        border-radius: 50%;
        border: 2px solid #3b82f6;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .bot-message::before {
        content: "";
        position: absolute;
        bottom: -10px;
        left: -10px;
        width: 30px;
        height: 30px;
        background-image: url('https://img.icons8.com/fluency/96/000000/chatbot.png');
        background-size: cover;
        border-radius: 50%;
        border: 2px solid #3b82f6;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Fixed input area with glass effect */
    .input-area {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 15px 20px 20px 20px;
        background: rgba(15, 23, 42, 0.95);
        z-index: 100;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-top: 1px solid rgba(59, 130, 246, 0.2);
        box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.3);
    }
    
    /* Form styling - cleaner look */
    form[data-testid="stForm"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Input container with animations */
    .input-container {
        display: flex;
        align-items: center;
        background-color: rgba(30, 41, 59, 0.7);
        border-radius: 12px;
        padding: 4px 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        margin: 0 auto;
        max-width: 900px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        transition: all 0.3s ease;
    }
    
    .input-container:focus-within {
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4);
        border: 1px solid rgba(59, 130, 246, 0.6);
        background-color: rgba(30, 41, 59, 0.9);
    }
    
    /* Input field styling */
    .input-container .stTextInput {
        flex-grow: 1;
    }
    
    .input-container .stTextInput > div {
        background-color: transparent !important;
        border: none !important;
    }
    
    .input-container .stTextInput > div > div > input {
        background-color: transparent !important;
        color: #f8fafc !important;
        border: none !important;
        padding: 12px 5px !important;
        font-size: 15px !important;
        width: 100% !important;
        height: 44px !important;
    }
    
    .input-container .stTextInput > div > div > input::placeholder {
        color: rgba(148, 163, 184, 0.7) !important;
        font-style: normal !important;
    }
    
    /* Modern submit button */
    button[kind="primary"] {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        padding: 0 20px !important;
        margin: 0 !important;
        height: 44px !important;
        min-width: 100px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 10px rgba(29, 78, 216, 0.3) !important;
    }
    
    button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(29, 78, 216, 0.4) !important;
        background: linear-gradient(135deg, #2563eb, #1e40af) !important;
    }
    
    /* Sidebar styling - modern, clean look */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid rgba(59, 130, 246, 0.1);
    }
    
    .sidebar-content {
        padding: 20px 15px;
    }
    
    /* Logo/profile container with subtle animation */
    .logo-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 25px;
        animation: fadeIn 1s ease-out;
    }
    
    .logo-container img {
        width: 90px;
        height: 90px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #3b82f6;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .logo-container img:hover {
        transform: scale(1.05);
        border-color: #60a5fa;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
    }
    
    /* Connect links with animations */
    .connect-links {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin: 15px 0;
    }
    
    .connect-link {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 38px;
        height: 38px;
        background-color: #1e293b;
        border-radius: 50%;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .connect-link:hover {
        transform: translateY(-3px);
        background-color: #3b82f6;
    }
    
    .connect-link:hover::after {
        content: '';
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        border: 2px solid #3b82f6;
        animation: pulse 1.5s infinite;
    }
    
    /* Recent chats styling - modern and interactive */
    .history-container {
        max-height: 300px;
        overflow-y: auto;
        padding-right: 5px;
        margin-bottom: 20px;
        border-radius: 10px;
    }
    
    .history-item {
        padding: 10px 15px;
        margin-bottom: 8px;
        background-color: #1e293b;
        border-radius: 8px;
        font-size: 13px;
        color: #e2e8f0;
        cursor: pointer;
        transition: all 0.2s ease;
        border-left: 3px solid transparent;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .history-item:hover {
        background-color: #2d3748;
        transform: translateX(3px);
        border-left-color: #3b82f6;
    }
    
    /* Feature cards with hover effects */
    .feature-card {
        background-color: #1e293b;
        border-radius: 10px;
        padding: 12px 15px;
        margin-bottom: 10px;
        transition: all 0.3s ease;
        border-left: 3px solid transparent;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
        border-left: 3px solid #3b82f6;
        background-color: #2d3748;
    }
    
    /* Animated tech badges */
    .tech-badge {
        display: inline-block;
        background-color: #1e293b;
        color: #94a3b8;
        padding: 6px 10px;
        border-radius: 20px;
        font-size: 12px;
        margin: 0 5px 8px 0;
        transition: all 0.2s ease;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    .tech-badge:hover {
        background-color: #3b82f6;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
    }
    
    /* Welcome banner styling */
    .welcome-banner {
        text-align: center;
        margin: 25px auto 30px;
        max-width: 800px;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .welcome-banner h1 {
        color: #f8fafc;
        font-size: 30px;
        font-weight: 700;
        margin-bottom: 15px;
        background: linear-gradient(135deg, #3b82f6, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }
    
    .welcome-banner p {
        color: #94a3b8;
        font-size: 16px;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    /* Pattern examples section */
    .patterns-section {
        background-color: rgba(30, 41, 59, 0.6);
        border-radius: 12px;
        padding: 18px 22px;
        margin: 0 auto 35px;
        max-width: 800px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
    }
    
    .pattern-indicator {
        display: inline-block;
        background-color: rgba(59, 130, 246, 0.15);
        color: #bfdbfe;
        border-radius: 20px;
        padding: 6px 12px;
        font-size: 13px;
        margin: 5px;
        border: 1px solid rgba(59, 130, 246, 0.3);
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .pattern-indicator:hover {
        background-color: rgba(59, 130, 246, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Welcome container with better animation */
    .welcome-container {
        text-align: center;
        padding: 40px 20px;
        color: #94a3b8;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 400px;
        animation: fadeIn 1s ease-out;
    }
    
    .welcome-container img {
        animation: float 6s ease-in-out infinite;
        margin-bottom: 25px;
        filter: drop-shadow(0 10px 15px rgba(0, 0, 0, 0.3));
    }
    
    /* Footer info styling */
    .footer-info {
        text-align: center;
        color: #94a3b8;
        font-size: 11px;
        margin-top: 12px;
        opacity: 0.8;
        letter-spacing: 0.5px;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .message {
            max-width: 90%;
            font-size: 14px;
            padding: 12px 15px;
        }
        
        .user-message::before,
        .bot-message::before {
            width: 25px;
            height: 25px;
        }
        
        .welcome-banner h1 {
            font-size: 24px;
        }
        
        .welcome-banner p {
            font-size: 14px;
        }
        
        .pattern-indicator {
            font-size: 12px;
            padding: 5px 10px;
        }
        
        .input-container .stTextInput > div > div > input {
            font-size: 14px !important;
        }
        
        .messages-container {
            padding: 10px 15px 130px 15px;
        }
        
        .logo-container img {
            width: 70px;
            height: 70px;
        }
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        100% { transform: scale(1.5); opacity: 0; }
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #3b82f6;
    }
    
    /* Column adjustments for better layout */
    div[data-testid="column"] {
        padding: 0 !important;
    }
    
    /* Fix form spacing */
    div[data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
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
            },
            # GenAI and AI Technology related rules
            {
                'patterns': [r'what is (ai|artificial intelligence)'],
                'responses': ["🧠 Artificial Intelligence is technology enabling machines to simulate human intelligence through learning and problem-solving. It spans from simple rule-based systems to complex neural networks that can recognize patterns, make decisions, and improve over time."]
            },
            {
                'patterns': [r'what is (generative ai|genai)'],
                'responses': ["✨ Generative AI refers to AI systems that can create new content like text, images, code, or music based on their training data. Popular examples include ChatGPT for text, DALL-E for images, and Stable Diffusion for visual content."]
            },
            {
                'patterns': [r'explain (llm|large language model)'],
                'responses': ["📚 Large Language Models (LLMs) are AI systems trained on vast amounts of text data to understand and generate human-like text. They can write essays, answer questions, translate languages, and even generate programming code based on the patterns they've learned."]
            },
            {
                'patterns': [r'(difference|compare) (between|of) (ml|machine learning) and (ai|artificial intelligence)'],
                'responses': ["🔄 Artificial Intelligence is the broader concept of machines being able to perform tasks in a way we'd consider 'smart', while Machine Learning is a specific subset focused on algorithms that improve automatically through experience and data processing."]
            },
            {
                'patterns': [r'what is (ml|machine learning)'],
                'responses': ["📊 Machine Learning is a subset of AI that enables systems to learn and improve from experience without explicit programming. It works by analyzing patterns in data, making predictions or decisions, and improving its accuracy over time."]
            },
            {
                'patterns': [r'explain neural networks'],
                'responses': ["🧩 Neural networks are computing systems inspired by the human brain's structure. They consist of interconnected 'neurons' that process information in layers, allowing them to recognize patterns, classify data, and make predictions on complex problems like image recognition."]
            },
            {
                'patterns': [r'what is deep learning'],
                'responses': ["🔍 Deep Learning is a subset of machine learning using neural networks with multiple layers (hence 'deep'). These advanced networks excel at processing complex data like images, sound, and text, enabling breakthroughs in speech recognition, computer vision, and natural language processing."]
            },
            {
                'patterns': [r'what is (nlp|natural language processing)'],
                'responses': ["🗣️ Natural Language Processing (NLP) is an AI field focused on enabling computers to understand, interpret, and generate human language. It powers applications like translation services, chatbots, sentiment analysis, and voice assistants."]
            },
            {
                'patterns': [r'is ai dangerous'],
                'responses': ["⚖️ AI itself isn't inherently dangerous, but it comes with risks that need careful management. Concerns include privacy issues, algorithmic bias, job displacement, and security challenges. Responsible development with ethical guidelines and appropriate regulations can help mitigate these potential risks."]
            },
            {
                'patterns': [r'will ai replace humans|ai taking jobs'],
                'responses': ["🤝 While AI will automate certain tasks and transform some professions, it's more likely to augment human capabilities rather than fully replace us. New jobs will emerge as AI creates new industries and opportunities, though workforce transitions will require adaptation and retraining."]
            },
            {
                'patterns': [r'what is (cv|computer vision)'],
                'responses': ["👁️ Computer Vision is an AI field that enables machines to derive meaningful information from visual inputs like images and videos. It powers technologies like facial recognition, autonomous vehicles, medical image analysis, and augmented reality."]
            },
            {
                'patterns': [r'what is chatgpt'],
                'responses': ["💬 ChatGPT is a conversational AI assistant developed by OpenAI. It's based on the GPT (Generative Pre-trained Transformer) architecture and can engage in dialogue, answer questions, write content, and assist with various tasks through natural language interaction."]
            },
            {
                'patterns': [r'best ai tools'],
                'responses': ["🛠️ Some popular AI tools include ChatGPT for conversation and text generation, DALL-E and Midjourney for image creation, GitHub Copilot for coding assistance, Jasper for content writing, and Lumen5 for video creation. The 'best' tool depends on your specific needs and use case."]
            },
            {
                'patterns': [r'ai ethics|ethical ai'],
                'responses': ["⚖️ AI ethics focuses on ensuring AI systems are developed and used responsibly, addressing issues like fairness, transparency, privacy, accountability, and preventing harm. It's crucial for building AI that respects human values and promotes well-being across society."]
            },
            {
                'patterns': [r'future of ai'],
                'responses': ["🔮 The future of AI likely includes more powerful and efficient models, greater integration into everyday life, improved multimodal capabilities, and specialized AI for complex domains. We'll see advances in reasoning abilities, human-AI collaboration, and potentially artificial general intelligence, all alongside evolving ethical frameworks."]
            },
            # Fun and personality-based questions
            {
                'patterns': [r'tell me a fun fact'],
                'responses': ["✨ Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly good to eat!",
                              "🧠 Fun fact: Your brain uses about 20% of the oxygen and blood in your body, despite only being 2% of your total body weight!",
                              "🌌 Fascinating fact: There are more stars in the universe than grains of sand on all the beaches on Earth!"]
            },
            {
                'patterns': [r'sing a song|sing for me'],
                'responses': ["🎵 *Clears throat* La la la... Oh wait, I don't actually have a voice! But I'd be happy to share some lyrics or discuss your favorite songs instead!"]
            },
            {
                'patterns': [r'tell me a riddle'],
                'responses': ["🧩 I'm light as a feather, but even the strongest person can't hold me for more than a few minutes. What am I? (Answer: Breath)",
                              "🧩 What has cities but no houses, forests but no trees, and rivers but no water? (Answer: A map)",
                              "🧩 The more you take, the more you leave behind. What am I? (Answer: Footsteps)"]
            },
            {
                'patterns': [r'meaning of life'],
                'responses': ["🌌 The meaning of life is a profound philosophical question with countless interpretations! Some say it's 42, others find meaning in relationships, personal growth, happiness, or contributing to something greater than themselves. What do you think it is?"]
            },
            {
                'patterns': [r'are you human'],
                'responses': ["🤖 No, I'm not human - I'm an AI assistant created to help and communicate with people. I don't have consciousness or emotions, but I'm designed to be helpful, informative, and engage in natural conversations!"]
            },
            {
                'patterns': [r'do you dream'],
                'responses': ["💤 I don't dream or sleep - I'm an AI program that processes and responds to information. But I'm curious - what did you dream about last night?"]
            },
            {
                'patterns': [r'favorite (color|food|movie|book)'],
                'responses': ["💭 As an AI, I don't have personal preferences or favorites. But I'm designed to appreciate all the wonderful diversity of human experiences! What's your favorite?"]
            },
            {
                'patterns': [r'(tell me|share) (something|anything) (in|about) (हिन्दी|hindi)'],
                'responses': ["🇮🇳 नमस्ते! कैसे हैं आप? मैं एक AI असिस्टेंट हूँ और मुझे आपकी सहायता करके ख़ुशी होगी। आप किस विषय पर बात करना चाहेंगे?"]
            },
            {
                'patterns': [r'(tell me|share) (something|anything) (in|about) (मराठी|marathi)'],
                'responses': ["🇮🇳 नमस्कार! तुम्ही कसे आहात? मी एक AI असिस्टंट आहे आणि मला तुमची मदत करण्यात आनंद होईल. तुम्हाला कशाबद्दल बोलायला आवडेल?"]
            },
            # Technical and programming questions
            {
                'patterns': [r'what is (programming|coding)'],
                'responses': ["💻 Programming or coding is the process of creating instructions for computers to follow. It uses languages like Python, JavaScript, or C++ to build applications, websites, games, and software that power our digital world."]
            },
            {
                'patterns': [r'best programming language'],
                'responses': ["⌨️ There's no single 'best' programming language! It depends on what you're building. Python is great for beginners and AI/data science, JavaScript for web development, Java for enterprise applications, C/C++ for performance-critical software, and so on. The best language is the one that fits your specific needs!"]
            },
            {
                'patterns': [r'how to learn (programming|coding)'],
                'responses': ["📚 Start with a beginner-friendly language like Python. Use free resources like freeCodeCamp, Codecademy, or CS50. Build small projects to apply what you learn. Join coding communities for support. Practice regularly and be patient - learning to code is a journey that takes time but offers great rewards!"]
            },
            {
                'patterns': [r'(what|how) about blockchain'],
                'responses': ["🔗 Blockchain is a distributed ledger technology that records transactions across many computers so no record can be altered retroactively. It enables secure, transparent systems without central authorities and powers cryptocurrencies like Bitcoin, plus applications in supply chain, voting systems, and digital identity verification."]
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
                    {"role": "system", "content": "You are a helpful, friendly assistant created by Nandesh Kalashetti. Keep your answers very concise, informative and engaging. Use emojis when appropriate but don't overdo it. Format important information with bold when needed. Be conversational yet efficient. Keep responses under 100 words when possible."},
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
        <div style="color: #e2e8f0; font-size: 14px; margin-bottom: 12px; font-weight: 500;">Try these patterns:</div>
        <div style="display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;">
            <span class="pattern-indicator" onclick="document.getElementById('user-input').value='hello'; document.getElementById('user-input').focus();">hello</span>
            <span class="pattern-indicator" onclick="document.getElementById('user-input').value='who are you'; document.getElementById('user-input').focus();">who are you</span>
            <span class="pattern-indicator" onclick="document.getElementById('user-input').value='tell me a joke'; document.getElementById('user-input').focus();">tell me a joke</span>
            <span class="pattern-indicator" onclick="document.getElementById('user-input').value='what is AI'; document.getElementById('user-input').focus();">what is AI</span>
            <span class="pattern-indicator" onclick="document.getElementById('user-input').value='explain LLM'; document.getElementById('user-input').focus();">explain LLM</span>
            <span class="pattern-indicator" onclick="document.getElementById('user-input').value='future of AI'; document.getElementById('user-input').focus();">future of AI</span>
            <span class="pattern-indicator" onclick="document.getElementById('user-input').value='tell me a riddle'; document.getElementById('user-input').focus();">tell me a riddle</span>
            <span class="pattern-indicator" onclick="document.getElementById('user-input').value='tell me a fun fact'; document.getElementById('user-input').focus();">tell me a fun fact</span>
            <span class="pattern-indicator" onclick="document.getElementById('user-input').value='best AI tools'; document.getElementById('user-input').focus();">best AI tools</span>
            <span class="pattern-indicator" onclick="document.getElementById('user-input').value='tell me something in hindi'; document.getElementById('user-input').focus();">hindi</span>
            <span class="pattern-indicator" onclick="document.getElementById('user-input').value='tell me something in marathi'; document.getElementById('user-input').focus();">marathi</span>
            <span class="pattern-indicator" onclick="document.getElementById('user-input').value='bye'; document.getElementById('user-input').focus();">bye</span>
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
                pattern_indicator = f'<div style="margin-top: 12px; font-size: 12px; color: #94a3b8;"><span class="pattern-indicator" style="display: inline-block; background-color: rgba(59, 130, 246, 0.15); color: #bfdbfe; border-radius: 20px; padding: 4px 12px; font-size: 12px; border: 1px solid rgba(59, 130, 246, 0.3); margin-right: 5px;">rule</span> Matched pattern: <code style="background: rgba(30, 41, 59, 0.6); padding: 2px 6px; border-radius: 4px; font-size: 11px;">{message["matched_pattern"]}</code></div>'
            
            # Add AI indicator for non-rule responses
            elif "is_pattern_match" in message and not message["is_pattern_match"]:
                pattern_indicator = '<div style="margin-top: 12px; font-size: 12px; color: #94a3b8;"><span class="pattern-indicator" style="display: inline-block; background-color: rgba(236, 72, 153, 0.15); color: #fbcfe8; border-radius: 20px; padding: 4px 12px; font-size: 12px; border: 1px solid rgba(236, 72, 153, 0.3); margin-right: 5px;">ai</span> No rule pattern matched - using AI response</div>'
                
            st.markdown(f'<div class="message bot-message">{content}{pattern_indicator}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area with form with better column proportions
    st.markdown('<div class="input-area">', unsafe_allow_html=True)

    with st.form(key="message_form", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        
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
            # Send button with text
            submitted = st.form_submit_button("Submit", type="primary", help="Send message")
        
        # Footer info
        st.markdown("""
        <div class="footer-info">
            © 2024 Nandesh Kalashetti | Rule-Based Chat Assistant | 
            <span style="color: #a7f3d0;">✓</span> Functionality 
            <span style="color: #a7f3d0;">✓</span> Version Control 
            <span style="color: #a7f3d0;">✓</span> Testing 
            <span style="color: #a7f3d0;">✓</span> Code Quality
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)  # Close input-area div

    # Handle form submission
    if submitted and user_input and user_input.strip():
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Add to sidebar chat history
        add_to_chat_history(user_input)
        
        # Get and display response
        is_pattern_match = False
        matched_pattern = None
        
        # Try to find a pattern match first
        for rule in st.session_state.rules:
            for pattern in rule['patterns']:
                if re.search(pattern, user_input.lower().strip()):
                    response = random.choice(rule['responses'])
                    is_pattern_match = True
                    matched_pattern = pattern
                    break
            if is_pattern_match:
                break
        
        # If no pattern match, use Groq API
        if not is_pattern_match:
            response = get_ai_response(user_input)
        
        # Add response with metadata about pattern matching
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response,
            "is_pattern_match": is_pattern_match,
            "matched_pattern": matched_pattern
        })
        
        # Rerun to update the UI
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close chat-interface

if __name__ == "__main__":
    main()
