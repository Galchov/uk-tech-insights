import requests
from django.conf import settings

from .base_provider import BaseNewsProvider


class NewsAPIProvider(BaseNewsProvider):
    BASE_URL = "https://newsapi.org/v2/everything"


    def fetch_articles(self, query='tech', language='en', page_size=100):
        params = {
            "q": query,
            "language": language,
            "pageSize": page_size,
            "apiKey": settings.NEWS_API_KEY,
        }

        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()

        return response.json().get('articles', [])
    