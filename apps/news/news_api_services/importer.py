from .provider_factory import get_provider
from apps.news.models import ExternalArticle


def normalize_and_store_articles(provider_name, **kwargs):
    provider = get_provider(provider_name)
    raw_articles = provider.fetch_articles(**kwargs)

    created_articles = 0

    for raw_article in raw_articles:
        article = provider.normalize_article(raw_article)

        if not article or ExternalArticle.objects.filter(title=article['title']).exists():
            continue

        ExternalArticle.objects.create(
            title=article['title'],
            author=article['author'],
            summary=article['summary'],
            content=article['content'],
            image_url=article['image_url'],
            source_name=article['source_name'],
            source_url=article['source_url'],
            published_at=article['published_at'],
            publication_status=ExternalArticle.PublicationStatus.PUBLISHED,
        )

        created_articles += 1

    return created_articles


# TODO: Performance - Implement bulk_create
