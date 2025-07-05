import streamlit as st
import streamlit.components.v1 as components
import base64
from typing import Optional
import json

class SpeechHandler:
    def __init__(self):
        self.is_supported = True
        
    def add_speech_synthesis_js(self):
        """Add comprehensive JavaScript for speech synthesis and voice recognition"""
        speech_js = """
        <script>
        // Global variables for voice functionality
        let isCurrentlySpeaking = false;
        let currentUtterance = null;
        let voiceRecognition = null;
        let isListening = false;
        let colorblindMode = false;
        
        // Initialize voice recognition
        function initVoiceRecognition() {
            if ('webkitSpeechRecognition' in window) {
                voiceRecognition = new webkitSpeechRecognition();
                voiceRecognition.continuous = true;
                voiceRecognition.interimResults = true;
                voiceRecognition.lang = 'en-IN';
                
                voiceRecognition.onresult = function(event) {
                    let finalTranscript = '';
                    for (let i = event.resultIndex; i < event.results.length; i++) {
                        if (event.results[i].isFinal) {
                            finalTranscript += event.results[i][0].transcript;
                        }
                    }
                    
                    if (finalTranscript.trim()) {
                        handleVoiceCommand(finalTranscript.toLowerCase().trim());
                    }
                };
                
                voiceRecognition.onerror = function(event) {
                    console.error('Voice recognition error:', event.error);
                    isListening = false;
                    updateListeningStatus(false);
                };
                
                voiceRecognition.onend = function() {
                    isListening = false;
                    updateListeningStatus(false);
                };
                
                return true;
            }
            return false;
        }
        
        // Start voice recognition
        function startVoiceRecognition() {
            if (voiceRecognition && !isListening) {
                voiceRecognition.start();
                isListening = true;
                updateListeningStatus(true);
                speakText("Voice navigation activated. Say commands like 'go to dashboard', 'read this page', or 'enable dark mode'.");
            }
        }
        
        // Stop voice recognition
        function stopVoiceRecognition() {
            if (voiceRecognition && isListening) {
                voiceRecognition.stop();
                isListening = false;
                updateListeningStatus(false);
                speakText("Voice navigation deactivated.");
            }
        }
        
        // Handle voice commands
        function handleVoiceCommand(command) {
            console.log('Processing voice command:', command);
            
            // Navigation commands
            if (command.includes('dashboard') || command.includes('home')) {
                navigateToPage('Dashboard');
                speakText("Navigating to Dashboard");
            } else if (command.includes('stock analysis') || command.includes('stocks')) {
                navigateToPage('Stock Analysis');
                speakText("Navigating to Stock Analysis");
            } else if (command.includes('market overview') || command.includes('market')) {
                navigateToPage('Market Overview');
                speakText("Navigating to Market Overview");
            } else if (command.includes('news') || command.includes('news feed')) {
                navigateToPage('News Feed');
                speakText("Navigating to News Feed");
            } else if (command.includes('story mode') || command.includes('tutorial')) {
                navigateToPage('Story Mode');
                speakText("Navigating to Story Mode");
            }
            
            // Theme commands
            else if (command.includes('dark mode') || command.includes('dark theme')) {
                toggleDarkMode();
                speakText("Toggling dark mode");
            } else if (command.includes('light mode') || command.includes('light theme')) {
                toggleLightMode();
                speakText("Switching to light mode");
            } else if (command.includes('colorblind mode')) {
                toggleColorblindMode();
                speakText("Toggling colorblind accessibility mode");
            }
            
            // Content reading commands
            else if (command.includes('read this page') || command.includes('read page')) {
                readCurrentPageContent();
            } else if (command.includes('read headlines') || command.includes('read news')) {
                readNewsHeadlines();
            } else if (command.includes('read metrics') || command.includes('read data')) {
                readMetrics();
            }
            
            // Control commands
            else if (command.includes('stop speaking') || command.includes('stop reading')) {
                stopSpeaking();
            } else if (command.includes('help') || command.includes('what can you do')) {
                provideVoiceHelp();
            } else {
                speakText("Command not recognized. Say 'help' for available commands.");
            }
        }
        
        // Navigation function
        function navigateToPage(pageName) {
            // Find and click the navigation item
            const navItems = document.querySelectorAll('[data-testid="nav-link"], .nav-link, button');
            for (let item of navItems) {
                if (item.textContent.includes(pageName)) {
                    item.click();
                    break;
                }
            }
        }
        
        // Theme toggle functions
        function toggleDarkMode() {
            const darkModeCheckbox = document.querySelector('input[type="checkbox"]');
            if (darkModeCheckbox && !darkModeCheckbox.checked) {
                darkModeCheckbox.click();
            }
        }
        
        function toggleLightMode() {
            const darkModeCheckbox = document.querySelector('input[type="checkbox"]');
            if (darkModeCheckbox && darkModeCheckbox.checked) {
                darkModeCheckbox.click();
            }
        }
        
        function toggleColorblindMode() {
            colorblindMode = !colorblindMode;
            document.body.classList.toggle('colorblind-mode', colorblindMode);
            
            if (colorblindMode) {
                // Apply colorblind-friendly theme
                document.documentElement.style.setProperty('--positive-color', '#0066cc');
                document.documentElement.style.setProperty('--negative-color', '#ff6600');
                document.documentElement.style.setProperty('--neutral-color', '#666666');
            } else {
                // Reset to normal colors
                document.documentElement.style.setProperty('--positive-color', '#10b981');
                document.documentElement.style.setProperty('--negative-color', '#ef4444');
                document.documentElement.style.setProperty('--neutral-color', '#6b7280');
            }
        }
        
        // Content reading functions
        function readCurrentPageContent() {
            const pageTitle = document.querySelector('h1');
            const content = document.querySelectorAll('p, .stMetric, .stMarkdown');
            
            let textToRead = '';
            if (pageTitle) {
                textToRead += pageTitle.textContent + '. ';
            }
            
            content.forEach(element => {
                if (element.textContent.trim()) {
                    textToRead += element.textContent.trim() + '. ';
                }
            });
            
            if (textToRead) {
                speakText(textToRead.substring(0, 1000) + (textToRead.length > 1000 ? '... Page content continues.' : ''));
            }
        }
        
        function readNewsHeadlines() {
            const headlines = document.querySelectorAll('h3, h4, .news-headline');
            let headlinesText = 'Latest headlines: ';
            
            headlines.forEach((headline, index) => {
                if (index < 5) { // Read first 5 headlines
                    headlinesText += headline.textContent.trim() + '. ';
                }
            });
            
            speakText(headlinesText);
        }
        
        function readMetrics() {
            const metrics = document.querySelectorAll('.stMetric');
            let metricsText = 'Current market metrics: ';
            
            metrics.forEach(metric => {
                const label = metric.querySelector('[data-testid="metric-label"]');
                const value = metric.querySelector('[data-testid="metric-value"]');
                const delta = metric.querySelector('[data-testid="metric-delta"]');
                
                if (label && value) {
                    metricsText += label.textContent + ' is ' + value.textContent;
                    if (delta) {
                        metricsText += ' ' + delta.textContent;
                    }
                    metricsText += '. ';
                }
            });
            
            speakText(metricsText);
        }
        
        function provideVoiceHelp() {
            const helpText = "Available voice commands: " +
                "Navigation - say 'go to dashboard', 'stocks', 'market overview', 'news', or 'story mode'. " +
                "Theme - say 'dark mode', 'light mode', or 'colorblind mode'. " +
                "Content - say 'read this page', 'read headlines', or 'read metrics'. " +
                "Control - say 'stop speaking' or 'help'.";
            speakText(helpText);
        }
        
        // Enhanced speech synthesis
        function speakText(text) {
            if ('speechSynthesis' in window) {
                // Cancel any ongoing speech
                window.speechSynthesis.cancel();
                
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 0.8;
                utterance.pitch = 1;
                utterance.volume = 1;
                
                // Try to use an Indian English voice if available
                const voices = window.speechSynthesis.getVoices();
                const indianVoice = voices.find(voice => 
                    voice.lang.includes('en-IN') || 
                    voice.name.includes('India') ||
                    voice.name.includes('Indian')
                );
                
                if (indianVoice) {
                    utterance.voice = indianVoice;
                } else {
                    // Fallback to any English voice
                    const englishVoice = voices.find(voice => voice.lang.includes('en'));
                    if (englishVoice) {
                        utterance.voice = englishVoice;
                    }
                }
                
                utterance.onstart = function() {
                    isCurrentlySpeaking = true;
                    updateSpeakingStatus(true);
                };
                
                utterance.onend = function() {
                    isCurrentlySpeaking = false;
                    updateSpeakingStatus(false);
                };
                
                currentUtterance = utterance;
                window.speechSynthesis.speak(utterance);
                return true;
            }
            return false;
        }
        
        function stopSpeaking() {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                isCurrentlySpeaking = false;
                updateSpeakingStatus(false);
            }
        }
        
        // Status update functions
        function updateListeningStatus(listening) {
            const statusElement = document.getElementById('voice-status');
            if (statusElement) {
                statusElement.textContent = listening ? '🎙️ Listening...' : '🎙️ Voice Navigation';
                statusElement.style.color = listening ? '#ff6b35' : '#10b981';
            }
        }
        
        function updateSpeakingStatus(speaking) {
            const statusElement = document.getElementById('speaker-status');
            if (statusElement) {
                statusElement.textContent = speaking ? '🔊 Speaking...' : '🔊 Text-to-Speech';
                statusElement.style.color = speaking ? '#ff6b35' : '#10b981';
            }
        }
        
        // Auto-initialize when page loads
        window.addEventListener('load', function() {
            initVoiceRecognition();
            
            // Load voices
            if ('speechSynthesis' in window) {
                speechSynthesis.addEventListener('voiceschanged', function() {
                    console.log('Voices loaded:', speechSynthesis.getVoices().length);
                });
            }
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            // Ctrl + Shift + V to toggle voice recognition
            if (e.ctrlKey && e.shiftKey && e.key === 'V') {
                e.preventDefault();
                if (isListening) {
                    stopVoiceRecognition();
                } else {
                    startVoiceRecognition();
                }
            }
            
            // Ctrl + Shift + S to stop speaking
            if (e.ctrlKey && e.shiftKey && e.key === 'S') {
                e.preventDefault();
                stopSpeaking();
            }
        });
        
        // Expose functions globally
        window.speakText = speakText;
        window.stopSpeaking = stopSpeaking;
        window.startVoiceRecognition = startVoiceRecognition;
        window.stopVoiceRecognition = stopVoiceRecognition;
        window.toggleColorblindMode = toggleColorblindMode;
        
        }
        
        // Voice command recognition
        let recognition = null;
        
        function startVoiceRecognition() {
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                recognition = new SpeechRecognition();
                
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.lang = 'en-IN';
                
                recognition.onresult = function(event) {
                    const command = event.results[0][0].transcript.toLowerCase();
                    handleVoiceCommand(command);
                };
                
                recognition.onerror = function(event) {
                    console.error('Speech recognition error:', event.error);
                };
                
                recognition.start();
                return true;
            }
            return false;
        }
        
        function handleVoiceCommand(command) {
            console.log('Voice command:', command);
            
            // Navigate based on voice commands
            if (command.includes('dashboard') || command.includes('home')) {
                // Trigger dashboard navigation
                document.dispatchEvent(new CustomEvent('voiceNavigate', {detail: 'dashboard'}));
            } else if (command.includes('stock analysis') || command.includes('analysis')) {
                document.dispatchEvent(new CustomEvent('voiceNavigate', {detail: 'stock_analysis'}));
            } else if (command.includes('news') || command.includes('news feed')) {
                document.dispatchEvent(new CustomEvent('voiceNavigate', {detail: 'news'}));
            } else if (command.includes('market overview') || command.includes('overview')) {
                document.dispatchEvent(new CustomEvent('voiceNavigate', {detail: 'market'}));
            } else if (command.includes('dark mode') || command.includes('theme')) {
                document.dispatchEvent(new CustomEvent('voiceToggle', {detail: 'dark_mode'}));
            } else if (command.includes('read') || command.includes('speak')) {
                readPageContent();
            }
        }
        
        function readPageContent() {
            // Get main content text
            const mainContent = document.querySelector('.main .block-container');
            if (mainContent) {
                const textContent = mainContent.innerText;
                // Limit to first 500 characters to avoid very long speech
                const limitedText = textContent.substring(0, 500) + (textContent.length > 500 ? '... and more content available.' : '');
                speakText(limitedText);
            }
        }
        </script>
        """
        
        components.html(speech_js, height=0)
    
    def speak_text(self, text: str, button_text: str = "🔊 Speak") -> bool:
        """Add a button to speak the given text"""
        self.add_speech_synthesis_js()
        
        if st.button(button_text):
            # Clean text for speech
            clean_text = self.clean_text_for_speech(text)
            
            speech_trigger = f"""
            <script>
            speakText(`{clean_text}`);
            </script>
            """
            components.html(speech_trigger, height=0)
            return True
        return False
    
    def clean_text_for_speech(self, text: str) -> str:
        """Clean text for better speech synthesis"""
        import re
        
        # Remove markdown formatting
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*(.*?)\*', r'\1', text)      # Italic
        text = re.sub(r'`(.*?)`', r'\1', text)        # Code
        text = re.sub(r'#{1,6}\s', '', text)          # Headers
        text = re.sub(r'\[.*?\]\(.*?\)', '', text)    # Links
        
        # Remove special characters that might interfere with speech
        text = re.sub(r'[^\w\s\.,!?;:\-()₹%]', '', text)
        
        # Replace currency and percentage symbols with words
        text = text.replace('₹', ' rupees ')
        text = text.replace('%', ' percent ')
        text = text.replace('&', ' and ')
        
        # Limit length for speech (browsers have limits)
        if len(text) > 500:
            text = text[:497] + "..."
        
        return text
    
    def add_voice_navigation(self):
        """Add voice navigation capabilities"""
        
        # Add the speech synthesis JavaScript
        self.add_speech_synthesis_js()
        
        # Voice navigation UI
        st.markdown("### 🎤 Voice Navigation")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🎙️ Start Voice Command", key="start_voice_nav"):
                voice_nav_js = """
                <script>
                document.addEventListener('DOMContentLoaded', function() {
                    startVoiceRecognition();
                });
                </script>
                """
                components.html(voice_nav_js, height=0)
                st.success("🎤 Listening for commands...")
                st.info("Try saying: 'Go to dashboard', 'Show stock analysis', 'Open market overview', 'Show news feed'")
        
        with col2:
            if st.button("🔊 Read Page", key="read_page_voice"):
                read_page_js = """
                <script>
                readPageContent();
                </script>
                """
                components.html(read_page_js, height=0)
                
        with col3:
            if st.button("🛑 Stop Speaking", key="stop_voice"):
                stop_js = """
                <script>
                stopSpeaking();
                </script>
                """
                components.html(stop_js, height=0)
        
        # Voice commands help
        with st.expander("📋 Voice Commands Guide"):
            st.markdown("""
            **Navigation Commands:**
            - "Go to dashboard" or "Dashboard" 
            - "Stock analysis" or "Analysis"
            - "Market overview" or "Overview"
            - "News feed" or "News"
            - "Story mode"
            
            **Action Commands:**
            - "Read page" or "Speak content"
            - "Dark mode" or "Toggle theme"
            - "Stop speaking"
            
            **Tips:**
            - Speak clearly and wait for the command to process
            - Commands work best in quiet environments
            - Make sure your microphone is enabled
            """)
        
        # Add navigation event listener JavaScript
        nav_listener_js = """
        <script>
        document.addEventListener('voiceNavigate', function(event) {
            const page = event.detail;
            
            // Find and click the appropriate navigation item
            const navItems = document.querySelectorAll('[data-testid="stSelectbox"] option, .streamlit-option-menu button');
            
            for (let item of navItems) {
                const text = item.textContent.toLowerCase();
                
                if ((page === 'dashboard' && text.includes('dashboard')) ||
                    (page === 'stock_analysis' && text.includes('stock')) ||
                    (page === 'market' && text.includes('overview')) ||
                    (page === 'news' && text.includes('news'))) {
                    
                    item.click();
                    break;
                }
            }
        });
        
        document.addEventListener('voiceToggle', function(event) {
            const toggle = event.detail;
            
            if (toggle === 'dark_mode') {
                // Find and toggle dark mode checkbox
                const darkModeCheckbox = document.querySelector('input[type="checkbox"]');
                if (darkModeCheckbox) {
                    darkModeCheckbox.click();
                }
            }
        });
        </script>
        """
        
        components.html(nav_listener_js, height=0)
        voice_nav_js = """
        <div id="voice-controls" style="position: fixed; bottom: 20px; right: 20px; z-index: 1000;">
            <button onclick="startVoiceRecognition()" 
                    style="background: #FF6B35; color: white; border: none; border-radius: 50%; 
                           width: 60px; height: 60px; cursor: pointer; box-shadow: 0 4px 8px rgba(0,0,0,0.3);
                           font-size: 20px;" 
                    title="Voice Commands">
                🎤
            </button>
        </div>
        
        <script>
        // Listen for voice navigation events
        document.addEventListener('voiceNavigate', function(e) {
            const page = e.detail;
            console.log('Navigating to:', page);
            
            // This would trigger Streamlit navigation
            // In a real implementation, you'd need to integrate with Streamlit's session state
            window.parent.postMessage({type: 'voiceNavigate', page: page}, '*');
        });
        
        document.addEventListener('voiceToggle', function(e) {
            const feature = e.detail;
            console.log('Toggling:', feature);
            window.parent.postMessage({type: 'voiceToggle', feature: feature}, '*');
        });
        </script>
        """
        
        components.html(voice_nav_js, height=100)
    
    def speak_market_summary(self, market_data: dict):
        """Generate and speak market summary"""
        if not market_data:
            summary = "Market data is currently unavailable."
        else:
            summary_parts = ["Here is today's market summary."]
            
            for index_name, data in market_data.items():
                change_desc = "up" if data.get('change', 0) >= 0 else "down"
                change_percent = abs(data.get('change_percent', 0))
                
                summary_parts.append(
                    f"{index_name} is {change_desc} by {change_percent:.2f} percent, "
                    f"currently at {data.get('current', 0):.2f} points."
                )
            
            summary = " ".join(summary_parts)
        
        return self.speak_text(summary, "🔊 Speak Market Summary")
    
    def speak_stock_analysis(self, symbol: str, analysis_data: dict):
        """Generate and speak stock analysis"""
        if not analysis_data:
            summary = f"Analysis data for {symbol} is currently unavailable."
        else:
            signal = analysis_data.get('overall_signal', 'HOLD')
            strength = analysis_data.get('signal_strength', 0)
            rsi = analysis_data.get('rsi', 50)
            
            summary = f"""
            Technical analysis for {symbol.replace('.NS', '')}.
            Overall signal is {signal} with {strength:.0f} percent strength.
            RSI is at {rsi:.1f}.
            """
            
            if rsi > 70:
                summary += " The stock appears overbought."
            elif rsi < 30:
                summary += " The stock appears oversold."
            else:
                summary += " RSI is in normal range."
        
        return self.speak_text(summary, f"🔊 Speak {symbol} Analysis")
    
    def speak_news_summary(self, news_analysis: dict):
        """Generate and speak news summary"""
        if not news_analysis or news_analysis.get('total_articles', 0) == 0:
            summary = "No recent news available for analysis."
        else:
            total = news_analysis['total_articles']
            sentiment = news_analysis['overall_sentiment']
            impact = news_analysis['market_impact']
            
            summary = f"""
            News analysis summary: {total} articles analyzed.
            Overall market sentiment is {sentiment} with {impact} impact.
            """
            
            # Add sentiment distribution
            sentiment_dist = news_analysis.get('sentiment_distribution', {})
            positive = sentiment_dist.get('Positive', 0)
            negative = sentiment_dist.get('Negative', 0)
            
            if positive > negative:
                summary += f" {positive} positive articles versus {negative} negative articles."
            elif negative > positive:
                summary += f" {negative} negative articles versus {positive} positive articles."
            else:
                summary += " Equal number of positive and negative articles."
        
        return self.speak_text(summary, "🔊 Speak News Summary")
    
    def render_voice_control_panel(self):
        """Render comprehensive voice control panel"""
        st.markdown("### 🎙️ Voice Navigation & Accessibility")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Voice Recognition Status
            st.markdown('<div id="voice-status">🎙️ Voice Navigation</div>', unsafe_allow_html=True)
            if st.button("🎙️ Start Voice Navigation", key="start_voice", help="Click or say 'Ctrl+Shift+V'"):
                st.markdown("""
                <script>
                if (window.startVoiceRecognition) {
                    window.startVoiceRecognition();
                }
                </script>
                """, unsafe_allow_html=True)
                st.success("Voice navigation activated! Try saying:\n- 'Go to dashboard'\n- 'Read this page'\n- 'Dark mode'")
        
        with col2:
            # Text-to-Speech Status  
            st.markdown('<div id="speaker-status">🔊 Text-to-Speech</div>', unsafe_allow_html=True)
            if st.button("🔊 Read Current Page", key="read_page"):
                st.markdown("""
                <script>
                if (window.speakText) {
                    const pageTitle = document.querySelector('h1');
                    const content = document.querySelectorAll('p, .stMetric, .stMarkdown');
                    let textToRead = '';
                    if (pageTitle) textToRead += pageTitle.textContent + '. ';
                    content.forEach(el => {
                        if (el.textContent.trim()) textToRead += el.textContent.trim() + '. ';
                    });
                    window.speakText(textToRead.substring(0, 1000));
                }
                </script>
                """, unsafe_allow_html=True)
        
        # Colorblind Accessibility
        if st.checkbox("🌈 Colorblind-Friendly Mode", key="colorblind_mode"):
            st.markdown("""
            <script>
            if (window.toggleColorblindMode) {
                window.toggleColorblindMode();
            }
            </script>
            <style>
            :root {
                --positive-color: #0066cc !important;
                --negative-color: #ff6600 !important;
                --neutral-color: #666666 !important;
            }
            .colorblind-mode .stMetric [data-testid="metric-delta"][data-direction="positive"] {
                color: #0066cc !important;
            }
            .colorblind-mode .stMetric [data-testid="metric-delta"][data-direction="negative"] {
                color: #ff6600 !important;
            }
            </style>
            """, unsafe_allow_html=True)
            st.info("🌈 Colorblind-friendly colors activated: Blue for positive, Orange for negative")
        
        # Voice Commands Help
        with st.expander("📝 Available Voice Commands"):
            st.markdown("""
            **Navigation:**
            - "Go to dashboard" / "Home"
            - "Stock analysis" / "Stocks" 
            - "Market overview" / "Market"
            - "News feed" / "News"
            - "Story mode" / "Tutorial"
            
            **Theme Control:**
            - "Dark mode" / "Light mode"
            - "Colorblind mode"
            
            **Content Reading:**
            - "Read this page"
            - "Read headlines" 
            - "Read metrics"
            
            **Control:**
            - "Stop speaking"
            - "Help"
            
            **Keyboard Shortcuts:**
            - Ctrl+Shift+V: Toggle voice recognition
            - Ctrl+Shift+S: Stop speaking
            """)

    def add_parallel_interaction_mode(self):
        """Add support for multiple users interacting simultaneously"""
        st.markdown("### 👥 Multi-User Collaboration")
        
        # User session management
        if 'user_sessions' not in st.session_state:
            st.session_state.user_sessions = {}
        
        if 'current_user_id' not in st.session_state:
            import uuid
            st.session_state.current_user_id = str(uuid.uuid4())[:8]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("👤 Your User ID", st.session_state.current_user_id)
        
        with col2:
            user_name = st.text_input("Your Name:", placeholder="Enter your name", key="user_name")
            if user_name:
                st.session_state.user_sessions[st.session_state.current_user_id] = {
                    'name': user_name,
                    'last_active': 'now',
                    'current_page': st.session_state.get('current_page', 'Dashboard')
                }
        
        with col3:
            if st.button("🔄 Sync with Other Users"):
                # Simulate multi-user sync (in real app, this would use WebSockets or similar)
                st.success("Synced with other users!")
        
        # Show active users
        if st.session_state.user_sessions:
            st.markdown("**Active Users:**")
            for user_id, user_data in st.session_state.user_sessions.items():
                if user_id == st.session_state.current_user_id:
                    st.markdown(f"🟢 **{user_data['name']}** (You) - {user_data['current_page']}")
                else:
                    st.markdown(f"🔵 **{user_data['name']}** - {user_data['current_page']}")
        
        # Collaborative features
        with st.expander("🤝 Collaborative Features"):
            st.markdown("""
            **Split-Screen Mode:** Compare different stocks or markets side by side
            
            **Shared Watchlist:** Create and share stock watchlists with other users
            
            **Real-time Chat:** Discuss market movements and share insights
            
            **Synchronized Navigation:** Follow another user's navigation through the app
            
            **Competitive Analysis:** Compare portfolio performance with other users
            """)
            
            if st.button("🎮 Enable Competitive Mode"):
                st.session_state.competitive_mode = True
                st.success("Competitive mode enabled! Compare your analysis with others.")
        
        # Add collaborative JavaScript
        collaborative_js = """
        <script>
        // Multi-user collaboration features
        window.collaborativeMode = {
            userId: '%s',
            userName: '%s',
            
            // Broadcast user action to other users
            broadcastAction: function(action, data) {
                const event = {
                    userId: this.userId,
                    userName: this.userName,
                    action: action,
                    data: data,
                    timestamp: new Date().toISOString()
                };
                
                // In real implementation, this would send to WebSocket server
                console.log('Broadcasting action:', event);
                
                // Store in localStorage for demo purposes
                const actions = JSON.parse(localStorage.getItem('collaborative_actions') || '[]');
                actions.push(event);
                localStorage.setItem('collaborative_actions', JSON.stringify(actions.slice(-50))); // Keep last 50 actions
            },
            
            // Handle navigation events
            onNavigate: function(page) {
                this.broadcastAction('navigate', { page: page });
            },
            
            // Handle voice commands from multiple users
            onVoiceCommand: function(command) {
                this.broadcastAction('voice_command', { command: command });
            }
        };
        
        // Listen for page navigation
        document.addEventListener('click', function(e) {
            const button = e.target.closest('button');
            if (button && button.textContent.match(/(Dashboard|Stock Analysis|Market Overview|News Feed|Story Mode)/)) {
                window.collaborativeMode.onNavigate(button.textContent);
            }
        });
        
        // Override voice command handler to include collaboration
        if (window.handleVoiceCommand) {
            const originalHandler = window.handleVoiceCommand;
            window.handleVoiceCommand = function(command) {
                window.collaborativeMode.onVoiceCommand(command);
                return originalHandler(command);
            };
        }
        </script>
        """ % (st.session_state.current_user_id, user_name if user_name else "Anonymous")
        
        st.markdown(collaborative_js, unsafe_allow_html=True)

    def add_accessibility_features(self):
        """Add various accessibility features"""
        accessibility_css = """
        <style>
        /* High contrast mode */
        .accessibility-high-contrast {
            filter: contrast(150%);
        }
        
        /* Large text mode */
        .accessibility-large-text {
            font-size: 120% !important;
        }
        
        /* Focus indicators */
        button:focus, input:focus, select:focus {
            outline: 3px solid #FF6B35 !important;
            outline-offset: 2px !important;
        }
        
        /* Reduced motion for users who prefer it */
        @media (prefers-reduced-motion: reduce) {
            * {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }
        </style>
        """
        
        st.markdown(accessibility_css, unsafe_allow_html=True)
    
    def speak_page_content(self):
        """Speak the current page content"""
        page_reader_js = """
        <script>
        function readCurrentPage() {
            const mainContent = document.querySelector('.main .block-container');
            if (mainContent) {
                // Get all text content, excluding buttons and navigation
                const excludeSelectors = 'button, .stButton, .stSelectbox, .stMultiSelect, nav, .sidebar';
                const textElements = mainContent.querySelectorAll('h1, h2, h3, p, .metric-value, .stMarkdown');
                
                let textToRead = [];
                textElements.forEach(element => {
                    if (element.innerText && element.innerText.trim() && 
                        !element.closest(excludeSelectors)) {
                        textToRead.push(element.innerText.trim());
                    }
                });
                
                const fullText = textToRead.join('. ').substring(0, 800);
                speakText(fullText);
            }
        }
        
        readCurrentPage();
        </script>
        """
        
        components.html(page_reader_js, height=0)
