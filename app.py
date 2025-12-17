import streamlit as st
import requests
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="المدفع للخدمات المالية | Al-Mdfaa Financial Services",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for ChatGPT/Claude-like interface with Arabic support
st.markdown("""
<style>
    /* Import beautiful Arabic-friendly fonts */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&family=IBM+Plex+Sans+Arabic:wght@300;400;500;600&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'IBM Plex Sans Arabic', 'Cairo', sans-serif;
    }
    
    /* Chat container */
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 2rem 1rem;
        min-height: 100vh;
    }
    
    /* Header */
    .chat-header {
        text-align: center;
        padding: 2rem 0 3rem 0;
        background: linear-gradient(180deg, rgba(255,255,255,0.05) 0%, transparent 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .chat-header h1 {
        color: #ffd700;
        font-family: 'Space Grotesk', 'Cairo', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        margin: 0;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
        letter-spacing: -0.5px;
    }
    
    .chat-header p {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    /* Message styling */
    .message {
        display: flex;
        margin-bottom: 1.5rem;
        animation: slideIn 0.3s ease-out;
        gap: 1rem;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .message.user {
        justify-content: flex-end;
        direction: rtl;
    }
    
    .message.bot {
        justify-content: flex-start;
        direction: rtl;
    }
    
    .message-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        flex-shrink: 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .message.user .message-avatar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        order: 1;
    }
    
    .message.bot .message-avatar {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        color: #1a1a2e;
        font-weight: 700;
    }
    
    .message-content {
        max-width: 70%;
        padding: 1rem 1.5rem;
        border-radius: 18px;
        line-height: 1.6;
        font-size: 1rem;
        direction: rtl;
        text-align: right;
        position: relative;
        word-wrap: break-word;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .message.user .message-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-bottom-right-radius: 4px;
        order: 0;
    }
    
    .message.bot .message-content {
        background: rgba(255, 255, 255, 0.95);
        color: #1a1a2e;
        border-bottom-left-radius: 4px;
        border: 1px solid rgba(255, 215, 0, 0.2);
    }
    
    /* Timestamp */
    .message-time {
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.4);
        margin-top: 0.3rem;
        text-align: right;
        direction: rtl;
    }
    
    .message.user .message-time {
        text-align: left;
    }
    
    /* Input area */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid rgba(255, 215, 0, 0.3) !important;
        border-radius: 24px !important;
        padding: 1rem 1.5rem !important;
        color: white !important;
        font-size: 1rem !important;
        direction: rtl !important;
        text-align: right !important;
        font-family: 'IBM Plex Sans Arabic', 'Cairo', sans-serif !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ffd700 !important;
        box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.1) !important;
        background: rgba(255, 255, 255, 0.15) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
        direction: rtl !important;
    }
    
    /* Send button */
    .stButton > button {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%) !important;
        color: #1a1a2e !important;
        border: none !important;
        border-radius: 24px !important;
        padding: 0.75rem 2.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3) !important;
        font-family: 'Cairo', sans-serif !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Clear chat button */
    .clear-button {
        background: rgba(255, 255, 255, 0.1) !important;
        color: rgba(255, 255, 255, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 0.5rem 1.5rem !important;
        font-size: 0.9rem !important;
        font-family: 'Cairo', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    .clear-button:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        color: white !important;
    }
    
    /* Loading animation */
    .typing-indicator {
        display: flex;
        gap: 5px;
        padding: 1rem;
        direction: ltr;
    }
    
    .typing-indicator span {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: rgba(255, 215, 0, 0.7);
        animation: bounce 1.4s infinite ease-in-out;
    }
    
    .typing-indicator span:nth-child(1) {
        animation-delay: -0.32s;
    }
    
    .typing-indicator span:nth-child(2) {
        animation-delay: -0.16s;
    }
    
    @keyframes bounce {
        0%, 80%, 100% {
            transform: scale(0);
        }
        40% {
            transform: scale(1);
        }
    }
    
    /* Welcome message */
    .welcome-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        text-align: center;
        direction: rtl;
    }
    
    .welcome-card h3 {
        color: #ffd700;
        margin-bottom: 1rem;
        font-family: 'Cairo', sans-serif;
        font-weight: 600;
    }
    
    .welcome-card p {
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.8;
        font-size: 1rem;
    }
    
    /* Suggestion chips */
    .suggestion-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
        margin-top: 1.5rem;
        justify-content: center;
        direction: rtl;
    }
    
    .chip {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 20px;
        padding: 0.5rem 1.2rem;
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        backdrop-filter: blur(5px);
    }
    
    .chip:hover {
        background: rgba(255, 215, 0, 0.2);
        border-color: #ffd700;
        color: #ffd700;
        transform: translateY(-2px);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 215, 0, 0.3);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 215, 0, 0.5);
    }
    
    /* Footer info */
    .footer-info {
        text-align: center;
        color: rgba(255, 255, 255, 0.4);
        font-size: 0.85rem;
        padding: 2rem 0 1rem 0;
        direction: rtl;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'sender_id' not in st.session_state:
    st.session_state.sender_id = f"user_{datetime.now().strftime('%Y%m%d%H%M%S')}"

# Rasa configuration
RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"

def send_message_to_rasa(message: str, sender_id: str):
    """Send message to Rasa and get response"""
    try:
        payload = {
            "sender": sender_id,
            "message": message
        }
        response = requests.post(RASA_SERVER_URL, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return [{"text": f"⚠️ عذراً، حدث خطأ في الاتصال بالخادم. يرجى المحاولة مرة أخرى.\n\nSorry, connection error. Please try again.\n\nError: {str(e)}"}]

def display_message(role: str, content: str, timestamp: str = None):
    """Display a chat message with avatar and styling"""
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M")
    
    avatar = "👤" if role == "user" else "💰"
    
    st.markdown(f"""
    <div class="message {role}">
        <div class="message-avatar">{avatar}</div>
        <div>
            <div class="message-content">{content}</div>
            <div class="message-time">{timestamp}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
<div class="chat-header">
    <h1>💰 المدفع للخدمات المالية</h1>
    <p>Al-Mdfaa Financial Services • مساعدك الذكي للحوالات المالية</p>
</div>
""", unsafe_allow_html=True)

# Welcome message (shown only when no messages)
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-card">
        <h3>👋 أهلاً وسهلاً بك!</h3>
        <p>
            أنا المساعد الذكي للمدفع. يمكنني مساعدتك في:<br>
            ✓ الاستعلام عن الحوالات المالية<br>
            ✓ معرفة مواقع الفروع وأوقات العمل<br>
            ✓ السؤال عن الرسوم وأسعار الصرف<br>
            ✓ خطوات إرسال واستلام الأموال
        </p>
        <p style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.7;">
            Welcome! I'm Al-Mdfaa's AI assistant. I can help you with transfers, branches, fees, and exchange rates.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Suggestion chips
    st.markdown("""
    <div class="suggestion-chips">
        <div class="chip" onclick="document.querySelector('input').value='أين الفروع؟'">📍 أين الفروع؟</div>
        <div class="chip" onclick="document.querySelector('input').value='ما هي الرسوم؟'">💵 ما هي الرسوم؟</div>
        <div class="chip" onclick="document.querySelector('input').value='أسعار الصرف'">💱 أسعار الصرف</div>
        <div class="chip" onclick="document.querySelector('input').value='كيف أرسل حوالة؟'">📤 كيف أرسل حوالة؟</div>
    </div>
    """, unsafe_allow_html=True)

# Display chat history
for msg in st.session_state.messages:
    display_message(msg["role"], msg["content"], msg.get("timestamp"))

# Chat input area
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "Message",
        placeholder="اكتب رسالتك هنا... Type your message here...",
        key="user_input",
        label_visibility="collapsed"
    )

with col2:
    send_button = st.button("إرسال", use_container_width=True)

# Clear chat button (in sidebar or bottom)
if st.session_state.messages:
    if st.button("🗑️ مسح المحادثة", key="clear_chat", help="Clear conversation"):
        st.session_state.messages = []
        st.rerun()

# Handle send button or Enter key
if send_button and user_input:
    # Add user message
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": timestamp
    })
    
    # Show typing indicator
    with st.spinner(""):
        st.markdown("""
        <div class="message bot">
            <div class="message-avatar">💰</div>
            <div class="message-content">
                <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Get response from Rasa
        responses = send_message_to_rasa(user_input, st.session_state.sender_id)
    
    # Add bot responses
    for response in responses:
        if "text" in response:
            st.session_state.messages.append({
                "role": "bot",
                "content": response["text"],
                "timestamp": datetime.now().strftime("%H:%M")
            })
    
    # Rerun to update chat display
    st.rerun()

# Footer
st.markdown("""
<div class="footer-info">
    Built with ❤️ for Al-Mdfaa Financial Services
</div>
""", unsafe_allow_html=True)