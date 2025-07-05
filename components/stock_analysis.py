import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from utils.data_fetcher import DataFetcher
from utils.technical_analysis import TechnicalAnalyzer
from utils.speech_handler import SpeechHandler

def render_stock_analysis():
    """Render the stock analysis page"""
    
    # Initialize components
    data_fetcher = DataFetcher()
    tech_analyzer = TechnicalAnalyzer()
    speech_handler = SpeechHandler()
    
    # Page header
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1>📊 Stock Technical Analysis</h1>
        <p style='color: #666; font-size: 18px;'>Deep dive into Indian stock fundamentals and technicals</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stock selection section
    render_stock_selector(data_fetcher)
    
    # Main analysis content
    if 'selected_stock' in st.session_state and st.session_state.selected_stock:
        stock_symbol = st.session_state.selected_stock
        
        with st.spinner(f'🔍 Analyzing {stock_symbol}...'):
            # Fetch stock data
            stock_data = data_fetcher.get_stock_data(stock_symbol, "1y")
            
            if stock_data:
                render_stock_overview(stock_data, data_fetcher)
                render_technical_analysis(stock_data, tech_analyzer, stock_symbol)
                render_price_charts(stock_data, tech_analyzer, stock_symbol)
                render_trading_signals(stock_data, tech_analyzer)
                
                # Voice features
                if st.session_state.get('voice_enabled', False):
                    render_voice_analysis_features(stock_symbol, tech_analyzer, stock_data, speech_handler)
            else:
                render_stock_error_page()
    else:
        render_stock_selection_guide()

def render_stock_selector(data_fetcher):
    """Render stock selection interface"""
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        # Load sector-wise organization for better UX
        try:
            import json
            with open("assets/indian_stocks.json", "r", encoding="utf-8") as f:
                stock_data = json.load(f)
            
            # Create sector-wise stock organization
            sector_options = ["All Stocks"] + list(stock_data.get("sector_wise_stocks", {}).keys())
            selected_sector = st.selectbox(
                "🏭 Filter by Sector:",
                options=sector_options,
                help="Filter stocks by business sector"
            )
            
            # Get stocks based on sector selection
            if selected_sector == "All Stocks":
                available_stocks = list(data_fetcher.indian_symbols.keys())
            else:
                sector_stocks = stock_data.get("sector_wise_stocks", {}).get(selected_sector, {})
                available_stocks = list(sector_stocks.keys())
            
            # Sort stocks alphabetically by company name
            available_stocks.sort(key=lambda x: data_fetcher.indian_symbols.get(x, x))
            
        except Exception as e:
            # Fallback to all stocks if sector loading fails
            available_stocks = list(data_fetcher.indian_symbols.keys())
            available_stocks.sort(key=lambda x: data_fetcher.indian_symbols.get(x, x))
        
        selected_stock = st.selectbox(
            "📈 Select Stock for Analysis:",
            options=available_stocks,
            format_func=lambda x: f"{x.replace('.NS', '')} - {data_fetcher.indian_symbols.get(x, 'Unknown')}",
            help=f"Choose from {len(available_stocks)} Indian stocks listed on NSE"
        )
        
        st.session_state.selected_stock = selected_stock
    
    with col2:
        # Time period selection
        time_periods = {
            "1mo": "1 Month",
            "3mo": "3 Months", 
            "6mo": "6 Months",
            "1y": "1 Year",
            "2y": "2 Years",
            "5y": "5 Years"
        }
        
        selected_period = st.selectbox(
            "📅 Analysis Period:",
            options=list(time_periods.keys()),
            format_func=lambda x: time_periods[x],
            index=3,  # Default to 1 year
            help="Select time period for historical analysis"
        )
        
        st.session_state.analysis_period = selected_period
    
    with col3:
        if st.button("🔄 Analyze", type="primary"):
            if selected_stock:
                st.rerun()
            else:
                st.warning("Please select a stock first")

def render_stock_overview(stock_data, data_fetcher):
    """Render stock overview section"""
    st.subheader("📋 Stock Overview")
    
    # Get basic info
    info = stock_data.get('info', {})
    history = stock_data['history']
    latest = history.iloc[-1]
    prev = history.iloc[-2] if len(history) > 1 else latest
    
    # Calculate metrics
    current_price = latest['Close']
    change = current_price - prev['Close']
    change_percent = (change / prev['Close']) * 100 if prev['Close'] != 0 else 0
    
    # Display key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Current Price",
            f"₹{current_price:.2f}",
            f"{change:+.2f} ({change_percent:+.2f}%)"
        )
    
    with col2:
        st.metric(
            "Day High",
            f"₹{latest['High']:.2f}"
        )
    
    with col3:
        st.metric(
            "Day Low", 
            f"₹{latest['Low']:.2f}"
        )
    
    with col4:
        st.metric(
            "Volume",
            f"{latest['Volume']:,}"
        )
    
    with col5:
        # Calculate 52-week high/low
        week_52_high = history['High'].max()
        week_52_low = history['Low'].min()
        st.metric(
            "52W High/Low",
            f"₹{week_52_high:.2f}",
            f"Low: ₹{week_52_low:.2f}"
        )
    
    # Company information if available
    if info:
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if 'longBusinessSummary' in info:
                st.markdown("**Business Summary:**")
                st.write(info['longBusinessSummary'][:500] + "..." if len(info.get('longBusinessSummary', '')) > 500 else info.get('longBusinessSummary', 'Not available'))
        
        with col2:
            st.markdown("**Key Information:**")
            key_info = []
            
            if 'sector' in info:
                key_info.append(f"**Sector:** {info['sector']}")
            if 'industry' in info:
                key_info.append(f"**Industry:** {info['industry']}")
            if 'marketCap' in info:
                market_cap = info['marketCap'] / 10000000  # Convert to crores
                key_info.append(f"**Market Cap:** ₹{market_cap:.0f} Cr")
            if 'dividendYield' in info and info['dividendYield']:
                key_info.append(f"**Dividend Yield:** {info['dividendYield']*100:.2f}%")
            
            for item in key_info:
                st.markdown(item)

def render_technical_analysis(stock_data, tech_analyzer, stock_symbol):
    """Render technical analysis section"""
    st.subheader("🔬 Technical Analysis")
    
    # Get technical summary
    tech_summary = tech_analyzer.get_technical_summary(stock_data['history'])
    
    # Overall signal display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        signal = tech_summary['overall_signal']
        signal_color = {
            'BUY': 'green',
            'SELL': 'red', 
            'HOLD': 'orange'
        }
        
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; border-radius: 10px; 
                    background-color: rgba(0,0,0,0.05); border: 2px solid {signal_color.get(signal, 'gray')};'>
            <h2 style='color: {signal_color.get(signal, 'gray')}; margin: 0;'>{signal}</h2>
            <p style='margin: 5px 0 0 0;'>Overall Signal</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        strength = tech_summary['signal_strength']
        st.metric(
            "Signal Strength",
            f"{strength:.0f}%",
            help="Confidence level of the technical signal"
        )
    
    with col3:
        rsi = tech_summary['rsi']
        rsi_status = "Overbought" if rsi > 70 else "Oversold" if rsi < 30 else "Normal"
        rsi_color = "red" if rsi > 70 else "green" if rsi < 30 else "blue"
        
        st.markdown(f"""
        <div style='text-align: center; padding: 15px; border-radius: 8px; 
                    background-color: rgba(0,0,0,0.05);'>
            <h3 style='color: {rsi_color}; margin: 0;'>{rsi:.1f}</h3>
            <p style='margin: 5px 0 0 0;'>RSI ({rsi_status})</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Technical indicators breakdown
    st.markdown("---")
    st.markdown("### 📊 Individual Indicators")
    
    col1, col2, col3 = st.columns(3)
    
    signals = tech_summary['individual_signals']
    
    with col1:
        ma_signal = signals.get('ma_crossover', 0)
        ma_text = "Bullish" if ma_signal > 0 else "Bearish" if ma_signal < 0 else "Neutral"
        ma_emoji = "📈" if ma_signal > 0 else "📉" if ma_signal < 0 else "➡️"
        
        st.markdown(f"""
        **Moving Average Crossover**  
        {ma_emoji} {ma_text}
        """)
    
    with col2:
        rsi_signal = signals.get('rsi', 0)
        rsi_text = "Buy Signal" if rsi_signal > 0 else "Sell Signal" if rsi_signal < 0 else "Neutral"
        rsi_emoji = "🟢" if rsi_signal > 0 else "🔴" if rsi_signal < 0 else "🟡"
        
        st.markdown(f"""
        **RSI Signal**  
        {rsi_emoji} {rsi_text}
        """)
    
    with col3:
        macd_signal = signals.get('macd', 0)
        macd_text = "Bullish Cross" if macd_signal > 0 else "Bearish Cross" if macd_signal < 0 else "No Signal"
        macd_emoji = "🟢" if macd_signal > 0 else "🔴" if macd_signal < 0 else "⚪"
        
        st.markdown(f"""
        **MACD Signal**  
        {macd_emoji} {macd_text}
        """)
    
    # Support and resistance levels
    if tech_summary['support_levels'] or tech_summary['resistance_levels']:
        st.markdown("---")
        st.markdown("### 🎯 Support & Resistance Levels")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if tech_summary['support_levels']:
                st.markdown("**Support Levels:**")
                for level in tech_summary['support_levels'][-3:]:  # Show last 3
                    st.markdown(f"• ₹{level:.2f}")
        
        with col2:
            if tech_summary['resistance_levels']:
                st.markdown("**Resistance Levels:**")
                for level in tech_summary['resistance_levels'][-3:]:  # Show last 3
                    st.markdown(f"• ₹{level:.2f}")

def render_price_charts(stock_data, tech_analyzer, stock_symbol):
    """Render interactive price charts"""
    st.subheader("📈 Interactive Charts")
    
    # Chart type selection
    chart_type = st.radio(
        "Select Chart Type:",
        ["Candlestick with Indicators", "Line Chart", "Volume Analysis"],
        horizontal=True
    )
    
    if chart_type == "Candlestick with Indicators":
        # Technical analysis chart
        fig = tech_analyzer.create_technical_chart(stock_data['history'], stock_symbol)
        st.plotly_chart(fig, use_container_width=True)
        
    elif chart_type == "Line Chart":
        # Simple line chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=stock_data['history'].index,
            y=stock_data['history']['Close'],
            mode='lines',
            name='Close Price',
            line=dict(color='#FF6B35', width=2)
        ))
        
        # Add moving averages
        sma_20 = tech_analyzer.calculate_sma(stock_data['history']['Close'], 20)
        sma_50 = tech_analyzer.calculate_sma(stock_data['history']['Close'], 50)
        
        fig.add_trace(go.Scatter(
            x=stock_data['history'].index,
            y=sma_20,
            mode='lines',
            name='SMA 20',
            line=dict(color='orange', width=1)
        ))
        
        fig.add_trace(go.Scatter(
            x=stock_data['history'].index,
            y=sma_50,
            mode='lines',
            name='SMA 50',
            line=dict(color='blue', width=1)
        ))
        
        fig.update_layout(
            title=f'{stock_symbol} - Price Movement',
            xaxis_title='Date',
            yaxis_title='Price (₹)',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    elif chart_type == "Volume Analysis":
        # Volume analysis chart
        fig = go.Figure()
        
        # Price line
        fig.add_trace(go.Scatter(
            x=stock_data['history'].index,
            y=stock_data['history']['Close'],
            mode='lines',
            name='Price',
            yaxis='y',
            line=dict(color='#FF6B35')
        ))
        
        # Volume bars
        volume_colors = ['green' if stock_data['history']['Close'].iloc[i] >= stock_data['history']['Open'].iloc[i] 
                        else 'red' for i in range(len(stock_data['history']))]
        
        fig.add_trace(go.Bar(
            x=stock_data['history'].index,
            y=stock_data['history']['Volume'],
            name='Volume',
            yaxis='y2',
            marker_color=volume_colors,
            opacity=0.7
        ))
        
        # Volume moving average
        volume_sma = tech_analyzer.calculate_volume_sma(stock_data['history']['Volume'])
        fig.add_trace(go.Scatter(
            x=stock_data['history'].index,
            y=volume_sma,
            mode='lines',
            name='Volume SMA',
            yaxis='y2',
            line=dict(color='purple', dash='dash')
        ))
        
        fig.update_layout(
            title=f'{stock_symbol} - Price vs Volume',
            xaxis_title='Date',
            yaxis=dict(title='Price (₹)', side='left'),
            yaxis2=dict(title='Volume', side='right', overlaying='y'),
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)

def render_trading_signals(stock_data, tech_analyzer):
    """Render trading signals and recommendations"""
    st.subheader("🎯 Trading Recommendations")
    
    # Get recent signals
    signals = tech_analyzer.generate_signals(stock_data['history'])
    
    # Create recommendation based on signals
    signal_strength = sum(signals.values())
    
    if signal_strength >= 2:
        recommendation = "STRONG BUY"
        rec_color = "green"
        rec_emoji = "🟢"
    elif signal_strength == 1:
        recommendation = "BUY"
        rec_color = "lightgreen"
        rec_emoji = "🟢"
    elif signal_strength == -1:
        recommendation = "SELL"
        rec_color = "lightcoral"
        rec_emoji = "🔴"
    elif signal_strength <= -2:
        recommendation = "STRONG SELL"
        rec_color = "red"
        rec_emoji = "🔴"
    else:
        recommendation = "HOLD"
        rec_color = "orange"
        rec_emoji = "🟡"
    
    # Display recommendation
    st.markdown(f"""
    <div style='text-align: center; padding: 25px; border-radius: 15px; 
                background-color: {rec_color}; color: white; margin: 20px 0;'>
        <h2 style='margin: 0;'>{rec_emoji} {recommendation}</h2>
        <p style='margin: 10px 0 0 0; opacity: 0.9;'>Based on current technical indicators</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Trading plan suggestions
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Trading Plan")
        
        current_price = stock_data['history']['Close'].iloc[-1]
        
        if recommendation in ["BUY", "STRONG BUY"]:
            entry_price = current_price
            stop_loss = current_price * 0.95  # 5% stop loss
            target_1 = current_price * 1.08   # 8% target
            target_2 = current_price * 1.15   # 15% target
            
            st.markdown(f"""
            **Entry:** ₹{entry_price:.2f}  
            **Stop Loss:** ₹{stop_loss:.2f} (-5%)  
            **Target 1:** ₹{target_1:.2f} (+8%)  
            **Target 2:** ₹{target_2:.2f} (+15%)  
            """)
            
        elif recommendation in ["SELL", "STRONG SELL"]:
            st.markdown(f"""
            **Current Price:** ₹{current_price:.2f}  
            **Recommendation:** Consider selling  
            **Re-entry:** Wait for support levels  
            """)
            
        else:  # HOLD
            st.markdown(f"""
            **Current Price:** ₹{current_price:.2f}  
            **Recommendation:** Hold position  
            **Action:** Monitor for breakout signals  
            """)
    
    with col2:
        st.markdown("### ⚠️ Risk Management")
        st.markdown("""
        **Important Notes:**
        - Always use stop losses
        - Don't invest more than 5% in single stock
        - Monitor market conditions
        - Technical analysis is not guaranteed
        - Consider fundamental analysis too
        
        **Disclaimer:** This is for educational purposes only. 
        Please consult a financial advisor before trading.
        """)

def render_voice_analysis_features(stock_symbol, tech_analyzer, stock_data, speech_handler):
    """Render voice-enabled analysis features"""
    st.markdown("---")
    st.subheader("🎤 Voice Analysis Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔊 Speak Technical Analysis"):
            tech_summary = tech_analyzer.get_technical_summary(stock_data['history'])
            speech_handler.speak_stock_analysis(stock_symbol, tech_summary)
    
    with col2:
        if st.button("🔊 Speak Current Price"):
            current_price = stock_data['history']['Close'].iloc[-1]
            price_text = f"Current price of {stock_symbol.replace('.NS', '')} is {current_price:.2f} rupees"
            speech_handler.speak_text(price_text)
    
    with col3:
        if st.button("🔊 Speak Trading Signal"):
            tech_summary = tech_analyzer.get_technical_summary(stock_data['history'])
            signal = tech_summary['overall_signal']
            strength = tech_summary['signal_strength']
            signal_text = f"Trading signal for {stock_symbol.replace('.NS', '')} is {signal} with {strength:.0f} percent confidence"
            speech_handler.speak_text(signal_text)

def render_stock_error_page():
    """Render creative error page for stock analysis"""
    st.markdown("""
    <div style='text-align: center; padding: 50px; background: linear-gradient(135deg, #FF6B35, #F7931E); 
                border-radius: 20px; color: white; margin: 30px 0;'>
        <h1>🏛️ स्टॉक डेटा अनुपलब्ध</h1>
        <h2>Stock Data Temporarily Unavailable</h2>
        
        <div style='margin: 30px 0;'>
            <p style='font-size: 18px; margin: 10px 0;'>
                🕐 बाज़ार के घंटों के दौरान फिर से कोशिश करें<br>
                <em>Please try again during market hours</em>
            </p>
            
            <p style='font-size: 16px; opacity: 0.9;'>
                📊 NSE: 9:15 AM - 3:30 PM IST<br>
                📈 BSE: 9:15 AM - 3:30 PM IST
            </p>
        </div>
        
        <div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0;'>
            <h3>🔄 What's happening?</h3>
            <p>Our systems are connecting to market data providers. This usually takes just a moment!</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Alternative actions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📰 Check Market News"):
            st.session_state.current_page = "news_feed"
            st.rerun()
    
    with col2:
        if st.button("📊 Market Overview"):
            st.session_state.current_page = "market_overview"
            st.rerun()
    
    with col3:
        if st.button("🏠 Back to Dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()

def render_stock_selection_guide():
    """Render guide for stock selection"""
    st.markdown("""
    <div style='text-align: center; padding: 40px; background-color: rgba(255, 107, 53, 0.1); 
                border-radius: 15px; margin: 20px 0;'>
        <h2>📈 Select a Stock for Analysis</h2>
        <p style='font-size: 18px; color: #666;'>
            Choose from popular Indian stocks to get detailed technical analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Popular stock categories
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🏦 Banking Stocks
        - HDFCBANK.NS - HDFC Bank
        - KOTAKBANK.NS - Kotak Bank
        - ICICIBANK.NS - ICICI Bank
        """)
    
    with col2:
        st.markdown("""
        ### 💻 IT Stocks  
        - TCS.NS - Tata Consultancy
        - INFY.NS - Infosys
        - WIPRO.NS - Wipro
        """)
    
    with col3:
        st.markdown("""
        ### 🏭 Large Cap Stocks
        - RELIANCE.NS - Reliance Industries
        - LT.NS - Larsen & Toubro
        - ITC.NS - ITC Limited
        """)
    
    st.info("💡 **Tip:** Use the dropdown above to select any stock and start your analysis!")
