import streamlit as st
from utils.speech_handler import SpeechHandler

def render_voice_features():
    """Render the Voice Features page with all accessibility and collaboration features"""
    
    # Page header
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%); border-radius: 15px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0; font-size: 2.5rem;">🎙️ Voice Features & Accessibility</h1>
        <p style="color: white; margin: 0.5rem 0 0 0; font-size: 1.2rem;">Advanced voice navigation and multi-user collaboration</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize speech handler
    speech_handler = SpeechHandler()
    speech_handler.add_speech_synthesis_js()
    
    # Create tabs for different voice features
    tab1, tab2 = st.tabs(["🎙️ Voice Navigation", "🔊 Text-to-Speech"])
    
    with tab1:
        st.markdown("### 🎙️ Voice Navigation & Control")
        
        # Voice Navigation Panel
        speech_handler.render_voice_control_panel()
        
        # Voice command tutorial
        st.markdown("---")
        st.markdown("### 🎯 Voice Command Tutorial")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Navigation Commands
            - **"Go to dashboard"** - Navigate to main dashboard
            - **"Stock analysis"** - Open stock analysis page
            - **"Market overview"** - View market overview
            - **"News feed"** - Go to news section
            - **"Story mode"** - Start learning tutorial
            - **"Voice features"** - Return to this page
            """)
        
        with col2:
            st.markdown("""
            #### Control Commands
            - **"Dark mode"** - Switch to dark theme
            - **"Light mode"** - Switch to light theme
            - **"Colorblind mode"** - Toggle accessibility colors
            - **"Stop speaking"** - Stop text-to-speech
            - **"Help"** - Get voice command help
            """)
        
        # Voice recognition status
        st.markdown("### 🔍 Voice Recognition Status")
        status_placeholder = st.empty()
        
        # Add JavaScript for real-time status updates
        st.markdown("""
        <script>
        function updateVoiceStatus() {
            const statusDiv = document.querySelector('[data-testid="stEmpty"]');
            if (statusDiv && window.isListening !== undefined) {
                if (window.isListening) {
                    statusDiv.innerHTML = '<div style="color: #00FF00; font-weight: bold;">🎙️ Listening for commands...</div>';
                } else {
                    statusDiv.innerHTML = '<div style="color: #666;">🎙️ Voice recognition inactive</div>';
                }
            }
        }
        
        // Update status every second
        setInterval(updateVoiceStatus, 1000);
        </script>
        """, unsafe_allow_html=True)
        
        with status_placeholder.container():
            st.info("🎙️ Voice recognition inactive - Click 'Start Voice Navigation' to begin")
    
    with tab2:
        st.markdown("### 🔊 Text-to-Speech Features")
        
        # Content reading options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Read Current Page", type="primary"):
                st.markdown("""
                <script>
                if (window.readCurrentPageContent) {
                    window.readCurrentPageContent();
                } else {
                    window.speakText = window.speakText || function(text) {
                        const utterance = new SpeechSynthesisUtterance(text);
                        utterance.rate = 0.8;
                        utterance.pitch = 1;
                        utterance.volume = 1;
                        speechSynthesis.speak(utterance);
                    };
                    window.speakText("Reading voice features page. This page contains voice navigation controls, text to speech options, and multi-user collaboration features.");
                }
                </script>
                """, unsafe_allow_html=True)
                st.success("Reading page content...")
        
        with col2:
            if st.button("📰 Read Headlines"):
                st.markdown("""
                <script>
                if (window.readNewsHeadlines) {
                    window.readNewsHeadlines();
                } else {
                    window.speakText = window.speakText || function(text) {
                        const utterance = new SpeechSynthesisUtterance(text);
                        speechSynthesis.speak(utterance);
                    };
                    window.speakText("Currently viewing voice features page. Navigate to news feed to read headlines.");
                }
                </script>
                """, unsafe_allow_html=True)
                st.success("Reading headlines...")
        
        with col3:
            if st.button("📊 Read Market Data"):
                st.markdown("""
                <script>
                if (window.readMetrics) {
                    window.readMetrics();
                } else {
                    window.speakText = window.speakText || function(text) {
                        const utterance = new SpeechSynthesisUtterance(text);
                        speechSynthesis.speak(utterance);
                    };
                    window.speakText("Navigate to dashboard or market overview to hear market data and metrics.");
                }
                </script>
                """, unsafe_allow_html=True)
                st.success("Reading market data...")
        
        # Voice settings
        st.markdown("### ⚙️ Voice Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            voice_speed = st.slider("🎛️ Speech Speed", 0.5, 2.0, 0.8, 0.1)
            st.markdown(f"""
            <script>
            window.voiceSettings = window.voiceSettings || {{}};
            window.voiceSettings.rate = {voice_speed};
            </script>
            """, unsafe_allow_html=True)
        
        with col2:
            voice_pitch = st.slider("🎵 Voice Pitch", 0.5, 2.0, 1.0, 0.1)
            st.markdown(f"""
            <script>
            window.voiceSettings = window.voiceSettings || {{}};
            window.voiceSettings.pitch = {voice_pitch};
            </script>
            """, unsafe_allow_html=True)
        
        # Test voice settings
        if st.button("🎤 Test Voice Settings"):
            st.markdown(f"""
            <script>
            const utterance = new SpeechSynthesisUtterance("Hello! This is a test of your voice settings. Speed is {voice_speed} and pitch is {voice_pitch}.");
            utterance.rate = {voice_speed};
            utterance.pitch = {voice_pitch};
            speechSynthesis.speak(utterance);
            </script>
            """, unsafe_allow_html=True)
    

    
    # Accessibility information
    st.markdown("---")
    st.markdown("### ♿ Accessibility Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### Visual Accessibility
        - **High Contrast Mode** - Enhanced text visibility
        - **Colorblind Support** - Alternative color schemes
        - **Large Text Options** - Adjustable font sizes
        - **Screen Reader Support** - Compatible with assistive technology
        """)
    
    with col2:
        st.markdown("""
        #### Audio Accessibility
        - **Voice Navigation** - Navigate without mouse/keyboard
        - **Audio Feedback** - Spoken confirmation of actions
        - **Market Data Reading** - Hear live market updates
        - **Multi-language Support** - Indian English voice options
        """)
    
    with col3:
        st.markdown("""
        #### Keyboard Accessibility
        - **Ctrl+Shift+V** - Toggle voice recognition
        - **Ctrl+Shift+S** - Stop speaking
        - **Tab Navigation** - Navigate with keyboard
        - **Enter to Activate** - Use enter key for buttons
        """)
    
    # Footer with instructions
    st.markdown("---")
    st.info("""
    💡 **Getting Started:**
    1. Click "Start Voice Navigation" to enable voice commands
    2. Say "Go to dashboard" to navigate or "Read this page" to hear content
    3. Use "Dark mode" or "Light mode" to change themes
    4. Try "Help" for a full list of voice commands
    """)