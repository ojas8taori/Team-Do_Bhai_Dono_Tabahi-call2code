import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

@st.cache_data(ttl=60)  # Cache for 1 minute
def get_stock_data(symbol, period="1y"):
    """
    Fetch stock data using yfinance
    
    Args:
        symbol (str): Stock symbol
        period (str): Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
    
    Returns:
        pd.DataFrame: Stock data with OHLCV
    """
    try:
        # Create ticker object
        ticker = yf.Ticker(symbol)
        
        # Get historical data
        hist = ticker.history(period=period)
        
        if hist.empty:
            return None
        
        return hist
        
    except Exception as e:
        st.error(f"Error fetching stock data for {symbol}: {str(e)}")
        return None

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_stock_metrics(symbol):
    """
    Fetch key financial metrics for a stock
    
    Args:
        symbol (str): Stock symbol
    
    Returns:
        dict: Dictionary containing financial metrics
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        if not info:
            return None
        
        metrics = {
            'pe_ratio': info.get('trailingPE', None),
            'roe': info.get('returnOnEquity', None),
            'market_cap': info.get('marketCap', None),
            'dividend_yield': info.get('dividendYield', None),
            'eps': info.get('trailingEps', None),
            'book_value': info.get('bookValue', None),
            'debt_to_equity': info.get('debtToEquity', None),
            'current_ratio': info.get('currentRatio', None),
            'revenue_growth': info.get('revenueGrowth', None),
            'profit_margin': info.get('profitMargins', None),
            'beta': info.get('beta', None),
            '52_week_high': info.get('fiftyTwoWeekHigh', None),
            '52_week_low': info.get('fiftyTwoWeekLow', None),
            'volume': info.get('volume', None),
            'avg_volume': info.get('averageVolume', None),
            'shares_outstanding': info.get('sharesOutstanding', None),
            'float_shares': info.get('floatShares', None)
        }
        
        # Convert ROE to percentage if available
        if metrics['roe']:
            metrics['roe'] = metrics['roe'] * 100
        
        # Convert dividend yield to percentage if available
        if metrics['dividend_yield']:
            metrics['dividend_yield'] = metrics['dividend_yield'] * 100
        
        # Convert profit margin to percentage if available
        if metrics['profit_margin']:
            metrics['profit_margin'] = metrics['profit_margin'] * 100
        
        return metrics
        
    except Exception as e:
        st.error(f"Error fetching metrics for {symbol}: {str(e)}")
        return None

def get_real_time_price(symbol):
    """
    Get real-time price for a stock
    
    Args:
        symbol (str): Stock symbol
    
    Returns:
        dict: Dictionary with current price info
    """
    try:
        ticker = yf.Ticker(symbol)
        
        # Get real-time data (last 1 day)
        hist = ticker.history(period="1d", interval="1m")
        
        if hist.empty:
            return None
        
        current_price = hist['Close'].iloc[-1]
        previous_close = ticker.info.get('regularMarketPreviousClose', hist['Close'].iloc[0])
        
        change = current_price - previous_close
        change_percent = (change / previous_close) * 100 if previous_close != 0 else 0
        
        return {
            'current_price': current_price,
            'previous_close': previous_close,
            'change': change,
            'change_percent': change_percent,
            'timestamp': datetime.now()
        }
        
    except Exception as e:
        st.error(f"Error fetching real-time price for {symbol}: {str(e)}")
        return None

def search_stocks(query):
    """
    Search for stocks based on query
    
    Args:
        query (str): Search query
    
    Returns:
        list: List of matching stock symbols
    """
    try:
        # This is a simplified search - in production, you might want to use
        # a more comprehensive stock search API
        
        # Common stock symbols for quick search
        common_stocks = {
            'apple': 'AAPL',
            'microsoft': 'MSFT',
            'google': 'GOOGL',
            'amazon': 'AMZN',
            'tesla': 'TSLA',
            'meta': 'META',
            'nvidia': 'NVDA',
            'reliance': 'RELIANCE.NS',
            'tcs': 'TCS.NS',
            'infosys': 'INFY.NS',
            'hdfc': 'HDFCBANK.NS',
            'icici': 'ICICIBANK.NS',
            'sbi': 'SBIN.NS',
            'wipro': 'WIPRO.NS',
            'bharti': 'BHARTIARTL.NS'
        }
        
        query_lower = query.lower()
        matches = []
        
        for name, symbol in common_stocks.items():
            if query_lower in name or query_lower in symbol.lower():
                matches.append(symbol)
        
        # If no matches found, try the query as a direct symbol
        if not matches:
            matches.append(query.upper())
        
        return matches
        
    except Exception as e:
        st.error(f"Error searching stocks: {str(e)}")
        return []

def get_stock_timeframe_data(symbol, timeframe):
    """
    Get stock data for specific timeframe
    
    Args:
        symbol (str): Stock symbol
        timeframe (str): Timeframe (1D, 1W, 1M, 3M, 1Y)
    
    Returns:
        pd.DataFrame: Stock data
    """
    try:
        period_map = {
            '1D': '1d',
            '1W': '5d',
            '1M': '1mo',
            '3M': '3mo',
            '1Y': '1y'
        }
        
        period = period_map.get(timeframe, '1y')
        
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        return hist
        
    except Exception as e:
        st.error(f"Error fetching timeframe data for {symbol}: {str(e)}")
        return None
