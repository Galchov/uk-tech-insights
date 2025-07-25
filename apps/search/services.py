from django.db.models import Q

from apps.companies.models import Company, Industry, Location
from apps.learning.models import Article, Tutorial
from apps.news.models import NewsArticle
from apps.technologies.models import Technology


def search_database(query):
    results = []

    if not query or not query.strip():
        return []
    
    company_matches = Company.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )

    for item in company_matches:
        results.append({
            'type': 'Company',
            'title': item.name,
            'url': item.get_absolute_url(),
            'snippet': item.description[:200],
        })

    news_matches = NewsArticle.objects.filter(
        Q(title__icontains=query) |
        Q(summary__icontains=query) |
        Q(content__icontains=query)
    )

    for item in news_matches:
        results.append({
            'type': 'News Article',
            'title': item.title,
            'url': item.get_absolute_url(),
            'snippet': item.summary[:200],
        })

    # TODO: Implement evaluation for all models

    return results
