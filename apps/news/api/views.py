from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from django.db.models import Q

from apps.news.models import InternalArticle, ExternalArticle
from .serializers import UnifiedArticleSerializer, InternalArticleSerializer


class UnifiedArticleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UnifiedArticleSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = list(InternalArticle.objects.filter(publication_status='PUBLISHED')) + \
                   list(ExternalArticle.objects.filter(publication_status='PUBLISHED'))

        request = self.request
        search = request.GET.get('search')
        category = request.GET.get('category')
        source_type = request.GET.get('type')
        ordering = request.GET.get('ordering')

        if search:
            queryset = [
                article for article in queryset
                if search.lower() in article.title.lower()
                or search.lower() in article.summary.lower()
                or search.lower() in article.content.lower()
            ]

        if category:
            queryset = [article for article in queryset if str(article.category).lower() == category.lower()]

        if source_type == 'internal':
            queryset = [article for article in queryset if isinstance(article, InternalArticle)]
        elif source_type == 'external':
            queryset = [article for article in queryset if isinstance(article, ExternalArticle)]

        if ordering:
            reverse = ordering.startswith('-')
            key = ordering.lstrip('-')
            if key in ['published_at', 'title']:
                queryset.sort(key=lambda x: getattr(x, key), reverse=reverse)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page_size = 10
        try:
            page = int(request.GET.get('page', 1))
        except ValueError:
            page = 1

        start = (page - 1) * page_size
        end = start + page_size
        paginated_queryset = queryset[start:end]

        serializer = self.get_serializer(paginated_queryset, many=True, context={'request': request})
        return Response({
            'count': len(queryset),
            'page': page,
            'page_size': page_size,
            'results': serializer.data
        })


class InternalArticleViewSet(viewsets.ModelViewSet):
    queryset = InternalArticle.objects.all()
    serializer_class = InternalArticleSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()

    def get_queryset(self):
        if self.request.user.is_staff:
            return InternalArticle.objects.all()
        return InternalArticle.objects.filter(publication_status='PUBLISHED')
