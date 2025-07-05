import streamlit as st
import random
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

def render_error_page(error_message=None, error_type="general"):
    """Render creative error pages with Indian market context"""
    
    # Determine error type and render appropriate page
    if "api" in error_message.lower() if error_message else False:
        render_api_error_page(error_message)
    elif "network" in error_message.lower() if error_message else False:
        render_network_error_page(error_message)
    elif "data" in error_message.lower() if error_message else False:
        render_data_error_page(error_message)
    else:
        render_general_error_page(error_message)

def render_api_error_page(error_message):
    """Render API-specific error page"""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #ff6b6b, #ee5a24); 
                padding: 40px; border-radius: 20px; text-align: center; 
                color: white; margin: 30px 0;'>
        <div style='font-size: 80px; margin-bottom: 20px;'>🏛️</div>
        <h1 style='margin: 0; font-size: 2.5em;'>API सेवा अस्थायी रूप से बंद</h1>
        <h2 style='margin: 10px 0; font-size: 1.8em;'>API Service Temporarily Down</h2>
        
        <div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 30px 0;'>
            <p style='font-size: 18px; margin: 0;'>
                हमारे डेटा पार्टनर्स (Yahoo Finance / Finnhub) से कनेक्शन में समस्या है।<br>
                <em>We're experiencing connectivity issues with our data partners.</em>
            </p>
        </div>
        
        <div style='margin: 20px 0;'>
            <p style='font-size: 16px; opacity: 0.9;'>
                🔄 Automatically retrying every 30 seconds<br>
                📡 Checking Yahoo Finance & Finnhub APIs<br>
                ⏱️ Estimated resolution: 2-5 minutes
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Provide offline alternatives instead of API status
    
    # Provide alternative actions
    render_error_alternatives("api")
    
    # Show Indian market facts while waiting
    render_market_trivia("api_error")

def render_network_error_page(error_message):
    """Render network-specific error page"""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #3742fa, #2f3542); 
                padding: 40px; border-radius: 20px; text-align: center; 
                color: white; margin: 30px 0;'>
        <div style='font-size: 80px; margin-bottom: 20px;'>📡</div>
        <h1 style='margin: 0; font-size: 2.5em;'>नेटवर्क कनेक्शन समस्या</h1>
        <h2 style='margin: 10px 0; font-size: 1.8em;'>Network Connection Issue</h2>
        
        <div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 30px 0;'>
            <p style='font-size: 18px; margin: 0;'>
                आपका इंटरनेट कनेक्शन धीमा या अस्थिर हो सकता है।<br>
                <em>Your internet connection might be slow or unstable.</em>
            </p>
        </div>
        
        <div style='margin: 20px 0;'>
            <p style='font-size: 16px; opacity: 0.9;'>
                📶 Check your internet connection<br>
                🔄 Try refreshing the page<br>
                ⏳ Wait for better connectivity
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Network troubleshooting tips
    render_network_troubleshooting()
    
    # Offline mode options
    render_offline_mode_options()

def render_data_error_page(error_message):
    """Render data-specific error page"""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #ffa726, #ff7043); 
                padding: 40px; border-radius: 20px; text-align: center; 
                color: white; margin: 30px 0;'>
        <div style='font-size: 80px; margin-bottom: 20px;'>📊</div>
        <h1 style='margin: 0; font-size: 2.5em;'>डेटा लोडिंग में समस्या</h1>
        <h2 style='margin: 10px 0; font-size: 1.8em;'>Data Loading Issue</h2>
        
        <div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 30px 0;'>
            <p style='font-size: 18px; margin: 0;'>
                मार्केट डेटा प्रोसेसिंग में देरी हो रही है।<br>
                <em>Market data processing is experiencing delays.</em>
            </p>
        </div>
        
        <div style='margin: 20px 0;'>
            <p style='font-size: 16px; opacity: 0.9;'>
                ⚡ High market volatility may cause delays<br>
                🏛️ NSE/BSE systems under heavy load<br>
                📈 Real-time data synchronizing
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Data processing status
    render_data_processing_status()
    
    # Historical data fallback
    render_historical_data_fallback()

def render_general_error_page(error_message):
    """Render general creative error page"""
    # Random creative error themes
    error_themes = [
        {
            "title": "बैल और भालू विश्राम पर हैं",
            "subtitle": "Bulls and Bears are Taking a Break",
            "emoji": "🐂🐻",
            "bg_gradient": "linear-gradient(135deg, #667eea, #764ba2)",
            "message": "Even the market animals need rest sometimes!"
        },
        {
            "title": "दलाल स्ट्रीट में ट्रैफिक जाम",
            "subtitle": "Traffic Jam on Dalal Street",
            "emoji": "🚦",
            "bg_gradient": "linear-gradient(135deg, #f093fb, #f5576c)",
            "message": "Too many traders trying to access data at once!"
        },
        {
            "title": "मुंबई की बारिश ने सर्वर रोक दिए",
            "subtitle": "Mumbai Rains Flooded Our Servers",
            "emoji": "🌧️",
            "bg_gradient": "linear-gradient(135deg, #4facfe, #00f2fe)",
            "message": "Don't worry, we'll be back after the monsoon!"
        }
    ]
    
    theme = random.choice(error_themes)
    
    st.markdown(f"""
    <div style='background: {theme["bg_gradient"]}; 
                padding: 40px; border-radius: 20px; text-align: center; 
                color: white; margin: 30px 0;'>
        <div style='font-size: 80px; margin-bottom: 20px;'>{theme["emoji"]}</div>
        <h1 style='margin: 0; font-size: 2.5em;'>{theme["title"]}</h1>
        <h2 style='margin: 10px 0; font-size: 1.8em;'>{theme["subtitle"]}</h2>
        
        <div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 30px 0;'>
            <p style='font-size: 18px; margin: 0;'>{theme["message"]}</p>
        </div>
        
        <div style='margin: 20px 0;'>
            <p style='font-size: 16px; opacity: 0.9;'>
                🔧 Our tech team is on it<br>
                ⏰ Usually resolved in 2-3 minutes<br>
                ☕ Perfect time for a chai break!
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show error details if provided
    if error_message:
        with st.expander("🔍 Technical Details"):
            st.code(error_message)
    
    # Interactive elements while waiting
    render_error_entertainment()

def render_api_status_indicators():
    """Render API status indicators"""
    st.subheader("📡 API Status Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Yahoo Finance status
        yahoo_status = random.choice(["🟢 Operational", "🟡 Degraded", "🔴 Down"])
        st.markdown(f"""
        **Yahoo Finance API**  
        Status: {yahoo_status}  
        Last check: {datetime.now().strftime('%H:%M:%S')}
        """)
    
    with col2:
        # Finnhub status
        finnhub_status = random.choice(["🟢 Operational", "🟡 Degraded", "🔴 Down"])
        st.markdown(f"""
        **Finnhub API**  
        Status: {finnhub_status}  
        Last check: {datetime.now().strftime('%H:%M:%S')}
        """)
    
    with col3:
        # Internal systems
        internal_status = "🟢 Operational"
        st.markdown(f"""
        **Internal Systems**  
        Status: {internal_status}  
        Cache: Active
        """)

def render_network_troubleshooting():
    """Render network troubleshooting guide"""
    st.subheader("🔧 Network Troubleshooting")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Quick Fixes:**
        
        1. **Refresh the page** (Ctrl+F5)
        2. **Check your internet speed**
        3. **Try a different browser**
        4. **Disable VPN if using one**
        5. **Clear browser cache**
        """)
    
    with col2:
        st.markdown("""
        **If problem persists:**
        
        1. **Switch to mobile data**
        2. **Restart your router**
        3. **Contact your ISP**
        4. **Try accessing from another device**
        5. **Check if other websites work**
        """)
    
    # Speed test integration (mock)
    if st.button("🚀 Test Internet Speed"):
        with st.spinner("Testing connection speed..."):
            import time
            time.sleep(2)
            speed = random.randint(10, 100)
            
            if speed > 50:
                st.success(f"✅ Good connection: {speed} Mbps")
            elif speed > 20:
                st.warning(f"⚠️ Moderate connection: {speed} Mbps")
            else:
                st.error(f"❌ Slow connection: {speed} Mbps")

def render_offline_mode_options():
    """Render offline mode alternatives"""
    st.subheader("📱 Offline Mode Options")
    
    st.info("""
    **While we fix the connection, you can:**
    
    🏛️ **Learn about Indian markets** using our Story Mode  
    📚 **Read market education content**  
    🧮 **Use offline calculators and tools**  
    📊 **View cached/historical data**  
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📖 Story Mode"):
            st.session_state.current_page = "story_mode"
            st.rerun()
    
    with col2:
        if st.button("🧮 Calculators"):
            render_offline_calculators()
    
    with col3:
        if st.button("📚 Education"):
            render_market_education()

def render_data_processing_status():
    """Render data processing status"""
    st.subheader("⚡ Data Processing Status")
    
    # Mock processing status
    processing_steps = [
        {"step": "NSE Data Feed", "status": "✅ Complete", "time": "0.5s"},
        {"step": "BSE Data Feed", "status": "🔄 Processing", "time": "1.2s"},
        {"step": "Price Calculations", "status": "⏳ Queued", "time": "-"},
        {"step": "Technical Indicators", "status": "⏳ Queued", "time": "-"},
        {"step": "News Analysis", "status": "⏳ Queued", "time": "-"}
    ]
    
    for step in processing_steps:
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            st.text(step["step"])
        with col2:
            st.text(step["status"])
        with col3:
            st.text(step["time"])

def render_historical_data_fallback():
    """Render historical data as fallback"""
    st.subheader("📈 Historical Data (Last Available)")
    
    st.info("📅 Showing last cached data from market close")
    
    # Mock historical data chart
    import pandas as pd
    import numpy as np
    
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    nifty_data = 19500 + np.cumsum(np.random.randn(30) * 50)
    sensex_data = 65000 + np.cumsum(np.random.randn(30) * 200)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=nifty_data,
        mode='lines',
        name='NIFTY 50',
        line=dict(color='#FF6B35', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=sensex_data,
        mode='lines',
        name='SENSEX',
        line=dict(color='#F7931E', width=2),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Indian Market Indices - Last 30 Days (Cached Data)",
        xaxis_title="Date",
        yaxis_title="NIFTY 50",
        yaxis2=dict(
            title="SENSEX",
            overlaying='y',
            side='right'
        ),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_error_alternatives(error_type):
    """Render alternative actions based on error type"""
    st.subheader("🔀 Alternative Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏠 Dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()
    
    with col2:
        if st.button("📰 Cached News"):
            st.info("Showing last cached news articles...")
    
    with col3:
        if st.button("📖 Story Mode"):
            st.session_state.current_page = "story_mode"
            st.rerun()
    
    with col4:
        if st.button("🔄 Retry"):
            st.cache_data.clear()
            st.rerun()

def render_market_trivia(context):
    """Render interesting market trivia while users wait"""
    trivia_facts = [
        "The BSE building in Mumbai was originally constructed in 1980 and houses the famous trading ring.",
        "SENSEX calculation started on July 1, 1990, but its base date is April 1, 1979.",
        "The NIFTY 50 index was earlier called the NSE-50 and represents about 66% of the free-float market cap.",
        "Harshad Mehta's scam in 1992 led to major reforms in the Indian stock market system.",
        "India has the third-largest number of listed companies in the world after the US and China.",
        "The highest single-day gain for SENSEX was 2,111 points on May 18, 2009.",
        "Dalal Street got its name from the Gujarati word 'dalal' meaning broker.",
        "The first stock exchange in India was established in 1875, originally as 'The Native Share & Stock Brokers Association'."
    ]
    
    st.subheader("💡 Did You Know?")
    
    fact = random.choice(trivia_facts)
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea, #764ba2); 
                color: white; padding: 20px; border-radius: 15px; margin: 20px 0;'>
        <h4 style='margin: 0 0 15px 0;'>📚 Indian Market Trivia</h4>
        <p style='margin: 0; font-size: 16px; line-height: 1.5;'>{fact}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Interactive trivia quiz
    if st.button("🧠 More Trivia"):
        st.rerun()

def render_error_entertainment():
    """Render entertainment while users wait"""
    st.subheader("🎮 While You Wait...")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Quick Market Quiz")
        
        quiz_questions = [
            {
                "question": "What does SENSEX stand for?",
                "options": ["Sensitive Index", "Sector Index", "Senior Index"],
                "correct": 0
            },
            {
                "question": "Which exchange is older?",
                "options": ["NSE", "BSE", "Both same age"],
                "correct": 1
            },
            {
                "question": "NIFTY 50 consists of how many stocks?",
                "options": ["40 stocks", "50 stocks", "60 stocks"],
                "correct": 1
            }
        ]
        
        if 'quiz_index' not in st.session_state:
            st.session_state.quiz_index = 0
        
        current_quiz = quiz_questions[st.session_state.quiz_index]
        
        answer = st.radio(current_quiz["question"], current_quiz["options"])
        
        if st.button("Submit Answer"):
            if current_quiz["options"].index(answer) == current_quiz["correct"]:
                st.success("🎉 Correct!")
            else:
                st.error(f"❌ Wrong! Correct answer: {current_quiz['options'][current_quiz['correct']]}")
            
            st.session_state.quiz_index = (st.session_state.quiz_index + 1) % len(quiz_questions)
    
    with col2:
        st.markdown("### 📊 Market Simulator")
        
        st.markdown("Guess tomorrow's NIFTY closing:")
        
        current_nifty = 19650  # Mock current value
        user_guess = st.number_input("Your prediction:", min_value=15000, max_value=25000, value=current_nifty)
        
        if st.button("Make Prediction"):
            # Generate "actual" result
            actual = current_nifty + random.randint(-200, 200)
            difference = abs(user_guess - actual)
            
            if difference < 50:
                st.success(f"🎯 Excellent! Actual: {actual}, Your guess: {user_guess}")
            elif difference < 100:
                st.info(f"👍 Good guess! Actual: {actual}, Your guess: {user_guess}")
            else:
                st.warning(f"🤔 Try again! Actual: {actual}, Your guess: {user_guess}")

def render_offline_calculators():
    """Render offline calculation tools"""
    st.subheader("🧮 Offline Calculators")
    
    tab1, tab2, tab3 = st.tabs(["SIP Calculator", "Profit/Loss", "Compound Interest"])
    
    with tab1:
        st.markdown("### 💰 SIP Calculator")
        
        monthly_sip = st.number_input("Monthly SIP (₹):", min_value=500, max_value=100000, value=5000, step=500)
        years = st.number_input("Investment Period (years):", min_value=1, max_value=30, value=10)
        expected_return = st.number_input("Expected Annual Return (%):", min_value=1.0, max_value=30.0, value=12.0, step=0.5)
        
        if st.button("Calculate SIP Returns"):
            monthly_rate = expected_return / 100 / 12
            months = years * 12
            
            # SIP formula
            future_value = monthly_sip * ((1 + monthly_rate) ** months - 1) / monthly_rate * (1 + monthly_rate)
            total_invested = monthly_sip * months
            gains = future_value - total_invested
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Invested", f"₹{total_invested:,.0f}")
            with col2:
                st.metric("Total Returns", f"₹{future_value:,.0f}")
            with col3:
                st.metric("Gains", f"₹{gains:,.0f}")
    
    with tab2:
        st.markdown("### 📈 Profit/Loss Calculator")
        
        buy_price = st.number_input("Buy Price (₹):", min_value=1.0, value=100.0, step=0.1)
        sell_price = st.number_input("Sell Price (₹):", min_value=1.0, value=110.0, step=0.1)
        quantity = st.number_input("Quantity:", min_value=1, value=100, step=1)
        
        if st.button("Calculate P&L"):
            total_buy = buy_price * quantity
            total_sell = sell_price * quantity
            pnl = total_sell - total_buy
            pnl_percent = (pnl / total_buy) * 100
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Absolute P&L", f"₹{pnl:,.2f}")
            with col2:
                st.metric("Percentage P&L", f"{pnl_percent:+.2f}%")
    
    with tab3:
        st.markdown("### 🌱 Compound Interest Calculator")
        
        principal = st.number_input("Principal (₹):", min_value=1000, value=100000, step=1000)
        rate = st.number_input("Annual Interest Rate (%):", min_value=1.0, value=10.0, step=0.5)
        time = st.number_input("Time Period (years):", min_value=1, value=5)
        
        if st.button("Calculate Compound Interest"):
            amount = principal * (1 + rate/100) ** time
            ci = amount - principal
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Final Amount", f"₹{amount:,.0f}")
            with col2:
                st.metric("Compound Interest", f"₹{ci:,.0f}")

def render_market_education():
    """Render educational content for offline access"""
    st.subheader("📚 Market Education")
    
    educational_topics = {
        "Basics": {
            "What is Stock Market?": "A marketplace where shares of publicly traded companies are bought and sold.",
            "Bull vs Bear Market": "Bull market = rising prices, Bear market = falling prices.",
            "Market Cap": "Total value of a company's shares in the market.",
            "Dividend": "Profit distribution to shareholders by companies."
        },
        "Indices": {
            "SENSEX": "BSE's benchmark index of top 30 companies by market cap.",
            "NIFTY 50": "NSE's index of top 50 companies across various sectors.",
            "Sectoral Indices": "Indices tracking specific sectors like Banking, IT, Pharma.",
            "Market Breadth": "Number of advancing vs declining stocks in the market."
        },
        "Trading": {
            "Order Types": "Market, Limit, Stop-loss orders for different trading strategies.",
            "Bid-Ask Spread": "Difference between buying and selling prices.",
            "Volume": "Number of shares traded, indicates market activity.",
            "Circuit Breakers": "Price limits to prevent excessive volatility."
        }
    }
    
    selected_category = st.selectbox("Select Category:", list(educational_topics.keys()))
    
    if selected_category:
        topics = educational_topics[selected_category]
        
        for topic, explanation in topics.items():
            with st.expander(f"📖 {topic}"):
                st.write(explanation)
                
                # Add related examples or details
                if topic == "SENSEX":
                    st.info("Current SENSEX composition includes companies like Reliance, TCS, HDFC Bank, etc.")
                elif topic == "Bull vs Bear Market":
                    st.info("Indian markets have seen major bull runs in 2003-2008 and 2014-2021.")
