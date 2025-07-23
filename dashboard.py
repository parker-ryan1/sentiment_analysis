#!/usr/bin/env python3
"""
Simple Stock Sentiment Dashboard
Displays sentiment analysis results in a readable format
"""

import os
from sentiment_analyzer import SentimentAnalyzer
import pandas as pd
from datetime import datetime
import json

class SentimentDashboard:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        self.analyzer = SentimentAnalyzer(config_path)
        
    def display_stock_card(self, result):
        """Display a formatted stock analysis card"""
        symbol = result['symbol']
        sentiment = result['weighted_sentiment']
        stock_data = result['stock_context']
        
        # Determine color based on sentiment
        if sentiment > 0.1:
            sentiment_color = "🟢"
        elif sentiment < -0.1:
            sentiment_color = "🔴"
        else:
            sentiment_color = "🟡"
        
        print(f"\n{sentiment_color} {symbol} - {stock_data.get('company_name', 'N/A')}")
        print("─" * 50)
        print(f"💰 Price: ${stock_data.get('current_price', 'N/A')} ({stock_data.get('price_change_pct', 'N/A'):+.2f}%)")
        print(f"📊 Sentiment: {sentiment:.3f} ({result['sentiment_label'].upper()})")
        print(f"📰 News Articles: {result['news_sentiment']['articles_count']}")
        print(f"🎯 Recommendation: {result['recommendation']}")
        
    def show_portfolio_dashboard(self, symbols):
        """Display portfolio sentiment dashboard"""
        print("📈 STOCK SENTIMENT DASHBOARD")
        print("=" * 60)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        results = []
        for symbol in symbols:
            try:
                result = self.analyzer.analyze_stock_sentiment(symbol)
                results.append(result)
                self.display_stock_card(result)
            except Exception as e:
                print(f"❌ Error analyzing {symbol}: {e}")
        
        # Summary statistics
        if results:
            sentiments = [r['weighted_sentiment'] for r in results]
            avg_sentiment = sum(sentiments) / len(sentiments)
            
            print(f"\n📊 PORTFOLIO SUMMARY")
            print("─" * 30)
            print(f"Stocks Analyzed: {len(results)}")
            print(f"Average Sentiment: {avg_sentiment:.3f}")
            print(f"Bullish Stocks: {sum(1 for s in sentiments if s > 0.1)}")
            print(f"Bearish Stocks: {sum(1 for s in sentiments if s < -0.1)}")
            print(f"Neutral Stocks: {sum(1 for s in sentiments if -0.1 <= s <= 0.1)}")
        
        return results
    
    def show_sector_dashboard(self):
        """Display sector sentiment analysis"""
        with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r') as f:
            config = json.load(f)
        
        sectors = config['sectors']
        
        print("\n🏭 SECTOR SENTIMENT ANALYSIS")
        print("=" * 60)
        
        sector_results = self.analyzer.get_sector_sentiment(sectors)
        
        # Sort sectors by sentiment
        sorted_sectors = sorted(sector_results.items(), 
                              key=lambda x: x[1]['average_sentiment'], 
                              reverse=True)
        
        for sector, data in sorted_sectors:
            sentiment = data['average_sentiment']
            if sentiment > 0.1:
                icon = "🚀"
            elif sentiment < -0.1:
                icon = "📉"
            else:
                icon = "➡️"
            
            print(f"{icon} {sector:<15} | {sentiment:+.3f} ({data['sentiment_label'].upper()}) | {data['stocks_analyzed']} stocks")
        
        return sector_results
    
    def export_to_csv(self, results, filename="sentiment_analysis.csv"):
        """Export results to CSV file"""
        if not results:
            print("No results to export")
            return
        
        # Flatten the results for CSV export
        csv_data = []
        for result in results:
            row = {
                'symbol': result['symbol'],
                'timestamp': result['timestamp'],
                'weighted_sentiment': result['weighted_sentiment'],
                'sentiment_label': result['sentiment_label'],
                'recommendation': result['recommendation'],
                'news_sentiment': result['news_sentiment']['sentiment'],
                'news_articles_count': result['news_sentiment']['articles_count'],
                'current_price': result['stock_context'].get('current_price', 'N/A'),
                'price_change_pct': result['stock_context'].get('price_change_pct', 'N/A'),
                'company_name': result['stock_context'].get('company_name', 'N/A')
            }
            csv_data.append(row)
        
        df = pd.DataFrame(csv_data)
        df.to_csv(filename, index=False)
        print(f"📄 Results exported to {filename}")

def main():
    dashboard = SentimentDashboard()
    
    # Example portfolio
    portfolio = ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA"]
    
    # Show portfolio dashboard
    results = dashboard.show_portfolio_dashboard(portfolio)
    
    # Show sector analysis
    dashboard.show_sector_dashboard()
    
    # Export results
    if results:
        dashboard.export_to_csv(results)

if __name__ == "__main__":
    main()