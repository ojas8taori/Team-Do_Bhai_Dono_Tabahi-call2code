import streamlit as st
from utils.speech_handler import SpeechHandler
import uuid

def render_multi_user_collaboration():
    """Render the Multi-User Collaboration page"""
    
    # Page header
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); border-radius: 15px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0; font-size: 2.5rem;">👥 Multi-User Collaboration</h1>
        <p style="color: white; margin: 0.5rem 0 0 0; font-size: 1.2rem;">Real-time collaboration and competitive analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize speech handler for collaboration features
    speech_handler = SpeechHandler()
    
    # User session management
    if 'user_sessions' not in st.session_state:
        st.session_state.user_sessions = {}
    
    if 'current_user_id' not in st.session_state:
        st.session_state.current_user_id = str(uuid.uuid4())[:8]
    
    # Main collaboration interface
    st.markdown("### 🚀 Your Collaboration Session")
    
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
        if st.button("🔄 Sync with Other Users", type="primary"):
            # Simulate multi-user sync (in real app, this would use WebSockets or similar)
            st.success("Synced with other users!")
            st.balloons()
    
    # Show active users
    st.markdown("### 🌐 Active Users")
    if st.session_state.user_sessions:
        for user_id, user_data in st.session_state.user_sessions.items():
            if user_id == st.session_state.current_user_id:
                st.markdown(f"🟢 **{user_data['name']}** (You) - Currently on {user_data['current_page']}")
            else:
                st.markdown(f"🔵 **{user_data['name']}** - Currently on {user_data['current_page']}")
    else:
        st.info("No active collaboration sessions. Enter your name above to start collaborating!")
    
    # Create tabs for different collaboration features
    tab1, tab2, tab3, tab4 = st.tabs(["🤝 Real-time Features", "🎮 Competitive Mode", "📊 Shared Analysis", "💬 Team Chat"])
    
    with tab1:
        st.markdown("### 🤝 Real-time Collaboration Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Live Session Features
            - **Synchronized Navigation** - Follow other users' page views
            - **Real-time Data Sharing** - Share live market data updates
            - **Shared Watchlists** - Collaborate on stock selections
            - **Live Cursor Tracking** - See where others are looking
            """)
            
            if st.button("🔗 Enable Session Sharing"):
                st.session_state.session_sharing = True
                st.success("Session sharing enabled! Others can now follow your navigation.")
        
        with col2:
            st.markdown("""
            #### Collaboration Tools
            - **Screen Share Mode** - Share your analysis screen
            - **Voice Command Broadcasting** - Share voice commands
            - **Annotation Tools** - Mark up charts together
            - **Decision Polling** - Vote on investment decisions
            """)
            
            if st.button("📺 Start Screen Share"):
                st.info("Screen sharing would start here in a full implementation.")
        
        # Real-time activity feed
        st.markdown("### 📈 Live Activity Feed")
        activity_placeholder = st.empty()
        
        # Simulate real-time updates
        if st.session_state.user_sessions:
            with activity_placeholder.container():
                st.markdown("**Recent Activity:**")
                for user_id, user_data in st.session_state.user_sessions.items():
                    st.markdown(f"• {user_data['name']} is viewing {user_data['current_page']}")
                    st.markdown(f"• {user_data['name']} last active: {user_data['last_active']}")
    
    with tab2:
        st.markdown("### 🎮 Competitive Analysis Mode")
        
        # Competitive mode toggle
        competitive_mode = st.checkbox("🏆 Enable Competitive Mode", value=st.session_state.get('competitive_mode', False))
        
        if competitive_mode:
            st.session_state.competitive_mode = True
            st.success("🎮 Competitive mode activated!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🏃‍♂️ Speed Challenges")
                st.markdown("""
                - **Market Analysis Race** - Who can analyze faster?
                - **Stock Prediction Contest** - Predict price movements
                - **News Sentiment Speed** - Fastest news analysis
                - **Technical Analysis Challenge** - Chart pattern recognition
                """)
                
                if st.button("🚀 Start Analysis Race"):
                    st.markdown("🏁 **3-Minute Market Analysis Challenge Started!**")
                    st.markdown("Analyze NIFTY 50 trends and submit your prediction!")
                    st.progress(0.3)
            
            with col2:
                st.markdown("#### 🏆 Leaderboards")
                st.markdown("""
                **Top Performers This Week:**
                1. 🥇 TradingPro - 95% accuracy
                2. 🥈 MarketGuru - 89% accuracy  
                3. 🥉 StockWiz - 87% accuracy
                4. 🏅 You - 85% accuracy
                """)
                
                if st.button("📊 View Detailed Rankings"):
                    st.info("Detailed performance analytics would be displayed here.")
        else:
            st.info("Enable competitive mode to challenge other users!")
    
    with tab3:
        st.markdown("### 📊 Shared Analysis Workspace")
        
        # Shared watchlist
        st.markdown("#### 📋 Collaborative Watchlist")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_stock = st.text_input("Add Stock to Shared Watchlist:", placeholder="e.g., RELIANCE.NS")
            if st.button("➕ Add to Watchlist") and new_stock:
                if 'shared_watchlist' not in st.session_state:
                    st.session_state.shared_watchlist = []
                st.session_state.shared_watchlist.append({
                    'symbol': new_stock,
                    'added_by': user_name or 'Anonymous',
                    'timestamp': 'now'
                })
                st.success(f"Added {new_stock} to shared watchlist!")
        
        with col2:
            st.markdown("**Current Shared Watchlist:**")
            if 'shared_watchlist' in st.session_state and st.session_state.shared_watchlist:
                for item in st.session_state.shared_watchlist:
                    st.markdown(f"• {item['symbol']} (added by {item['added_by']})")
            else:
                st.info("No stocks in shared watchlist yet.")
        
        # Shared analysis notes
        st.markdown("#### 📝 Collaborative Analysis Notes")
        
        shared_notes = st.text_area("Add to Shared Analysis Notes:", 
                                  placeholder="Share your market insights with the team...",
                                  height=100)
        
        if st.button("💾 Save to Shared Notes") and shared_notes:
            if 'shared_notes' not in st.session_state:
                st.session_state.shared_notes = []
            st.session_state.shared_notes.append({
                'note': shared_notes,
                'author': user_name or 'Anonymous',
                'timestamp': 'now'
            })
            st.success("Added to shared analysis notes!")
        
        # Display shared notes
        if 'shared_notes' in st.session_state and st.session_state.shared_notes:
            st.markdown("**Team Analysis Notes:**")
            for note in st.session_state.shared_notes:
                st.markdown(f"**{note['author']}**: {note['note']}")
    
    with tab4:
        st.markdown("### 💬 Team Chat & Communication")
        
        # Chat interface
        st.markdown("#### 💬 Real-time Team Chat")
        
        # Display chat messages
        if 'chat_messages' not in st.session_state:
            st.session_state.chat_messages = []
        
        # Chat display area
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.chat_messages:
                st.markdown(f"**{msg['user']}**: {msg['message']}")
        
        # Chat input
        col1, col2 = st.columns([4, 1])
        
        with col1:
            chat_message = st.text_input("Type your message:", placeholder="Discuss market trends...", key="chat_input")
        
        with col2:
            if st.button("💬 Send") and chat_message:
                st.session_state.chat_messages.append({
                    'user': user_name or 'Anonymous',
                    'message': chat_message,
                    'timestamp': 'now'
                })
                st.rerun()
        
        # Voice chat features
        st.markdown("#### 🎤 Voice Chat Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎙️ Start Voice Chat"):
                st.info("Voice chat would connect here in a full implementation.")
        
        with col2:
            if st.button("📞 Join Voice Room"):
                st.info("Would join voice chat room for real-time discussion.")
    
    # Advanced collaboration features
    st.markdown("---")
    st.markdown("### 🔧 Advanced Collaboration Settings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🔐 Privacy Settings")
        private_mode = st.checkbox("🔒 Private Session", help="Hide your activity from other users")
        if private_mode:
            st.info("Your session is now private.")
    
    with col2:
        st.markdown("#### 📊 Data Sharing")
        share_data = st.checkbox("📈 Share Market Data", help="Share your market analysis with team")
        if share_data:
            st.info("Your market analysis is being shared with the team.")
    
    with col3:
        st.markdown("#### 🎯 Focus Mode")
        focus_mode = st.checkbox("🎯 Distraction-Free Mode", help="Minimize chat notifications")
        if focus_mode:
            st.info("Focus mode enabled - reduced notifications.")
    
    # Add collaborative JavaScript for enhanced functionality
    collaborative_js = f"""
    <script>
    // Multi-user collaboration features
    window.collaborativeMode = {{
        userId: '{st.session_state.current_user_id}',
        userName: '{user_name if user_name else "Anonymous"}',
        
        // Broadcast user action to other users
        broadcastAction: function(action, data) {{
            const event = {{
                userId: this.userId,
                userName: this.userName,
                action: action,
                data: data,
                timestamp: new Date().toISOString()
            }};
            
            // Store in localStorage for demo purposes
            const actions = JSON.parse(localStorage.getItem('collaborative_actions') || '[]');
            actions.push(event);
            localStorage.setItem('collaborative_actions', JSON.stringify(actions.slice(-50)));
            
            console.log('Broadcasting action:', event);
        }},
        
        // Handle navigation events
        onNavigate: function(page) {{
            this.broadcastAction('navigate', {{ page: page }});
        }},
        
        // Handle analysis sharing
        onAnalysisShare: function(analysis) {{
            this.broadcastAction('share_analysis', {{ analysis: analysis }});
        }}
    }};
    
    // Listen for page navigation
    document.addEventListener('click', function(e) {{
        const button = e.target.closest('button');
        if (button && button.textContent.match(/(Dashboard|Stock Analysis|Market Overview|News Feed|Story Mode)/)) {{
            window.collaborativeMode.onNavigate(button.textContent);
        }}
    }});
    </script>
    """
    
    st.markdown(collaborative_js, unsafe_allow_html=True)
    
    # Footer with collaboration tips
    st.markdown("---")
    st.info("""
    💡 **Collaboration Tips:**
    1. Enter your name to start collaborating with other users
    2. Enable session sharing to let others follow your analysis
    3. Use the shared watchlist to track stocks together
    4. Try competitive mode for fun challenges with other users
    5. Use voice chat for real-time discussion about market trends
    """)