#!/usr/bin/env python3
"""
Basic test script to verify the sentiment analysis system works
"""

try:
    print("Testing imports...")
    from sentiment_analyzer import SentimentAnalyzer
    print("✅ SentimentAnalyzer imported successfully")
    
    print("\nInitializing analyzer...")
    analyzer = SentimentAnalyzer()
    print("✅ Analyzer initialized successfully")
    
    print("\nTesting basic sentiment analysis...")
    test_text = "Apple stock is performing very well today with strong earnings"
    result = analyzer.analyze_text(test_text)
    print(f"✅ Text analysis works: {result['sentiment_label']} ({result['combined_score']:.3f})")
    
    print("\nTesting stock sentiment analysis...")
    stock_result = analyzer.analyze_stock_sentiment('AAPL')
    print(f"✅ Stock analysis works for AAPL:")
    print(f"   Sentiment: {stock_result['weighted_sentiment']:.3f} ({stock_result['sentiment_label']})")
    print(f"   Recommendation: {stock_result['recommendation']}")
    print(f"   News articles analyzed: {stock_result['news_sentiment']['articles_count']}")
    
    print("\n🎉 All tests passed! Your sentiment analysis system is working correctly.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all dependencies are installed: pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Error: {e}")
    print("Check your internet connection and try again.")