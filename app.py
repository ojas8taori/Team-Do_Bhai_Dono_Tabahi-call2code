import streamlit as st
import os
import json
from datetime import datetime, time
import pytz
from streamlit_option_menu import option_menu

# Import custom components
from components.dashboard import render_dashboard
from components.stock_analysis import render_stock_analysis
from components.news_feed import render_news_feed
from components.market_overview import render_market_overview
from components.story_mode import render_story_mode
from components.error_handler import render_error_page
from utils.speech_handler import SpeechHandler

# Page configuration
st.set_page_config(
    page_title="Stonks GPT - Indian Stock Market Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS with theme support
def load_css():
    with open("styles/custom.css") as f:
        css_content = f.read()
        
    # Apply dark mode if enabled with ABSOLUTE FORCE
    if st.session_state.get('dark_mode', False):
        css_content += """
        /* ABSOLUTE DARK MODE - FORCE WHITE TEXT EVERYWHERE */
        html, body, .stApp, .stApp * {
            color: white !important;
        }
        
        .stApp {
            background: linear-gradient(135deg, #0f1419, #1a1f2e) !important;
        }
        
        .stSidebar {
            background: linear-gradient(180deg, #1e2139, #2a2d4a) !important;
            border-right: 2px solid #3d4465 !important;
        }
        
        /* FORCE EVERY SINGLE ELEMENT TO BE WHITE */
        * {
            color: white !important;
        }
        
        /* Override CSS variables for dark mode */
        :root {
            --text-primary: white !important;
            --text-secondary: white !important;
            --text-muted: white !important;
        }
        
        /* Enhanced text visibility with dark blue for better readability */
        .stMarkdown, .stMarkdown p, .stMarkdown div, .stText, .stCaption {
            color: #1e3a8a !important;
        }
        
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
            color: #1e40af !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Specific fixes for metric labels and values with smaller font sizes */
        .stMetric .metric-label, .stMetric label {
            color: #1e3a8a !important;
            font-size: 0.8rem !important;
        }
        
        .stMetric .metric-value, .stMetric [data-testid="metric-value"] {
            color: #1e40af !important;
            font-size: 1.2rem !important;
        }
        
        /* Fix for all text elements with smaller fonts */
        .stMarkdown *, .stText *, .stCaption * {
            color: #1e3a8a !important;
            font-size: 0.9rem !important;
        }
        
        /* Fix for sidebar text */
        .stSidebar .stMarkdown, .stSidebar .stMarkdown p, .stSidebar .stText {
            color: #1e3a8a !important;
        }
        
        /* Metric container adjustments for better fit */
        .stMetric {
            padding: 0.8rem !important;
        }
        
        .stMetric > div {
            padding: 0.5rem !important;
        }
        
        /* Form elements with gradient backgrounds */
        .stSelectbox > div > div, .stTextInput > div > div > input {
            background: linear-gradient(135deg, #2a2d4a, #363b5c) !important;
            border: 1px solid #4a5080 !important;
            color: #ffffff !important;
            border-radius: 8px !important;
        }
        
        .stSelectbox > div > div:hover, .stTextInput > div > div > input:hover {
            border-color: #FF8A65 !important;
            box-shadow: 0 0 10px rgba(255, 138, 101, 0.3) !important;
        }
        
        /* Colorful gradient buttons */
        .stButton > button {
            background: linear-gradient(135deg, #667eea, #764ba2) !important;
            border: none !important;
            color: #ffffff !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #764ba2, #667eea) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
        }
        
        /* Enhanced metric cards with gradients */
        .stMetric {
            background: linear-gradient(135deg, #2a2d4a, #363b5c) !important;
            border: 1px solid #4a5080 !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        }
        
        .stMetric:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 25px rgba(0,0,0,0.3) !important;
        }
        
        /* Enhanced sidebar elements */
        .stSidebar .stMarkdown, .stSidebar .stSelectbox label {
            color: #e8e9f3 !important;
        }
        
        /* Colorful header with Indian flag inspired gradients */
        .main-header {
            background: linear-gradient(135deg, #FF8A65, #FFB74D, #4CAF50) !important;
            box-shadow: 0 8px 32px rgba(255, 138, 101, 0.3) !important;
        }
        
        /* Enhanced chart containers */
        .stPlotlyChart {
            background: linear-gradient(135deg, #2a2d4a, #363b5c) !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        }
        
        /* Expander styling */
        .stExpander {
            background: linear-gradient(135deg, #2a2d4a, #363b5c) !important;
            border: 1px solid #4a5080 !important;
            border-radius: 10px !important;
        }
        
        .stExpander .streamlit-expanderHeader {
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            background: linear-gradient(135deg, #2a2d4a, #363b5c) !important;
            border-radius: 8px !important;
            padding: 0.5rem !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            color: #e8e9f3 !important;
            border-radius: 6px !important;
            margin: 0 0.25rem !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea, #764ba2) !important;
            color: #ffffff !important;
        }
        
        /* Alert boxes */
        .stAlert {
            background: linear-gradient(135deg, #2a2d4a, #363b5c) !important;
            border-left: 4px solid #FF8A65 !important;
            color: #e8e9f3 !important;
            border-radius: 8px !important;
        }
        
        /* Success/Error specific colors */
        .stSuccess {
            border-left-color: #4CAF50 !important;
            background: linear-gradient(135deg, rgba(76, 175, 80, 0.1), rgba(76, 175, 80, 0.05)) !important;
        }
        
        .stError {
            border-left-color: #F44336 !important;
            background: linear-gradient(135deg, rgba(244, 67, 54, 0.1), rgba(244, 67, 54, 0.05)) !important;
        }
        
        .stWarning {
            border-left-color: #FF9800 !important;
            background: linear-gradient(135deg, rgba(255, 152, 0, 0.1), rgba(255, 152, 0, 0.05)) !important;
        }
        
        .stInfo {
            border-left-color: #2196F3 !important;
            background: linear-gradient(135deg, rgba(33, 150, 243, 0.1), rgba(33, 150, 243, 0.05)) !important;
        }
        """
    
    # Apply accessibility mode if enabled
    if st.session_state.get('accessibility_mode', False):
        css_content += """
        /* Accessibility mode styles */
        .stApp {
            font-size: 120% !important;
        }
        button:focus,
        input:focus,
        select:focus {
            outline: 3px solid #FF6B35 !important;
            outline-offset: 2px !important;
        }
        .stButton > button {
            font-size: 1.2em !important;
            padding: 0.8rem 1.5rem !important;
        }
        """
    
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    
    # Add JavaScript to force white text in dark mode
    if st.session_state.get('dark_mode', False):
        st.markdown("""
        <script>
        function forceWhiteText() {
            // Set data-theme attribute
            document.documentElement.setAttribute('data-theme', 'dark');
            document.body.setAttribute('data-theme', 'dark');
            
            // Force all text to white
            const style = document.createElement('style');
            style.textContent = `
                * { color: white !important; }
                .stApp * { color: white !important; }
                .stMetric * { color: white !important; }
                [data-testid="metric-container"] * { color: white !important; }
                [data-testid="metric-label"] { color: white !important; }
                [data-testid="metric-value"] { color: white !important; }
                [data-testid="metric-delta"] { color: white !important; }
            `;
            document.head.appendChild(style);
        }
        
        // Execute immediately
        forceWhiteText();
        
        // Re-execute on DOM changes
        const observer = new MutationObserver(forceWhiteText);
        observer.observe(document.body, { childList: true, subtree: true });
        
        // Re-execute every 100ms to catch any new elements
        setInterval(forceWhiteText, 100);
        </script>
        """, unsafe_allow_html=True)

# Load translations
@st.cache_data
def load_translations():
    with open("assets/translations.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Initialize session state
def initialize_session_state():
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    if 'voice_enabled' not in st.session_state:
        st.session_state.voice_enabled = False
    if 'story_mode_completed' not in st.session_state:
        st.session_state.story_mode_completed = False
    if 'skip_story_mode' not in st.session_state:
        st.session_state.skip_story_mode = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Story Mode'  # Default to Story Mode
    if 'accessibility_mode' not in st.session_state:
        st.session_state.accessibility_mode = False
    if 'market_sentiment' not in st.session_state:
        st.session_state.market_sentiment = 'neutral'

# Check if Indian market is open
def is_market_open():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    market_open = time(9, 15)  # 9:15 AM IST
    market_close = time(15, 30)  # 3:30 PM IST
    
    # Check if it's a weekday and within market hours
    if now.weekday() < 5 and market_open <= now.time() <= market_close:
        return True
    return False

# Dynamic theming based on dark mode and market sentiment
def apply_dynamic_theme():
    # Apply dark mode styling
    if st.session_state.dark_mode:
        st.markdown("""
        <script>
        document.documentElement.setAttribute('data-theme', 'dark');
        document.body.setAttribute('data-theme', 'dark');
        </script>
        <style>
        [data-theme="dark"] .stApp {
            background-color: #0e1117 !important;
            color: #fafafa !important;
        }
        [data-theme="dark"] .stSidebar {
            background-color: #262730 !important;
            color: #fafafa !important;
        }
        [data-theme="dark"] .stSidebar .stMarkdown p,
        [data-theme="dark"] .stSidebar .stMarkdown div,
        [data-theme="dark"] .stSidebar .stSelectbox label,
        [data-theme="dark"] .stSidebar .stCheckbox label {
            color: #fafafa !important;
        }
        [data-theme="dark"] .stButton button {
            background-color: #262730 !important;
            color: #fafafa !important;
            border: 1px solid #3d3d3d !important;
        }
        [data-theme="dark"] .stMetric {
            background-color: #1a1a1a !important;
            color: #fafafa !important;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <script>
        document.documentElement.removeAttribute('data-theme');
        document.body.removeAttribute('data-theme');
        </script>
        """, unsafe_allow_html=True)
    
    # Apply market sentiment theming
    sentiment = st.session_state.get('market_sentiment', 'neutral')
    if sentiment == 'bullish':
        st.markdown("""
        <style>
        .stApp > header {
            background-color: rgba(0, 128, 0, 0.1);
        }
        .market-status {
            color: #008000;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
    elif sentiment == 'bearish':
        st.markdown("""
        <style>
        .stApp > header {
            background-color: rgba(255, 0, 0, 0.1);
        }
        .market-status {
            color: #FF0000;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

# Sidebar configuration
def render_sidebar():
    with st.sidebar:
        st.image("https://pixabay.com/get/g35fbce5c96bfc82f81ebd3b0dd126bc07f98f95195a0409c6340c1cff3dcef489ebd461493db15a6f672e6ee307940681dad1bb4cf241adeb3e81a7ba61e3c1b_1280.jpg", 
                 width=200, caption="Indian Stock Market")
        
        # Market status
        market_status = "🟢 Market Open" if is_market_open() else "🔴 Market Closed"
        st.markdown(f'<p class="market-status">{market_status}</p>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Settings
        st.subheader("⚙️ Settings")
        
        # Language selection
        languages = {'en': 'English', 'hi': 'हिंदी', 'mr': 'मराठी', 'gu': 'ગુજરાતી'}
        selected_lang = st.selectbox("Language / भाषा", 
                                   options=list(languages.keys()),
                                   format_func=lambda x: languages[x],
                                   index=list(languages.keys()).index(st.session_state.language))
        
        if selected_lang != st.session_state.language:
            st.session_state.language = selected_lang
            st.rerun()
        
        # Dark mode toggle
        dark_mode_new = st.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode)
        if dark_mode_new != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode_new
            st.rerun()
        
        # Accessibility features
        accessibility_new = st.checkbox("♿ Accessibility Mode", value=st.session_state.accessibility_mode)
        if accessibility_new != st.session_state.accessibility_mode:
            st.session_state.accessibility_mode = accessibility_new
            st.rerun()
        
        # Voice navigation
        voice_new = st.checkbox("🎤 Voice Navigation", value=st.session_state.voice_enabled)
        if voice_new != st.session_state.voice_enabled:
            st.session_state.voice_enabled = voice_new
            st.rerun()
        
        if st.session_state.voice_enabled:
            speech_handler = SpeechHandler()
            st.markdown("#### 🎤 Voice Commands")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🎙️ Listen", help="Click to start voice recognition"):
                    # Simple voice command interface
                    st.info("🎤 Say: 'dashboard', 'stock analysis', 'market overview', or 'news feed'")
                    
            with col2:
                if st.button("🔊 Read Page", help="Read current page content"):
                    st.info("🔊 Reading page content...")
            
            # Voice command suggestions
            st.markdown("""
            **Voice Commands:**
            - "Dashboard" - Go to main dashboard
            - "Stock Analysis" - Open stock analysis page  
            - "Market Overview" - View market overview
            - "News Feed" - Show news and analysis
            """)
            
            # Add improved voice navigation JavaScript
            voice_js = '''
            <script>
            let recognition = null;
            let isListening = false;
            
            function startVoiceRecognition() {
                if (isListening) return;
                
                if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                    recognition = new SpeechRecognition();
                    
                    recognition.continuous = false;
                    recognition.interimResults = false;
                    recognition.lang = 'en-IN';
                    
                    recognition.onstart = function() {
                        isListening = true;
                        console.log('Voice recognition started');
                    };
                    
                    recognition.onresult = function(event) {
                        const command = event.results[0][0].transcript.toLowerCase();
                        console.log('Voice command received:', command);
                        handleVoiceCommand(command);
                    };
                    
                    recognition.onerror = function(event) {
                        console.error('Speech recognition error:', event.error);
                        isListening = false;
                    };
                    
                    recognition.onend = function() {
                        isListening = false;
                        console.log('Voice recognition ended');
                    };
                    
                    recognition.start();
                } else {
                    alert('Voice recognition not supported in this browser');
                }
            }
            
            function handleVoiceCommand(command) {
                console.log('Processing voice command:', command);
                
                // Try to find and click the appropriate navigation menu item
                let targetButton = null;
                
                // Look for streamlit-option-menu buttons first
                const menuButtons = document.querySelectorAll('.streamlit-option-menu button, [data-testid="stSelectbox"] div, button[role="tab"]');
                
                for (let button of menuButtons) {
                    const text = button.textContent.toLowerCase();
                    
                    if (command.includes('dashboard') && text.includes('dashboard')) {
                        targetButton = button;
                        break;
                    } else if (command.includes('stock') && text.includes('stock')) {
                        targetButton = button;
                        break;
                    } else if (command.includes('market') && text.includes('market')) {
                        targetButton = button;
                        break;
                    } else if (command.includes('news') && text.includes('news')) {
                        targetButton = button;
                        break;
                    } else if (command.includes('story') && text.includes('story')) {
                        targetButton = button;
                        break;
                    }
                }
                
                if (targetButton) {
                    console.log('Clicking navigation button:', targetButton.textContent);
                    targetButton.click();
                } else {
                    console.log('No matching navigation found for command:', command);
                }
            }
            
            // Auto-start when Listen button is clicked
            document.addEventListener('click', function(e) {
                const buttonText = e.target.textContent || e.target.innerText || '';
                if (buttonText.includes('Listen') || buttonText.includes('🎙️')) {
                    console.log('Listen button clicked, starting voice recognition');
                    setTimeout(startVoiceRecognition, 200);
                }
            });
            
            // Also listen for button clicks in parent elements
            document.addEventListener('click', function(e) {
                const button = e.target.closest('button');
                if (button) {
                    const buttonText = button.textContent || button.innerText || '';
                    if (buttonText.includes('Listen') || buttonText.includes('🎙️')) {
                        console.log('Listen button parent clicked, starting voice recognition');
                        setTimeout(startVoiceRecognition, 200);
                    }
                }
            });
            </script>
            '''
            
            st.markdown(voice_js, unsafe_allow_html=True)
        
        st.markdown("---")

def main():
    # Initialize
    initialize_session_state()
    load_css()
    apply_dynamic_theme()
    
    # Load translations
    translations = load_translations()
    lang = st.session_state.language
    
    # Main header
    app_title = translations[lang]["app_title"]
    tagline = translations[lang]["tagline"]
    st.title(f"📈 {app_title}")
    st.markdown(f"*{tagline}*")
    
    # Check if user needs story mode (default behavior)
    if not st.session_state.story_mode_completed and not st.session_state.skip_story_mode:
        st.info("🎭 Welcome to Stonks GPT! We recommend starting with our interactive Story Mode to learn about Indian stock markets.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎭 Start Story Mode Tutorial", type="primary"):
                st.session_state.current_page = "Story Mode"
                st.rerun()
        with col2:
            if st.button("⏭️ Skip to Dashboard"):
                st.session_state.skip_story_mode = True
                st.session_state.current_page = "Dashboard"
                st.rerun()
    
    # Set default page based on story mode status
    if not st.session_state.story_mode_completed and not st.session_state.skip_story_mode:
        default_page = "Story Mode"
        default_index = 4  # Story Mode is at index 4
    else:
        default_page = st.session_state.get('current_page', 'Dashboard')
        default_index = 0
    
    # Navigation menu
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Stock Analysis", "Market Overview", "News Feed", "Story Mode"],
        icons=["speedometer2", "graph-up", "globe", "newspaper", "book"],
        menu_icon="cast",
        default_index=default_index,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "center",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#FF6B35"},
        }
    )
    
    # Update current page
    st.session_state.current_page = selected
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    try:
        if selected == "Dashboard":
            render_dashboard()
        elif selected == "Stock Analysis":
            render_stock_analysis()
        elif selected == "Market Overview":
            render_market_overview()
        elif selected == "News Feed":
            render_news_feed()
        elif selected == "Story Mode":
            render_story_mode()
    except Exception as e:
        st.error("⚠️ Application Error")
        render_error_page(str(e))
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>🇮🇳 Made with ❤️ for Indian Investors | Data from Yahoo Finance & Finnhub</p>
            <p>Market hours: 9:15 AM - 3:30 PM IST (Mon-Fri)</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
