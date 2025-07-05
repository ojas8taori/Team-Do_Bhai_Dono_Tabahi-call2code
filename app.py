import streamlit as st
import pandas as pd
import datetime
import time
from utils.stock_data import get_stock_data, get_stock_metrics
from utils.market_news import get_market_news
from utils.nse_bse_data import get_top_gainers_losers
from utils.charts import create_candlestick_chart

# Page configuration
st.set_page_config(
    page_title="StonkGPT - Stock Analysis Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .time-display {
        position: fixed;
        top: 10px;
        right: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        z-index: 1000;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .watchlist-stock {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: 10px;
        border-left: 4px solid #fff;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .stMetric {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-radius: 10px;
    }
    .stTextInput > div > div > input {
        background: linear-gradient(135deg, #e3ffe7 0%, #d9e7ff 100%);
        border-radius: 10px;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# Live time display
def display_live_time():
    # Convert to IST
    import pytz
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S IST")
    st.markdown(f'<div class="time-display">{current_time}</div>', unsafe_allow_html=True)

# Main app layout
def main():
    # Display live time
    display_live_time()
    
    # Main header
    st.markdown('<h1 class="main-header">📈 StonkGPT</h1>', unsafe_allow_html=True)
    
    # Market indices display
    st.markdown("### 📊 Market Indices")
    
    # Get market indices data
    from utils.nse_bse_data import get_market_indices
    
    with st.spinner('Loading real-time market data...'):
        indices_data = get_market_indices()
    
    if indices_data:
        indices_cols = st.columns(len(indices_data))
        
        for i, (index_name, index_info) in enumerate(indices_data.items()):
            with indices_cols[i]:
                change_color = "#2ecc71" if index_info['change'] >= 0 else "#e74c3c"
                change_symbol = "↗" if index_info['change'] >= 0 else "↘"
                st.markdown(f"""
                <div style="
                    background: white;
                    border: 1px solid #e0e0e0;
                    padding: 1rem;
                    border-radius: 8px;
                    text-align: center;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    margin-bottom: 1rem;
                ">
                    <div style="font-weight: bold; font-size: 0.85rem; color: #666; margin-bottom: 0.3rem;">{index_name}</div>
                    <div style="font-size: 1.4rem; font-weight: bold; color: #2c3e50; margin: 0.2rem 0;">{index_info['value']:,.2f}</div>
                    <div style="color: {change_color}; font-size: 0.9rem; font-weight: 500;">
                        {change_symbol} {index_info['change']:+.2f} ({index_info['change_percent']:+.2f}%)
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("Unable to fetch real-time market indices data. Please check your internet connection or try again later.")
    
    st.markdown("---")
    
    # Sidebar for navigation and watchlist
    with st.sidebar:
        st.header("Navigation")
        
        # Stock input
        st.subheader("🔍 Search Stock")
        stock_symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, RELIANCE.NS)", key="stock_input")
        
        # Helper text for Indian stocks
        st.caption("For NSE stocks: add .NS (e.g., RELIANCE.NS, TCS.NS)")
        st.caption("For BSE stocks: add .BO (e.g., RELIANCE.BO)")
        
        # Watchlist section
        st.subheader("📋 Watchlist")
        
        # Add to watchlist
        if stock_symbol and st.button("Add to Watchlist"):
            if stock_symbol.upper() not in st.session_state.watchlist:
                st.session_state.watchlist.append(stock_symbol.upper())
                st.success(f"Added {stock_symbol.upper()} to watchlist!")
            else:
                st.warning("Stock already in watchlist!")
        
        # Display watchlist
        if st.session_state.watchlist:
            for i, stock in enumerate(st.session_state.watchlist):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f'<div class="watchlist-stock">{stock}</div>', unsafe_allow_html=True)
                with col2:
                    if st.button("❌", key=f"remove_{i}"):
                        st.session_state.watchlist.remove(stock)
                        st.rerun()
        else:
            st.info("No stocks in watchlist")
        
        # Market overview toggle
        st.subheader("📊 Market Overview")
        show_market_overview = st.checkbox("Show Top Gainers/Losers", value=True)
        
        # News section
        st.markdown("---")
        st.subheader("📰 Market News")
        news_type = st.radio("News Type", ["Economic News", "Company News"], key="news_type")
        
        if news_type == "Economic News":
            # Display economic market news
            if st.button("📰 Load Economic News", key="load_general_news"):
                from utils.finnhub_news import get_general_market_news
                
                with st.spinner("Loading economic news..."):
                    news_articles = get_general_market_news(limit=5)
                    
                    if news_articles:
                        st.subheader("Latest Economic News")
                        for i, article in enumerate(news_articles[:3]):  # Show top 3 in sidebar
                            with st.expander(f"📄 {article['title'][:40]}...", expanded=False):
                                st.write(f"**Source:** {article['source']}")
                                st.write(f"**Published:** {article['published_at']}")
                                st.write(article['description'][:150] + "...")
                                if article['url']:
                                    st.markdown(f"[Read More]({article['url']})")
                    else:
                        st.info("No economic news available")
        
        elif news_type == "Company News" and stock_symbol:
            # Display stock-specific news
            if st.button(f"📰 Load {stock_symbol} News", key="load_stock_news"):
                from utils.finnhub_news import get_stock_news
                
                with st.spinner(f"Loading news for {stock_symbol}..."):
                    news_articles = get_stock_news(stock_symbol, limit=5)
                    
                    if news_articles:
                        st.subheader(f"Latest {stock_symbol} News")
                        for i, article in enumerate(news_articles[:3]):  # Show top 3 in sidebar
                            with st.expander(f"📄 {article['title'][:40]}...", expanded=False):
                                st.write(f"**Source:** {article['source']}")
                                st.write(f"**Published:** {article['published_at']}")
                                st.write(article['description'][:150] + "...")
                                if article['url']:
                                    st.markdown(f"[Read More]({article['url']})")
                    else:
                        st.info(f"No news available for {stock_symbol}")
        
        elif news_type == "Company News" and not stock_symbol:
            st.info("Please enter a stock symbol to see company news")
    
    # Main content area
    if stock_symbol:
        # Stock analysis section
        st.header(f"📊 Stock Analysis: {stock_symbol.upper()}")
        
        try:
            # Get stock data
            stock_data = get_stock_data(stock_symbol)
            metrics = get_stock_metrics(stock_symbol)
            
            if stock_data is not None and not stock_data.empty:
                # Display current price and metrics
                col1, col2, col3, col4 = st.columns(4)
                
                current_price = stock_data['Close'].iloc[-1]
                prev_close = stock_data['Close'].iloc[-2] if len(stock_data) > 1 else current_price
                price_change = current_price - prev_close
                price_change_pct = (price_change / prev_close) * 100 if prev_close != 0 else 0
                
                # Determine currency symbol based on stock symbol
                currency_symbol = "₹" if any(x in stock_symbol.upper() for x in ['.NS', '.BO']) else "$"
                
                with col1:
                    st.metric("Current Price", f"{currency_symbol}{current_price:.2f}", f"{price_change:+.2f} ({price_change_pct:+.2f}%)")
                
                with col2:
                    if metrics and 'pe_ratio' in metrics:
                        st.metric("P/E Ratio", f"{metrics['pe_ratio']:.2f}" if metrics['pe_ratio'] else "N/A")
                    else:
                        st.metric("P/E Ratio", "N/A")
                
                with col3:
                    if metrics and 'roe' in metrics:
                        st.metric("ROE", f"{metrics['roe']:.2f}%" if metrics['roe'] else "N/A")
                    else:
                        st.metric("ROE", "N/A")
                
                with col4:
                    if metrics and 'market_cap' in metrics:
                        market_cap = metrics['market_cap']
                        if market_cap:
                            if market_cap > 1e12:
                                st.metric("Market Cap", f"{currency_symbol}{market_cap/1e12:.2f}T")
                            elif market_cap > 1e9:
                                st.metric("Market Cap", f"{currency_symbol}{market_cap/1e9:.2f}B")
                            else:
                                st.metric("Market Cap", f"{currency_symbol}{market_cap/1e6:.2f}M")
                        else:
                            st.metric("Market Cap", "N/A")
                    else:
                        st.metric("Market Cap", "N/A")
                
                # Chart section with sentiment analysis
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader("📈 Interactive Chart")
                
                with col2:
                    # Sentiment analysis button
                    if st.button("🔍 Analyze Sentiment", key="sentiment_btn"):
                        from utils.finnhub_news import analyze_stock_sentiment, get_sentiment_color, get_sentiment_emoji
                        
                        with st.spinner("Analyzing sentiment..."):
                            sentiment_data = analyze_stock_sentiment(stock_symbol)
                            
                            # Display sentiment result
                            sentiment_color = get_sentiment_color(sentiment_data['sentiment'])
                            sentiment_emoji = get_sentiment_emoji(sentiment_data['sentiment'])
                            
                            st.markdown(f"""
                            <div style="background-color: {sentiment_color}20; padding: 10px; border-radius: 5px; border-left: 4px solid {sentiment_color};">
                                <h4>{sentiment_emoji} {sentiment_data['sentiment']} Sentiment</h4>
                                <p><strong>Confidence:</strong> {sentiment_data['confidence']:.1%}</p>
                                <p><strong>Articles Analyzed:</strong> {sentiment_data['total_articles']}</p>
                                <p><strong>Breakdown:</strong> {sentiment_data['positive_articles']} Positive, {sentiment_data['negative_articles']} Negative, {sentiment_data['neutral_articles']} Neutral</p>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Timeframe selection
                timeframe = st.selectbox(
                    "Select Timeframe",
                    ["1D", "1W", "1M", "3M", "1Y"],
                    index=2
                )
                
                # Chart type selection
                chart_tabs = st.tabs(["📊 Price Chart", "📈 Technical Analysis"])
                
                with chart_tabs[0]:
                    # Create and display main price chart
                    chart = create_candlestick_chart(stock_data, stock_symbol, timeframe)
                    st.plotly_chart(chart, use_container_width=True)
                
                with chart_tabs[1]:
                    # Technical indicators chart
                    from utils.charts import create_technical_indicators_chart, calculate_technical_indicators
                    
                    # Calculate indicators for current values
                    tech_data = calculate_technical_indicators(stock_data.copy())
                    
                    # Display current technical indicator values
                    st.subheader("📊 Current Technical Indicators")
                    
                    if not tech_data.empty:
                        tech_cols = st.columns(4)
                        
                        with tech_cols[0]:
                            if 'RSI' in tech_data.columns:
                                current_rsi = tech_data['RSI'].iloc[-1]
                                if pd.notna(current_rsi):
                                    rsi_color = "🔴" if current_rsi >= 70 else "🟢" if current_rsi <= 30 else "🟡"
                                    st.metric("RSI", f"{current_rsi:.1f}", help="Relative Strength Index")
                                    if current_rsi >= 70:
                                        st.caption("🔴 Overbought")
                                    elif current_rsi <= 30:
                                        st.caption("🟢 Oversold")
                                    else:
                                        st.caption("🟡 Neutral")
                        
                        with tech_cols[1]:
                            if 'MACD' in tech_data.columns and 'MACD_Signal' in tech_data.columns:
                                current_macd = tech_data['MACD'].iloc[-1]
                                current_signal = tech_data['MACD_Signal'].iloc[-1]
                                if pd.notna(current_macd) and pd.notna(current_signal):
                                    macd_diff = current_macd - current_signal
                                    trend = "🔴 Bearish" if macd_diff < 0 else "🟢 Bullish"
                                    st.metric("MACD", f"{current_macd:.3f}")
                                    st.caption(f"Signal: {current_signal:.3f}")
                                    st.caption(trend)
                        
                        with tech_cols[2]:
                            if 'MA20' in tech_data.columns and 'MA50' in tech_data.columns:
                                ma20 = tech_data['MA20'].iloc[-1]
                                ma50 = tech_data['MA50'].iloc[-1]
                                current_price = tech_data['Close'].iloc[-1]
                                if pd.notna(ma20) and pd.notna(ma50):
                                    trend = "🟢 Bullish" if ma20 > ma50 else "🔴 Bearish"
                                    st.metric("MA20", f"{currency_symbol}{ma20:.2f}")
                                    st.caption(f"MA50: {currency_symbol}{ma50:.2f}")
                                    st.caption(trend)
                        
                        with tech_cols[3]:
                            if 'BB_Upper' in tech_data.columns and 'BB_Lower' in tech_data.columns:
                                bb_upper = tech_data['BB_Upper'].iloc[-1]
                                bb_lower = tech_data['BB_Lower'].iloc[-1]
                                current_price = tech_data['Close'].iloc[-1]
                                if pd.notna(bb_upper) and pd.notna(bb_lower):
                                    if current_price >= bb_upper:
                                        bb_signal = "🔴 Overbought"
                                    elif current_price <= bb_lower:
                                        bb_signal = "🟢 Oversold"
                                    else:
                                        bb_signal = "🟡 Normal"
                                    st.metric("BB Upper", f"{currency_symbol}{bb_upper:.2f}")
                                    st.caption(f"Lower: {currency_symbol}{bb_lower:.2f}")
                                    st.caption(bb_signal)
                    
                    st.markdown("---")
                    
                    # Technical indicators chart
                    tech_chart = create_technical_indicators_chart(stock_data, stock_symbol)
                    st.plotly_chart(tech_chart, use_container_width=True)
                
                # Additional metrics
                if metrics:
                    st.subheader("📋 Additional Metrics")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.write("**Volume**")
                        st.write(f"{stock_data['Volume'].iloc[-1]:,}" if not stock_data['Volume'].empty else "N/A")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.write("**52W High**")
                        st.write(f"{currency_symbol}{stock_data['High'].max():.2f}" if not stock_data['High'].empty else "N/A")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.write("**52W Low**")
                        st.write(f"{currency_symbol}{stock_data['Low'].min():.2f}" if not stock_data['Low'].empty else "N/A")
                        st.markdown('</div>', unsafe_allow_html=True)
                
                # News section
                st.subheader("📰 Latest News")
                try:
                    news_data = get_market_news(stock_symbol)
                    
                    if news_data and len(news_data) > 0:
                        for article in news_data[:5]:  # Show top 5 news
                            with st.expander(f"📄 {article.get('title', 'No Title')}"):
                                st.write(f"**Source:** {article.get('source', 'Unknown')}")
                                st.write(f"**Published:** {article.get('published_at', 'Unknown')}")
                                if article.get('description'):
                                    st.write(article['description'])
                                if article.get('url'):
                                    st.markdown(f"[Read full article]({article['url']})")
                    else:
                        st.info("No recent news available for this stock. News data might be limited without API key.")
                except Exception as e:
                    st.warning(f"Unable to fetch news data: {str(e)}")
                
            else:
                st.error("Unable to fetch stock data. Please check the symbol and try again.")
                
        except Exception as e:
            st.error(f"Error fetching stock data: {str(e)}")
    
    # Market overview section
    if show_market_overview:
        st.header("🌐 Market Overview")
        
        try:
            # Get NSE/BSE data
            from utils.nse_bse_data import format_market_data
            
            with st.spinner('Loading real-time gainers and losers data...'):
                market_data = get_top_gainers_losers()
            
            if market_data and (market_data.get('gainers') or market_data.get('losers')):
                formatted_data = format_market_data(market_data)
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📈 Top Gainers")
                    if 'gainers' in formatted_data and formatted_data['gainers']:
                        gainers_df = pd.DataFrame(formatted_data['gainers'])
                        st.dataframe(gainers_df, use_container_width=True, hide_index=True)
                    else:
                        st.info("No gainers data available currently")
                
                with col2:
                    st.subheader("📉 Top Losers")
                    if 'losers' in formatted_data and formatted_data['losers']:
                        losers_df = pd.DataFrame(formatted_data['losers'])
                        st.dataframe(losers_df, use_container_width=True, hide_index=True)
                    else:
                        st.info("No losers data available currently")
            else:
                st.warning("Unable to fetch real-time gainers/losers data. This may be due to market hours or connectivity issues.")
                
        except Exception as e:
            st.error(f"Error fetching market data: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown("**StonkGPT** - AI-Powered Stock Analysis Platform")
    st.markdown("*Data provided by Yahoo Finance API and various financial sources*")

# Auto-refresh functionality
def auto_refresh():
    """Auto refresh the app every 5 minutes"""
    time.sleep(300)  # 5 minutes
    st.rerun()

if __name__ == "__main__":
    main()
