import streamlit as st
import pandas as pd
from textblob import TextBlob
import re
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import requests
from collections import Counter

class NewsAnalyzer:
    def __init__(self):
        self.positive_keywords = [
            'growth', 'profit', 'gain', 'rise', 'increase', 'bullish', 'positive',
            'strong', 'boost', 'surge', 'rally', 'upgrade', 'buy', 'outperform'
        ]
        
        self.negative_keywords = [
            'loss', 'decline', 'fall', 'drop', 'bearish', 'negative', 'weak',
            'crash', 'plunge', 'downgrade', 'sell', 'underperform', 'concern'
        ]
        
        self.indian_companies = {
            'reliance': 'RELIANCE.NS',
            'tcs': 'TCS.NS',
            'infosys': 'INFY.NS',
            'hdfc': 'HDFCBANK.NS',
            'wipro': 'WIPRO.NS',
            'icici': 'ICICIBANK.NS',
            'sbi': 'SBIN.NS',
            'bharti': 'BHARTIARTL.NS',
            'adani': 'ADANIENT.NS',
            'tata': 'TATAMOTORS.NS'
        }
    
    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of news text using TextBlob"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Convert polarity to sentiment label
            if polarity > 0.1:
                sentiment = 'Positive'
                emoji = '📈'
            elif polarity < -0.1:
                sentiment = 'Negative'
                emoji = '📉'
            else:
                sentiment = 'Neutral'
                emoji = '➡️'
            
            # Calculate confidence based on subjectivity
            confidence = (1 - subjectivity) * 100
            
            return {
                'sentiment': sentiment,
                'polarity': polarity,
                'subjectivity': subjectivity,
                'confidence': confidence,
                'emoji': emoji
            }
        except Exception as e:
            st.error(f"Error analyzing sentiment: {str(e)}")
            return {
                'sentiment': 'Neutral',
                'polarity': 0,
                'subjectivity': 0.5,
                'confidence': 0,
                'emoji': '➡️'
            }
    
    def extract_market_impact_keywords(self, text: str) -> Dict:
        """Extract market impact keywords from news text"""
        text_lower = text.lower()
        
        positive_count = sum(1 for keyword in self.positive_keywords if keyword in text_lower)
        negative_count = sum(1 for keyword in self.negative_keywords if keyword in text_lower)
        
        impact_score = positive_count - negative_count
        
        if impact_score > 0:
            impact = 'Bullish'
            color = 'green'
        elif impact_score < 0:
            impact = 'Bearish'
            color = 'red'
        else:
            impact = 'Neutral'
            color = 'gray'
        
        return {
            'impact': impact,
            'score': impact_score,
            'positive_keywords': positive_count,
            'negative_keywords': negative_count,
            'color': color
        }
    
    def categorize_news(self, news_item: Dict) -> str:
        """Categorize news into different types"""
        headline = news_item.get('headline', '').lower()
        summary = news_item.get('summary', '').lower()
        text = f"{headline} {summary}"
        
        categories = {
            'Earnings': ['earnings', 'profit', 'revenue', 'quarterly', 'annual', 'results'],
            'Merger & Acquisition': ['merger', 'acquisition', 'takeover', 'buyout', 'deal'],
            'Market News': ['market', 'trading', 'index', 'nifty', 'sensex', 'exchange'],
            'Policy & Regulation': ['policy', 'regulation', 'government', 'rbi', 'sebi', 'ministry'],
            'Technology': ['technology', 'digital', 'ai', 'automation', 'tech', 'innovation'],
            'Banking & Finance': ['bank', 'finance', 'loan', 'credit', 'npa', 'deposit'],
            'Energy': ['oil', 'gas', 'renewable', 'solar', 'energy', 'power'],
            'Auto': ['auto', 'car', 'vehicle', 'automobile', 'ev', 'electric'],
            'Pharma & Healthcare': ['pharma', 'drug', 'medicine', 'healthcare', 'hospital'],
            'Real Estate': ['real estate', 'property', 'housing', 'construction', 'builder']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return 'General'
    
    def extract_mentioned_companies(self, text: str) -> List[str]:
        """Extract mentioned Indian companies from news text"""
        text_lower = text.lower()
        mentioned = []
        
        for company, symbol in self.indian_companies.items():
            if company in text_lower:
                mentioned.append(symbol)
        
        return list(set(mentioned))  # Remove duplicates
    
    def analyze_news_batch(self, news_list: List[Dict]) -> Dict:
        """Analyze a batch of news articles"""
        if not news_list:
            return {
                'total_articles': 0,
                'sentiment_distribution': {},
                'category_distribution': {},
                'overall_sentiment': 'Neutral',
                'top_companies': [],
                'market_impact': 'Neutral'
            }
        
        analyzed_news = []
        sentiment_counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
        category_counts = Counter()
        all_companies = []
        total_polarity = 0
        
        for news_item in news_list:
            # Analyze individual news item
            headline = news_item.get('headline', '')
            summary = news_item.get('summary', '')
            text = f"{headline} {summary}"
            
            sentiment_analysis = self.analyze_sentiment(text)
            market_impact = self.extract_market_impact_keywords(text)
            category = self.categorize_news(news_item)
            mentioned_companies = self.extract_mentioned_companies(text)
            
            analyzed_item = {
                'original': news_item,
                'sentiment': sentiment_analysis,
                'market_impact': market_impact,
                'category': category,
                'mentioned_companies': mentioned_companies,
                'datetime': datetime.fromtimestamp(news_item.get('datetime', 0)) if news_item.get('datetime') else datetime.now()
            }
            
            analyzed_news.append(analyzed_item)
            
            # Update counters
            sentiment_counts[sentiment_analysis['sentiment']] += 1
            category_counts[category] += 1
            all_companies.extend(mentioned_companies)
            total_polarity += sentiment_analysis['polarity']
        
        # Calculate overall metrics
        avg_polarity = total_polarity / len(news_list) if news_list else 0
        
        if avg_polarity > 0.1:
            overall_sentiment = 'Positive'
            market_impact = 'Bullish'
        elif avg_polarity < -0.1:
            overall_sentiment = 'Negative'
            market_impact = 'Bearish'
        else:
            overall_sentiment = 'Neutral'
            market_impact = 'Mixed'
        
        # Get top mentioned companies
        company_counts = Counter(all_companies)
        top_companies = company_counts.most_common(5)
        
        return {
            'analyzed_news': analyzed_news,
            'total_articles': len(news_list),
            'sentiment_distribution': sentiment_counts,
            'category_distribution': dict(category_counts),
            'overall_sentiment': overall_sentiment,
            'market_impact': market_impact,
            'average_polarity': avg_polarity,
            'top_companies': top_companies
        }
    
    def generate_news_summary(self, analyzed_data: Dict) -> str:
        """Generate a text summary of news analysis"""
        if analyzed_data['total_articles'] == 0:
            return "No news articles to analyze."
        
        total = analyzed_data['total_articles']
        sentiment_dist = analyzed_data['sentiment_distribution']
        overall_sentiment = analyzed_data['overall_sentiment']
        market_impact = analyzed_data['market_impact']
        
        positive_pct = (sentiment_dist.get('Positive', 0) / total) * 100
        negative_pct = (sentiment_dist.get('Negative', 0) / total) * 100
        neutral_pct = (sentiment_dist.get('Neutral', 0) / total) * 100
        
        summary = f"""
        📊 **News Analysis Summary**
        
        **Total Articles Analyzed:** {total}
        
        **Sentiment Breakdown:**
        - 📈 Positive: {sentiment_dist.get('Positive', 0)} articles ({positive_pct:.1f}%)
        - 📉 Negative: {sentiment_dist.get('Negative', 0)} articles ({negative_pct:.1f}%)
        - ➡️ Neutral: {sentiment_dist.get('Neutral', 0)} articles ({neutral_pct:.1f}%)
        
        **Overall Market Sentiment:** {overall_sentiment} ({market_impact})
        
        **Top News Categories:**
        """
        
        for category, count in list(analyzed_data['category_distribution'].items())[:3]:
            percentage = (count / total) * 100
            summary += f"\n- {category}: {count} articles ({percentage:.1f}%)"
        
        if analyzed_data['top_companies']:
            summary += "\n\n**Most Mentioned Companies:**"
            for company, count in analyzed_data['top_companies'][:3]:
                summary += f"\n- {company}: {count} mentions"
        
        return summary
    
    def filter_news_by_sentiment(self, analyzed_news: List[Dict], sentiment: str) -> List[Dict]:
        """Filter news by sentiment"""
        return [news for news in analyzed_news if news['sentiment']['sentiment'] == sentiment]
    
    def filter_news_by_category(self, analyzed_news: List[Dict], category: str) -> List[Dict]:
        """Filter news by category"""
        return [news for news in analyzed_news if news['category'] == category]
    
    def get_trending_topics(self, analyzed_news: List[Dict]) -> List[Tuple[str, int]]:
        """Extract trending topics from news headlines"""
        all_headlines = [news['original'].get('headline', '') for news in analyzed_news]
        
        # Simple keyword extraction (could be improved with NLP)
        keywords = []
        for headline in all_headlines:
            words = re.findall(r'\b[A-Za-z]{4,}\b', headline.lower())
            keywords.extend(words)
        
        # Filter out common words
        stop_words = {'said', 'says', 'will', 'with', 'from', 'this', 'that', 'they', 'their', 'company', 'market', 'stock', 'share', 'price'}
        filtered_keywords = [word for word in keywords if word not in stop_words]
        
        keyword_counts = Counter(filtered_keywords)
        return keyword_counts.most_common(10)
