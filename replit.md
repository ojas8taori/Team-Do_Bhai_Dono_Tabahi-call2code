# Stonks GPT - Indian Stock Market Platform

## Overview

Stonks GPT is a comprehensive Streamlit-based web application designed specifically for Indian stock market analysis and education. The platform provides real-time market data, technical analysis, news sentiment analysis, and an interactive learning mode with multilingual support (English and Hindi). The application focuses on NSE and BSE markets, offering both beginner-friendly features and advanced analytical tools.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit with custom CSS styling
- **UI Components**: Modular component-based architecture with reusable widgets
- **Theming**: Dynamic light/dark mode with Indian market-inspired color scheme (saffron, green, BSE blue, NSE green)
- **Responsive Design**: Wide layout optimized for financial dashboards
- **Accessibility**: Voice synthesis support and accessibility mode for inclusive design

### Backend Architecture
- **Data Layer**: Multi-source data fetching with caching mechanisms
- **Analysis Engine**: Custom technical analysis and news sentiment processing
- **Session Management**: Streamlit session state for user preferences and navigation
- **Error Handling**: Comprehensive error management with user-friendly fallbacks

### Component Structure
```
app.py                 # Main application entry point
components/           # UI components
├── dashboard.py      # Main market dashboard
├── stock_analysis.py # Individual stock analysis
├── news_feed.py      # News and sentiment analysis
├── market_overview.py # Market-wide overview
├── story_mode.py     # Educational interactive mode
└── error_handler.py  # Error page handling
utils/               # Business logic utilities
├── data_fetcher.py   # Market data retrieval
├── technical_analysis.py # Technical indicators
├── news_analyzer.py  # News sentiment analysis
└── speech_handler.py # Voice/accessibility features
```

## Key Components

### Data Sources
- **Primary**: Yahoo Finance API for real-time stock data and historical prices
- **Secondary**: Finnhub API for additional market data and news
- **Caching**: 5-minute TTL for market data to balance freshness with performance

### Market Coverage
- **Indices**: NIFTY 50, BSE SENSEX, NIFTY Bank, NIFTY IT
- **Stocks**: Focus on Indian blue-chip stocks with NSE/BSE listings
- **Sectors**: Technology, Banking, Energy, Consumer goods, and more

### Technical Analysis Features
- Moving averages (SMA, EMA)
- Momentum indicators (RSI, MACD)
- Volatility indicators (Bollinger Bands)
- Chart patterns and trading signals
- Custom Indian market-specific analysis

### Educational Features
- Interactive story mode with character-based learning
- Multilingual content (English/Hindi)
- Voice narration for accessibility
- Progressive difficulty levels

## Data Flow

1. **Data Ingestion**: Multi-source data fetching from Yahoo Finance and Finnhub APIs
2. **Processing**: Real-time technical analysis and sentiment processing
3. **Caching**: Streamlit cache decorators for performance optimization
4. **Presentation**: Dynamic dashboard rendering with plotly visualizations
5. **User Interaction**: Session state management for personalized experience

## External Dependencies

### APIs and Data Sources
- **Yahoo Finance**: Primary source for Indian stock market data
- **Finnhub**: Secondary data source and news feeds
- **TextBlob**: Natural language processing for news sentiment analysis

### Python Libraries
- **Streamlit**: Web application framework
- **Plotly**: Interactive financial charts and visualizations
- **Pandas/NumPy**: Data manipulation and numerical analysis
- **yfinance**: Yahoo Finance data wrapper
- **finnhub-python**: Finnhub API client

### Frontend Libraries
- **streamlit-option-menu**: Enhanced navigation components
- **Custom CSS**: Indian market-themed styling with responsive design

## Deployment Strategy

### Environment Setup
- Python 3.8+ runtime environment
- Environment variables for API keys (FINNHUB_API_KEY)
- Static asset serving for translations and market data

### Configuration
- Page configuration optimized for financial dashboards
- Wide layout with expanded sidebar
- Custom favicon and page title
- CSS injection for consistent theming

### Performance Optimization
- Data caching with appropriate TTL values
- Lazy loading for heavy computational tasks
- Efficient session state management
- Spinner animations for better user experience

## Changelog
- July 05, 2025: Initial setup
- July 05, 2025: Updated app name to "Stonks GPT", fixed settings panel functionality (dark mode, language switching, voice features now work properly), expanded stock database from 10 to 50+ stocks with sector-wise filtering
- July 05, 2025: Completed migration from Replit Agent to Replit environment. Enhanced styling with vibrant gradients, improved dark mode visibility (fixed black text issues), added colorful aesthetic elements including Indian flag-inspired gradients, enhanced button animations, and improved form element styling for better user experience in both light and dark modes

## User Preferences

Preferred communication style: Simple, everyday language.