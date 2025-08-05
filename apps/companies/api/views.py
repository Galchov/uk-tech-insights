from rest_framework import viewsets

from apps.companies.models import Company
from .serializers import CompanySerializer
from .permissions import IsAdminOrReadOnly


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    