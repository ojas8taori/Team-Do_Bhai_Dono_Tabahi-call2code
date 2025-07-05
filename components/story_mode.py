import streamlit as st
import time
import random
from datetime import datetime
from utils.speech_handler import SpeechHandler

def render_story_mode():
    """Render interactive story mode for learning about Indian markets"""
    
    speech_handler = SpeechHandler()
    
    # Initialize story mode state
    if 'story_step' not in st.session_state:
        st.session_state.story_step = 0
    if 'story_character' not in st.session_state:
        st.session_state.story_character = 'raj'
    if 'story_language' not in st.session_state:
        st.session_state.story_language = st.session_state.get('language', 'en')
    
    # Story mode header
    render_story_header()
    
    # Character selection
    if st.session_state.story_step == 0:
        render_character_selection()
    else:
        # Main story progression
        render_story_content(speech_handler)
    
    # Story navigation
    render_story_navigation()

def render_story_header():
    """Render story mode header with Indian theme"""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #FF6B35, #F7931E); 
                padding: 30px; border-radius: 20px; text-align: center; 
                color: white; margin-bottom: 30px; position: relative;'>
        <div style='position: absolute; top: 10px; right: 20px; font-size: 30px;'>
            🏛️
        </div>
        <h1 style='margin: 0; font-size: 2.5em;'>📚 बाज़ार की कहानी</h1>
        <h2 style='margin: 10px 0; font-size: 1.8em;'>Story Mode: Journey Through Indian Markets</h2>
        <p style='font-size: 18px; margin: 0; opacity: 0.9;'>
            एक इंटरैक्टिव यात्रा • An Interactive Learning Journey
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_character_selection():
    """Render character selection for personalized experience"""
    st.markdown("## 👥 अपना गाइड चुनें | Choose Your Guide")
    
    col1, col2, col3 = st.columns(3)
    
    characters = {
        'raj': {
            'name': 'राज | Raj',
            'description': 'Experienced trader from Mumbai',
            'emoji': '👨‍💼',
            'specialty': 'Technical Analysis',
            'background': 'A seasoned trader who has been in Dalal Street for 15 years'
        },
        'priya': {
            'name': 'प्रिया | Priya',
            'description': 'Financial analyst and educator',
            'emoji': '👩‍🏫',
            'specialty': 'Fundamental Analysis',
            'background': 'A finance professor who explains complex concepts simply'
        },
        'arjun': {
            'name': 'अर्जुन | Arjun',
            'description': 'Young fintech entrepreneur',
            'emoji': '👨‍💻',
            'specialty': 'Modern Trading Tech',
            'background': 'A tech-savvy investor who loves data and algorithms'
        }
    }
    
    for i, (char_id, char_info) in enumerate(characters.items()):
        with [col1, col2, col3][i]:
            if st.button(
                f"{char_info['emoji']} {char_info['name']}\n{char_info['description']}", 
                key=f"char_{char_id}",
                help=char_info['background']
            ):
                st.session_state.story_character = char_id
                st.session_state.story_step = 1
                st.rerun()
            
            st.markdown(f"""
            **Specialty:** {char_info['specialty']}  
            {char_info['background']}
            """)

def render_story_content(speech_handler):
    """Render main story content based on current step"""
    character = get_character_info(st.session_state.story_character)
    step = st.session_state.story_step
    
    # Story content based on step
    if step == 1:
        render_introduction(character, speech_handler)
    elif step == 2:
        render_market_basics(character, speech_handler)
    elif step == 3:
        render_exchanges_story(character, speech_handler)
    elif step == 4:
        render_indices_story(character, speech_handler)
    elif step == 5:
        render_trading_basics(character, speech_handler)
    elif step == 6:
        render_investment_strategies(character, speech_handler)
    elif step == 7:
        render_risk_management(character, speech_handler)
    elif step == 8:
        render_market_analysis(character, speech_handler)
    elif step == 9:
        render_conclusion(character, speech_handler)
    else:
        render_completion()

def get_character_info(char_id):
    """Get character information"""
    characters = {
        'raj': {
            'name': 'राज | Raj',
            'emoji': '👨‍💼',
            'voice_style': 'experienced',
            'greeting': 'नमस्ते! Welcome to the exciting world of Indian stock markets!'
        },
        'priya': {
            'name': 'प्रिया | Priya', 
            'emoji': '👩‍🏫',
            'voice_style': 'educational',
            'greeting': 'Hello! Let me guide you through the fundamentals of investing.'
        },
        'arjun': {
            'name': 'अर्जुन | Arjun',
            'emoji': '👨‍💻',
            'voice_style': 'modern',
            'greeting': 'Hey there! Ready to explore the tech side of trading?'
        }
    }
    return characters.get(char_id, characters['raj'])

def render_introduction(character, speech_handler):
    """Render introduction story"""
    st.markdown(f"## {character['emoji']} Welcome from {character['name']}")
    
    intro_content = f"""
    {character['greeting']}
    
    I'm {character['name']}, and I'll be your guide through the fascinating world of Indian stock markets. 
    
    **What we'll explore together:**
    
    🏛️ **The Story of Indian Markets**
    - How BSE became Asia's oldest stock exchange
    - The evolution from floor trading to digital
    - Major milestones in Indian market history
    
    📊 **Understanding the Basics**
    - What are stocks and how do they work?
    - NSE vs BSE - the two major exchanges
    - NIFTY 50 and SENSEX indices
    
    💡 **Practical Knowledge**
    - How to analyze stocks
    - Investment strategies for Indian markets
    - Risk management techniques
    
    Ready to begin this journey? Let's start with the basics!
    """
    
    st.markdown(intro_content)
    
    # Interactive element
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎯 Let's Start Learning!", type="primary"):
            st.session_state.story_step = 2
            st.rerun()
    
    with col2:
        if st.session_state.get('voice_enabled', False):
            if st.button("🔊 Hear Introduction"):
                speech_handler.speak_text(intro_content)
    
    # Fun fact
    render_story_fun_fact("Did you know? The Bombay Stock Exchange (BSE) was established in 1875, making it one of the oldest stock exchanges in Asia!")

def render_market_basics(character, speech_handler):
    """Render market basics story"""
    st.markdown(f"## {character['emoji']} Chapter 1: Market Fundamentals")
    
    basics_content = f"""
    Great! Let me start with the very basics, {character['name']} style.
    
    ### 🏭 What is the Stock Market?
    
    Imagine you want to start a samosa business in Mumbai. You need ₹10 lakhs but only have ₹2 lakhs. 
    You can ask 8 friends to invest ₹1 lakh each. In return, you give each friend 10% ownership in your business.
    
    **This is exactly what companies do in the stock market!**
    
    ### 📈 How Do Stock Prices Move?
    
    If your samosa business does well:
    - More people want to buy shares
    - Price goes up 📈
    
    If business is slow:
    - People want to sell shares  
    - Price goes down 📉
    
    ### 🇮🇳 The Indian Context
    
    In India, we have:
    - **Over 5,000 listed companies**
    - **2 major exchanges: NSE & BSE**
    - **Trading in Indian Rupees (₹)**
    - **Specific market hours: 9:15 AM - 3:30 PM**
    """
    
    st.markdown(basics_content)
    
    # Interactive quiz
    render_interactive_quiz("What happens to stock price when more people want to buy?", 
                          ["Price goes up", "Price goes down", "Price stays same"], 
                          0, "Correct! When demand increases, prices rise.")
    
    # Voice feature
    if st.session_state.get('voice_enabled', False):
        if st.button("🔊 Hear This Chapter"):
            speech_handler.speak_text(basics_content)

def render_exchanges_story(character, speech_handler):
    """Render story about Indian stock exchanges"""
    st.markdown(f"## {character['emoji']} Chapter 2: NSE vs BSE - The Tale of Two Exchanges")
    
    exchanges_content = f"""
    Now let me tell you the story of India's two giants: NSE and BSE.
    
    ### 🏛️ BSE (Bombay Stock Exchange) - The Veteran
    
    **Established: 1875**
    - Asia's oldest stock exchange
    - Located at Dalal Street, Mumbai
    - Home to the famous SENSEX index
    - Started under a banyan tree!
    
    **Fun Story**: In 1855, 22 stockbrokers used to meet under a banyan tree near Mumbai Town Hall. 
    This informal gathering eventually became the BSE!
    
    ### 🏢 NSE (National Stock Exchange) - The Modernizer
    
    **Established: 1992**
    - India's largest stock exchange by volume
    - Introduced electronic trading to India
    - Home to the NIFTY 50 index
    - Completely paperless from day one
    
    ### 🤔 NSE vs BSE: Which is Better?
    
    **NSE Advantages:**
    - Higher liquidity
    - Faster trade execution
    - More modern technology
    
    **BSE Advantages:**
    - Historical significance
    - More listed companies
    - Lower listing costs
    
    **Truth**: Both are excellent! Most serious traders use both exchanges.
    """
    
    st.markdown(exchanges_content)
    
    # Visual comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🏛️ BSE
        - **Founded:** 1875
        - **Companies:** 5,000+
        - **Index:** SENSEX
        - **Claim to Fame:** Oldest in Asia
        """)
    
    with col2:
        st.markdown("""
        ### 🏢 NSE  
        - **Founded:** 1992
        - **Companies:** 2,000+
        - **Index:** NIFTY 50
        - **Claim to Fame:** Largest by volume
        """)
    
    render_story_fun_fact("The famous BSE building has a statue of a bull and bear, symbolizing market ups and downs!")

def render_indices_story(character, speech_handler):
    """Render story about market indices"""
    st.markdown(f"## {character['emoji']} Chapter 3: SENSEX & NIFTY - The Market Barometers")
    
    indices_content = f"""
    Think of SENSEX and NIFTY as the "temperature" of the Indian stock market.
    
    ### 📊 SENSEX - The Original
    
    **Full Name**: BSE Sensitive Index  
    **Started**: 1986  
    **Companies**: Top 30 companies on BSE
    
    **How it works**: Like a basket of 30 best fruits from the market. 
    If most fruits are fresh (stocks doing well), the basket is valuable.
    
    **Base Value**: 100 (in 1979)  
    **Current Level**: Around 65,000+ points
    
    ### 📈 NIFTY 50 - The Modern Giant
    
    **Full Name**: National Stock Exchange Fifty  
    **Started**: 1996  
    **Companies**: Top 50 companies on NSE
    
    **Why 50?** More companies = better representation of the entire market.
    
    ### 🤔 SENSEX vs NIFTY: What's the Difference?
    
    **SENSEX (30 companies):**
    - Older and more traditional
    - Higher per-point value
    - More sensitive to large-cap moves
    
    **NIFTY 50 (50 companies):**
    - Better market representation
    - More stable
    - Preferred by institutional investors
    
    ### 💡 Pro Tip from {character['name']}:
    
    Both indices generally move in the same direction. If SENSEX is up 1%, 
    NIFTY is usually up around 1% too. They're like two friends who always 
    walk together!
    """
    
    st.markdown(indices_content)
    
    # Interactive calculation
    st.markdown("### 🧮 Let's Calculate!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sensex_points = st.number_input("If SENSEX moves from 65,000 to 65,650, what's the % change?", 
                                       min_value=0.0, max_value=10.0, step=0.1, key="sensex_calc")
        
        if sensex_points == 1.0:
            st.success("🎉 Correct! (65,650 - 65,000) / 65,000 * 100 = 1%")
        elif sensex_points > 0:
            st.info("Try again! Hint: (New - Old) / Old * 100")
    
    with col2:
        st.markdown("""
        **Quick Formula:**
        
        % Change = (New Value - Old Value) / Old Value × 100
        
        **Example:**
        - Old SENSEX: 65,000
        - New SENSEX: 65,650
        - Change: 1%
        """)

def render_trading_basics(character, speech_handler):
    """Render trading basics story"""
    st.markdown(f"## {character['emoji']} Chapter 4: How to Actually Trade")
    
    trading_content = f"""
    Now comes the exciting part - let's learn how to actually buy and sell stocks!
    
    ### 🏪 The Trading Process (Step by Step)
    
    **Step 1: Open a Demat Account**
    - Like a digital locker for your shares
    - Choose from: Zerodha, Groww, Angel One, etc.
    - Need: PAN, Aadhaar, Bank account
    
    **Step 2: Add Money**
    - Transfer money from bank to trading account
    - This is your "buying power"
    
    **Step 3: Research & Select Stocks**
    - Use our platform for analysis! 📊
    - Check company fundamentals
    - Look at technical indicators
    
    **Step 4: Place Your Order**
    
    ### 📱 Types of Orders (Made Simple)
    
    **Market Order**: "Buy now at current price"
    - ✅ Gets executed immediately
    - ❌ You might pay slightly more/less
    
    **Limit Order**: "Buy only at ₹100 or less"
    - ✅ You control the exact price
    - ❌ Might not get executed if price doesn't reach
    
    **Stop Loss**: "Sell if price falls to ₹90"
    - ✅ Protects you from big losses
    - ❌ Might sell during temporary dips
    
    ### ⏰ Market Timing
    
    **Pre-Open**: 9:00-9:15 AM (Order matching)
    **Regular**: 9:15 AM-3:30 PM (Live trading)
    **Post-Close**: 3:40-4:00 PM (Settlement)
    
    ### 💰 Trading vs Investing
    
    **Trading** (Short-term):
    - Buy today, sell tomorrow/next week
    - Higher risk, higher potential returns
    - Requires more time and attention
    
    **Investing** (Long-term):
    - Buy and hold for months/years
    - Lower risk, steady returns
    - Less time-consuming
    """
    
    st.markdown(trading_content)
    
    # Interactive order simulation
    render_order_simulation()

def render_order_simulation():
    """Render interactive order placement simulation"""
    st.markdown("### 🎮 Try Placing an Order (Simulation)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Order Details:**")
        
        order_type = st.selectbox("Order Type", ["Market", "Limit", "Stop Loss"])
        quantity = st.number_input("Quantity", min_value=1, max_value=100, value=10)
        
        if order_type == "Limit":
            limit_price = st.number_input("Limit Price (₹)", min_value=1.0, value=100.0)
        elif order_type == "Stop Loss":
            stop_price = st.number_input("Stop Loss Price (₹)", min_value=1.0, value=90.0)
        
        if st.button("Place Order (Simulation)", type="primary"):
            st.success(f"✅ {order_type} order for {quantity} shares placed successfully!")
    
    with col2:
        st.markdown("**Current Price: ₹100.50**")
        st.markdown("**Available Cash: ₹10,000**")
        
        if quantity > 0:
            estimated_cost = quantity * 100.50
            st.markdown(f"**Estimated Cost: ₹{estimated_cost:,.2f}**")
            
            if estimated_cost <= 10000:
                st.success("✅ Sufficient funds")
            else:
                st.error("❌ Insufficient funds")

def render_investment_strategies(character, speech_handler):
    """Render investment strategies story"""
    st.markdown(f"## {character['emoji']} Chapter 5: Investment Strategies for Indians")
    
    strategies_content = f"""
    Let me share some proven strategies that work well in Indian markets.
    
    ### 🎯 Strategy 1: SIP in Index Funds
    
    **What**: Systematic Investment Plan in NIFTY/SENSEX funds
    **How**: Invest ₹5,000 every month automatically
    **Why**: Rupee cost averaging + compounding power
    
    **Example**: ₹5,000/month for 10 years = ₹6 lakhs invested
    With 12% annual returns = ₹11.5 lakhs! 🚀
    
    ### 🔍 Strategy 2: Quality Stock Picking
    
    **Focus on**: Companies with these qualities
    - Consistent profit growth
    - Low debt
    - Strong management
    - Growing industry
    
    **Indian Examples**: TCS, HDFC Bank, Asian Paints, Page Industries
    
    ### 📊 Strategy 3: Sector Rotation
    
    **Concept**: Different sectors perform well at different times
    
    **Examples**:
    - **Monsoon Season**: Fertilizer, FMCG stocks
    - **Festival Season**: Auto, Consumer goods
    - **Budget Time**: Infrastructure, Defense
    - **Results Season**: All sectors based on earnings
    
    ### 🛡️ Strategy 4: Defensive Investing
    
    **For Conservative Investors**:
    - Dividend-paying stocks
    - Blue-chip companies
    - Government bonds
    - Fixed deposits
    
    ### 💡 {character['name']}'s Personal Strategy Mix:
    
    - 40% Index funds (NIFTY/SENSEX)
    - 30% Quality individual stocks
    - 20% Sector-specific funds
    - 10% International funds
    
    **Remember**: This is just an example. Your strategy should match your risk appetite!
    """
    
    st.markdown(strategies_content)
    
    # Risk appetite quiz
    render_risk_appetite_quiz()

def render_risk_appetite_quiz():
    """Render risk appetite assessment quiz"""
    st.markdown("### 🎯 What's Your Risk Appetite?")
    
    questions = [
        {
            "question": "If your investment drops 20% in a month, you would:",
            "options": ["Sell immediately", "Hold and wait", "Buy more at lower price"],
            "scores": [1, 2, 3]
        },
        {
            "question": "Your investment timeline is:",
            "options": ["Less than 1 year", "1-5 years", "More than 5 years"],
            "scores": [1, 2, 3]
        },
        {
            "question": "Your knowledge of stock markets:",
            "options": ["Beginner", "Intermediate", "Advanced"],
            "scores": [1, 2, 3]
        }
    ]
    
    total_score = 0
    
    for i, q in enumerate(questions):
        answer = st.radio(q["question"], q["options"], key=f"risk_q_{i}")
        if answer:
            score_index = q["options"].index(answer)
            total_score += q["scores"][score_index]
    
    if total_score > 0:
        if total_score <= 4:
            risk_profile = "Conservative"
            recommendation = "Focus on FDs, bonds, and blue-chip dividend stocks"
            color = "green"
        elif total_score <= 7:
            risk_profile = "Moderate"
            recommendation = "Mix of index funds, quality stocks, and some growth picks"
            color = "orange"
        else:
            risk_profile = "Aggressive"
            recommendation = "Growth stocks, small-caps, and sector-specific investments"
            color = "red"
        
        st.markdown(f"""
        <div style='padding: 20px; border-radius: 10px; background-color: rgba(0,0,0,0.05); 
                    border-left: 5px solid {color};'>
            <h4>Your Risk Profile: {risk_profile}</h4>
            <p><strong>Recommendation:</strong> {recommendation}</p>
        </div>
        """, unsafe_allow_html=True)

def render_risk_management(character, speech_handler):
    """Render risk management story"""
    st.markdown(f"## {character['emoji']} Chapter 6: Managing Risk Like a Pro")
    
    risk_content = f"""
    Risk management is what separates successful investors from gamblers. Let me teach you the golden rules.
    
    ### 🛡️ The Golden Rules of Risk Management
    
    **Rule 1: Never Put All Eggs in One Basket**
    - Don't invest more than 5% in any single stock
    - Diversify across sectors
    - Mix of large-cap, mid-cap, small-cap
    
    **Rule 2: Stop Loss is Your Best Friend**
    - Set stop loss at 10-15% below your buy price
    - Example: Buy at ₹100, set stop loss at ₹90
    - Better to lose 10% than 50%!
    
    **Rule 3: Position Sizing**
    - Start small when learning
    - Never invest money you need in next 2 years
    - Emergency fund first, then invest
    
    ### 📊 Risk vs Reward in Indian Context
    
    **Low Risk (5-8% returns)**:
    - Fixed Deposits
    - Government bonds
    - Large-cap dividend stocks
    
    **Medium Risk (8-15% returns)**:
    - Index funds
    - Blue-chip stocks
    - Balanced mutual funds
    
    **High Risk (15%+ potential returns)**:
    - Small-cap stocks
    - Sector-specific funds
    - Individual stock picking
    
    ### 🚨 Common Mistakes to Avoid
    
    **Mistake 1**: Following tips from WhatsApp groups
    **Solution**: Do your own research
    
    **Mistake 2**: Panic selling during market crashes
    **Solution**: Have a long-term view
    
    **Mistake 3**: Putting all money in "hot" stocks
    **Solution**: Diversification
    
    **Mistake 4**: Not having an emergency fund
    **Solution**: 6 months expenses in FD/savings
    
    ### 💡 {character['name']}'s Emergency Protocol
    
    **When market crashes 20%+:**
    1. Don't panic - it's normal!
    2. Check if your stocks' fundamentals are still strong
    3. If yes, consider buying more
    4. If no, cut losses and move on
    5. Never borrow money to invest more
    """
    
    st.markdown(risk_content)
    
    # Risk calculator
    render_risk_calculator()

def render_risk_calculator():
    """Render simple risk calculation tool"""
    st.markdown("### 🧮 Risk Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        total_portfolio = st.number_input("Total Portfolio Value (₹)", min_value=10000, value=100000, step=10000)
        single_stock_amount = st.number_input("Amount in Single Stock (₹)", min_value=1000, value=10000, step=1000)
        
        concentration_risk = (single_stock_amount / total_portfolio) * 100
        
        if concentration_risk > 10:
            risk_color = "red"
            risk_message = "⚠️ High concentration risk!"
        elif concentration_risk > 5:
            risk_color = "orange"
            risk_message = "⚡ Moderate risk"
        else:
            risk_color = "green"
            risk_message = "✅ Well diversified"
    
    with col2:
        st.markdown(f"""
        **Portfolio Analysis:**
        
        Concentration in single stock: **{concentration_risk:.1f}%**
        
        <div style='color: {risk_color}; font-weight: bold;'>
        {risk_message}
        </div>
        
        **Recommendation:**
        - Keep single stock exposure below 5%
        - Maximum 10% for high-conviction picks
        - Diversify across 15-20 stocks minimum
        """, unsafe_allow_html=True)

def render_market_analysis(character, speech_handler):
    """Render market analysis story"""
    st.markdown(f"## {character['emoji']} Chapter 7: Reading the Market Like a Pro")
    
    analysis_content = f"""
    Now let's learn how to analyze the market and make informed decisions.
    
    ### 📊 Fundamental Analysis - The Company Detective Work
    
    **What to Check**:
    
    **1. Financial Health**
    - Revenue growth: Is company earning more each year?
    - Profit margins: How much profit from each ₹100 revenue?
    - Debt levels: Too much debt is dangerous
    
    **2. Valuation Metrics**
    - P/E Ratio: Price to Earnings (lower is generally better)
    - Indian market average P/E: ~20-25
    - Compare with industry peers
    
    **3. Management Quality**
    - Track record of CEO/MD
    - Transparency in communications
    - Corporate governance ratings
    
    ### 📈 Technical Analysis - Reading the Charts
    
    **Basic Patterns**:
    
    **Support & Resistance**
    - Support: Price level where stock usually stops falling
    - Resistance: Price level where stock usually stops rising
    - Breakouts above resistance = bullish signal
    
    **Moving Averages**
    - 50-day MA: Short-term trend
    - 200-day MA: Long-term trend
    - When 50-day crosses above 200-day = Golden Cross (bullish)
    
    **Volume Analysis**
    - High volume + price rise = Strong momentum
    - High volume + price fall = Weak sentiment
    - Low volume moves = Less reliable
    
    ### 📰 News & Sentiment Analysis
    
    **What Moves Indian Markets**:
    - RBI policy announcements
    - Government budget
    - Monsoon predictions
    - Global events (US Fed rates, crude oil)
    - Company earnings results
    - FII/DII buying/selling
    
    ### 🎯 {character['name']}'s Analysis Checklist
    
    **Before Buying Any Stock**:
    ✅ Company growing for 3+ years?
    ✅ P/E ratio reasonable vs peers?
    ✅ Debt-to-equity ratio below 1?
    ✅ Management has good track record?
    ✅ Industry outlook positive?
    ✅ Technical charts looking good?
    ✅ Recent news positive/neutral?
    
    **If 5+ checkmarks = Consider buying**
    **If 3- checkmarks = Stay away**
    """
    
    st.markdown(analysis_content)
    
    # Interactive analysis tool
    render_stock_analysis_simulator()

def render_stock_analysis_simulator():
    """Render stock analysis simulation"""
    st.markdown("### 🔍 Stock Analysis Simulator")
    
    # Sample stock data for simulation
    sample_stocks = {
        "TCS": {"pe": 22, "debt_equity": 0.1, "revenue_growth": 8, "margin": 25},
        "RELIANCE": {"pe": 15, "debt_equity": 0.4, "revenue_growth": 12, "margin": 18},
        "ZOMATO": {"pe": -1, "debt_equity": 0.2, "revenue_growth": 65, "margin": -5}
    }
    
    selected_stock = st.selectbox("Choose a stock to analyze:", list(sample_stocks.keys()))
    
    if selected_stock:
        stock_data = sample_stocks[selected_stock]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Financial Metrics:**")
            st.write(f"P/E Ratio: {stock_data['pe']}")
            st.write(f"Debt/Equity: {stock_data['debt_equity']}")
            st.write(f"Revenue Growth: {stock_data['revenue_growth']}%")
            st.write(f"Profit Margin: {stock_data['margin']}%")
        
        with col2:
            st.markdown("**Analysis:**")
            
            score = 0
            
            # P/E analysis
            if 15 <= stock_data['pe'] <= 25:
                st.write("✅ P/E ratio looks reasonable")
                score += 1
            elif stock_data['pe'] > 25:
                st.write("⚠️ P/E ratio seems high")
            else:
                st.write("❌ Negative P/E (company losing money)")
            
            # Debt analysis
            if stock_data['debt_equity'] < 0.5:
                st.write("✅ Low debt levels")
                score += 1
            else:
                st.write("⚠️ High debt levels")
            
            # Growth analysis
            if stock_data['revenue_growth'] > 10:
                st.write("✅ Good revenue growth")
                score += 1
            else:
                st.write("⚠️ Slow revenue growth")
            
            # Margin analysis
            if stock_data['margin'] > 15:
                st.write("✅ Healthy profit margins")
                score += 1
            else:
                st.write("❌ Low/negative margins")
            
            # Final recommendation
            if score >= 3:
                st.success(f"🎯 Score: {score}/4 - Consider for investment")
            elif score >= 2:
                st.warning(f"⚡ Score: {score}/4 - Proceed with caution")
            else:
                st.error(f"🚨 Score: {score}/4 - Avoid for now")

def render_conclusion(character, speech_handler):
    """Render story conclusion"""
    st.markdown(f"## {character['emoji']} Chapter 8: Your Journey Begins!")
    
    conclusion_content = f"""
    Congratulations! 🎉 You've completed the journey through Indian stock markets with {character['name']}.
    
    ### 🎓 What You've Learned
    
    ✅ **Market Basics**: How stocks work and why prices move
    ✅ **Exchanges**: The story of NSE and BSE
    ✅ **Indices**: Understanding SENSEX and NIFTY 50
    ✅ **Trading**: How to actually buy and sell stocks
    ✅ **Strategies**: Different approaches for different goals
    ✅ **Risk Management**: Protecting your capital
    ✅ **Analysis**: Reading companies and charts
    
    ### 🚀 Your Next Steps
    
    **Immediate Actions**:
    1. Open a demat account with a good broker
    2. Start with small amounts (₹5,000-10,000)
    3. Begin with index funds or blue-chip stocks
    4. Set up SIPs for regular investing
    
    **Learning Path**:
    1. Read annual reports of companies you're interested in
    2. Follow financial news (ET, Moneycontrol, etc.)
    3. Use our platform for regular analysis
    4. Join investment communities for learning
    
    **Long-term Vision**:
    - Build a diversified portfolio over 5-10 years
    - Reinvest dividends for compounding
    - Stay disciplined during market volatility
    - Review and rebalance annually
    
    ### 💡 Final Words from {character['name']}
    
    "Remember, investing is not about getting rich quick. It's about building wealth slowly and steadily. 
    The Indian market has given excellent returns to patient investors over the long term.
    
    Stay curious, stay disciplined, and most importantly - never stop learning!
    
    Best of luck on your investment journey! 🇮🇳📈"
    
    ### 🎁 Bonus Resources
    
    **Books to Read**:
    - "The Intelligent Investor" by Benjamin Graham
    - "Coffee Can Investing" by Saurabh Mukherjea
    - "The Little Book of Common Sense Investing" by John Bogle
    
    **Websites to Follow**:
    - NSE/BSE official websites
    - Moneycontrol, Economic Times
    - Value Research for mutual funds
    - Our platform for regular analysis!
    """
    
    st.markdown(conclusion_content)
    
    # Completion certificate
    render_completion_certificate(character)

def render_completion_certificate(character):
    """Render completion certificate"""
    st.markdown("### 🏆 Certificate of Completion")
    
    completion_date = datetime.now().strftime("%B %d, %Y")
    
    certificate_html = f"""
    <div style='border: 3px solid #FF6B35; padding: 30px; text-align: center; 
                background: linear-gradient(135deg, #fff, #f8f9fa); border-radius: 15px; margin: 20px 0;'>
        <h1 style='color: #FF6B35; margin: 0;'>🏆 प्रमाण पत्र | Certificate</h1>
        <h2 style='margin: 20px 0;'>Indian Stock Market Story Mode</h2>
        
        <p style='font-size: 18px; margin: 20px 0;'>
            This certifies that you have successfully completed the interactive journey 
            through Indian stock markets with guide <strong>{character['name']}</strong>
        </p>
        
        <p style='font-size: 16px; color: #666; margin: 20px 0;'>
            Completed on: {completion_date}
        </p>
        
        <div style='margin: 30px 0;'>
            <p style='font-size: 14px; color: #888;'>
                You are now equipped with fundamental knowledge of:
            </p>
            <p style='font-size: 14px;'>
                NSE • BSE • SENSEX • NIFTY 50 • Trading • Risk Management • Analysis
            </p>
        </div>
        
        <p style='font-size: 12px; color: #999; margin: 20px 0;'>
            Bharatiya Bazaar - Indian Stock Market Platform
        </p>
    </div>
    """
    
    st.markdown(certificate_html, unsafe_allow_html=True)
    
    # Mark story mode as completed
    if st.button("🎯 Complete Story Mode", type="primary"):
        st.session_state.story_mode_completed = True
        st.success("🎉 Congratulations! You can now explore the platform freely.")
        
        if st.button("🏠 Go to Dashboard"):
            st.session_state.story_step = 0  # Reset for next time
            st.rerun()

def render_completion():
    """Render completion state"""
    st.markdown("## 🎉 Story Mode Completed!")
    
    st.markdown("""
    You have successfully completed the Indian Stock Market Story Mode!
    
    Feel free to:
    - Explore the dashboard for real-time data
    - Analyze specific stocks
    - Read market news and sentiment analysis
    - Use voice features for accessibility
    
    Thank you for learning with us! 🇮🇳
    """)
    
    if st.button("🔄 Restart Story Mode"):
        st.session_state.story_step = 0
        st.session_state.story_mode_completed = False
        st.rerun()

def render_story_navigation():
    """Render story navigation controls"""
    if st.session_state.story_step > 0:
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.session_state.story_step > 1:
                if st.button("⬅️ Previous"):
                    st.session_state.story_step -= 1
                    st.rerun()
        
        with col2:
            st.markdown(f"**Chapter {st.session_state.story_step}/8**")
        
        with col3:
            if st.session_state.story_step < 9:
                if st.button("Next ➡️"):
                    st.session_state.story_step += 1
                    st.rerun()

def render_interactive_quiz(question, options, correct_index, explanation):
    """Render interactive quiz element"""
    st.markdown("### 🧠 Quick Quiz")
    
    answer = st.radio(question, options, key=f"quiz_{question[:20]}")
    
    if answer:
        if options.index(answer) == correct_index:
            st.success(f"✅ {explanation}")
        else:
            st.error(f"❌ Try again! Correct answer: {options[correct_index]}")

def render_story_fun_fact(fact):
    """Render fun fact box"""
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea, #764ba2); 
                color: white; padding: 15px; border-radius: 10px; margin: 20px 0;'>
        <h4 style='margin: 0 0 10px 0;'>💡 Did You Know?</h4>
        <p style='margin: 0; font-size: 14px;'>{fact}</p>
    </div>
    """, unsafe_allow_html=True)
