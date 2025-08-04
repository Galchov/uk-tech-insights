import requests
from django.conf import settings
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.text import Truncator

from .base_provider import BaseNewsProvider


class NewsAPIProvider(BaseNewsProvider):
    BASE_URL = "https://newsapi.org/v2/everything"

    def fetch_articles(self, **kwargs):
        params = {
            "q": kwargs.get("query", "tech"),
            "language": kwargs.get("language", "en"),
            "pageSize": kwargs.get("page_size", 20),
            "apiKey": settings.NEWS_API_KEY,
        }

        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()

        return response.json().get('articles', [])
    
    def normalize_article(self, raw_article):
        title = Truncator(raw_article.get("title")).chars(300)
        author = raw_article.get("author") or ""
        summary = raw_article.get("description") or ""
        content = raw_article.get("content") or ""
        image_url = raw_article.get("urlToImage")
        source_url = raw_article.get("url")
        source_name = Truncator(raw_article.get("source", {}).get("name", "")).chars(300)
        published_at = parse_datetime(raw_article.get("publishedAt")) or timezone.now()

        article_data = {
            "title": title,
            "author": author,
            "summary": summary,
            "content": content,
            "source_name": source_name,
            "source_url": source_url,
            "image_url": image_url,
            "published_at": published_at,
        }

        return article_data
    