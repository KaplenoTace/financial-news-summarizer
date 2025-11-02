# fetch_news.py - Fetch financial news from multiple sources

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from config import NEWSAPI_KEY, RAW_DATA_DIR
from newsapi import NewsApiClient
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsCollector:
    def __init__(self, api_key=None):
        self.api_key = api_key or NEWSAPI_KEY
        if self.api_key and self.api_key != 'YOUR_NEWS_API_KEY_HERE':
            self.newsapi = NewsApiClient(api_key=self.api_key)
        else:
            self.newsapi = None
            logger.warning("No valid API key. Using sample data.")
    
    def fetch_newsapi_articles(self, query='finance', days_back=7):
        '''Fetch news from NewsAPI.org'''
        if not self.newsapi:
            return self._get_sample_data()
        
        try:
            from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            articles = self.newsapi.get_everything(
                q=query,
                language='en',
                from_param=from_date,
                sort_by='relevancy',
                page_size=100
            )
            
            data = []
            for article in articles['articles']:
                data.append({
                    'title': article['title'],
                    'description': article['description'],
                    'content': article['content'],
                    'url': article['url'],
                    'source': article['source']['name'],
                    'published_at': article['publishedAt'],
                    'author': article['author']
                })
            
            return pd.DataFrame(data)
        
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return self._get_sample_data()
    
    def _get_sample_data(self):
        '''Return sample financial news for testing'''
        sample_data = [
            {
                'title': 'Federal Reserve Raises Interest Rates',
                'description': 'The Fed announced a quarter-point rate hike...',
                'content': 'In a widely anticipated move, the Federal Reserve...',
                'url': 'https://example.com/fed-rates',
                'source': 'Financial Times',
                'published_at': datetime.now().isoformat(),
                'author': 'John Smith'
            },
            {
                'title': 'Stock Market Reaches New Highs',
                'description': 'Major indices close at record levels...',
                'content': 'The S&P 500 and Dow Jones reached all-time highs...',
                'url': 'https://example.com/stock-highs',
                'source': 'Wall Street Journal',
                'published_at': datetime.now().isoformat(),
                'author': 'Jane Doe'
            },
            {
                'title': 'Tech Stocks Lead Market Rally',
                'description': 'Technology sector shows strong performance...',
                'content': 'Leading tech companies posted impressive earnings...',
                'url': 'https://example.com/tech-rally',
                'source': 'Bloomberg',
                'published_at': datetime.now().isoformat(),
                'author': 'Bob Johnson'
            }
        ]
        return pd.DataFrame(sample_data)
    
    def save_news_data(self, df, filename=None):
        '''Save collected news to CSV'''
        if filename is None:
            filename = f'financial_news_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        filepath = RAW_DATA_DIR / filename
        df.to_csv(filepath, index=False)
        logger.info(f"Saved {len(df)} articles to {filepath}")
        return filepath

if __name__ == '__main__':
    collector = NewsCollector()
    logger.info("Fetching financial news...")
    df = collector.fetch_newsapi_articles(query='stock market finance', days_back=7)
    logger.info(f"Collected {len(df)} articles")
    collector.save_news_data(df)
