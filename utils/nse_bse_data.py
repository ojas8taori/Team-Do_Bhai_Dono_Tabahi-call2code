import requests
import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
import trafilatura
import json
import re

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_top_gainers_losers():
    """
    Get real-time top gainers and losers using Yahoo Finance
    
    Returns:
        dict: Dictionary containing gainers and losers data
    """
    try:
        import yfinance as yf
        
        # Comprehensive NSE stocks list covering major indices and sectors
        # Using a broader selection from NIFTY 500, NIFTY Midcap, and NIFTY Smallcap
        nse_stocks = [
            # NIFTY 50 stocks
            'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'BHARTIARTL.NS', 'INFY.NS',
            'ICICIBANK.NS', 'SBIN.NS', 'LICI.NS', 'ITC.NS', 'HINDUNILVR.NS',
            'LT.NS', 'KOTAKBANK.NS', 'AXISBANK.NS', 'MARUTI.NS', 'SUNPHARMA.NS',
            'ONGC.NS', 'NTPC.NS', 'ASIANPAINT.NS', 'NESTLEIND.NS', 'TATAMOTORS.NS',
            'M&M.NS', 'BAJFINANCE.NS', 'WIPRO.NS', 'ULTRACEMCO.NS', 'TATASTEEL.NS',
            'ADANIENT.NS', 'HCLTECH.NS', 'POWERGRID.NS', 'COALINDIA.NS', 'JSWSTEEL.NS',
            'TECHM.NS', 'TITAN.NS', 'DIVISLAB.NS', 'DRREDDY.NS', 'BRITANNIA.NS',
            'CIPLA.NS', 'BAJAJFINSV.NS', 'EICHERMOT.NS', 'HEROMOTOCO.NS', 'APOLLOHOSP.NS',
            'HINDALCO.NS', 'GRASIM.NS', 'ADANIPORTS.NS', 'TRENT.NS', 'SHRIRAMFIN.NS',
            
            # NIFTY Next 50 and Popular Mid-caps
            'ADANIGREEN.NS', 'ADANIPOWER.NS', 'GODREJCP.NS', 'PIDILITIND.NS', 'BANDHANBNK.NS',
            'GAIL.NS', 'VEDL.NS', 'INDIGO.NS', 'HAVELLS.NS', 'MARICO.NS',
            'LUPIN.NS', 'SHREECEM.NS', 'TORNTPHARM.NS', 'BAJAJ-AUTO.NS', 'MOTHERSON.NS',
            'DABUR.NS', 'COLPAL.NS', 'SIEMENS.NS', 'BOSCHLTD.NS', 'PAGEIND.NS',
            'DMART.NS', 'GODREJPROP.NS', 'MPHASIS.NS', 'LTTS.NS', 'PERSISTENT.NS',
            
            # Banking & Financial Services
            'PNB.NS', 'BANKBARODA.NS', 'CANBK.NS', 'IDFCFIRSTB.NS', 'PFC.NS',
            'RECLTD.NS', 'LICHSGFIN.NS', 'BAJAJHLDNG.NS', 'SBILIFE.NS', 'HDFCLIFE.NS',
            'RBLBANK.NS', 'FEDERALBNK.NS', 'AUBANK.NS', 'YESBANK.NS', 'INDUSINDBK.NS',
            
            # Technology & IT Services
            'COFORGE.NS', 'KPITTECH.NS', 'OFSS.NS', 'LTIM.NS', 'TATAELXSI.NS',
            
            # Pharma & Healthcare  
            'BIOCON.NS', 'GLENMARK.NS', 'ALKEM.NS', 'AUROPHARMA.NS', 'GRANULES.NS',
            'LALPATHLAB.NS', 'METROPOLIS.NS', 'FORTIS.NS', 'MAXHEALTH.NS',
            
            # Auto & Auto Components
            'ASHOKLEY.NS', 'TVSMOTOR.NS', 'ESCORTS.NS', 'BALKRISIND.NS', 'APOLLOTYRE.NS',
            'FORCEMOT.NS', 'MAHINDCIE.NS', 'EXIDEIND.NS', 'BHARATFORG.NS',
            
            # FMCG & Consumer
            'JUBLFOOD.NS', 'PGHH.NS', 'EMAMILTD.NS', 'BERGEPAINT.NS', 'VOLTAS.NS',
            'WHIRLPOOL.NS', 'CROMPTON.NS', 'RELAXO.NS', 'VIPIND.NS',
            
            # Metals & Mining
            'SAIL.NS', 'NMDC.NS', 'MOIL.NS', 'NATIONALUM.NS', 'HINDZINC.NS',
            'JINDALSTEL.NS', 'SAILPL.NS', 'RATNAMANI.NS', 'APL.NS',
            
            # Infrastructure & Real Estate
            'CONCOR.NS', 'GMRINFRA.NS', 'IRB.NS', 'HUDCO.NS', 'PRESTIGE.NS',
            'SOBHA.NS', 'BRIGADE.NS', 'PHOENIXLTD.NS',
            
            # Energy & Utilities
            'ADANIGAS.NS', 'IGL.NS', 'GUJGASLTD.NS', 'ATGL.NS', 'NHPC.NS',
            'SJVN.NS', 'TATAPOWER.NS', 'TORNTPOWER.NS',
            
            # Telecom & Media
            'GTPL.NS', 'RCOM.NS', 'IDEA.NS', 'ZEEL.NS', 'SUNTV.NS',
            
            # Chemicals & Fertilizers
            'UPL.NS', 'GNFC.NS', 'DEEPAKNTR.NS', 'BALRAMCHIN.NS', 'AAVAS.NS',
            
            # Textile & Apparel
            'AIAENG.NS', 'RAYMOND.NS', 'GOKEX.NS', 'ARVIND.NS',
            
            # Hotels & Tourism
            'INDHOTEL.NS', 'LEMONTREE.NS', 'CHALET.NS', 'MAHLOG.NS',
            
            # New Age Tech/Startups
            'IRCTC.NS', 'EASEMYTRIP.NS', 'CARTRADE.NS', 'DEVYANI.NS',
            
            # Diversified
            'GODREJIND.NS', 'MAHLIFE.NS', 'WELCORP.NS', 'EIHOTEL.NS'
        ]
        
        gainers = []
        losers = []
        
        for symbol in nse_stocks:
            try:
                ticker = yf.Ticker(symbol)
                
                # Get 2-day history to calculate change
                hist = ticker.history(period="2d")
                
                if not hist.empty and len(hist) >= 2:
                    current_price = hist['Close'].iloc[-1]
                    prev_close = hist['Close'].iloc[-2]
                    
                    change = current_price - prev_close
                    change_percent = (change / prev_close) * 100 if prev_close != 0 else 0
                    
                    stock_data = {
                        'symbol': symbol,
                        'price': current_price,
                        'change': change,
                        'change_percent': change_percent
                    }
                    
                    # Categorize as gainer or loser
                    if change_percent > 0:
                        gainers.append(stock_data)
                    elif change_percent < 0:
                        losers.append(stock_data)
                
            except Exception:
                # Skip individual stocks that fail
                continue
        
        # Sort gainers by percentage change (descending)
        gainers.sort(key=lambda x: x['change_percent'], reverse=True)
        
        # Sort losers by percentage change (ascending - most negative first)
        losers.sort(key=lambda x: x['change_percent'])
        
        return {
            'gainers': gainers[:10],  # Top 10 gainers
            'losers': losers[:10]     # Top 10 losers
        }
        
    except Exception as e:
        # If real-time data fails, try fallback sources
        try:
            sources = [get_nse_data, get_moneycontrol_data]
            
            for source_func in sources:
                try:
                    data = source_func()
                    if data and (data.get('gainers') or data.get('losers')):
                        return data
                except Exception:
                    continue
        except Exception:
            pass
        
        return {'gainers': [], 'losers': []}

def get_nse_data():
    """
    Scrape data from NSE website
    
    Returns:
        dict: Market data
    """
    try:
        # NSE API endpoints (these might change)
        gainers_url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        session = requests.Session()
        session.headers.update(headers)
        
        # Get NSE homepage first (to get cookies)
        session.get("https://www.nseindia.com", timeout=10)
        
        # Now try to get market data
        response = session.get(gainers_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            gainers = []
            losers = []
            
            for stock in data.get('data', []):
                stock_data = {
                    'symbol': stock.get('symbol', ''),
                    'price': stock.get('lastPrice', 0),
                    'change': stock.get('change', 0),
                    'change_percent': stock.get('pChange', 0)
                }
                
                if stock_data['change_percent'] > 0:
                    gainers.append(stock_data)
                elif stock_data['change_percent'] < 0:
                    losers.append(stock_data)
            
            # Sort by change percentage
            gainers.sort(key=lambda x: x['change_percent'], reverse=True)
            losers.sort(key=lambda x: x['change_percent'])
            
            return {
                'gainers': gainers[:10],
                'losers': losers[:10]
            }
        
        return None
        
    except Exception as e:
        return None

def get_moneycontrol_data():
    """
    Scrape data from MoneyControl website
    
    Returns:
        dict: Market data
    """
    try:
        gainers_url = "https://www.moneycontrol.com/stocks/marketstats/indexcomp.php?optex=NSE&opttopic=indexcomp&index=9"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(gainers_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            gainers = []
            losers = []
            
            # Find table with stock data
            tables = soup.find_all('table')
            
            for table in tables:
                rows = table.find_all('tr')
                
                for row in rows[1:]:  # Skip header
                    cells = row.find_all('td')
                    
                    if len(cells) >= 4:
                        try:
                            symbol = cells[0].get_text(strip=True)
                            price = float(cells[1].get_text(strip=True).replace(',', ''))
                            change = float(cells[2].get_text(strip=True).replace(',', ''))
                            change_percent = float(cells[3].get_text(strip=True).replace('%', ''))
                            
                            stock_data = {
                                'symbol': symbol,
                                'price': price,
                                'change': change,
                                'change_percent': change_percent
                            }
                            
                            if change_percent > 0:
                                gainers.append(stock_data)
                            elif change_percent < 0:
                                losers.append(stock_data)
                                
                        except (ValueError, IndexError):
                            continue
            
            # Sort by change percentage
            gainers.sort(key=lambda x: x['change_percent'], reverse=True)
            losers.sort(key=lambda x: x['change_percent'])
            
            return {
                'gainers': gainers[:10],
                'losers': losers[:10]
            }
        
        return None
        
    except Exception as e:
        return None

def get_investing_com_data():
    """
    Scrape data from Investing.com
    
    Returns:
        dict: Market data
    """
    try:
        # Use trafilatura for better content extraction
        gainers_url = "https://in.investing.com/equities/india-adrs"
        
        downloaded = trafilatura.fetch_url(gainers_url)
        if not downloaded:
            return None
        
        text_content = trafilatura.extract(downloaded)
        if not text_content:
            return None
        
        # Parse the content for stock data (simplified approach)
        lines = text_content.split('\n')
        
        gainers = []
        losers = []
        
        for line in lines:
            # Look for patterns that might indicate stock data
            if '%' in line and any(char.isdigit() for char in line):
                # Extract potential stock information
                parts = line.split()
                
                for i, part in enumerate(parts):
                    if '%' in part and part.replace('%', '').replace('-', '').replace('+', '').replace('.', '').isdigit():
                        try:
                            change_percent = float(part.replace('%', '').replace('+', ''))
                            
                            # Try to find symbol and price in nearby parts
                            symbol = parts[i-2] if i >= 2 else f"Stock{len(gainers) + len(losers) + 1}"
                            price = float(parts[i-1].replace(',', '')) if i >= 1 else 0
                            
                            stock_data = {
                                'symbol': symbol,
                                'price': price,
                                'change': price * change_percent / 100,
                                'change_percent': change_percent
                            }
                            
                            if change_percent > 0:
                                gainers.append(stock_data)
                            elif change_percent < 0:
                                losers.append(stock_data)
                                
                        except (ValueError, IndexError):
                            continue
        
        # Sort by change percentage
        gainers.sort(key=lambda x: x['change_percent'], reverse=True)
        losers.sort(key=lambda x: x['change_percent'])
        
        return {
            'gainers': gainers[:10],
            'losers': losers[:10]
        }
        
    except Exception as e:
        return None

@st.cache_data(ttl=300)  # Cache for 5 minutes for real-time data
def get_market_indices():
    """
    Get current market indices data from Yahoo Finance
    
    Returns:
        dict: Market indices data
    """
    try:
        import yfinance as yf
        
        # Define index symbols
        index_symbols = {
            'NIFTY 50': '^NSEI',
            'SENSEX': '^BSESN', 
            'NIFTY BANK': '^NSEBANK',
            'NIFTY IT': '^CNXIT',
            'S&P 500': '^GSPC'
        }
        
        indices = {}
        
        for index_name, symbol in index_symbols.items():
            try:
                # Get ticker data
                ticker = yf.Ticker(symbol)
                
                # Get current data
                hist = ticker.history(period="2d")  # Get 2 days to calculate change
                info = ticker.info
                
                if not hist.empty and len(hist) >= 1:
                    current_price = hist['Close'].iloc[-1]
                    
                    # Calculate change
                    if len(hist) >= 2:
                        prev_close = hist['Close'].iloc[-2]
                    else:
                        # Fallback to info if available
                        prev_close = info.get('regularMarketPreviousClose', current_price)
                    
                    change = current_price - prev_close
                    change_percent = (change / prev_close) * 100 if prev_close != 0 else 0
                    
                    indices[index_name] = {
                        'value': current_price,
                        'change': change,
                        'change_percent': change_percent
                    }
                else:
                    # Fallback if no historical data
                    market_price = info.get('regularMarketPrice', 0)
                    prev_close = info.get('regularMarketPreviousClose', market_price)
                    
                    if market_price and prev_close:
                        change = market_price - prev_close
                        change_percent = (change / prev_close) * 100 if prev_close != 0 else 0
                        
                        indices[index_name] = {
                            'value': market_price,
                            'change': change,
                            'change_percent': change_percent
                        }
                        
            except Exception as e:
                # If individual index fails, continue with others
                continue
        
        # If no real data available, return empty dict
        return indices if indices else {}
        
    except Exception as e:
        return {}

def format_market_data(data):
    """
    Format market data for display
    
    Args:
        data (dict): Raw market data
    
    Returns:
        dict: Formatted market data
    """
    try:
        formatted_data = {
            'gainers': [],
            'losers': []
        }
        
        for gainer in data.get('gainers', []):
            # Determine currency symbol
            currency = "₹" if any(x in gainer['symbol'] for x in ['.NS', '.BO']) else "$"
            formatted_data['gainers'].append({
                'Symbol': gainer['symbol'],
                'Price': f"{currency}{gainer['price']:.2f}",
                'Change': f"{gainer['change']:+.2f}",
                'Change %': f"{gainer['change_percent']:+.2f}%"
            })
        
        for loser in data.get('losers', []):
            # Determine currency symbol  
            currency = "₹" if any(x in loser['symbol'] for x in ['.NS', '.BO']) else "$"
            formatted_data['losers'].append({
                'Symbol': loser['symbol'],
                'Price': f"{currency}{loser['price']:.2f}",
                'Change': f"{loser['change']:+.2f}",
                'Change %': f"{loser['change_percent']:+.2f}%"
            })
        
        return formatted_data
        
    except Exception as e:
        return {'gainers': [], 'losers': []}

def get_sector_performance():
    """
    Get sector-wise performance data
    
    Returns:
        dict: Sector performance data
    """
    try:
        # This would typically come from a financial API
        # For now, return sample data structure
        sectors = [
            {'name': 'Banking', 'change_percent': 1.2},
            {'name': 'IT', 'change_percent': -0.8},
            {'name': 'Pharma', 'change_percent': 2.1},
            {'name': 'Auto', 'change_percent': -1.5},
            {'name': 'FMCG', 'change_percent': 0.3},
            {'name': 'Metals', 'change_percent': 1.8},
            {'name': 'Oil & Gas', 'change_percent': -0.2},
            {'name': 'Realty', 'change_percent': 3.2}
        ]
        
        return sectors
        
    except Exception as e:
        return []

def get_sample_data():
    """
    Get sample market data as fallback
    
    Returns:
        dict: Sample market data
    """
    return {
        'gainers': [
            {'symbol': 'RELIANCE.NS', 'price': 2450.50, 'change': 45.30, 'change_percent': 1.88},
            {'symbol': 'TCS.NS', 'price': 3890.25, 'change': 65.75, 'change_percent': 1.72},
            {'symbol': 'HDFCBANK.NS', 'price': 1650.80, 'change': 25.40, 'change_percent': 1.56},
            {'symbol': 'INFY.NS', 'price': 1745.35, 'change': 22.10, 'change_percent': 1.28},
            {'symbol': 'BHARTIARTL.NS', 'price': 1089.60, 'change': 12.85, 'change_percent': 1.19}
        ],
        'losers': [
            {'symbol': 'TATASTEEL.NS', 'price': 145.75, 'change': -3.25, 'change_percent': -2.18},
            {'symbol': 'BAJFINANCE.NS', 'price': 6890.40, 'change': -125.60, 'change_percent': -1.79},
            {'symbol': 'MARUTI.NS', 'price': 10850.20, 'change': -156.80, 'change_percent': -1.43},
            {'symbol': 'KOTAKBANK.NS', 'price': 1789.50, 'change': -24.50, 'change_percent': -1.35},
            {'symbol': 'WIPRO.NS', 'price': 578.30, 'change': -7.20, 'change_percent': -1.23}
        ]
    }

def validate_market_data(data):
    """
    Validate market data structure
    
    Args:
        data (dict): Market data to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        if not isinstance(data, dict):
            return False
        
        if 'gainers' not in data or 'losers' not in data:
            return False
        
        if not isinstance(data['gainers'], list) or not isinstance(data['losers'], list):
            return False
        
        # Check structure of first item in each list
        for category in ['gainers', 'losers']:
            if data[category]:
                item = data[category][0]
                required_keys = ['symbol', 'price', 'change', 'change_percent']
                
                if not all(key in item for key in required_keys):
                    return False
        
        return True
        
    except Exception as e:
        return False
