from rest_framework import viewsets, mixins

from apps.news.models import InternalArticle, ExternalArticle
from .serializers import UnifiedArticleSerializer


class UnifiedArticleViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UnifiedArticleSerializer

    def get_queryset(self):
        internal = InternalArticle.objects.filter(publication_status='PUBLISHED')
        external = ExternalArticle.objects.filter(publication_status='PUBLISHED')
        return list(internal) + list(external)

    def get_object(self):
        slug = self.kwargs['slug']
        try:
            return InternalArticle.objects.get(slug=slug, publication_status='PUBLISHED')
        except InternalArticle.DoesNotExist:
            return ExternalArticle.objects.get(slug=slug, publication_status='PUBLISHED')
