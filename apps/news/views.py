from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from itertools import chain
from operator import attrgetter

from .models import InternalArticle, ExternalArticle, NewsCategory, NewsSource
from .forms import InternalArticleForm


class ArticleListView(View):
    template_name = 'news/article_list.html'

    def get(self, request, *args, **kwargs):
        internal_article = InternalArticle.objects.filter(publication_status='PUBLISHED')
        external_article = ExternalArticle.objects.filter(publication_status='PUBLISHED')

        articles = sorted(
            chain(internal_article, external_article),
            key=attrgetter('published_at'),
            reverse=True,
        )

        context = {
            'articles': articles,
        }

        return render(request, self.template_name, context)
    

class InternalArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = InternalArticle
    form_class = InternalArticleForm
    template_name = 'news/article_form.html'
    permission_required = 'news.add_internalarticle'
    

class NewsArticleDetailView(DetailView):
    model = ExternalArticle
    template_name = 'news/article_detail.html'
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        qs = ExternalArticle.objects.all()

        if not self.request.user.is_staff:
            qs = qs.filter(publication_status=ExternalArticle.PublicationStatus.PUBLISHED)
        return qs


# class NewsByCategoryListView(ListView):
#     model = NewsArticle
#     template_name = 'news/article_list_by_category.html'
#     context_object_name = 'articles'
#     paginate_by = 10

#     def get_queryset(self):
#         self.category = get_object_or_404(NewsCategory, slug=self.kwargs['slug'])
#         return NewsArticle.objects.filter(
#             category=self.category,
#             status=NewsArticle.PublicationStatus.PUBLISHED
#         ).order_by('-created_at')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['category'] = self.category
#         return context


# class NewsBySourceListView(ListView):
#     model = NewsArticle
#     template_name = 'news/article_list_by_source.html'
#     context_object_name = 'articles'
#     paginate_by = 10

#     def get_queryset(self):
#         self.source = get_object_or_404(NewsSource, slug=self.kwargs['slug'])
#         return NewsArticle.objects.filter(
#             source=self.source,
#             status=NewsArticle.PublicationStatus.PUBLISHED
#         ).order_by('-created_at')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['source'] = self.source
#         return context


# class NewsArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = NewsArticle
#     form_class = NewsArticleForm
#     template_name = 'news/article_form.html'
#     slug_field = 'slug'
#     slug_url_kwarg = 'slug'
#     permission_required = 'news.change_newsarticle'

#     def test_func(self):
#         article = self.get_object()
#         return self.request.user in article.authors.all() or self.request.user.is_staff


# class NewsArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = NewsArticle
#     template_name = 'news/article_confirm_delete.html'
#     success_url = reverse_lazy('news:article_list')
#     slug_field = 'slug'
#     slug_url_kwarg = 'slug'
#     permission_required = 'news.delete_newsarticle'

#     def test_func(self):
#         return self.request.user.is_staff or self.request.user.groups.filter(name__in=['Moderators']).exists()
