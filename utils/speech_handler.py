import streamlit as st
import streamlit.components.v1 as components
import base64
from typing import Optional
import json

class SpeechHandler:
    def __init__(self):
        self.is_supported = True
        
    def add_speech_synthesis_js(self):
        """Add JavaScript for speech synthesis"""
        speech_js = """
        <script>
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
                
                window.speechSynthesis.speak(utterance);
                return true;
            }
            return false;
        }
        
        function stopSpeaking() {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
            }
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
