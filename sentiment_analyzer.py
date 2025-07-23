import json
import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime, timedelta
import logging
import yfinance as yf
import requests
from newspaper import Article
import re
import time
from typing import List, Dict, Optional
import numpy as np
import os
from dotenv import load_dotenv
import praw

class SentimentAnalyzer:
    def __init__(self, config_path="config.json"):
        # Load environment variables
        load_dotenv()
        
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.vader = SentimentIntensityAnalyzer()
        self.logger = self._setup_logger()
        
        # Initialize Reddit API if credentials are available
        self.reddit = self._setup_reddit()
    
    def _setup_logger(self):
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(__name__)
    
    def _setup_reddit(self):
        """Initialize Reddit API client"""
        try:
            client_id = os.getenv('REDDIT_CLIENT_ID')
            client_secret = os.getenv('REDDIT_CLIENT_SECRET')
            user_agent = os.getenv('REDDIT_USER_AGENT')
            
            if client_id and client_secret and user_agent:
                reddit = praw.Reddit(
                    client_id=client_id,
                    client_secret=client_secret,
                    user_agent=user_agent
                )
                self.logger.info("Reddit API initialized successfully")
                return reddit
            else:
                self.logger.warning("Reddit API credentials not found in .env file")
                return None
        except Exception as e:
            self.logger.error(f"Failed to initialize Reddit API: {e}")
            return None
    
    def analyze_text(self, text):
        """Analyze sentiment of a single text using multiple methods"""
        # VADER sentiment (good for social media)
        vader_scores = self.vader.polarity_scores(text)
        
        # TextBlob sentiment (good for formal text)
        blob = TextBlob(text)
        textblob_polarity = blob.sentiment.polarity
        textblob_subjectivity = blob.sentiment.subjectivity
        
        # Combined score
        combined_score = (vader_scores['compound'] + textblob_polarity) / 2
        
        return {
            'vader_compound': vader_scores['compound'],
            'vader_positive': vader_scores['pos'],
            'vader_negative': vader_scores['neg'],
            'vader_neutral': vader_scores['neu'],
            'textblob_polarity': textblob_polarity,
            'textblob_subjectivity': textblob_subjectivity,
            'combined_score': combined_score,
            'sentiment_label': self._get_sentiment_label(combined_score)
        }
    
    def _get_sentiment_label(self, score):
        """Convert numerical score to categorical label"""
        if score >= 0.1:
            return 'positive'
        elif score <= -0.1:
            return 'negative'
        else:
            return 'neutral'
    
    def analyze_batch(self, texts):
        """Analyze sentiment for multiple texts"""
        results = []
        for text in texts:
            result = self.analyze_text(text)
            result['text'] = text[:100] + "..." if len(text) > 100 else text
            results.append(result)
        
        return pd.DataFrame(results)
    
    def calculate_weighted_sentiment(self, news_sentiment, social_sentiment, technical_sentiment=0):
        """Calculate weighted sentiment score based on different sources"""
        weights = self.config['sentiment_weights']
        
        weighted_score = (
            news_sentiment * weights['news'] +
            social_sentiment * weights['social'] +
            technical_sentiment * weights['technical']
        )
        
        return weighted_score
    
    def get_stock_news_sentiment(self, symbol: str, days_back: int = 7) -> Dict:
        """Get sentiment analysis for stock-related news"""
        try:
            # Get stock info
            stock = yf.Ticker(symbol)
            
            # Get recent news
            news = stock.news
            if not news:
                self.logger.warning(f"No news found for {symbol}")
                return {'sentiment': 0, 'articles_count': 0, 'confidence': 0}
            
            # Analyze news sentiment
            sentiments = []
            valid_articles = 0
            
            for article in news[:10]:  # Limit to recent 10 articles
                try:
                    title = article.get('title', '')
                    summary = article.get('summary', '')
                    text = f"{title}. {summary}"
                    
                    if text.strip():
                        sentiment = self.analyze_text(text)
                        sentiments.append(sentiment['combined_score'])
                        valid_articles += 1
                        
                except Exception as e:
                    self.logger.error(f"Error processing article: {e}")
                    continue
            
            if not sentiments:
                return {'sentiment': 0, 'articles_count': 0, 'confidence': 0}
            
            avg_sentiment = np.mean(sentiments)
            confidence = min(valid_articles / 5.0, 1.0)  # Confidence based on article count
            
            return {
                'sentiment': avg_sentiment,
                'articles_count': valid_articles,
                'confidence': confidence,
                'sentiment_label': self._get_sentiment_label(avg_sentiment)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting news sentiment for {symbol}: {e}")
            return {'sentiment': 0, 'articles_count': 0, 'confidence': 0}
    
    def get_reddit_sentiment(self, symbol: str, limit: int = 25) -> Dict:
        """Get sentiment from Reddit discussions"""
        if not self.reddit:
            self.logger.info(f"Reddit sentiment analysis for {symbol} - API integration needed")
            return {'sentiment': 0, 'posts_count': 0, 'confidence': 0}
        
        try:
            # Search for posts about the stock symbol
            subreddits = ['stocks', 'investing', 'SecurityAnalysis', 'ValueInvesting', 'StockMarket']
            all_posts = []
            
            for subreddit_name in subreddits:
                try:
                    subreddit = self.reddit.subreddit(subreddit_name)
                    # Search for the stock symbol
                    posts = subreddit.search(f"{symbol} OR ${symbol}", limit=limit//len(subreddits), time_filter='week')
                    
                    for post in posts:
                        if post.selftext and len(post.selftext) > 20:  # Filter out very short posts
                            all_posts.append({
                                'title': post.title,
                                'text': post.selftext[:500],  # Limit text length
                                'score': post.score,
                                'created': post.created_utc
                            })
                except Exception as e:
                    self.logger.warning(f"Error accessing subreddit {subreddit_name}: {e}")
                    continue
            
            if not all_posts:
                return {'sentiment': 0, 'posts_count': 0, 'confidence': 0}
            
            # Analyze sentiment of posts
            sentiments = []
            for post in all_posts:
                text = f"{post['title']}. {post['text']}"
                sentiment = self.analyze_text(text)
                # Weight by post score (upvotes)
                weight = max(1, post['score']) if post['score'] > 0 else 1
                sentiments.extend([sentiment['combined_score']] * min(weight, 5))  # Cap weight at 5
            
            if sentiments:
                avg_sentiment = np.mean(sentiments)
                confidence = min(len(all_posts) / 10.0, 1.0)  # Confidence based on post count
                
                return {
                    'sentiment': avg_sentiment,
                    'posts_count': len(all_posts),
                    'confidence': confidence,
                    'sentiment_label': self._get_sentiment_label(avg_sentiment)
                }
            
            return {'sentiment': 0, 'posts_count': 0, 'confidence': 0}
            
        except Exception as e:
            self.logger.error(f"Error getting Reddit sentiment for {symbol}: {e}")
            return {'sentiment': 0, 'posts_count': 0, 'confidence': 0}
    
    def analyze_stock_sentiment(self, symbol: str) -> Dict:
        """Comprehensive stock sentiment analysis"""
        self.logger.info(f"Analyzing sentiment for {symbol}")
        
        # Get news sentiment
        news_sentiment = self.get_stock_news_sentiment(symbol)
        
        # Get social media sentiment (placeholder)
        social_sentiment = self.get_reddit_sentiment(symbol)
        
        # Calculate weighted sentiment
        weighted_sentiment = self.calculate_weighted_sentiment(
            news_sentiment['sentiment'],
            social_sentiment['sentiment']
        )
        
        # Get stock price data for context
        stock_data = self.get_stock_context(symbol)
        
        return {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'news_sentiment': news_sentiment,
            'social_sentiment': social_sentiment,
            'weighted_sentiment': weighted_sentiment,
            'sentiment_label': self._get_sentiment_label(weighted_sentiment),
            'stock_context': stock_data,
            'recommendation': self._get_stock_recommendation(weighted_sentiment, stock_data)
        }
    
    def get_stock_context(self, symbol: str) -> Dict:
        """Get basic stock context data"""
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="5d")
            info = stock.info
            
            if hist.empty:
                return {'error': 'No price data available'}
            
            current_price = hist['Close'].iloc[-1]
            prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            price_change = ((current_price - prev_price) / prev_price) * 100
            
            return {
                'current_price': round(current_price, 2),
                'price_change_pct': round(price_change, 2),
                'volume': int(hist['Volume'].iloc[-1]) if 'Volume' in hist else 0,
                'market_cap': info.get('marketCap', 'N/A'),
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'company_name': info.get('longName', symbol)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting stock context for {symbol}: {e}")
            return {'error': str(e)}
    
    def _get_stock_recommendation(self, sentiment: float, stock_data: Dict) -> str:
        """Generate basic stock recommendation based on sentiment and price action"""
        if 'error' in stock_data:
            return "HOLD - Insufficient data"
        
        price_change = stock_data.get('price_change_pct', 0)
        
        # Simple recommendation logic
        if sentiment > 0.3 and price_change > 0:
            return "BUY - Strong positive sentiment with price momentum"
        elif sentiment > 0.1:
            return "BUY - Positive sentiment detected"
        elif sentiment < -0.3 and price_change < 0:
            return "SELL - Strong negative sentiment with price decline"
        elif sentiment < -0.1:
            return "SELL - Negative sentiment detected"
        else:
            return "HOLD - Neutral sentiment"
    
    def analyze_portfolio_sentiment(self, symbols: List[str]) -> pd.DataFrame:
        """Analyze sentiment for multiple stocks"""
        results = []
        
        for symbol in symbols:
            try:
                result = self.analyze_stock_sentiment(symbol)
                results.append(result)
                time.sleep(1)  # Rate limiting
            except Exception as e:
                self.logger.error(f"Error analyzing {symbol}: {e}")
                continue
        
        return pd.DataFrame(results)
    
    def get_sector_sentiment(self, sector_symbols: Dict[str, List[str]]) -> Dict:
        """Analyze sentiment by sector"""
        sector_results = {}
        
        for sector, symbols in sector_symbols.items():
            self.logger.info(f"Analyzing {sector} sector")
            sector_sentiments = []
            
            for symbol in symbols:
                try:
                    result = self.analyze_stock_sentiment(symbol)
                    sector_sentiments.append(result['weighted_sentiment'])
                    time.sleep(1)
                except Exception as e:
                    self.logger.error(f"Error analyzing {symbol} in {sector}: {e}")
                    continue
            
            if sector_sentiments:
                avg_sentiment = np.mean(sector_sentiments)
                sector_results[sector] = {
                    'average_sentiment': avg_sentiment,
                    'sentiment_label': self._get_sentiment_label(avg_sentiment),
                    'stocks_analyzed': len(sector_sentiments)
                }
        
        return sector_results