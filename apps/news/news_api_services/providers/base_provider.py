from abc import ABC, abstractmethod


class BaseNewsProvider(ABC):

    @abstractmethod
    def fetch_articles(self, **kwargs):
        """Fetch raw articles from different providers."""
        pass

    @abstractmethod
    def normalize_article(self, raw_article):
        """Convert raw article data into a standard format."""
        pass
