import streamlit as st
import requests
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="المدفع للخدمات المالية | Al-Mdfaa Financial Services",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Light Theme with proper Arabic support
st.markdown("""
<style>
    /* Import beautiful Arabic-friendly fonts */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&family=Tajawal:wght@300;400;500;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling - Light Theme */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 50%, #f0f4f8 100%);
    }
    
    /* Global Arabic font fix */
    * {
        font-family: 'Tajawal', 'Cairo', 'Arial', sans-serif !important;
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
        background: linear-gradient(180deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.5) 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 100, 80, 0.15);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    }
    
    .chat-header h1 {
        color: #006450;
        font-family: 'Tajawal', 'Cairo', sans-serif !important;
        font-weight: 700;
        font-size: 2.5rem;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .chat-header p {
        color: #555;
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
        align-items: flex-start;
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
        flex-direction: row-reverse;
    }
    
    .message.bot {
        flex-direction: row;
    }
    
    .message-avatar {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        flex-shrink: 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .message.user .message-avatar {
        background: linear-gradient(135deg, #4a90d9 0%, #357abd 100%);
    }
    
    .message.bot .message-avatar {
        background: linear-gradient(135deg, #006450 0%, #008060 100%);
        color: white;
        font-weight: 700;
    }
    
    .message-wrapper {
        max-width: 70%;
        display: flex;
        flex-direction: column;
    }
    
    .message.user .message-wrapper {
        align-items: flex-end;
    }
    
    .message.bot .message-wrapper {
        align-items: flex-start;
    }
    
    .message-content {
        padding: 1rem 1.5rem;
        border-radius: 18px;
        line-height: 1.8;
        font-size: 1.05rem;
        direction: rtl;
        text-align: right;
        word-wrap: break-word;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        font-family: 'Tajawal', 'Cairo', sans-serif !important;
        unicode-bidi: plaintext;
    }
    
    .message.user .message-content {
        background: linear-gradient(135deg, #4a90d9 0%, #357abd 100%);
        color: white;
        border-bottom-right-radius: 4px;
    }
    
    .message.bot .message-content {
        background: white;
        color: #333;
        border-bottom-left-radius: 4px;
        border: 1px solid rgba(0, 100, 80, 0.15);
    }
    
    /* Timestamp */
    .message-time {
        font-size: 0.75rem;
        color: #888;
        margin-top: 0.4rem;
        direction: ltr;
    }
    
    .message.user .message-time {
        text-align: right;
        padding-right: 0.5rem;
    }
    
    .message.bot .message-time {
        text-align: left;
        padding-left: 0.5rem;
    }
    
    /* Welcome message */
    .welcome-card {
        background: white;
        border: 1px solid rgba(0, 100, 80, 0.15);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        text-align: center;
        direction: rtl;
    }
    
    .welcome-card h3 {
        color: #006450;
        margin-bottom: 1rem;
        font-family: 'Tajawal', 'Cairo', sans-serif !important;
        font-weight: 600;
        font-size: 1.5rem;
    }
    
    .welcome-card p {
        color: #555;
        line-height: 2;
        font-size: 1.05rem;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(0, 100, 80, 0.3);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 100, 80, 0.5);
    }
    
    /* Footer info */
    .footer-info {
        text-align: center;
        color: #888;
        font-size: 0.85rem;
        padding: 2rem 0 1rem 0;
        direction: rtl;
    }
    
    /* Chat input customization */
    .stChatInput {
        border-color: rgba(0, 100, 80, 0.3) !important;
    }
    
    .stChatInput > div {
        background: white !important;
        border: 2px solid rgba(0, 100, 80, 0.2) !important;
        border-radius: 24px !important;
    }
    
    .stChatInput textarea {
        font-family: 'Tajawal', 'Cairo', sans-serif !important;
        font-size: 1rem !important;
    }
    
    /* Clear button styling */
    .stButton > button {
        background: linear-gradient(135deg, #006450 0%, #008060 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 10px rgba(0, 100, 80, 0.2) !important;
        font-family: 'Tajawal', 'Cairo', sans-serif !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(0, 100, 80, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'sender_id' not in st.session_state:
    st.session_state.sender_id = f"user_{datetime.now().strftime('%Y%m%d%H%M%S')}"
if 'last_input' not in st.session_state:
    st.session_state.last_input = ""

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
    
    # Escape HTML but preserve line breaks
    safe_content = content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
    
    st.markdown(f"""
    <div class="message {role}">
        <div class="message-avatar">{avatar}</div>
        <div class="message-wrapper">
            <div class="message-content">{safe_content}</div>
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
            أنا المساعد الذكي للمدفع. يمكنني مساعدتك في:<br><br>
            ✓ الاستعلام عن الحوالات المالية<br>
            ✓ معرفة مواقع الفروع وأوقات العمل<br>
            ✓ السؤال عن الرسوم وأسعار الصرف<br>
            ✓ خطوات إرسال واستلام الأموال
        </p>
        <p style="margin-top: 1.5rem; font-size: 0.95rem; opacity: 0.7;">
            Welcome! I'm Al-Mdfaa's AI assistant. I can help you with transfers, branches, fees, and exchange rates.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Display chat history
for msg in st.session_state.messages:
    display_message(msg["role"], msg["content"], msg.get("timestamp"))

# Clear chat button at the top if there are messages
if st.session_state.messages:
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🗑️ مسح المحادثة", key="clear_chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.last_input = ""
            st.rerun()

# Chat input using st.chat_input
user_input = st.chat_input("اكتب رسالتك هنا... Type your message here...")

# Handle message input with duplicate prevention
if user_input and user_input != st.session_state.last_input:
    # Store this input to prevent duplicates
    st.session_state.last_input = user_input
    
    # Add user message
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": timestamp
    })
    
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
