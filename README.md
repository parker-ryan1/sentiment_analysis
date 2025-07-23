# Stock Sentiment Analysis for Investment Decisions

A comprehensive sentiment analysis system designed specifically for stock picking and investment decision making. This system analyzes news sentiment, social media discussions, and combines multiple data sources to provide actionable investment insights.

## Features

- **Multi-source Sentiment Analysis**: Combines news articles, social media, and technical indicators
- **Real-time Stock Data**: Integration with Yahoo Finance for current stock prices and context
- **Portfolio Analysis**: Analyze sentiment for multiple stocks simultaneously
- **Sector Analysis**: Compare sentiment across different market sectors
- **Investment Recommendations**: Generate buy/sell/hold recommendations based on sentiment
- **Interactive Dashboard**: Visual representation of sentiment data
- **Export Capabilities**: Save analysis results to CSV and JSON formats

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure the system by editing `config.json` with your preferences.

## Quick Start

### Basic Usage

```python
from sentiment_analyzer import SentimentAnalyzer

# Initialize analyzer
analyzer = SentimentAnalyzer('config.json')

# Analyze a single stock
result = analyzer.analyze_stock_sentiment('AAPL')
print(f"AAPL Sentiment: {result['weighted_sentiment']:.3f}")
print(f"Recommendation: {result['recommendation']}")
```

### Run Examples

```bash
# Run demonstration examples
python stock_sentiment_main.py

# Interactive mode
python stock_sentiment_main.py --interactive

# Generate analysis report
python stock_sentiment_main.py --report AAPL GOOGL MSFT
```

### Dashboard

```bash
# Launch sentiment dashboard
python dashboard.py
```

## Core Components

### SentimentAnalyzer Class

The main class that handles all sentiment analysis operations:

- `analyze_stock_sentiment(symbol)`: Comprehensive analysis for a single stock
- `analyze_portfolio_sentiment(symbols)`: Batch analysis for multiple stocks
- `get_sector_sentiment(sectors)`: Analyze sentiment by market sector
- `get_stock_news_sentiment(symbol)`: Extract sentiment from recent news

### Configuration

Edit `config.json` to customize:

- **Sentiment Weights**: Adjust importance of news vs social media vs technical analysis
- **Sectors**: Define stock groupings for sector analysis
- **Thresholds**: Set buy/sell sentiment thresholds
- **Rate Limiting**: Control API request frequency

### Key Features

#### 1. News Sentiment Analysis
- Fetches recent news articles for stocks
- Uses VADER and TextBlob for sentiment scoring
- Provides confidence scores based on article count

#### 2. Multi-factor Scoring
- Combines multiple sentiment sources with configurable weights
- Generates overall sentiment scores from -1 (very negative) to +1 (very positive)

#### 3. Investment Recommendations
- **BUY**: Positive sentiment with price momentum
- **SELL**: Negative sentiment with price decline
- **HOLD**: Neutral sentiment or mixed signals

#### 4. Portfolio Management
- Analyze multiple stocks simultaneously
- Generate portfolio-wide sentiment summaries
- Export results for further analysis

## Usage Examples

### Single Stock Analysis

```python
analyzer = SentimentAnalyzer()
result = analyzer.analyze_stock_sentiment('TSLA')

print(f"Stock: {result['symbol']}")
print(f"Sentiment: {result['weighted_sentiment']:.3f}")
print(f"Recommendation: {result['recommendation']}")
```

### Portfolio Analysis

```python
portfolio = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'NVDA']
results = analyzer.analyze_portfolio_sentiment(portfolio)

for _, stock in results.iterrows():
    print(f"{stock['symbol']}: {stock['sentiment_label']} - {stock['recommendation']}")
```

### Sector Comparison

```python
sectors = {
    'Technology': ['AAPL', 'GOOGL', 'MSFT'],
    'Electric Vehicles': ['TSLA', 'NIO', 'RIVN'],
    'Banking': ['JPM', 'BAC', 'WFC']
}

sector_sentiment = analyzer.get_sector_sentiment(sectors)
for sector, data in sector_sentiment.items():
    print(f"{sector}: {data['sentiment_label']} ({data['average_sentiment']:.3f})")
```

## Output Format

Each analysis returns a comprehensive dictionary containing:

```json
{
  "symbol": "AAPL",
  "timestamp": "2024-01-15T10:30:00",
  "news_sentiment": {
    "sentiment": 0.25,
    "articles_count": 8,
    "confidence": 0.8,
    "sentiment_label": "positive"
  },
  "weighted_sentiment": 0.22,
  "sentiment_label": "positive",
  "stock_context": {
    "current_price": 185.50,
    "price_change_pct": 2.1,
    "company_name": "Apple Inc."
  },
  "recommendation": "BUY - Positive sentiment detected"
}
```

## Testing the System

Try it out with a quick test:

```bash
cd sentiment_analysis
python -c "
from sentiment_analyzer import SentimentAnalyzer
analyzer = SentimentAnalyzer()
result = analyzer.analyze_stock_sentiment('AAPL')
print(f'AAPL Sentiment: {result[\"weighted_sentiment\"]:.3f} ({result[\"sentiment_label\"]})')
print(f'Recommendation: {result[\"recommendation\"]}')
"
```

## Limitations

- **News Coverage**: Sentiment quality depends on available news articles
- **Social Media**: Reddit integration requires API setup (placeholder included)
- **Rate Limits**: Yahoo Finance has rate limiting - built-in delays included
- **Market Hours**: Some data may be delayed outside trading hours

## Disclaimer

This tool is for educational and research purposes only. Always conduct your own research and consult with financial advisors before making investment decisions. Past performance does not guarantee future results.