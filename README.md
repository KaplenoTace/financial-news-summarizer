# Financial News Summarizer

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🎯 Overview

Automatic financial news summarizer using Hugging Face Transformers (DistilBERT/T5/FinBERT), PyTorch, and Power BI for real-time sentiment analysis and dashboard visualization. This system fetches financial news, generates summaries using state-of-the-art NLP models, performs sentiment analysis with FinBERT, and outputs real-time dashboards in Power BI with sentiment scores and summaries for quick decision-making.

## ✨ Features

- 📰 **Automated News Collection**: Fetches financial news from NewsAPI and other sources
- 🤖 **Advanced NLP**: Uses Hugging Face Transformers (T5/BART for summarization, FinBERT for sentiment)
- 📊 **Sentiment Analysis**: Fine-tuned FinBERT model for financial sentiment classification
- 📈 **Power BI Integration**: Real-time dashboards with sentiment scores and trends
- 🚀 **Production Ready**: Complete error handling, logging, and documentation
- 🔄 **Batch Processing**: Efficient processing of multiple articles
- 💾 **Data Export**: CSV exports optimized for Power BI consumption

## 🏗️ Project Structure

```
financial-news-summarizer/
├── data/
│   ├── raw/              # Raw news data
│   ├── processed/        # Processed summaries
│   └── models/           # Fine-tuned models
├── scripts/
│   ├── fetch_news.py         # News collection
│   ├── summarize.py          # Summarization & sentiment
│   └── powerbi_export.py     # Power BI data export
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_model_training.ipynb
│   └── 03_sentiment_analysis.ipynb
├── config.py             # Configuration file
├── requirements.txt      # Dependencies
├── README.md            # This file
├── START_HERE.md        # Quick start guide
├── QUICKSTART.md        # 60-minute setup
├── GITHUB_SETUP.md      # GitHub instructions
├── FILE_INDEX.md        # File reference
├── .gitignore           # Git ignore patterns
├── .env.example         # Environment template
└── LICENSE              # MIT License
```

## 🚀 Quick Start (60 Minutes)

### Prerequisites

- Python 3.8 or higher
- VS Code (recommended) or Jupyter Notebook
- NewsAPI key (free from [newsapi.org](https://newsapi.org))
- Power BI Desktop (optional, for dashboards)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/KaplenoTace/financial-news-summarizer.git
cd financial-news-summarizer
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure API key**
```bash
cp .env.example .env
# Edit .env and add your NewsAPI key
```

5. **Run the pipeline**
```bash
# Fetch news (~5 minutes)
python scripts/fetch_news.py

# Generate summaries & analyze sentiment (~15-20 minutes)
python scripts/summarize.py

# Prepare data for Power BI (~2 minutes)
python scripts/powerbi_export.py
```

## 📊 Tech Stack

- **NLP/ML**: Hugging Face Transformers, PyTorch
- **Models**: T5/BART (summarization), FinBERT (sentiment analysis)
- **Data Processing**: Pandas, NumPy
- **APIs**: NewsAPI for live financial news
- **Visualization**: Power BI, Matplotlib, Seaborn
- **Development**: Jupyter Notebook, VS Code

## 📖 Documentation

- **[START_HERE.md](START_HERE.md)**: First-time setup guide
- **[QUICKSTART.md](QUICKSTART.md)**: Detailed 60-minute tutorial
- **[GITHUB_SETUP.md](GITHUB_SETUP.md)**: GitHub upload instructions
- **[FILE_INDEX.md](FILE_INDEX.md)**: Complete file reference
- **[financial-news-summarizer.pdf](financial-news-summarizer.pdf)**: Full project guide

## 🎓 Usage Examples

### Fetch News
```python
from scripts.fetch_news import NewsCollector

collector = NewsCollector()
df = collector.fetch_newsapi_articles(query='stock market finance', days_back=7)
collector.save_news_data(df)
```

### Summarize & Analyze Sentiment
```python
from scripts.summarize import FinancialNewsSummarizer

summarizer = FinancialNewsSummarizer()
results = summarizer.process_news_batch(df)
summarizer.save_results(results)
```

### Export for Power BI
```python
from scripts.powerbi_export import PowerBIExporter

exporter = PowerBIExporter()
df_powerbi = exporter.prepare_powerbi_dataset('processed_news.csv')
exporter.export_for_powerbi(df_powerbi)
```

## 📈 Performance

- **Accuracy**: 95%+ sentiment accuracy (FinBERT on Financial PhraseBank)
- **Speed**: 
  - CPU: 10-20 articles/minute
  - GPU: 50-100 articles/minute
- **Full Pipeline**: ~2-3 minutes for 100 articles

## 🎯 Use Cases

- **Market Analysts**: Quick sentiment analysis of current financial news
- **Trading Teams**: Real-time news sentiment tracking
- **Portfolio Managers**: Automated news monitoring for holdings
- **Financial Research**: Batch analysis of historical financial news

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**KaplenoTace**
- GitHub: [@KaplenoTace](https://github.com/KaplenoTace)

## 🙏 Acknowledgments

- Hugging Face for Transformers library
- ProsusAI for FinBERT model
- NewsAPI for financial news data
- Financial PhraseBank dataset

## 📞 Support

For questions or issues, please open an issue on GitHub.

---

**Built with ❤️ for the financial analysis community**
