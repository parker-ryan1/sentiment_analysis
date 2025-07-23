#!/usr/bin/env python3
"""
Stock Sentiment Analysis for Investment Decision Making
Usage examples and main execution script
"""

import os
import sys
from sentiment_analyzer import SentimentAnalyzer
import pandas as pd
import json

def main():
    # Initialize the sentiment analyzer
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    analyzer = SentimentAnalyzer(config_path)
    
    print("🚀 Stock Sentiment Analysis for Investment Decisions")
    print("=" * 60)
    
    # Example 1: Single stock analysis
    print("\n📊 Single Stock Analysis Example:")
    symbol = "AAPL"
    result = analyzer.analyze_stock_sentiment(symbol)
    
    print(f"\nStock: {result['symbol']}")
    print(f"Company: {result['stock_context'].get('company_name', 'N/A')}")
    print(f"Current Price: ${result['stock_context'].get('current_price', 'N/A')}")
    print(f"Price Change: {result['stock_context'].get('price_change_pct', 'N/A')}%")
    print(f"News Sentiment: {result['news_sentiment']['sentiment']:.3f} ({result['news_sentiment']['sentiment_label']})")
    print(f"Articles Analyzed: {result['news_sentiment']['articles_count']}")
    print(f"Overall Sentiment: {result['weighted_sentiment']:.3f} ({result['sentiment_label']})")
    print(f"Recommendation: {result['recommendation']}")
    
    # Example 2: Portfolio analysis
    print("\n📈 Portfolio Analysis Example:")
    portfolio = ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA"]
    portfolio_df = analyzer.analyze_portfolio_sentiment(portfolio)
    
    if not portfolio_df.empty:
        print("\nPortfolio Sentiment Summary:")
        for _, row in portfolio_df.iterrows():
            print(f"{row['symbol']}: {row['weighted_sentiment']:.3f} ({row['sentiment_label']}) - {row['recommendation']}")
    
    # Example 3: Sector analysis
    print("\n🏭 Sector Analysis Example:")
    sectors = {
        "Technology": ["AAPL", "GOOGL", "MSFT"],
        "Electric Vehicles": ["TSLA", "NIO", "RIVN"],
        "Banking": ["JPM", "BAC", "WFC"]
    }
    
    sector_results = analyzer.get_sector_sentiment(sectors)
    
    print("\nSector Sentiment Summary:")
    for sector, data in sector_results.items():
        print(f"{sector}: {data['average_sentiment']:.3f} ({data['sentiment_label']}) - {data['stocks_analyzed']} stocks analyzed")

def interactive_mode():
    """Interactive mode for custom stock analysis"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    analyzer = SentimentAnalyzer(config_path)
    
    print("\n🎯 Interactive Stock Sentiment Analysis")
    print("Enter stock symbols (comma-separated) or 'quit' to exit:")
    
    while True:
        user_input = input("\nStock symbols: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        
        if not user_input:
            continue
        
        symbols = [s.strip().upper() for s in user_input.split(',')]
        
        for symbol in symbols:
            try:
                print(f"\nAnalyzing {symbol}...")
                result = analyzer.analyze_stock_sentiment(symbol)
                
                print(f"📊 {symbol} Analysis:")
                print(f"  Sentiment Score: {result['weighted_sentiment']:.3f}")
                print(f"  Sentiment Label: {result['sentiment_label']}")
                print(f"  Recommendation: {result['recommendation']}")
                print(f"  News Articles: {result['news_sentiment']['articles_count']}")
                
            except Exception as e:
                print(f"❌ Error analyzing {symbol}: {e}")

def save_analysis_report(symbols, output_file="sentiment_report.json"):
    """Save detailed analysis report to file"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    analyzer = SentimentAnalyzer(config_path)
    
    results = []
    for symbol in symbols:
        try:
            result = analyzer.analyze_stock_sentiment(symbol)
            results.append(result)
        except Exception as e:
            print(f"Error analyzing {symbol}: {e}")
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"📄 Analysis report saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--interactive":
            interactive_mode()
        elif sys.argv[1] == "--report":
            symbols = sys.argv[2:] if len(sys.argv) > 2 else ["AAPL", "GOOGL", "MSFT"]
            save_analysis_report(symbols)
        else:
            print("Usage:")
            print("  python stock_sentiment_main.py                 # Run examples")
            print("  python stock_sentiment_main.py --interactive   # Interactive mode")
            print("  python stock_sentiment_main.py --report AAPL GOOGL  # Generate report")
    else:
        main()