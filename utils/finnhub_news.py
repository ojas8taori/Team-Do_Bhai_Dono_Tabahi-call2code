"""
Finnhub News and Sentiment Analysis Module
Handles news fetching and sentiment analysis for stocks using Finnhub API
"""

import finnhub
import os
import streamlit as st
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
import json

# Load environment variables
load_dotenv()

# Initialize Finnhub client
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

@st.cache_data(ttl=900)  # Cache for 15 minutes
def get_stock_news(symbol, limit=10):
    """
    Fetch news for a specific stock using Finnhub API
    
    Args:
        symbol (str): Stock symbol (with or without .NS/.BO suffix)
        limit (int): Number of news articles to fetch
    
    Returns:
        list: List of news articles
    """
    try:
        # Clean symbol for API call
        clean_symbol = symbol.replace('.NS', '').replace('.BO', '').upper()
        
        # For Indian stocks, try to map to US ticker or get relevant company name
        indian_to_us_mapping = {
            'RELIANCE': 'RIGD',  # Reliance Industries
            'TCS': 'TTM',        # Tata Consultancy Services 
            'INFY': 'INFY',      # Infosys
            'WIPRO': 'WIT',      # Wipro
            'HDFCBANK': 'HDB',   # HDFC Bank
            'ICICIBANK': 'IBN',  # ICICI Bank
            'BHARTIARTL': 'IBN', # Bharti Airtel
            'ITC': 'ITCB',       # ITC Limited
        }
        
        # Try US equivalent first for better news coverage
        us_symbol = indian_to_us_mapping.get(clean_symbol, clean_symbol)
        
        # Calculate date range (last 30 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # Format dates for API
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')
        
        # Try to fetch news with US symbol first
        news = []
        try:
            news = finnhub_client.company_news(us_symbol, _from=start_str, to=end_str)
        except:
            pass
            
        # If no news found with US symbol, try original symbol
        if not news and us_symbol != clean_symbol:
            try:
                news = finnhub_client.company_news(clean_symbol, _from=start_str, to=end_str)
            except:
                pass
        
        # If still no news, try market news filtered by company name
        if not news:
            general_news = finnhub_client.general_news('general', min_id=0)
            company_keywords = [clean_symbol.lower(), 
                              symbol.replace('.NS', '').replace('.BO', '').lower()]
            
            # Filter general news for company mentions
            news = []
            for article in general_news:
                headline = article.get('headline', '').lower()
                summary = article.get('summary', '').lower()
                
                if any(keyword in headline or keyword in summary for keyword in company_keywords):
                    news.append(article)
                    if len(news) >= limit:
                        break
        
        # Format news data
        formatted_news = []
        for article in news[:limit]:
            formatted_news.append({
                'title': article.get('headline', 'No Title'),
                'description': article.get('summary', 'No Description'),
                'url': article.get('url', ''),
                'published_at': datetime.fromtimestamp(article.get('datetime', 0)).strftime('%Y-%m-%d %H:%M:%S'),
                'source': article.get('source', 'Finnhub'),
                'image': article.get('image', ''),
                'category': article.get('category', 'Company News')
            })
        
        return formatted_news
    
    except Exception as e:
        print(f"Error fetching news for {symbol}: {str(e)}")
        return []

@st.cache_data(ttl=900)  # Cache for 15 minutes
def get_general_market_news(limit=15):
    """
    Fetch general market news
    
    Args:
        limit (int): Number of news articles to fetch
    
    Returns:
        list: List of market news articles
    """
    try:
        # Fetch economic news from multiple categories
        all_news = []
        
        # Try different economic news categories
        economic_categories = ['forex', 'general', 'crypto']
        
        for category in economic_categories:
            try:
                category_news = finnhub_client.general_news(category, min_id=0)
                if category_news:
                    all_news.extend(category_news)
            except:
                continue
        
        # Filter for economic/market related keywords
        economic_keywords = [
            'economy', 'economic', 'gdp', 'inflation', 'interest rate', 'fed', 'federal reserve',
            'market', 'stocks', 'trading', 'dow', 'nasdaq', 'recession', 'bull market', 'bear market',
            'earnings', 'revenue', 'profit', 'financial', 'banking', 'central bank', 'monetary policy',
            'nse', 'bse', 'sensex', 'nifty', 'rbi', 'reserve bank', 'india', 'indian economy'
        ]
        
        # Filter news for economic content
        filtered_news = []
        for article in all_news:
            title = article.get('headline', '').lower()
            summary = article.get('summary', '').lower()
            
            # Check if article contains economic keywords
            if any(keyword in title or keyword in summary for keyword in economic_keywords):
                filtered_news.append(article)
        
        # Use filtered economic news, fallback to general if none found
        news = filtered_news if filtered_news else all_news
        
        # Format news data
        formatted_news = []
        for article in news[:limit]:
            formatted_news.append({
                'title': article.get('headline', 'No Title'),
                'description': article.get('summary', 'No Description'),
                'url': article.get('url', ''),
                'published_at': datetime.fromtimestamp(article.get('datetime', 0)).strftime('%Y-%m-%d %H:%M:%S'),
                'source': article.get('source', 'Finnhub'),
                'image': article.get('image', ''),
                'category': article.get('category', 'General')
            })
        
        return formatted_news
    
    except Exception as e:
        st.error(f"Error fetching general market news: {str(e)}")
        return []

def analyze_stock_sentiment(symbol):
    """
    Analyze sentiment for a stock using news data
    
    Args:
        symbol (str): Stock symbol
    
    Returns:
        dict: Sentiment analysis results
    """
    try:
        # Get recent news for the stock
        news_articles = get_stock_news(symbol, limit=10)
        
        if not news_articles:
            return {
                'sentiment': 'Neutral',
                'confidence': 0.5,
                'score': 0,
                'total_articles': 0,
                'positive_articles': 0,
                'negative_articles': 0,
                'neutral_articles': 0
            }
        
        # Simple sentiment analysis based on keywords
        positive_keywords = [
            'gain', 'rise', 'surge', 'bull', 'positive', 'growth', 'profit', 'strong', 
            'beat', 'outperform', 'upgrade', 'buy', 'rally', 'soar', 'jump', 'climb'
        ]
        
        negative_keywords = [
            'fall', 'drop', 'decline', 'bear', 'negative', 'loss', 'weak', 'miss', 
            'underperform', 'downgrade', 'sell', 'crash', 'plunge', 'tumble', 'slide'
        ]
        
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for article in news_articles:
            title_lower = article['title'].lower()
            desc_lower = article['description'].lower()
            
            # Count positive and negative keywords
            pos_score = sum(1 for keyword in positive_keywords if keyword in title_lower or keyword in desc_lower)
            neg_score = sum(1 for keyword in negative_keywords if keyword in title_lower or keyword in desc_lower)
            
            if pos_score > neg_score:
                positive_count += 1
            elif neg_score > pos_score:
                negative_count += 1
            else:
                neutral_count += 1
        
        total_articles = len(news_articles)
        
        # Calculate overall sentiment
        if positive_count > negative_count:
            sentiment = 'Positive'
            confidence = positive_count / total_articles
            score = (positive_count - negative_count) / total_articles
        elif negative_count > positive_count:
            sentiment = 'Negative'
            confidence = negative_count / total_articles
            score = (negative_count - positive_count) / total_articles * -1
        else:
            sentiment = 'Neutral'
            confidence = 0.5
            score = 0
        
        return {
            'sentiment': sentiment,
            'confidence': min(confidence, 1.0),
            'score': score,
            'total_articles': total_articles,
            'positive_articles': positive_count,
            'negative_articles': negative_count,
            'neutral_articles': neutral_count
        }
    
    except Exception as e:
        st.error(f"Error analyzing sentiment for {symbol}: {str(e)}")
        return {
            'sentiment': 'Neutral',
            'confidence': 0.5,
            'score': 0,
            'total_articles': 0,
            'positive_articles': 0,
            'negative_articles': 0,
            'neutral_articles': 0
        }

def get_sentiment_color(sentiment):
    """
    Get color for sentiment display
    
    Args:
        sentiment (str): Sentiment value
    
    Returns:
        str: Color code
    """
    if sentiment == 'Positive':
        return '#4CAF50'  # Green
    elif sentiment == 'Negative':
        return '#FF5252'  # Red
    else:
        return '#FFA726'  # Orange

def get_sentiment_emoji(sentiment):
    """
    Get emoji for sentiment display
    
    Args:
        sentiment (str): Sentiment value
    
    Returns:
        str: Emoji
    """
    if sentiment == 'Positive':
        return '😊'
    elif sentiment == 'Negative':
        return '😔'
    else:
        return '😐'

def format_news_for_display(news_articles):
    """
    Format news articles for Streamlit display
    
    Args:
        news_articles (list): List of news articles
    
    Returns:
        list: Formatted news articles
    """
    formatted_articles = []
    
    for article in news_articles:
        formatted_articles.append({
            'title': article['title'],
            'description': article['description'][:200] + '...' if len(article['description']) > 200 else article['description'],
            'url': article['url'],
            'published_at': article['published_at'],
            'source': article['source'],
            'category': article['category']
        })
    
    return formatted_articles