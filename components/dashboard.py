import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import time
from utils.data_fetcher import DataFetcher
from utils.speech_handler import SpeechHandler

def render_dashboard():
    """Render the main dashboard"""
    
    # Initialize data fetcher and speech handler
    data_fetcher = DataFetcher()
    speech_handler = SpeechHandler()
    
    # Add accessibility features
    speech_handler.add_accessibility_features()
    
    # Header with loading animation
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <h1>🇮🇳 Indian Market Dashboard</h1>
                <p style='color: #666; font-size: 18px;'>Real-time insights from NSE & BSE</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Market status and quick stats
    render_market_status()
    
    # Main dashboard content
    with st.container():
        # Loading state with Indian market context
        with st.spinner('📊 Loading market data from NSE & BSE...'):
            time.sleep(1)  # Simulate loading for better UX
            
            # Market overview section
            st.subheader("📈 Market Overview")
            render_market_overview_widgets(data_fetcher)
            
            st.markdown("---")
            
            # Quick stock lookup
            st.subheader("🔍 Quick Stock Lookup")
            render_quick_stock_lookup(data_fetcher)
            
            st.markdown("---")
            
            # Sector performance
            st.subheader("🏭 Sector Performance")
            render_sector_performance(data_fetcher)
            
            st.markdown("---")
            
            # Recent news preview
            st.subheader("📰 Market News Preview")
            render_news_preview(data_fetcher)
    
    # Voice navigation and speech features
    if st.session_state.get('voice_enabled', False):
        speech_handler.add_voice_navigation()
        
        # Speak dashboard summary button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔊 Speak Dashboard Summary", key="speak_dashboard"):
                market_data = data_fetcher.get_market_overview()
                speech_handler.speak_market_summary(market_data)

def render_market_status():
    """Render market status indicator"""
    col1, col2, col3, col4 = st.columns(4)
    
    # Current time in IST
    ist_time = datetime.now().strftime("%I:%M %p IST")
    
    with col1:
        st.metric(
            label="🕐 Current Time",
            value=ist_time,
            help="Indian Standard Time"
        )
    
    with col2:
        # Market status
        now = datetime.now()
        if now.weekday() < 5 and 9 <= now.hour <= 15:  # Simplified market hours check
            status = "🟢 OPEN"
            color = "green"
        else:
            status = "🔴 CLOSED"
            color = "red"
        
        st.markdown(f"""
        <div style='text-align: center; padding: 10px; border-radius: 10px; background-color: rgba(0,0,0,0.05);'>
            <h3 style='color: {color}; margin: 0;'>{status}</h3>
            <p style='margin: 0; font-size: 14px;'>Market Status</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.metric(
            label="🏛️ Exchanges",
            value="NSE • BSE",
            help="National Stock Exchange • Bombay Stock Exchange"
        )
    
    with col4:
        # Trading session info
        st.metric(
            label="⏰ Trading Hours",
            value="9:15 AM - 3:30 PM",
            help="Monday to Friday (IST)"
        )

def render_market_overview_widgets(data_fetcher):
    """Render market overview widgets"""
    try:
        # Get market data with loading state
        market_data = data_fetcher.get_market_overview()
        
        if not market_data:
            st.warning("⚠️ Market data temporarily unavailable. Please try again later.")
            render_error_fallback()
            return
        
        # Display indices
        cols = st.columns(len(market_data))
        
        for i, (index_name, data) in enumerate(market_data.items()):
            with cols[i]:
                current = data.get('current', 0)
                change = data.get('change', 0)
                change_percent = data.get('change_percent', 0)
                
                # Dynamic color based on change
                delta_color = "normal" if change >= 0 else "inverse"
                
                st.metric(
                    label=f"📊 {index_name}",
                    value=f"₹{current:,.2f}",
                    delta=f"{change_percent:+.2f}%",
                    delta_color=delta_color,
                    help=f"Current value and daily change for {index_name}"
                )
        
        # Update market sentiment in session state
        avg_change = sum(data.get('change_percent', 0) for data in market_data.values()) / len(market_data)
        if avg_change > 0.5:
            st.session_state.market_sentiment = 'bullish'
        elif avg_change < -0.5:
            st.session_state.market_sentiment = 'bearish'
        else:
            st.session_state.market_sentiment = 'neutral'
            
    except Exception as e:
        st.error(f"Error loading market overview: {str(e)}")
        render_error_fallback()

def render_quick_stock_lookup(data_fetcher):
    """Render quick stock lookup widget"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Get all available Indian stocks for comprehensive lookup
        all_stocks = list(data_fetcher.indian_symbols.keys())
        
        # Add search functionality
        search_query = st.text_input(
            "🔍 Search for stocks:",
            placeholder="Type company name or symbol (e.g., RELIANCE, TCS, INFY)",
            help="Search from 50+ Indian stocks including NIFTY 50, BSE SENSEX companies and more"
        )
        
        # Filter stocks based on search query
        if search_query:
            filtered_stocks = []
            search_lower = search_query.lower()
            
            for symbol in all_stocks:
                company_name = data_fetcher.indian_symbols.get(symbol, '').lower()
                symbol_clean = symbol.replace('.NS', '').lower()
                
                if (search_lower in company_name or 
                    search_lower in symbol_clean or
                    symbol_clean.startswith(search_lower)):
                    filtered_stocks.append(symbol)
            
            # Show filtered results
            if filtered_stocks:
                selected_stock = st.selectbox(
                    f"Found {len(filtered_stocks)} matching stocks:",
                    options=filtered_stocks,
                    format_func=lambda x: f"{x.replace('.NS', '')} - {data_fetcher.indian_symbols.get(x, 'Unknown')}",
                    help="Select from the filtered results"
                )
            else:
                st.warning("No stocks found matching your search. Try different keywords.")
                selected_stock = None
        else:
            # Show popular stocks as default
            popular_stocks = [
                'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 
                'HINDUNILVR.NS', 'ITC.NS', 'KOTAKBANK.NS', 'LT.NS',
                'SBIN.NS', 'BHARTIARTL.NS', 'ICICIBANK.NS', 'WIPRO.NS'
            ]
            
            selected_stock = st.selectbox(
                f"Select from popular stocks (or search above from {len(all_stocks)} total stocks):",
                options=popular_stocks,
                format_func=lambda x: f"{x.replace('.NS', '')} - {data_fetcher.indian_symbols.get(x, 'Unknown')}",
                help="Choose from popular Indian stocks or use the search above"
            )
    
    with col2:
        lookup_button = st.button("📈 Get Quote", key="quick_lookup")
    
    # Handle stock selection
    if search_query and not filtered_stocks:
        selected_stock = None
    elif not search_query:
        # selected_stock is already set from the popular stocks selectbox
        pass
    
    if lookup_button and selected_stock:
        with st.spinner(f'Getting latest data for {selected_stock}...'):
            stock_data = data_fetcher.get_stock_data(selected_stock, "5d")
            
            if stock_data:
                latest = stock_data['history'].iloc[-1]
                prev = stock_data['history'].iloc[-2] if len(stock_data['history']) > 1 else latest
                
                change = latest['Close'] - prev['Close']
                change_percent = (change / prev['Close']) * 100 if prev['Close'] != 0 else 0
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Current Price", f"₹{latest['Close']:.2f}")
                with col2:
                    st.metric("Change", f"₹{change:+.2f}", f"{change_percent:+.2f}%")
                with col3:
                    st.metric("Volume", f"{latest['Volume']:,}")
                with col4:
                    st.metric("High/Low", f"₹{latest['High']:.2f} / ₹{latest['Low']:.2f}")
            else:
                st.error("Unable to fetch stock data. Please try again.")

def render_top_performers(data_fetcher):
    """Render top gainers and losers"""
    try:
        with st.spinner('🔄 Analyzing top performers...'):
            gainers, losers = data_fetcher.get_top_gainers_losers()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🟢 Top Gainers")
            if gainers:
                for stock in gainers[:5]:
                    with st.container():
                        st.markdown(f"""
                        <div style='padding: 10px; margin: 5px; border-radius: 5px; 
                                    border-left: 4px solid green; background-color: rgba(0,255,0,0.05);'>
                            <strong>{stock['name']}</strong> ({stock['symbol'].replace('.NS', '')})<br>
                            ₹{stock['price']:.2f} 
                            <span style='color: green;'>+{stock['change_percent']:.2f}%</span>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No gainers data available")
        
        with col2:
            st.markdown("### 🔴 Top Losers")
            if losers:
                for stock in losers[:5]:
                    with st.container():
                        st.markdown(f"""
                        <div style='padding: 10px; margin: 5px; border-radius: 5px; 
                                    border-left: 4px solid red; background-color: rgba(255,0,0,0.05);'>
                            <strong>{stock['name']}</strong> ({stock['symbol'].replace('.NS', '')})<br>
                            ₹{stock['price']:.2f} 
                            <span style='color: red;'>{stock['change_percent']:.2f}%</span>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No losers data available")
                
    except Exception as e:
        st.error(f"Error loading top performers: {str(e)}")

def render_sector_performance(data_fetcher):
    """Render sector performance chart"""
    try:
        with st.spinner('📊 Loading sector performance...'):
            sector_data = data_fetcher.get_sector_performance()
        
        if sector_data:
            # Create sector performance chart
            sectors = list(sector_data.keys())
            changes = [data['avg_change'] for data in sector_data.values()]
            
            fig = px.bar(
                x=sectors,
                y=changes,
                title="Sector Performance Today",
                labels={'x': 'Sectors', 'y': 'Average Change (%)'},
                color=changes,
                color_continuous_scale=['red', 'yellow', 'green']
            )
            
            fig.update_layout(
                height=400,
                showlegend=False,
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sector performance data will be available during market hours")
            
    except Exception as e:
        st.error(f"Error loading sector performance: {str(e)}")

def render_news_preview(data_fetcher):
    """Render news preview section"""
    try:
        with st.spinner('📰 Fetching latest market news...'):
            news = data_fetcher.get_general_market_news()
        
        if news:
            for item in news[:3]:  # Show top 3 news items
                with st.container():
                    st.markdown(f"""
                    <div style='padding: 15px; margin: 10px 0; border-radius: 10px; 
                                background-color: rgba(0,0,0,0.02); border-left: 4px solid #FF6B35;'>
                        <h4 style='margin: 0 0 10px 0; color: #333;'>{item.get('headline', 'News Headline')}</h4>
                        <p style='margin: 0; color: #666; font-size: 14px;'>
                            {item.get('summary', 'News summary unavailable')[:200]}...
                        </p>
                        <p style='margin: 10px 0 0 0; font-size: 12px; color: #999;'>
                            Source: {item.get('source', 'Unknown')} | 
                            {datetime.fromtimestamp(item.get('datetime', 0)).strftime('%Y-%m-%d %H:%M') if item.get('datetime') else 'Time unknown'}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Link to full news section
            if st.button("📰 View All News"):
                st.session_state.current_page = "news_feed"
                st.rerun()
        else:
            st.info("📰 News feed will be available shortly")
            
    except Exception as e:
        st.error(f"Error loading news: {str(e)}")

def render_error_fallback():
    """Render error fallback content with Indian market context"""
    st.markdown("""
    <div style='text-align: center; padding: 40px; background-color: rgba(255, 107, 53, 0.1); 
                border-radius: 15px; margin: 20px 0;'>
        <h2>🏛️ मार्केट डेटा लोड हो रहा है...</h2>
        <h3>Market Data Loading...</h3>
        <p>
            हमारे सिस्टम वर्तमान में NSE और BSE से लेटेस्ट डेटा प्राप्त कर रहे हैं।<br>
            <em>Our systems are currently fetching the latest data from NSE and BSE.</em>
        </p>
        <p style='color: #666; font-size: 14px;'>
            🕐 कृपया कुछ समय प्रतीक्षा करें | Please wait a moment<br>
            📊 Real-time market data updating...
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show some static information while loading
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **NSE (National Stock Exchange)**
        - Founded: 1992
        - Location: Mumbai
        - Index: NIFTY 50
        """)
    
    with col2:
        st.info("""
        **BSE (Bombay Stock Exchange)**
        - Founded: 1875
        - Location: Mumbai  
        - Index: SENSEX
        """)
    
    with col3:
        st.info("""
        **Trading Hours**
        - Pre-open: 9:00-9:15 AM
        - Regular: 9:15 AM-3:30 PM
        - Post-close: 3:40-4:00 PM
        """)
