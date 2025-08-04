from rest_framework import serializers
from apps.news.models import InternalArticle, ExternalArticle
from django.contrib.auth import get_user_model


User = get_user_model()

class UnifiedArticleSerializer(serializers.Serializer):
    title = serializers.CharField()
    slug = serializers.SlugField()
    summary = serializers.CharField()
    content = serializers.CharField()
    published_at = serializers.DateTimeField()
    category = serializers.StringRelatedField()

    image_url = serializers.SerializerMethodField()

    source_name = serializers.SerializerMethodField()
    source_url = serializers.SerializerMethodField()

    author = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        if isinstance(obj, ExternalArticle):
            return obj.image_url
        elif isinstance(obj, InternalArticle) and obj.cover_image:
            request = self.context.get("request")
            return request.build_absolute_uri(obj.cover_image.url) if request else obj.cover_image.url
        return None

    def get_source_name(self, obj):
        if isinstance(obj, ExternalArticle):
            return obj.source_name or ""
        return "UK Tech Insights"

    def get_source_url(self, obj):
        if isinstance(obj, ExternalArticle):
            return obj.source_url or ""
        request = self.context.get("request")
        return request.build_absolute_uri(obj.get_absolute_url()) if request else obj.get_absolute_url()

    def get_author(self, obj):
        if isinstance(obj, ExternalArticle):
            return obj.author or ""
        elif isinstance(obj, InternalArticle):
            return [user.get_full_name() or user.username for user in obj.authors.all()]
        return None
