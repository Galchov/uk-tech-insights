from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.text import Truncator

from .provider_factory import get_provider
from apps.news.models import ExternalArticle


def normalize_and_store_articles(provider_name, **kwargs):
    provider = get_provider(provider_name)
    articles = provider.fetch_articles(**kwargs)

    created_articles = 0

    for article in articles:
        title = article.get("title")
        if not title:
            continue

        title = Truncator(title).chars(300)

        if ExternalArticle.objects.filter(title=title).exists():
            continue

        content = article.get("content") or ""
        description = article.get('description') or ""
        summary = Truncator(description or content).chars(500)

        source_name = Truncator(article.get("source", {}).get("name") or "").chars(300)
        image_url = article.get("urlToImage")
        source_url = article.get("url")
        published_at_raw = article.get("publishedAt")

        try:
            published_at = parse_datetime(published_at_raw) if published_at_raw else timezone.now()
        except Exception:
            published_at = timezone.now()

        ExternalArticle.objects.create(
            title=title,
            summary=summary,
            content=content,
            image_url=image_url,
            source_name=source_name,
            source_url=source_url,
            published_at=published_at,
            publication_status=ExternalArticle.PublicationStatus.PUBLISHED,
        )

        created_articles += 1

    return created_articles
