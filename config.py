# config.py - Configuration for Financial News Summarizer

import os
from pathlib import Path

# Project Paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
MODELS_DIR = DATA_DIR / 'models'

# Create directories
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# API Keys
NEWSAPI_KEY = os.getenv('NEWSAPI_KEY', 'YOUR_NEWS_API_KEY_HERE')  # Get from newsapi.org

# Model Configuration
SUMMARIZATION_MODEL = 't5-small'
SENTIMENT_MODEL = 'distilbert-base-uncased-finetuned-sst-2-english'
FINANCIAL_SENTIMENT_MODEL = 'ProsusAI/finbert'

# Training Parameters
BATCH_SIZE = 8
LEARNING_RATE = 2e-5
NUM_EPOCHS = 3
MAX_LENGTH = 512
MAX_SUMMARY_LENGTH = 128

# Processing Settings
MIN_ARTICLE_LENGTH = 50  # Minimum characters for processing
MAX_ARTICLES_PER_BATCH = 100

# Power BI Export Settings
EXPORT_FORMAT = 'csv'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
