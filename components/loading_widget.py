"""
Custom loading widget with market facts
"""

import streamlit as st
import time
import random
from utils.market_facts import MarketFacts

class LoadingWidget:
    def __init__(self):
        self.market_facts = MarketFacts()
    
    def show_loading_with_facts(self, context="general", duration=2):
        """Show loading spinner with market facts"""
        loading_message = self.market_facts.get_loading_message(context)
        
        # Create a placeholder for the loading content
        loading_container = st.empty()
        
        with loading_container.container():
            # Custom loading animation with facts
            st.markdown(f"""
            <div style='text-align: center; padding: 2rem; 
                        background: linear-gradient(135deg, rgba(255, 107, 53, 0.1), rgba(52, 152, 219, 0.1));
                        border-radius: 15px; border: 2px solid rgba(255, 107, 53, 0.3);'>
                <div style='display: flex; justify-content: center; align-items: center; margin-bottom: 1rem;'>
                    <div class='loading-spinner'></div>
                </div>
                <div style='color: var(--text-primary); font-size: 1rem; margin-bottom: 1rem;'>
                    {loading_message.split('💡')[0].strip()}
                </div>
                <div style='background: rgba(255, 107, 53, 0.1); padding: 1rem; border-radius: 10px; 
                            border-left: 4px solid #FF6B35; text-align: left;'>
                    <strong>💡 Did you know?</strong><br>
                    <span style='color: var(--text-secondary); font-size: 0.9rem;'>
                        {loading_message.split('💡')[1].strip() if '💡' in loading_message else self.market_facts.get_random_fact()}
                    </span>
                </div>
            </div>
            
            <style>
            .loading-spinner {{
                border: 3px solid rgba(255, 107, 53, 0.3);
                border-top: 3px solid #FF6B35;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
            }}
            
            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
            </style>
            """, unsafe_allow_html=True)
        
        # Wait for the specified duration
        time.sleep(duration)
        
        # Clear the loading widget
        loading_container.empty()
    
    def show_sentiment_based_alert(self, sentiment, message, value=None):
        """Show alert with sentiment-based styling"""
        styling = self.market_facts.get_sentiment_based_styling(sentiment, value)
        
        st.markdown(f"""
        <div style='background: {styling["background"]}; 
                    padding: 1rem; border-radius: 10px; margin: 1rem 0;
                    border: 2px solid {styling["border_color"]}; color: {styling["text_color"]};
                    box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
            <div style='display: flex; align-items: center; gap: 0.5rem;'>
                <span style='font-size: 1.2rem;'>{styling["emoji"]}</span>
                <span style='font-weight: bold; font-size: 1rem;'>{message}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def show_market_status_with_sentiment(self, market_data):
        """Show market status with dynamic theming based on overall sentiment"""
        if not market_data:
            return
        
        # Calculate overall market sentiment
        total_change = sum(data.get('change_percent', 0) for data in market_data.values())
        avg_change = total_change / len(market_data) if market_data else 0
        
        if avg_change > 0.5:
            sentiment = "bullish"
            status_text = f"Markets are UP by {avg_change:.2f}% on average"
        elif avg_change < -0.5:
            sentiment = "bearish"
            status_text = f"Markets are DOWN by {abs(avg_change):.2f}% on average"
        else:
            sentiment = "neutral"
            status_text = f"Markets are FLAT with {avg_change:.2f}% average change"
        
        self.show_sentiment_based_alert(sentiment, status_text, avg_change)
    
    def show_stock_analysis_sentiment(self, analysis_result, stock_name):
        """Show stock analysis with sentiment-based theming"""
        if not analysis_result:
            return
        
        # Extract sentiment from analysis
        signals = analysis_result.get('signals', {})
        overall_signal = signals.get('overall_signal', 'neutral')
        
        message = f"{stock_name}: {overall_signal.upper()} signal detected"
        self.show_sentiment_based_alert(overall_signal, message)