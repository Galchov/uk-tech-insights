from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UnifiedArticleViewSet

router = DefaultRouter()
router.register(r'articles', UnifiedArticleViewSet, basename='unified-article')

urlpatterns = router.urls
