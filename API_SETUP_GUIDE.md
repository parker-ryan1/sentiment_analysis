# API Setup Guide for Stock Sentiment Analysis

This guide will help you set up various APIs to enhance your sentiment analysis with real-time data from multiple sources.

## 🔧 Quick Setup Steps

1. **Copy the `.env` file template** (already created)
2. **Get API credentials** from the services below
3. **Update the `.env` file** with your credentials
4. **Test the integration**

## 📱 Reddit API Setup (Recommended - Free)

Reddit provides excellent stock discussion data from communities like r/stocks, r/investing, etc.

### Steps:
1. **Create a Reddit account** (if you don't have one)
2. **Go to Reddit App Preferences**: https://www.reddit.com/prefs/apps
3. **Click "Create App" or "Create Another App"**
4. **Fill out the form:**
   - **Name**: `StockSentimentBot` (or any name)
   - **App type**: Select `script`
   - **Description**: `Stock sentiment analysis bot`
   - **About URL**: Leave blank
   - **Redirect URI**: `http://localhost:8080` (required but not used)
5. **Click "Create app"**
6. **Copy your credentials:**
   - **Client ID**: The string under your app name (looks like: `abc123def456`)
   - **Client Secret**: The "secret" field
   - **User Agent**: Use format `StockSentimentBot/1.0 by YourRedditUsername`

### Update your `.env` file:
```env
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=StockSentimentBot/1.0 by YourRedditUsername
```

## 📰 News API Setup (Optional)

Get news sentiment from multiple sources.

### Steps:
1. **Go to**: https://newsapi.org/
2. **Sign up for free account** (up to 1000 requests/day)
3. **Get your API key** from the dashboard
4. **Update `.env`:**
```env
NEWS_API_KEY=your_news_api_key_here
```

## 🐦 Twitter/X API Setup (Optional - Paid)

Twitter/X now requires paid access for API usage.

### Steps:
1. **Go to**: https://developer.twitter.com/
2. **Apply for developer account**
3. **Create a new app**
4. **Get your Bearer Token**
5. **Update `.env`:**
```env
TWITTER_BEARER_TOKEN=your_bearer_token_here
```

## 📊 Alpha Vantage API Setup (Optional)

Additional stock data and news.

### Steps:
1. **Go to**: https://www.alphavantage.co/support/#api-key
2. **Get free API key** (500 requests/day)
3. **Update `.env`:**
```env
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
```

## 🧪 Testing Your Setup

After setting up your APIs, test them:

```bash
# Test basic functionality
python test_basic.py

# Test with API integration
python stock_sentiment_main.py

# Interactive testing
python stock_sentiment_main.py --interactive
```

## 📝 Current `.env` File Template

Your `.env` file should look like this (replace with your actual credentials):

```env
# Reddit API Configuration (RECOMMENDED)
REDDIT_CLIENT_ID=abc123def456
REDDIT_CLIENT_SECRET=your_secret_here
REDDIT_USER_AGENT=StockSentimentBot/1.0 by YourUsername

# News API Configuration (Optional)
NEWS_API_KEY=your_news_api_key_here

# Twitter/X API Configuration (Optional - Paid)
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here

# Alpha Vantage API (Optional)
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
```

## 🚀 Priority Setup Order

1. **Reddit API** - Free and provides excellent stock discussion data
2. **News API** - Free tier available, good for news sentiment
3. **Alpha Vantage** - Free tier for additional stock data
4. **Twitter/X** - Only if you have paid access

## 🔍 What Each API Provides

- **Reddit**: Community discussions, sentiment from retail investors
- **News API**: Professional news articles, earnings reports
- **Twitter/X**: Real-time social sentiment, breaking news
- **Alpha Vantage**: Additional stock data, company news

## ⚠️ Important Notes

- **Keep your `.env` file secure** - never commit it to version control
- **API rate limits** - The system includes delays to respect limits
- **Free tiers** - Most APIs have free tiers sufficient for testing
- **Reddit is the best starting point** - Free and provides rich data

## 🆘 Troubleshooting

### Reddit API Issues:
- Make sure your app type is "script"
- Check that your User Agent follows the format: `AppName/Version by Username`
- Verify your Client ID and Secret are correct

### General Issues:
- Check your internet connection
- Verify API credentials are correctly formatted
- Look at the console logs for specific error messages

## 📞 Need Help?

If you encounter issues:
1. Check the console output for error messages
2. Verify your API credentials
3. Test with a simple stock symbol like "AAPL"
4. Make sure your `.env` file is in the correct directory

Once you have at least Reddit API set up, you'll see much richer sentiment analysis with real community discussions!