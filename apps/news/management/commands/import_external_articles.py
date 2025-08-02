from django.core.management.base import BaseCommand

from apps.news.news_api_services.importer import normalize_and_store_articles


class Command(BaseCommand):
    help = "Import external articles from news providers"

    def add_arguments(self, parser):
        parser.add_argument('--provider', type=str, default='newsapi', help='News provider key (e.g. newsapi)')
    
    def handle(self, *args, **options):
        provider_name = options['provider']
        count = normalize_and_store_articles(provider_name)
        self.stdout.write(self.style.SUCCESS(f"{count} articles imported from {provider_name}."))
