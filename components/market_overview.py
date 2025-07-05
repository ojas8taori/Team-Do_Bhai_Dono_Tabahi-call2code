import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from utils.data_fetcher import DataFetcher
from utils.technical_analysis import TechnicalAnalyzer
from utils.speech_handler import SpeechHandler

def render_market_overview():
    """Render comprehensive market overview page"""
    
    # Initialize components
    data_fetcher = DataFetcher()
    tech_analyzer = TechnicalAnalyzer()
    speech_handler = SpeechHandler()
    
    # Page header with dynamic theming
    render_market_header()
    
    # Market status and live updates
    render_live_market_status(data_fetcher)
    
    # Main overview sections
    with st.container():
        # Indices performance
        render_indices_dashboard(data_fetcher)
        
        st.markdown("---")
        
        # Market breadth and health
        render_market_breadth(data_fetcher)
        
        st.markdown("---")
        
        # Sector rotation and heatmap
        render_sector_heatmap(data_fetcher)
        
        st.markdown("---")
        
        # Market trends and patterns
        render_market_trends(data_fetcher, tech_analyzer)
        
        st.markdown("---")
        
        # Economic indicators
        render_economic_indicators()
        
        st.markdown("---")
        
        # International markets impact
        render_global_market_impact()
    
    # Voice features
    if st.session_state.get('voice_enabled', False):
        render_voice_market_features(data_fetcher, speech_handler)

def render_market_header():
    """Render dynamic market header"""
    # Get current market sentiment for dynamic theming
    sentiment = st.session_state.get('market_sentiment', 'neutral')
    
    if sentiment == 'bullish':
        header_color = "#d4edda"
        accent_color = "#28a745"
        emoji = "📈"
        status_text = "बुलिश बाज़ार"
    elif sentiment == 'bearish':
        header_color = "#f8d7da"
        accent_color = "#dc3545"
        emoji = "📉"
        status_text = "बेयरिश बाज़ार"
    else:
        header_color = "#fff3cd"
        accent_color = "#ffc107"
        emoji = "➡️"
        status_text = "स्थिर बाज़ार"
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {header_color}, white); 
                padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 30px;
                border-left: 5px solid {accent_color};'>
        <h1 style='color: {accent_color}; margin: 0;'>
            {emoji} भारतीय बाज़ार अवलोकन | Indian Market Overview
        </h1>
        <p style='font-size: 18px; color: #666; margin: 10px 0;'>
            Real-time insights from NSE & BSE • {status_text}
        </p>
        <p style='font-size: 14px; color: #888; margin: 0;'>
            Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_live_market_status(data_fetcher):
    """Render live market status with real-time updates"""
    st.subheader("🔴 Live Market Status")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Current time and market status
    now = datetime.now()
    market_open = 9 <= now.hour <= 15 and now.weekday() < 5
    
    with col1:
        status = "🟢 LIVE" if market_open else "🔴 CLOSED"
        next_session = "Pre-open starts at 9:00 AM" if not market_open else "Market closes at 3:30 PM"
        
        st.markdown(f"""
        <div style='text-align: center; padding: 15px; border-radius: 10px; 
                    background-color: rgba(0,0,0,0.05);'>
            <h3 style='margin: 0; color: {"green" if market_open else "red"};'>{status}</h3>
            <p style='margin: 5px 0 0 0; font-size: 12px;'>{next_session}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        ist_time = now.strftime("%H:%M:%S")
        st.metric(
            "IST Time",
            ist_time,
            help="Indian Standard Time"
        )
    
    with col3:
        # Trading session info
        if market_open:
            session_time = now.strftime("%H:%M")
            if "09:00" <= session_time <= "09:15":
                session = "Pre-Open"
            elif "09:15" <= session_time <= "15:30":
                session = "Regular"
            elif "15:40" <= session_time <= "16:00":
                session = "Post-Close"
            else:
                session = "Extended"
        else:
            session = "Closed"
        
        st.metric("Session", session)
    
    with col4:
        # Market volatility indicator
        volatility = "Normal"  # This would be calculated from actual data
        vol_color = "green"
        
        st.markdown(f"""
        <div style='text-align: center; padding: 15px; border-radius: 10px; 
                    background-color: rgba(0,0,0,0.05);'>
            <h3 style='margin: 0; color: {vol_color};'>{volatility}</h3>
            <p style='margin: 5px 0 0 0; font-size: 12px;'>Volatility</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        # FII/DII activity indicator
        st.metric(
            "FII Activity",
            "Buying",
            "+₹2,500 Cr",
            help="Foreign Institutional Investors activity"
        )

def render_indices_dashboard(data_fetcher):
    """Render comprehensive indices dashboard"""
    st.subheader("📊 Major Indices Performance")
    
    # Fetch market data
    with st.spinner('📈 Loading indices data...'):
        market_data = data_fetcher.get_market_overview()
    
    if market_data:
        # Main indices metrics
        cols = st.columns(len(market_data))
        
        for i, (index_name, data) in enumerate(market_data.items()):
            with cols[i]:
                current = data.get('current', 0)
                change = data.get('change', 0)
                change_percent = data.get('change_percent', 0)
                volume = data.get('volume', 0)
                
                # Dynamic color and emoji
                if change_percent > 0:
                    delta_color = "normal"
                    trend_emoji = "📈"
                    bg_color = "rgba(0, 255, 0, 0.1)"
                elif change_percent < 0:
                    delta_color = "inverse"
                    trend_emoji = "📉"
                    bg_color = "rgba(255, 0, 0, 0.1)"
                else:
                    delta_color = "off"
                    trend_emoji = "➡️"
                    bg_color = "rgba(128, 128, 128, 0.1)"
                
                st.markdown(f"""
                <div style='background: {bg_color}; padding: 15px; border-radius: 10px; margin-bottom: 10px;'>
                    <h4 style='margin: 0;'>{trend_emoji} {index_name}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                st.metric(
                    label="Current Level",
                    value=f"{current:,.2f}",
                    delta=f"{change_percent:+.2f}% ({change:+.2f})",
                    delta_color=delta_color
                )
                
                if volume > 0:
                    st.caption(f"Volume: {volume:,.0f}")
        
        # Historical performance chart
        render_indices_chart(data_fetcher, market_data)
    else:
        st.warning("⚠️ Unable to load indices data. Market may be closed or experiencing connectivity issues.")
        render_indices_fallback()

def render_indices_chart(data_fetcher, market_data):
    """Render historical indices performance chart"""
    st.markdown("### 📈 Indices Trend (Last 30 Days)")
    
    # Create mock historical data for demonstration
    # In production, this would fetch actual historical data
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    
    fig = go.Figure()
    
    colors = ['#FF6B35', '#F7931E', '#FFD23F', '#06FFA5']
    
    for i, (index_name, data) in enumerate(market_data.items()):
        # Generate trend data (in production, fetch real historical data)
        base_value = data.get('current', 50000)
        trend_data = np.random.normal(0, 0.01, 30).cumsum()
        values = base_value * (1 + trend_data)
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=values,
            mode='lines',
            name=index_name,
            line=dict(color=colors[i % len(colors)], width=3),
            hovertemplate=f'{index_name}: %{{y:,.2f}}<extra></extra>'
        ))
    
    fig.update_layout(
        title="30-Day Index Performance",
        xaxis_title="Date",
        yaxis_title="Index Value",
        height=400,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_market_breadth(data_fetcher):
    """Render market breadth indicators"""
    st.subheader("🎯 Market Breadth & Health")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Advance-Decline ratio
        advances = 1250  # This would be fetched from real data
        declines = 850
        unchanged = 100
        
        ad_ratio = advances / declines if declines > 0 else 0
        
        st.metric(
            "Advance/Decline",
            f"{ad_ratio:.2f}",
            f"↗️ {advances} | ↘️ {declines}",
            help="Ratio of advancing to declining stocks"
        )
    
    with col2:
        # New highs vs new lows
        new_highs = 85
        new_lows = 25
        
        st.metric(
            "New Highs/Lows",
            f"{new_highs}/{new_lows}",
            f"+{new_highs - new_lows}",
            help="Stocks hitting 52-week highs vs lows"
        )
    
    with col3:
        # Market cap participation
        large_cap_change = 1.2
        mid_cap_change = 0.8
        small_cap_change = -0.3
        
        st.markdown("""
        **Market Cap Performance**
        - Large Cap: +1.2%
        - Mid Cap: +0.8%
        - Small Cap: -0.3%
        """)
    
    with col4:
        # Sector rotation
        leading_sector = "Banking"
        lagging_sector = "Auto"
        
        st.markdown(f"""
        **Sector Rotation**
        - Leading: {leading_sector}
        - Lagging: {lagging_sector}
        """)
    
    # Market breadth chart
    render_breadth_chart()

def render_breadth_chart():
    """Render market breadth visualization"""
    col1, col2 = st.columns(2)
    
    with col1:
        # Advance-Decline chart
        categories = ['Advances', 'Declines', 'Unchanged']
        values = [1250, 850, 100]
        colors = ['green', 'red', 'gray']
        
        fig_pie = px.pie(
            values=values,
            names=categories,
            title="Market Breadth Distribution",
            color_discrete_sequence=colors
        )
        
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Market cap performance
        market_caps = ['Large Cap', 'Mid Cap', 'Small Cap']
        performance = [1.2, 0.8, -0.3]
        colors_bar = ['green' if x > 0 else 'red' for x in performance]
        
        fig_bar = px.bar(
            x=market_caps,
            y=performance,
            title="Market Cap Performance (%)",
            color=performance,
            color_continuous_scale=['red', 'yellow', 'green']
        )
        
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

def render_sector_heatmap(data_fetcher):
    """Render sector performance heatmap"""
    st.subheader("🏭 Sector Performance Heatmap")
    
    # Fetch sector data
    with st.spinner('🔄 Loading sector performance...'):
        sector_data = data_fetcher.get_sector_performance()
    
    if sector_data:
        # Create sector heatmap
        sectors = list(sector_data.keys())
        changes = [data['avg_change'] for data in sector_data.values()]
        
        # Create a more detailed heatmap with sub-sectors
        sector_matrix = create_sector_matrix(sectors, changes)
        
        fig = px.imshow(
            sector_matrix,
            labels=dict(x="Sub-Sectors", y="Main Sectors", color="Change %"),
            x=['Large Cap', 'Mid Cap', 'Small Cap'],
            y=sectors,
            color_continuous_scale='RdYlGn',
            aspect="auto"
        )
        
        fig.update_layout(
            title="Sector Performance Heatmap",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Sector leaders and laggards
        render_sector_leaders_laggards(sectors, changes)
    else:
        st.info("📊 Sector performance data will be available during market hours")

def create_sector_matrix(sectors, changes):
    """Create sector performance matrix for heatmap"""
    matrix = []
    for change in changes:
        # Create variations for different market caps
        large_cap = change
        mid_cap = change * 1.1  # Slightly different performance
        small_cap = change * 0.9
        matrix.append([large_cap, mid_cap, small_cap])
    
    return np.array(matrix)

def render_sector_leaders_laggards(sectors, changes):
    """Render sector leaders and laggards"""
    col1, col2 = st.columns(2)
    
    # Sort sectors by performance
    sector_performance = list(zip(sectors, changes))
    sector_performance.sort(key=lambda x: x[1], reverse=True)
    
    with col1:
        st.markdown("### 🏆 Sector Leaders")
        for sector, change in sector_performance[:3]:
            st.markdown(f"""
            <div style='padding: 10px; margin: 5px; border-radius: 5px; 
                        border-left: 4px solid green; background-color: rgba(0,255,0,0.05);'>
                <strong>{sector}</strong><br>
                <span style='color: green;'>+{change:.2f}%</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📉 Sector Laggards")
        for sector, change in sector_performance[-3:]:
            st.markdown(f"""
            <div style='padding: 10px; margin: 5px; border-radius: 5px; 
                        border-left: 4px solid red; background-color: rgba(255,0,0,0.05);'>
                <strong>{sector}</strong><br>
                <span style='color: red;'>{change:.2f}%</span>
            </div>
            """, unsafe_allow_html=True)

def render_market_trends(data_fetcher, tech_analyzer):
    """Render market trends and technical patterns"""
    st.subheader("📈 Market Trends & Patterns")
    
    # Market trend indicators
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 Technical Indicators")
        
        # Mock technical indicators for market indices
        nifty_rsi = 65.2
        sensex_rsi = 63.8
        
        rsi_color = "orange" if 30 < nifty_rsi < 70 else "red" if nifty_rsi > 70 else "green"
        
        st.markdown(f"""
        **NIFTY 50 Technical:**
        - RSI: <span style='color: {rsi_color};'>{nifty_rsi}</span>
        - MACD: Bullish
        - Support: 19,200
        - Resistance: 19,800
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🔄 Market Momentum")
        
        momentum_indicators = {
            "Short Term (5D)": "Bullish",
            "Medium Term (20D)": "Bullish", 
            "Long Term (50D)": "Neutral"
        }
        
        for period, signal in momentum_indicators.items():
            color = "green" if signal == "Bullish" else "red" if signal == "Bearish" else "orange"
            emoji = "📈" if signal == "Bullish" else "📉" if signal == "Bearish" else "➡️"
            
            st.markdown(f"{period}: <span style='color: {color};'>{emoji} {signal}</span>", 
                       unsafe_allow_html=True)
    
    with col3:
        st.markdown("### 🎯 Key Levels")
        
        key_levels = {
            "NIFTY 50": {"Support": "19,200", "Resistance": "19,800"},
            "SENSEX": {"Support": "63,500", "Resistance": "65,200"}
        }
        
        for index, levels in key_levels.items():
            st.markdown(f"""
            **{index}:**
            - Support: {levels['Support']}
            - Resistance: {levels['Resistance']}
            """)

def render_economic_indicators():
    """Render economic indicators affecting markets"""
    st.subheader("🏛️ Economic Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Repo Rate",
            "6.50%",
            delta=None,
            help="RBI Policy Rate"
        )
    
    with col2:
        st.metric(
            "CPI Inflation",
            "5.69%",
            delta="+0.11%",
            help="Consumer Price Index"
        )
    
    with col3:
        st.metric(
            "USD/INR",
            "₹83.25",
            delta="+0.15",
            help="US Dollar to Indian Rupee"
        )
    
    with col4:
        st.metric(
            "10Y Bond Yield",
            "7.18%",
            delta="-0.02%",
            help="10-Year Government Bond"
        )
    
    # Economic calendar
    st.markdown("### 📅 Upcoming Economic Events")
    
    economic_events = [
        {"Date": "2025-01-15", "Event": "CPI Data Release", "Impact": "High"},
        {"Date": "2025-01-20", "Event": "RBI Policy Meeting", "Impact": "High"},
        {"Date": "2025-01-25", "Event": "GDP Growth Data", "Impact": "Medium"},
        {"Date": "2025-01-30", "Event": "Union Budget 2025", "Impact": "Very High"}
    ]
    
    for event in economic_events:
        impact_color = {
            "Very High": "red",
            "High": "orange", 
            "Medium": "yellow",
            "Low": "green"
        }.get(event["Impact"], "gray")
        
        st.markdown(f"""
        <div style='padding: 10px; margin: 5px; border-radius: 5px; 
                    border-left: 4px solid {impact_color}; background-color: rgba(0,0,0,0.02);'>
            <strong>{event['Date']}</strong> - {event['Event']}<br>
            <span style='color: {impact_color}; font-size: 12px;'>Impact: {event['Impact']}</span>
        </div>
        """, unsafe_allow_html=True)

def render_global_market_impact():
    """Render global markets impact on Indian markets"""
    st.subheader("🌍 Global Markets Impact")
    
    # Global indices performance
    global_markets = {
        "US Markets": {"DOW": "+0.25%", "NASDAQ": "+0.18%", "S&P 500": "+0.31%"},
        "Asian Markets": {"Nikkei": "+0.45%", "Hang Seng": "-0.22%", "Shanghai": "+0.15%"},
        "European Markets": {"FTSE": "+0.12%", "DAX": "+0.28%", "CAC": "+0.19%"}
    }
    
    cols = st.columns(3)
    
    for i, (region, indices) in enumerate(global_markets.items()):
        with cols[i]:
            st.markdown(f"### {region}")
            
            for index, change in indices.items():
                color = "green" if change.startswith('+') else "red"
                st.markdown(f"{index}: <span style='color: {color};'>{change}</span>", 
                           unsafe_allow_html=True)
    
    # Correlation analysis
    st.markdown("### 🔗 Market Correlations")
    
    correlations = {
        "NIFTY vs S&P 500": 0.72,
        "NIFTY vs Nikkei": 0.45,
        "NIFTY vs FTSE": 0.38,
        "Sensex vs DOW": 0.68
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        for pair, corr in list(correlations.items())[:2]:
            st.metric(pair, f"{corr:.2f}", help="Correlation coefficient")
    
    with col2:
        for pair, corr in list(correlations.items())[2:]:
            st.metric(pair, f"{corr:.2f}", help="Correlation coefficient")

def render_voice_market_features(data_fetcher, speech_handler):
    """Render voice-enabled market features"""
    st.markdown("---")
    st.subheader("🎤 Voice Market Updates")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔊 Speak Market Summary"):
            market_data = data_fetcher.get_market_overview()
            speech_handler.speak_market_summary(market_data)
    
    with col2:
        if st.button("🔊 Speak Top Movers"):
            gainers, losers = data_fetcher.get_top_gainers_losers()
            
            if gainers:
                gainer_text = f"Top gainer is {gainers[0]['name']} up by {gainers[0]['change_percent']:.2f} percent"
                speech_handler.speak_text(gainer_text)
    
    with col3:
        if st.button("🔊 Speak Market Status"):
            now = datetime.now()
            market_open = 9 <= now.hour <= 15 and now.weekday() < 5
            
            status_text = "Market is currently open" if market_open else "Market is currently closed"
            speech_handler.speak_text(status_text)

def render_indices_fallback():
    """Render fallback content when indices data is unavailable"""
    st.markdown("""
    <div style='text-align: center; padding: 40px; background-color: rgba(255, 107, 53, 0.1); 
                border-radius: 15px; margin: 20px 0;'>
        <h3>📊 बाज़ार डेटा लोड हो रहा है...</h3>
        <h4>Market Data Loading...</h4>
        <p>
            कृपया प्रतीक्षा करें जब तक हम NSE और BSE से लेटेस्ट डेटा प्राप्त करते हैं।<br>
            <em>Please wait while we fetch the latest data from NSE and BSE.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show historical context while loading
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **Did you know?**
        The NIFTY 50 index represents approximately 66% of the free-float market capitalization of all Indian stocks listed on the NSE.
        """)
    
    with col2:
        st.info("""
        **Market Timing**
        Indian stock markets operate from 9:15 AM to 3:30 PM (IST) on weekdays, with a pre-opening session from 9:00 to 9:15 AM.
        """)
