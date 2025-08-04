from django.core.management.base import BaseCommand

from apps.news.news_api_services.importer import normalize_and_store_articles


class Command(BaseCommand):
    help = "Import external articles from news providers"

    def add_arguments(self, parser):
        parser.add_argument('--provider', type=str, default='newsapi')
        parser.add_argument('--query', type=str, default='tech')
        parser.add_argument('--language', type=str, default='en')
        parser.add_argument('--page_size', type=str, default=20)
    
    def handle(self, *args, **options):
        provider_name = options['provider']
        kwargs = {
            "query": options["query"],
            "language": options["language"],
            "page_size": options["page_size"],
        }
        count = normalize_and_store_articles(provider_name, **kwargs)
        self.stdout.write(self.style.SUCCESS(f'{count} articles about "{kwargs['query'].capitalize()}" imported from {provider_name}.'))
