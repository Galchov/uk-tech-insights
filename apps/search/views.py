from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Q

from apps.learning.models import Tutorial, Article
from apps.forum.models import ForumPost
from apps.news.models import NewsArticle


class GlobalSearchView(TemplateView):
    template_name = 'search/results.html'

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('q')
        context = super().get_context_data(**kwargs)

        if query:
            context['query'] = query

            context['posts'] = ForumPost.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            ).distinct()

            context['tutorials'] = Tutorial.objects.filter(
                Q(title__icontains=query) |
                Q(summary__icontains=query) |
                Q(content__icontains=query)
            ).distinct()

            context['articles'] = Article.objects.filter(
                Q(title__icontains=query) |
                Q(summary__icontains=query) |
                Q(content__icontains=query)
            ).distinct()

            context['news'] = NewsArticle.objects.filter(
                Q(title__icontains=query) |
                Q(summary__icontains=query) |
                Q(content__icontains=query)
            ).distinct()

        return context
