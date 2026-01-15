import streamlit as st
import time
from agent import CryptoAgent

st.set_page_config(page_title="Crypto Agent", page_icon="🪙", layout="wide")

# ==================== VIDEO BACKGROUND + CUSTOM CSS STYLING ====================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* CSS Variables for Easy Customization */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --accent-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --dark-bg: #0f0f1e;
        --card-bg: rgba(15, 15, 30, 0.85);
        --text-primary: #ffffff;
        --text-secondary: #b8b9d4;
        --accent-color: #667eea;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --border-radius: 16px;
        --transition-speed: 0.3s;
    }
    
    /* Video Background Container */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080"><defs><linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:%230f0f1e;stop-opacity:1"/><stop offset="50%" style="stop-color:%231a1a2e;stop-opacity:1"/><stop offset="100%" style="stop-color:%2316213e;stop-opacity:1"/></linearGradient></defs><rect width="1920" height="1080" fill="url(%23grad1)"/></svg>') no-repeat center center fixed;
        background-size: cover;
    }
    
    /* Optimized Background - Remove expensive animation */
    .stApp {
        background: linear-gradient(-45deg, #0f0f1e, #1a1a2e, #16213e, #0f3460);
        font-family: 'Inter', sans-serif;
        position: relative;
    }
    
    /* Main Container Styling */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1200px;
        position: relative;
        z-index: 1;
    }
    
    /* Title Styling with Gradient - Optimized */
    h1 {
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        font-size: 3rem !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.02em;
        will-change: auto;
    }
    
    /* Subtitle Styling */
    .stApp > div > div > div > div > p {
        color: var(--text-secondary) !important;
        font-size: 1.1rem;
    }
    
    /* Chat Message Styling - Optimized for performance */
    .stChatMessage {
        background: var(--card-bg) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: var(--border-radius) !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        transition: transform var(--transition-speed) ease, box-shadow var(--transition-speed) ease;
        will-change: transform;
    }
    
    .stChatMessage:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);
    }
    
    /* User Message Specific Styling */
    .stChatMessage[data-testid*="user"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%) !important;
        backdrop-filter: blur(10px);
        border-left: 3px solid var(--accent-color);
    }
    
    /* Assistant Message Specific Styling */
    .stChatMessage[data-testid*="assistant"] {
        background: linear-gradient(135deg, rgba(75, 192, 200, 0.15) 0%, rgba(0, 242, 254, 0.15) 100%) !important;
        backdrop-filter: blur(10px);
        border-left: 3px solid #4facfe;
    }
    
    /* Chat Input Field - Optimized */
    .stChatInput {
        background: var(--card-bg) !important;
        backdrop-filter: blur(10px);
        border-radius: var(--border-radius) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: border-color var(--transition-speed) ease, transform var(--transition-speed) ease;
    }
    
    .stChatInput:focus-within {
        border-color: var(--accent-color) !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
        transform: translateY(-2px);
    }
    
    .stChatInput textarea {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
    }
    
    .stChatInput textarea::placeholder {
        color: var(--text-secondary) !important;
    }
    
    /* Sidebar Styling with Glassmorphism */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 15, 30, 0.95) 0%, rgba(26, 26, 46, 0.95) 100%) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    section[data-testid="stSidebar"] > div {
        padding: 2rem 1.5rem;
    }
    
    /* Sidebar Headers */
    section[data-testid="stSidebar"] h2 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
        margin-bottom: 1rem !important;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    section[data-testid="stSidebar"] h3 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
        margin-top: 1.5rem !important;
    }
    
    /* Info Box Styling */
    .stAlert {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: var(--border-radius) !important;
        color: var(--text-primary) !important;
        padding: 1.25rem !important;
        transition: transform var(--transition-speed) ease;
    }
    
    .stAlert:hover {
        transform: translateX(5px);
    }
    
    /* Markdown in Sidebar */
    section[data-testid="stSidebar"] .stMarkdown {
        color: var(--text-secondary) !important;
        line-height: 1.8;
        transition: color var(--transition-speed) ease, transform var(--transition-speed) ease;
    }
    
    section[data-testid="stSidebar"] .stMarkdown:hover {
        color: var(--text-primary) !important;
        transform: translateX(3px);
    }
    
    section[data-testid="stSidebar"] .stMarkdown li {
        margin: 0.75rem 0;
        padding-left: 0.5rem;
        transition: padding-left var(--transition-speed) ease;
    }
    
    section[data-testid="stSidebar"] .stMarkdown li:hover {
        padding-left: 1rem;
    }
    
    /* Divider Styling */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.5), transparent);
        margin: 1.5rem 0;
    }
    
    /* Button Styling - Optimized */
    .stButton button {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--border-radius) !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        transition: transform var(--transition-speed) ease, box-shadow var(--transition-speed) ease !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        cursor: pointer;
        width: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.5);
    }
    
    .stButton button:active {
        transform: translateY(0) scale(0.98);
    }
    
    /* Spinner/Loading - Simplified */
    .stSpinner > div {
        border-color: var(--accent-color) transparent transparent transparent !important;
    }
    
    /* Code Blocks */
    code {
        background: rgba(102, 126, 234, 0.15) !important;
        color: #4facfe !important;
        padding: 0.2rem 0.5rem !important;
        border-radius: 6px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.9rem !important;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #7c8fed 0%, #8b5fcf 100%);
    }
    
    /* Markdown Text Styling */
    .stMarkdown {
        color: var(--text-primary);
        line-height: 1.7;
    }
    
    .stMarkdown p {
        margin-bottom: 1rem;
    }
    
    .stMarkdown strong {
        color: #4facfe;
        font-weight: 600;
    }
    
    /* Success/Warning indicators */
    .stMarkdown li:has(✅) {
        color: var(--success-color) !important;
    }
    
    .stMarkdown li:has(❌) {
        color: var(--warning-color) !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        h1 {
            font-size: 2rem !important;
        }
        
        .stChatMessage {
            padding: 1rem !important;
        }
    }
    
    /* Reduce animations for better performance */
    @media (prefers-reduced-motion: reduce) {
        * {
            animation: none !important;
            transition: none !important;
        }
    }
    
    /* Performance optimization - Use GPU acceleration */
    .stChatMessage,
    .stButton button,
    .stChatInput {
        transform: translateZ(0);
        backface-visibility: hidden;
        perspective: 1000px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== VIDEO BACKGROUND HTML ====================
st.markdown("""
<div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -2; overflow: hidden;">
    <iframe 
        src="https://www.youtube.com/embed/bBC-nXj3Ng4?autoplay=1&mute=1&loop=1&playlist=bBC-nXj3Ng4&controls=0&showinfo=0&rel=0&modestbranding=1&vq=hd1080"
        style="position: absolute; top: 50%; left: 50%; width: 177.77777778vh; height: 56.25vw; min-height: 100%; min-width: 100%; transform: translate(-50%, -50%);"
        frameborder="0"
        allow="autoplay; encrypted-media"
        allowfullscreen>
    </iframe>
    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15, 15, 30, 0.85);"></div>
</div>
""", unsafe_allow_html=True)

# ==================== MAIN APP ====================

st.title("🪙 Crypto Knowledge Agent")
st.write("Strictly factual. Powered by Knowledge Base & FreeCryptoAPI.")

# Initialize Agent
if "agent" not in st.session_state:
    st.session_state.agent = CryptoAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask about a coin (e.g., 'Tell me about Solana')"):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Agent Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.agent.process_query(prompt)
            # Simulate typing feel
            time.sleep(0.3) 
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# ==================== SIDEBAR ====================
with st.sidebar:
    st.header("About")
    st.info(
        "This agent uses a **Knowledge-First** approach.\n"
        "It checks a local database first, then falls back to an API.\n"
        "It **rejects** speculation and investment advice."
    )
    st.divider()
    st.subheader("Capabilities")
    st.markdown("- ✅ Coin Metadata")
    st.markdown("- ✅ Live/Cached Prices")
    st.markdown("- ❌ Price Predictions")
    st.markdown("- ❌ Financial Advice")
    st.divider()
    if st.button("Clear History"):
        st.session_state.messages = []
        st.rerun()
