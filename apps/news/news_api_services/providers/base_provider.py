from abc import ABC, abstractmethod


class BaseNewsProvider(ABC):

    @abstractmethod
    def fetch_articles(self, **kwargs):
        """Fetch raw articles from different providers."""
        pass
