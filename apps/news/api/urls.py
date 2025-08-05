from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UnifiedArticleViewSet, InternalArticleViewSet


router = DefaultRouter()
router.register(r'articles', UnifiedArticleViewSet, basename='unified-article')
router.register(r'internal-articles', InternalArticleViewSet, basename='internal-article')

urlpatterns = router.urls
