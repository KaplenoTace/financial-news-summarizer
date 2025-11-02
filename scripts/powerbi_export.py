# powerbi_export.py - Prepare data for Power BI

import pandas as pd
from datetime import datetime
from config import PROCESSED_DATA_DIR
import logging
import glob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PowerBIExporter:
    def __init__(self):
        self.processed_dir = PROCESSED_DATA_DIR
    
    def prepare_powerbi_dataset(self, input_file):
        logger.info(f"Loading data from {input_file}")
        df = pd.read_csv(input_file)
        
        # Convert sentiment to numeric
        sentiment_map = {
            'positive': 1, 'POSITIVE': 1,
            'negative': -1, 'NEGATIVE': -1,
            'neutral': 0, 'NEUTRAL': 0
        }
        df['sentiment_numeric'] = df['sentiment'].map(sentiment_map).fillna(0)
        
        # Extract date features
        df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce')
        df['date'] = df['published_at'].dt.date
        df['hour'] = df['published_at'].dt.hour
        df['day_of_week'] = df['published_at'].dt.day_name()
        df['month'] = df['published_at'].dt.month
        df['year'] = df['published_at'].dt.year
        
        # Categorize news
        def categorize(text):
            text = str(text).lower()
            if any(w in text for w in ['stock', 'market', 'trading', 'shares']):
                return 'Stock Market'
            elif any(w in text for w in ['bank', 'interest', 'fed', 'rate']):
                return 'Banking'
            elif any(w in text for w in ['tech', 'ai', 'software', 'technology']):
                return 'Technology'
            elif any(w in text for w in ['crypto', 'bitcoin', 'blockchain']):
                return 'Cryptocurrency'
            elif any(w in text for w in ['energy', 'oil', 'gas']):
                return 'Energy'
            else:
                return 'General'
        
        df['category'] = df['summary'].apply(categorize)
        
        # Calculate sentiment strength (absolute value)
        df['sentiment_strength'] = df['sentiment_score'].abs()
        
        # Create text length features
        df['summary_length'] = df['summary'].str.len()
        df['title_length'] = df['original_title'].str.len()
        
        # Drop rows with missing critical data
        df_clean = df.dropna(subset=['summary', 'sentiment'])
        
        logger.info(f"Prepared {len(df_clean)} records for Power BI")
        return df_clean
    
    def export_for_powerbi(self, df):
        filename = f'powerbi_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        filepath = self.processed_dir / filename
        df.to_csv(filepath, index=False)
        logger.info(f"Exported to: {filepath}")
        return filepath
    
    def generate_summary_stats(self, df):
        '''Generate summary statistics for dashboard'''
        stats = {
            'total_articles': len(df),
            'avg_sentiment': df['sentiment_numeric'].mean(),
            'positive_count': (df['sentiment_numeric'] == 1).sum(),
            'negative_count': (df['sentiment_numeric'] == -1).sum(),
            'neutral_count': (df['sentiment_numeric'] == 0).sum(),
            'avg_sentiment_score': df['sentiment_score'].mean(),
            'sources_count': df['source'].nunique(),
            'date_range': {
                'start': df['published_at'].min(),
                'end': df['published_at'].max()
            }
        }
        return stats

if __name__ == '__main__':
    exporter = PowerBIExporter()
    files = glob.glob(str(PROCESSED_DATA_DIR / 'processed_news_*.csv'))
    
    if files:
        latest_file = max(files)
        logger.info(f"Processing {latest_file}")
        df_powerbi = exporter.prepare_powerbi_dataset(latest_file)
        
        # Generate and print stats
        stats = exporter.generate_summary_stats(df_powerbi)
        logger.info(f"Summary stats: {stats}")
        
        # Export for Power BI
        exporter.export_for_powerbi(df_powerbi)
    else:
        logger.error("No processed files found. Run summarize.py first.")
