from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from .models import NewsArticle, NewsCategory, NewsSource
from .forms import NewsArticleForm


class NewsArticleListView(ListView):
    model = NewsArticle
    template_name = 'news/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10
    queryset = NewsArticle.objects.filter(publication_status=NewsArticle.PublicationStatus.PUBLISHED)


class NewsArticleDetailView(DetailView):
    model = NewsArticle
    template_name = 'news/article_detail.html'
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        qs = NewsArticle.objects.all()

        if not self.request.user.is_staff:
            qs = qs.filter(publication_status=NewsArticle.PublicationStatus.PUBLISHED)
        return qs


class NewsByCategoryListView(ListView):
    model = NewsArticle
    template_name = 'news/article_list_by_category.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(NewsCategory, slug=self.kwargs['slug'])
        return NewsArticle.objects.filter(
            category=self.category,
            status=NewsArticle.PublicationStatus.PUBLISHED
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class NewsBySourceListView(ListView):
    model = NewsArticle
    template_name = 'news/article_list_by_source.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        self.source = get_object_or_404(NewsSource, slug=self.kwargs['slug'])
        return NewsArticle.objects.filter(
            source=self.source,
            status=NewsArticle.PublicationStatus.PUBLISHED
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['source'] = self.source
        return context


class NewsArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = NewsArticle
    form_class = NewsArticleForm
    template_name = 'news/article_form.html'
    permission_required = 'news.add_newsarticle'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class NewsArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = NewsArticle
    form_class = NewsArticleForm
    template_name = 'news/article_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    permission_required = 'news.change_newsarticle'

    def test_func(self):
        article = self.get_object()
        return self.request.user in article.authors.all() or self.request.user.is_staff


class NewsArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    model = NewsArticle
    template_name = 'news/article_confirm_delete.html'
    success_url = reverse_lazy('news:article_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    permission_required = 'news.delete_newsarticle'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.groups.filter(name__in=['Moderators']).exists()
