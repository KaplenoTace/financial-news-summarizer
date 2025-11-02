# summarize.py - Summarization and sentiment analysis

import torch
from transformers import pipeline
import pandas as pd
from datetime import datetime
from config import *
import logging
import glob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinancialNewsSummarizer:
    def __init__(self, use_pretrained=True):
        self.device = 0 if torch.cuda.is_available() else -1
        
        # Load pre-trained models
        logger.info("Loading sentiment analysis model...")
        self.sentiment_analyzer = pipeline(
            'sentiment-analysis',
            model='ProsusAI/finbert',
            device=self.device
        )
        
        logger.info("Loading summarization model...")
        self.summarizer = pipeline(
            'summarization',
            model='facebook/bart-large-cnn',
            device=self.device
        )
    
    def analyze_sentiment(self, text):
        '''Analyze sentiment of text'''
        try:
            result = self.sentiment_analyzer(text[:512])[0]
            return {
                'sentiment': result['label'],
                'confidence': result['score']
            }
        except Exception as e:
            logger.warning(f"Sentiment analysis failed: {e}")
            return {'sentiment': 'neutral', 'confidence': 0.5}
    
    def summarize_text(self, text, max_length=130, min_length=30):
        '''Summarize text'''
        try:
            summary = self.summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )[0]['summary_text']
            return summary
        except Exception as e:
            logger.warning(f"Summarization failed: {e}")
            return text[:200] + '...'
    
    def process_news_batch(self, df):
        '''Process a batch of news articles'''
        results = []
        
        for idx, row in df.iterrows():
            logger.info(f"Processing {idx + 1}/{len(df)}...")
            
            text = row.get('content') or row.get('description') or row.get('title', '')
            
            if len(text) < MIN_ARTICLE_LENGTH:
                logger.warning(f"Skipping article {idx}: too short")
                continue
            
            summary = self.summarize_text(text)
            sentiment_result = self.analyze_sentiment(text)
            
            results.append({
                'original_title': row.get('title', ''),
                'source': row.get('source', ''),
                'url': row.get('url', ''),
                'published_at': row.get('published_at', ''),
                'summary': summary,
                'sentiment': sentiment_result['sentiment'],
                'sentiment_score': sentiment_result['confidence'],
                'processed_at': datetime.now()
            })
        
        return pd.DataFrame(results)
    
    def save_results(self, df, filename=None):
        if filename is None:
            filename = f'processed_news_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        filepath = PROCESSED_DATA_DIR / filename
        df.to_csv(filepath, index=False)
        logger.info(f"Saved to {filepath}")
        return filepath

if __name__ == '__main__':
    import glob
    
    summarizer = FinancialNewsSummarizer()
    news_files = glob.glob(str(RAW_DATA_DIR / '*.csv'))
    
    if news_files:
        latest_file = max(news_files)
        logger.info(f"Processing {latest_file}")
        df = pd.read_csv(latest_file)
        results = summarizer.process_news_batch(df)
        summarizer.save_results(results)
    else:
        logger.error("No news files found. Run fetch_news.py first.")
