from django.db.models import Q

from apps.companies.models import Company
from apps.learning.models import Article, Tutorial
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

    # TODO: Implement evaluation for all models

    return results
