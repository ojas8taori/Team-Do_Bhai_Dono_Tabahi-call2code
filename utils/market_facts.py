"""
Market facts and loading content for the Indian Stock Market
"""

import random

class MarketFacts:
    def __init__(self):
        self.facts = [
            "📈 The BSE Sensex was first compiled in 1986 and is Asia's first stock exchange.",
            "🏛️ NSE is the world's largest derivatives exchange by number of contracts traded.",
            "💰 India's stock market is worth over $4 trillion, making it the 5th largest globally.",
            "🕘 Indian markets trade for 6 hours and 15 minutes, from 9:15 AM to 3:30 PM IST.",
            "📊 Over 5,000 companies are listed on Indian stock exchanges.",
            "🎯 The NIFTY 50 represents about 65% of the free-float market capitalization.",
            "⚡ NSE processes over 6 billion trades daily on average.",
            "🏆 India has the highest number of retail investors globally - over 9 crore accounts.",
            "📱 Over 70% of trades in India now happen through mobile apps.",
            "💎 Reliance Industries is India's most valuable company by market cap.",
            "🔄 Circuit breakers halt trading if markets fall/rise by 10%, 15%, or 20%.",
            "📈 Bull markets in India are often driven by monsoon forecasts and budget announcements.",
            "🌟 TCS was the first Indian company to cross $100 billion market cap.",
            "⏰ Pre-market trading happens from 9:00-9:15 AM for price discovery.",
            "🏦 SBI is India's largest bank by assets and market capitalization.",
            "📊 F&O segment contributes to over 95% of total turnover on NSE.",
            "🎨 Green candles indicate price rise, red candles indicate price fall in charts.",
            "💡 Dividend yield in Indian markets averages around 1.2% annually.",
            "🔔 Market orders are executed immediately, limit orders wait for target price.",
            "📈 Indian markets have given average returns of 12-15% over the long term.",
            "🌍 FIIs (Foreign Institutional Investors) significantly impact market movements.",
            "📊 Sectoral rotation is common - when one sector falls, money moves to another.",
            "⚖️ SEBI regulates Indian capital markets and protects investor interests.",
            "🎯 Beta measures stock volatility relative to market - 1 means same as market.",
            "💰 Market cap = Share price × Total outstanding shares of a company.",
            "📈 PE ratio compares share price to earnings per share - lower can be better value.",
            "🔄 Algorithmic trading accounts for over 50% of cash market volumes.",
            "🏛️ BSE is Asia's first stock exchange, established in 1875.",
            "⭐ Blue chip stocks are shares of large, established, financially stable companies.",
            "📊 Volume indicates buying/selling interest - higher volume shows more activity.",
            "🎪 Muhurat trading happens on Diwali - considered auspicious for new investments.",
            "💎 Small cap stocks can give higher returns but carry higher risk.",
            "🌅 Opening price is determined by pre-market session auction.",
            "📈 Support level is price where stock tends to stop falling and bounce back.",
            "📉 Resistance level is price where stock tends to stop rising and fall back.",
            "⚡ High-frequency trading executes thousands of trades per second.",
            "🎯 Stop loss helps limit losses by automatically selling at predetermined price.",
            "💰 Bonus shares are free additional shares given to existing shareholders.",
            "🔄 Stock split divides existing shares into multiple shares at lower price.",
            "🏆 Nifty Bank index tracks performance of banking sector stocks.",
            "📊 P/B ratio compares share price to book value per share.",
            "🌟 IPO is when a private company offers shares to public for first time.",
            "💡 Mutual funds pool money from many investors to buy diversified portfolio.",
            "🎨 Candlestick patterns help predict future price movements.",
            "⚖️ Systematic Investment Plan (SIP) allows regular monthly investments.",
            "📈 Bull run refers to prolonged period of rising stock prices.",
            "📉 Bear market is when stocks fall 20% or more from recent highs.",
            "🔔 Ex-dividend date is when stock price adjusts down by dividend amount.",
            "💎 Rights issue allows existing shareholders to buy additional shares at discount.",
            "🌍 ADR/GDR allow Indian companies to list on foreign exchanges."
        ]
    
    def get_random_fact(self):
        """Get a random market fact"""
        return random.choice(self.facts)
    
    def get_loading_message(self, context="general"):
        """Get context-specific loading message with fact"""
        context_messages = {
            "market_data": [
                "Fetching live market data from NSE & BSE...",
                "Getting real-time prices from exchanges...",
                "Updating market indices and prices...",
                "Syncing with market data providers..."
            ],
            "stock_analysis": [
                "Analyzing stock performance and trends...",
                "Calculating technical indicators...",
                "Processing historical price data...",
                "Computing risk metrics and ratios..."
            ],
            "news": [
                "Gathering latest market news...",
                "Analyzing news sentiment...",
                "Fetching headlines from financial sources...",
                "Processing market updates..."
            ],
            "comparison": [
                "Comparing stock performances...",
                "Calculating relative metrics...",
                "Analyzing price movements...",
                "Processing comparison data..."
            ],
            "general": [
                "Loading market insights...",
                "Preparing your dashboard...",
                "Getting latest updates...",
                "Processing market information..."
            ]
        }
        
        messages = context_messages.get(context, context_messages["general"])
        loading_msg = random.choice(messages)
        fact = self.get_random_fact()
        
        return f"{loading_msg}\n\n💡 {fact}"
    
    def get_sentiment_based_styling(self, sentiment, value=None):
        """Get CSS styling based on market sentiment"""
        if sentiment.lower() in ['positive', 'bullish', 'buy', 'strong buy']:
            return {
                'color': '#00C851',
                'background': 'linear-gradient(135deg, #00C851, #2E7D32)',
                'border_color': '#00C851',
                'text_color': 'white',
                'emoji': '📈'
            }
        elif sentiment.lower() in ['negative', 'bearish', 'sell', 'strong sell']:
            return {
                'color': '#FF4444',
                'background': 'linear-gradient(135deg, #FF4444, #D32F2F)',
                'border_color': '#FF4444',
                'text_color': 'white',
                'emoji': '📉'
            }
        elif sentiment.lower() in ['neutral', 'hold', 'sideways']:
            return {
                'color': '#FFB74D',
                'background': 'linear-gradient(135deg, #FFB74D, #FF8F00)',
                'border_color': '#FFB74D',
                'text_color': 'white',
                'emoji': '➡️'
            }
        else:
            # Default based on numeric value if provided
            if value is not None:
                if value > 0:
                    return self.get_sentiment_based_styling('positive')
                elif value < 0:
                    return self.get_sentiment_based_styling('negative')
                else:
                    return self.get_sentiment_based_styling('neutral')
            
            # Default neutral styling
            return self.get_sentiment_based_styling('neutral')