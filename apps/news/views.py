from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from itertools import chain
from operator import attrgetter

from .models import InternalArticle, ExternalArticle, NewsCategory, NewsSource
from .forms import InternalArticleForm
from apps.common.models import Comment
from apps.common.forms import CommentForm


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
    

class NewsArticleDetailView(View):
    template_name = 'news/article_detail.html'
    context_object_name = 'article'
    
    def get_artcile(self, slug, user):
        internal_qs = InternalArticle.objects.all()
        external_qs = ExternalArticle.objects.all()

        if not user.is_staff:
            internal_qs = InternalArticle.objects.filter(publication_status=InternalArticle.publication_status.PUBLISHED)
            external_qs = ExternalArticle.objects.filter(publication_status=ExternalArticle.publication_status.PUBLISHED)

        try:
            return internal_qs.get(slug=slug)
        except InternalArticle.DoesNotExist:
            return get_object_or_404(external_qs, slug=slug)


    def get(self, request, slug):
        article = self.get_artcile(slug, request.user)

        content_type = ContentType.objects.get_for_model(article.__class__)
        comments = Comment.objects.filter(content_type=content_type, object_id=article.pk).order_by('-created_at')

        form = CommentForm()

        context = {
            'article': article,
            'comments': comments,
            'form': form,
        }

        return render(request, self.template_name, context)

    def post(self, request, slug):
        if not request.user.is_authenticated:
            return redirect('login')
        
        article = self.get_artcile(slug, request.user)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_object = article
            comment.save()
            return redirect(request.path)
        
        content_type = ContentType.objects.get_for_model(article.__class__)
        comments = Comment.objects.filter(content_type=content_type, object_id=article.pk)

        context = {
            'article': article,
            'comments': comments,
            'form': form,
        }

        return render(request, self.template_name, context)


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
