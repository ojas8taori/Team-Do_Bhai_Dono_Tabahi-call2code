import requests
import streamlit as st
from datetime import datetime, timedelta
import os
import trafilatura

@st.cache_data(ttl=900)  # Cache for 15 minutes
def get_market_news(symbol=None, limit=10):
    """
    Fetch market news for a specific stock or general market news
    
    Args:
        symbol (str, optional): Stock symbol to get news for
        limit (int): Number of news articles to fetch
    
    Returns:
        list: List of news articles
    """
    try:
        # Try NewsAPI first
        news_api_key = os.getenv("NEWS_API_KEY", "demo_key")
        
        if news_api_key and news_api_key != "demo_key":
            return get_news_from_api(symbol, limit, news_api_key)
        else:
            # Fallback to web scraping
            return get_news_from_scraping(symbol, limit)
            
    except Exception as e:
        st.error(f"Error fetching news: {str(e)}")
        return []

def get_news_from_api(symbol, limit, api_key):
    """
    Fetch news from NewsAPI
    
    Args:
        symbol (str): Stock symbol
        limit (int): Number of articles
        api_key (str): NewsAPI key
    
    Returns:
        list: List of news articles
    """
    try:
        base_url = "https://newsapi.org/v2/everything"
        
        # Build query based on symbol
        if symbol:
            # Extract company name from symbol if possible
            query_terms = [symbol]
            
            # Add common company name mappings
            company_mappings = {
                'AAPL': 'Apple',
                'MSFT': 'Microsoft',
                'GOOGL': 'Google',
                'AMZN': 'Amazon',
                'TSLA': 'Tesla',
                'META': 'Meta Facebook',
                'NVDA': 'NVIDIA',
                'RELIANCE.NS': 'Reliance Industries',
                'TCS.NS': 'TCS Tata Consultancy',
                'INFY.NS': 'Infosys',
                'HDFCBANK.NS': 'HDFC Bank',
                'ICICIBANK.NS': 'ICICI Bank',
                'SBIN.NS': 'State Bank India',
                'WIPRO.NS': 'Wipro',
                'BHARTIARTL.NS': 'Bharti Airtel'
            }
            
            if symbol in company_mappings:
                query_terms.append(company_mappings[symbol])
            
            query = " OR ".join(query_terms)
        else:
            query = "stock market OR financial markets OR economy"
        
        params = {
            'q': query,
            'apiKey': api_key,
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': limit,
            'domains': 'bloomberg.com,reuters.com,cnbc.com,marketwatch.com,yahoo.com,business-standard.com,economictimes.indiatimes.com'
        }
        
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('status') == 'ok':
            articles = []
            for article in data.get('articles', []):
                articles.append({
                    'title': article.get('title', 'No Title'),
                    'description': article.get('description', 'No Description'),
                    'source': article.get('source', {}).get('name', 'Unknown'),
                    'url': article.get('url', ''),
                    'published_at': article.get('publishedAt', ''),
                    'image_url': article.get('urlToImage', '')
                })
            
            return articles
        else:
            return []
            
    except Exception as e:
        st.error(f"Error fetching news from API: {str(e)}")
        return []

def get_news_from_scraping(symbol, limit):
    """
    Fallback method to scrape news from financial websites
    
    Args:
        symbol (str): Stock symbol
        limit (int): Number of articles
    
    Returns:
        list: List of news articles
    """
    try:
        articles = []
        
        # Try to get news from Yahoo Finance for the specific symbol
        if symbol:
            try:
                # Clean symbol for URL
                clean_symbol = symbol.replace('.NS', '').replace('.BO', '')
                yahoo_url = f"https://finance.yahoo.com/quote/{symbol}/news"
                
                downloaded = trafilatura.fetch_url(yahoo_url)
                if downloaded:
                    text_content = trafilatura.extract(downloaded)
                    
                    if text_content:
                        lines = text_content.split('\n')
                        headlines = []
                        
                        for line in lines:
                            line = line.strip()
                            # Look for news-like content
                            if (len(line) > 30 and len(line) < 200 and 
                                not line.startswith('http') and 
                                not line.isdigit() and
                                ('stock' in line.lower() or 'market' in line.lower() or 
                                 'company' in line.lower() or 'share' in line.lower() or
                                 clean_symbol.lower() in line.lower())):
                                headlines.append(line)
                        
                        for headline in headlines[:limit]:
                            articles.append({
                                'title': headline,
                                'description': f'Latest news about {symbol}',
                                'source': 'Yahoo Finance',
                                'url': yahoo_url,
                                'published_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'image_url': ''
                            })
                
            except Exception as e:
                pass
        
        # If no symbol-specific news, get general market news
        if not articles:
            general_news = [
                {
                    'title': 'Market Analysis: Stock Performance Review',
                    'description': 'Daily market analysis and stock performance insights',
                    'source': 'Market Analysis',
                    'url': 'https://finance.yahoo.com/news',
                    'published_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'image_url': ''
                },
                {
                    'title': 'Financial Markets Update',
                    'description': 'Latest updates from financial markets and trading activity',
                    'source': 'Financial News',
                    'url': 'https://finance.yahoo.com/news',
                    'published_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'image_url': ''
                },
                {
                    'title': 'Economic Indicators and Stock Trends',
                    'description': 'Analysis of key economic indicators affecting stock performance',
                    'source': 'Economic Analysis',
                    'url': 'https://finance.yahoo.com/news',
                    'published_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'image_url': ''
                }
            ]
            articles.extend(general_news[:limit])
        
        return articles[:limit]
        
    except Exception as e:
        # Return fallback news if scraping fails
        return [
            {
                'title': 'Market News Available',
                'description': 'News functionality is available. For full news access, please provide a NewsAPI key.',
                'source': 'System',
                'url': '',
                'published_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'image_url': ''
            }
        ]

def get_general_market_news(limit=5):
    """
    Get general market news
    
    Args:
        limit (int): Number of articles
    
    Returns:
        list: List of news articles
    """
    return get_market_news(symbol=None, limit=limit)

def format_news_date(date_string):
    """
    Format news date for display
    
    Args:
        date_string (str): Date string from news API
    
    Returns:
        str: Formatted date string
    """
    try:
        if not date_string:
            return "Unknown"
        
        # Parse the date string
        dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        
        # Format for display
        return dt.strftime("%Y-%m-%d %H:%M")
        
    except Exception as e:
        return "Unknown"

def is_news_relevant(article, symbol):
    """
    Check if news article is relevant to the stock symbol
    
    Args:
        article (dict): News article
        symbol (str): Stock symbol
    
    Returns:
        bool: True if relevant, False otherwise
    """
    try:
        if not symbol:
            return True
        
        # Check title and description for relevance
        content = f"{article.get('title', '')} {article.get('description', '')}".lower()
        
        # Basic relevance check
        symbol_lower = symbol.lower().replace('.ns', '').replace('.bo', '')
        
        return symbol_lower in content
        
    except Exception as e:
        return False
