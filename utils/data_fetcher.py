import yfinance as yf
import finnhub
import pandas as pd
import numpy as np
import streamlit as st
import os
import json
from datetime import datetime, timedelta
import requests
import time

class DataFetcher:
    def __init__(self):
        # Use the provided API key with fallback to environment variable
        api_key = os.getenv("FINNHUB_API_KEY", "d1kimi9r01qt8fooq9e0d1kimi9r01qt8fooq9eg")
        self.finnhub_client = finnhub.Client(api_key=api_key)
        
        # Load comprehensive Indian stock symbols from our assets
        self.indian_symbols = self._load_indian_stocks()
        
        # Major Indian indices
        self.indices = {
            '^NSEI': 'NIFTY 50',
            '^BSESN': 'BSE SENSEX',
            '^NSEBANK': 'NIFTY Bank',
            '^CNXIT': 'NIFTY IT'
        }
        
    def _load_indian_stocks(self):
        """Load Indian stock symbols from the assets file"""
        try:
            with open("assets/indian_stocks.json", "r", encoding="utf-8") as f:
                stock_data = json.load(f)
            
            # Combine blue chip stocks and sector-wise stocks
            symbols = {}
            
            # Add blue chip stocks
            for symbol, data in stock_data.get("blue_chip_stocks", {}).items():
                symbols[symbol] = data["name"]
            
            # Add sector-wise stocks
            for sector, stocks in stock_data.get("sector_wise_stocks", {}).items():
                for symbol, name in stocks.items():
                    if symbol not in symbols:  # Avoid duplicates
                        symbols[symbol] = name
            
            return symbols
            
        except Exception as e:
            # Fallback to basic symbols if file loading fails
            return {
                'RELIANCE.NS': 'Reliance Industries',
                'TCS.NS': 'Tata Consultancy Services',
                'INFY.NS': 'Infosys',
                'HDFCBANK.NS': 'HDFC Bank',
                'HINDUNILVR.NS': 'Hindustan Unilever',
                'ITC.NS': 'ITC Limited',
                'KOTAKBANK.NS': 'Kotak Mahindra Bank',
                'LT.NS': 'Larsen & Toubro',
                'BHARTIARTL.NS': 'Bharti Airtel',
                'ASIANPAINT.NS': 'Asian Paints'
            }
    
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_stock_data(_self, symbol, period="1y"):
        """Fetch stock data from Yahoo Finance"""
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period=period)
            info = stock.info
            
            if hist.empty:
                raise ValueError(f"No data found for symbol {symbol}")
            
            return {
                'history': hist,
                'info': info,
                'symbol': symbol
            }
        except Exception as e:
            st.error(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    @st.cache_data(ttl=600)  # Cache for 10 minutes
    def get_market_overview(_self):
        """Get market overview data"""
        try:
            overview = {}
            
            # Fetch major indices
            for symbol, name in _self.indices.items():
                data = _self.get_stock_data(symbol, "5d")
                if data:
                    latest = data['history'].iloc[-1]
                    prev = data['history'].iloc[-2] if len(data['history']) > 1 else latest
                    
                    overview[name] = {
                        'current': latest['Close'],
                        'change': latest['Close'] - prev['Close'],
                        'change_percent': ((latest['Close'] - prev['Close']) / prev['Close']) * 100,
                        'volume': latest['Volume']
                    }
            
            return overview
        except Exception as e:
            st.error(f"Error fetching market overview: {str(e)}")
            return {}
    
    @st.cache_data(ttl=900)  # Cache for 15 minutes
    def get_top_gainers_losers(_self):
        """Get top gainers and losers from Indian market"""
        try:
            gainers = []
            losers = []
            
            for symbol, name in _self.indian_symbols.items():
                data = _self.get_stock_data(symbol, "5d")
                if data and len(data['history']) >= 2:
                    latest = data['history'].iloc[-1]
                    prev = data['history'].iloc[-2]
                    
                    change_percent = ((latest['Close'] - prev['Close']) / prev['Close']) * 100
                    
                    stock_info = {
                        'symbol': symbol,
                        'name': name,
                        'price': latest['Close'],
                        'change': latest['Close'] - prev['Close'],
                        'change_percent': change_percent,
                        'volume': latest['Volume']
                    }
                    
                    if change_percent > 0:
                        gainers.append(stock_info)
                    else:
                        losers.append(stock_info)
            
            # Sort by change percentage
            gainers.sort(key=lambda x: x['change_percent'], reverse=True)
            losers.sort(key=lambda x: x['change_percent'])
            
            return gainers[:5], losers[:5]
        except Exception as e:
            st.error(f"Error fetching gainers/losers: {str(e)}")
            return [], []
    
    def get_company_news(self, symbol, days=7):
        """Fetch company news from Finnhub"""
        try:
            # Convert Yahoo Finance symbol to Finnhub format
            finnhub_symbol = symbol.replace('.NS', '').replace('.BO', '')
            
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Get news from Finnhub
            news = self.finnhub_client.company_news(
                finnhub_symbol, 
                _from=start_date.strftime('%Y-%m-%d'), 
                to=end_date.strftime('%Y-%m-%d')
            )
            
            return news[:10]  # Return top 10 news items
        except Exception as e:
            st.error(f"Error fetching news for {symbol}: {str(e)}")
            return []
    
    def get_general_market_news(self, category="general"):
        """Fetch general market news"""
        try:
            news = self.finnhub_client.general_news(category, min_id=0)
            # Filter for Indian market related news
            indian_keywords = ['india', 'indian', 'nse', 'bse', 'mumbai', 'sensex', 'nifty', 'rupee']
            filtered_news = []
            
            for item in news:
                if any(keyword.lower() in item.get('headline', '').lower() or 
                       keyword.lower() in item.get('summary', '').lower() 
                       for keyword in indian_keywords):
                    filtered_news.append(item)
            
            return filtered_news[:15]
        except Exception as e:
            st.error(f"Error fetching general news: {str(e)}")
            return []
    
    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def get_sector_performance(_self):
        """Get sector-wise performance data"""
        try:
            sectors = {
                'Banking': ['HDFCBANK.NS', 'KOTAKBANK.NS', 'ICICIBANK.NS'],
                'IT': ['TCS.NS', 'INFY.NS', 'WIPRO.NS'],
                'FMCG': ['HINDUNILVR.NS', 'ITC.NS', 'NESTLEIND.NS'],
                'Energy': ['RELIANCE.NS', 'ONGC.NS', 'NTPC.NS'],
                'Auto': ['MARUTI.NS', 'TATAMOTORS.NS', 'M&M.NS']
            }
            
            sector_data = {}
            
            for sector, symbols in sectors.items():
                sector_changes = []
                for symbol in symbols:
                    data = _self.get_stock_data(symbol, "5d")
                    if data and len(data['history']) >= 2:
                        latest = data['history'].iloc[-1]
                        prev = data['history'].iloc[-2]
                        change_percent = ((latest['Close'] - prev['Close']) / prev['Close']) * 100
                        sector_changes.append(change_percent)
                
                if sector_changes:
                    sector_data[sector] = {
                        'avg_change': np.mean(sector_changes),
                        'stocks_count': len(sector_changes)
                    }
            
            return sector_data
        except Exception as e:
            st.error(f"Error fetching sector performance: {str(e)}")
            return {}
    
    def get_real_time_quote(self, symbol):
        """Get real-time quote data"""
        try:
            # For Indian stocks, use Yahoo Finance for real-time data
            stock = yf.Ticker(symbol)
            
            # Get current market data
            todays_data = stock.history(period="1d", interval="1m")
            if not todays_data.empty:
                latest = todays_data.iloc[-1]
                return {
                    'price': latest['Close'],
                    'volume': latest['Volume'],
                    'timestamp': todays_data.index[-1]
                }
            else:
                # Fallback to daily data
                data = self.get_stock_data(symbol, "1d")
                if data:
                    latest = data['history'].iloc[-1]
                    return {
                        'price': latest['Close'],
                        'volume': latest['Volume'],
                        'timestamp': data['history'].index[-1]
                    }
            return None
        except Exception as e:
            st.error(f"Error fetching real-time quote for {symbol}: {str(e)}")
            return None
    
    def search_stocks(self, query):
        """Search for stocks based on query"""
        try:
            # Search in our predefined Indian stocks
            results = []
            query_lower = query.lower()
            
            for symbol, name in self.indian_symbols.items():
                if (query_lower in symbol.lower() or 
                    query_lower in name.lower()):
                    results.append({
                        'symbol': symbol,
                        'name': name,
                        'type': 'Indian Stock'
                    })
            
            return results[:10]
        except Exception as e:
            st.error(f"Error searching stocks: {str(e)}")
            return []
