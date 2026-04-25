import requests
import feedparser
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import time as time_module

class NewsFetcher:
    """
    The 'Eyes' of the CivilMind AI Agent.
    Fetches real-time news from UPSC-relevant sources.
    """
    def __init__(self):
        self.sources = {
            "PIB": "https://pib.gov.in/RssTicker.aspx",
            "The Hindu": "https://www.thehindu.com/news/national/feeder/default.rss",
            "Indian Express": "https://indianexpress.com/section/india/feed/"
        }

    def fetch_latest_news(self, limit=10):
        """
        Fetches headlines and summaries from all sources.
        Filters for news from Today and Yesterday only.
        """
        news_items = []
        cutoff_date = datetime.now() - timedelta(days=2)
        
        # 1. Fetch from RSS Feeds
        for source_name, url in self.sources.items():
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries:
                    # Parse date
                    published_parsed = entry.get('published_parsed')
                    if published_parsed:
                        pub_date = datetime.fromtimestamp(time_module.mktime(published_parsed))
                        if pub_date < cutoff_date:
                            continue # Skip old news
                            
                    news_items.append({
                        "source": source_name,
                        "title": entry.title,
                        "link": entry.link,
                        "summary": self._clean_html(entry.summary) if 'summary' in entry else "",
                        "published": entry.get('published', 'Today')
                    })
                    if len(news_items) >= limit: break
            except Exception as e:
                print(f"Error fetching from {source_name}: {e}")
        
        return news_items[:limit]

    def _clean_html(self, raw_html):
        """
        Strips HTML tags and removes noise.
        """
        if not raw_html: return ""
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext.strip()

    def get_structured_context(self, news_items):
        """
        Converts a list of news items into a single context string for Gemini.
        """
        context = "LATEST NEWS HEADLINES FOR UPSC ANALYSIS:\n"
        for item in news_items:
            context += f"Source: {item['source']}\nTitle: {item['title']}\nSummary: {item['summary'][:200]}...\n---\n"
        return context
