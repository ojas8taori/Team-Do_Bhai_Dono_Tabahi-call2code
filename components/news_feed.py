import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from utils.data_fetcher import DataFetcher
from utils.news_analyzer import NewsAnalyzer
from utils.speech_handler import SpeechHandler

def render_news_feed():
    """Render the news feed page with comprehensive analysis"""
    
    # Initialize components
    data_fetcher = DataFetcher()
    news_analyzer = NewsAnalyzer()
    speech_handler = SpeechHandler()
    
    # Page header
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1>📰 Indian Market News & Analysis</h1>
        <p style='color: #666; font-size: 18px;'>AI-powered news sentiment analysis for Indian markets</p>
    </div>
    """, unsafe_allow_html=True)
    
    # News controls and filters
    render_news_controls()
    
    # Load and analyze news
    with st.spinner('📡 Fetching latest market news and analyzing sentiment...'):
        news_data = fetch_and_analyze_news(data_fetcher, news_analyzer)
    
    if news_data:
        # News analysis dashboard
        render_news_dashboard(news_data, news_analyzer)
        
        # Detailed news feed
        render_detailed_news_feed(news_data)
        
        # Voice features
        if st.session_state.get('voice_enabled', False):
            render_voice_news_features(news_data, speech_handler)
    else:
        render_news_error_page()

def render_news_controls():
    """Render news filtering and control options"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        news_category = st.selectbox(
            "📂 Category:",
            ["All", "General Market", "Banking", "IT", "Auto", "Pharma", "Energy"],
            help="Filter news by sector"
        )
        st.session_state.news_category = news_category
    
    with col2:
        sentiment_filter = st.selectbox(
            "😊 Sentiment:",
            ["All", "Positive", "Negative", "Neutral"],
            help="Filter by news sentiment"
        )
        st.session_state.sentiment_filter = sentiment_filter
    
    with col3:
        time_range = st.selectbox(
            "📅 Time Range:",
            ["Today", "Last 3 days", "Last Week", "Last Month"],
            help="Select news time range"
        )
        st.session_state.time_range = time_range
    
    with col4:
        if st.button("🔄 Refresh News", type="primary"):
            st.cache_data.clear()
            st.rerun()

def fetch_and_analyze_news(data_fetcher, news_analyzer):
    """Fetch and analyze news data"""
    try:
        # Determine days based on time range
        time_range = st.session_state.get('time_range', 'Today')
        days_map = {
            'Today': 1,
            'Last 3 days': 3,
            'Last Week': 7,
            'Last Month': 30
        }
        days = days_map.get(time_range, 1)
        
        # Fetch general market news
        general_news = data_fetcher.get_general_market_news()
        
        # Fetch company-specific news for major Indian stocks
        company_news = []
        major_stocks = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS']
        
        for stock in major_stocks:
            try:
                stock_news = data_fetcher.get_company_news(stock, days)
                company_news.extend(stock_news)
            except:
                continue  # Skip if company news fails
        
        # Combine all news
        all_news = general_news + company_news
        
        if all_news:
            # Analyze news batch
            analyzed_data = news_analyzer.analyze_news_batch(all_news)
            return analyzed_data
        
        return None
        
    except Exception as e:
        st.error(f"Error fetching news: {str(e)}")
        return None

def render_news_dashboard(news_data, news_analyzer):
    """Render news analysis dashboard"""
    st.subheader("📊 News Analysis Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Articles",
            news_data['total_articles'],
            help="Total news articles analyzed"
        )
    
    with col2:
        overall_sentiment = news_data['overall_sentiment']
        sentiment_emoji = "📈" if overall_sentiment == "Positive" else "📉" if overall_sentiment == "Negative" else "➡️"
        
        st.markdown(f"""
        <div style='text-align: center; padding: 15px; border-radius: 10px; 
                    background-color: rgba(0,0,0,0.05);'>
            <h3 style='margin: 0;'>{sentiment_emoji} {overall_sentiment}</h3>
            <p style='margin: 5px 0 0 0; font-size: 14px;'>Market Sentiment</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        market_impact = news_data['market_impact']
        impact_color = "green" if market_impact == "Bullish" else "red" if market_impact == "Bearish" else "orange"
        
        st.markdown(f"""
        <div style='text-align: center; padding: 15px; border-radius: 10px; 
                    background-color: rgba(0,0,0,0.05);'>
            <h3 style='color: {impact_color}; margin: 0;'>{market_impact}</h3>
            <p style='margin: 5px 0 0 0; font-size: 14px;'>Market Impact</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_polarity = news_data.get('average_polarity', 0)
        polarity_score = f"{avg_polarity:+.3f}"
        
        st.metric(
            "Sentiment Score",
            polarity_score,
            help="Average sentiment polarity (-1 to +1)"
        )
    
    # Sentiment distribution chart
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Sentiment Distribution")
        
        sentiment_dist = news_data['sentiment_distribution']
        
        fig_pie = px.pie(
            values=list(sentiment_dist.values()),
            names=list(sentiment_dist.keys()),
            title="News Sentiment Breakdown",
            color_discrete_map={
                'Positive': '#00ff00',
                'Negative': '#ff0000',
                'Neutral': '#ffff00'
            }
        )
        
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown("### 📂 Category Distribution")
        
        category_dist = news_data['category_distribution']
        
        if category_dist:
            fig_bar = px.bar(
                x=list(category_dist.values()),
                y=list(category_dist.keys()),
                orientation='h',
                title="News by Category",
                color=list(category_dist.values()),
                color_continuous_scale='viridis'
            )
            
            fig_bar.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No category data available")
    
    # Top mentioned companies
    if news_data.get('top_companies'):
        st.markdown("---")
        st.markdown("### 🏢 Most Mentioned Companies")
        
        top_companies = news_data['top_companies']
        
        col1, col2, col3 = st.columns(3)
        
        for i, (company, count) in enumerate(top_companies[:3]):
            with [col1, col2, col3][i]:
                st.metric(
                    f"#{i+1} {company.replace('.NS', '')}",
                    f"{count} mentions"
                )
    
    # News summary
    st.markdown("---")
    st.markdown("### 📝 Analysis Summary")
    
    summary = news_analyzer.generate_news_summary(news_data)
    st.markdown(summary)

def render_detailed_news_feed(news_data):
    """Render detailed news articles with sentiment analysis"""
    st.markdown("---")
    st.subheader("📰 Detailed News Feed")
    
    analyzed_news = news_data.get('analyzed_news', [])
    
    if not analyzed_news:
        st.info("No news articles available for the selected filters.")
        return
    
    # Apply filters
    filtered_news = apply_news_filters(analyzed_news)
    
    if not filtered_news:
        st.warning("No articles match the selected filters. Try adjusting your filters.")
        return
    
    # Display news articles
    for i, news_item in enumerate(filtered_news[:20]):  # Limit to 20 articles
        render_news_article(news_item, i)

def apply_news_filters(analyzed_news):
    """Apply user-selected filters to news"""
    filtered = analyzed_news
    
    # Sentiment filter
    sentiment_filter = st.session_state.get('sentiment_filter', 'All')
    if sentiment_filter != 'All':
        filtered = [news for news in filtered if news['sentiment']['sentiment'] == sentiment_filter]
    
    # Category filter
    category_filter = st.session_state.get('news_category', 'All')
    if category_filter != 'All':
        if category_filter == 'General Market':
            filtered = [news for news in filtered if news['category'] in ['Market News', 'General']]
        else:
            filtered = [news for news in filtered if category_filter.lower() in news['category'].lower()]
    
    return filtered

def render_news_article(news_item, index):
    """Render individual news article with analysis"""
    original = news_item['original']
    sentiment = news_item['sentiment']
    market_impact = news_item['market_impact']
    category = news_item['category']
    mentioned_companies = news_item['mentioned_companies']
    
    # Article container
    with st.container():
        # Create expandable article
        with st.expander(f"📰 {original.get('headline', 'News Article')} | {sentiment['emoji']} {sentiment['sentiment']}", expanded=(index < 3)):
            
            # Article metadata
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**Category:** {category}")
                st.markdown(f"**Impact:** {market_impact['impact']} {market_impact['color']}")
            
            with col2:
                st.markdown(f"**Sentiment:** {sentiment['sentiment']} ({sentiment['confidence']:.1f}% confidence)")
                st.markdown(f"**Polarity:** {sentiment['polarity']:+.3f}")
            
            with col3:
                if mentioned_companies:
                    companies_text = ", ".join([comp.replace('.NS', '') for comp in mentioned_companies[:3]])
                    st.markdown(f"**Companies:** {companies_text}")
                
                if original.get('datetime'):
                    pub_time = datetime.fromtimestamp(original['datetime'])
                    st.markdown(f"**Published:** {pub_time.strftime('%Y-%m-%d %H:%M')}")
            
            # Article content
            st.markdown("---")
            
            # Headline
            st.markdown(f"### {original.get('headline', 'No headline available')}")
            
            # Summary/Content
            summary = original.get('summary', '')
            if summary:
                st.markdown(f"**Summary:** {summary}")
            
            # Source and URL
            col1, col2 = st.columns(2)
            
            with col1:
                if original.get('source'):
                    st.markdown(f"**Source:** {original['source']}")
            
            with col2:
                if original.get('url'):
                    st.markdown(f"[Read Full Article]({original['url']})")
            
            # Sentiment analysis details
            if st.session_state.get('show_detailed_analysis', False):
                st.markdown("---")
                st.markdown("**Detailed Analysis:**")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"- Positive keywords: {market_impact['positive_keywords']}")
                    st.markdown(f"- Negative keywords: {market_impact['negative_keywords']}")
                
                with col2:
                    st.markdown(f"- Subjectivity: {sentiment['subjectivity']:.3f}")
                    st.markdown(f"- Impact score: {market_impact['score']:+d}")

def render_voice_news_features(news_data, speech_handler):
    """Render voice-enabled news features"""
    st.markdown("---")
    st.subheader("🎤 Voice News Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔊 Speak News Summary"):
            speech_handler.speak_news_summary(news_data)
    
    with col2:
        if st.button("🔊 Read Top Headlines"):
            analyzed_news = news_data.get('analyzed_news', [])
            if analyzed_news:
                headlines = [news['original'].get('headline', '') for news in analyzed_news[:5]]
                headlines_text = "Here are today's top headlines: " + ". ".join(headlines)
                speech_handler.speak_text(headlines_text)
    
    with col3:
        if st.button("🔊 Speak Market Sentiment"):
            sentiment = news_data['overall_sentiment']
            impact = news_data['market_impact']
            total = news_data['total_articles']
            
            sentiment_text = f"Based on {total} articles analyzed, the overall market sentiment is {sentiment} with {impact} impact on the markets."
            speech_handler.speak_text(sentiment_text)
    
    # Advanced voice controls
    if st.checkbox("🎛️ Advanced Voice Controls"):
        col1, col2 = st.columns(2)
        
        with col1:
            selected_category = st.selectbox(
                "Speak news from category:",
                ["All", "Banking", "IT", "Auto", "Pharma", "Energy"]
            )
            
            if st.button("🔊 Speak Category News"):
                analyzed_news = news_data.get('analyzed_news', [])
                
                if selected_category == "All":
                    category_news = analyzed_news[:3]
                else:
                    category_news = [news for news in analyzed_news 
                                   if selected_category.lower() in news['category'].lower()][:3]
                
                if category_news:
                    headlines = [news['original'].get('headline', '') for news in category_news]
                    category_text = f"Here are {selected_category} news headlines: " + ". ".join(headlines)
                    speech_handler.speak_text(category_text)
        
        with col2:
            sentiment_to_speak = st.selectbox(
                "Speak news by sentiment:",
                ["Positive", "Negative", "Neutral"]
            )
            
            if st.button("🔊 Speak Sentiment News"):
                analyzed_news = news_data.get('analyzed_news', [])
                sentiment_news = [news for news in analyzed_news 
                                if news['sentiment']['sentiment'] == sentiment_to_speak][:3]
                
                if sentiment_news:
                    headlines = [news['original'].get('headline', '') for news in sentiment_news]
                    sentiment_text = f"Here are {sentiment_to_speak.lower()} news headlines: " + ". ".join(headlines)
                    speech_handler.speak_text(sentiment_text)

def render_news_error_page():
    """Render creative error page for news feed"""
    st.markdown("""
    <div style='text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea, #764ba2); 
                border-radius: 20px; color: white; margin: 30px 0;'>
        <h1>📰 समाचार सेवा अस्थायी रूप से अनुपलब्ध</h1>
        <h2>News Service Temporarily Unavailable</h2>
        
        <div style='margin: 30px 0;'>
            <p style='font-size: 18px; margin: 10px 0;'>
                🌐 हमारे समाचार भागीदार से कनेक्ट हो रहे हैं<br>
                <em>Connecting to our news partners</em>
            </p>
            
            <p style='font-size: 16px; opacity: 0.9;'>
                📡 Finnhub API • Yahoo Finance • Real-time updates
            </p>
        </div>
        
        <div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0;'>
            <h3>🔄 What's happening?</h3>
            <p>Our AI is preparing to analyze the latest market news for sentiment and impact. Please wait a moment!</p>
            
            <div style='margin: 20px 0;'>
                <p style='font-size: 14px; opacity: 0.8;'>
                    While you wait, did you know that BSE (Bombay Stock Exchange) is one of the oldest stock exchanges in Asia, established in 1875?
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Alternative actions while news loads
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Check Market Data"):
            st.session_state.current_page = "dashboard"
            st.rerun()
    
    with col2:
        if st.button("📈 Analyze Stocks"):
            st.session_state.current_page = "stock_analysis"
            st.rerun()
    
    with col3:
        if st.button("🔄 Retry News Feed"):
            st.cache_data.clear()
            st.rerun()
    
    # Show some interesting facts while loading
    st.markdown("---")
    st.markdown("### 💡 Did You Know?")
    
    facts = [
        "The Sensex was introduced in 1986 and is one of the oldest stock market indices in India.",
        "NIFTY 50 represents about 66% of the free-float market capitalization of Indian stocks.",
        "India has over 5,000 listed companies across NSE and BSE.",
        "The Indian stock market operates from 9:15 AM to 3:30 PM on weekdays.",
        "Mumbai's Dalal Street is often called the Wall Street of India."
    ]
    
    import random
    fact = random.choice(facts)
    
    st.info(f"📚 {fact}")
