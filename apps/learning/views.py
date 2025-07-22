from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import PermissionDenied

from .models import Article, Tutorial, TutorialProgress
from .forms import TutorialForm, ArticleForm


class LearningHomeView(TemplateView):
    template_name = 'learning/learning_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tutorials'] = Tutorial.objects.filter(is_published=True)
        context['articles'] = Article.objects.filter(is_published=True)
        context['page_title'] = "Learning Center"
        context['page_description'] = "Expand your skills with curated tutorials and insightful articles."
        return context


##### Tutorial Views #####

class TutorialListView(ListView):
    model = Tutorial
    template_name = 'learning/tutorial_list.html'
    context_object_name = 'tutorials'

    def get_queryset(self):
        queryset = Tutorial.objects.all().order_by('-created_at')

        queryset = queryset.filter(is_published=True)

        if self.request.GET.get('filter') == 'mine' and self.request.user.is_authenticated:
            queryset = Tutorial.objects.filter(authors=self.request.user).order_by('-created_at')

        elif self.request.GET.get('filter') == 'waiting' and (
            self.request.user.is_staff or
            self.request.user.is_superuser or
            self.request.user.has_perm('learning.can_publish_tutorials')
        ):
            queryset = Tutorial.objects.filter(is_published=False).order_by('-created_at')

        return queryset
    

class TutorialDetailView(DetailView):
    model = Tutorial
    template_name = 'learning/tutorial_detail.html'
    context_object_name = 'tutorial'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        user = self.request.user
        if not obj.is_published:
            if not user.is_authenticated:
                raise PermissionDenied("This tutorial is not published yet.")
            if not (user.is_staff or user.is_superuser or obj.authors.filter(pk=user.pk).exists()):
                raise PermissionDenied("You do not have permission to view this unpublished tutorial.")
            
        if obj.is_published:
            obj.views += 1
            obj.save(update_fields=['views'])

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tutorial = self.object

        context['comments'] = tutorial.comments.all()
        context['stars_count'] = tutorial.stars.count()
        context['tags'] = tutorial.tags.all()

        context['related_tutorials'] = Tutorial.objects.filter(
            is_published=True,
            difficulty=tutorial.difficulty,
        ).exclude(pk=tutorial.pk)[:5]

        context['is_author'] = False
        if self.request.user.is_authenticated:
            context['is_author'] = tutorial.authors.filter(pk=self.request.user.pk).exists()

            context['user_progress'] = TutorialProgress.objects.filter(
                user=self.request.user,
                tutorial=tutorial
            ).first()

        return context


class TutorialCreateView(PermissionRequiredMixin, CreateView):
    model = Tutorial
    form_class = TutorialForm
    template_name = 'learning/tutorial_form.html'
    permission_required = 'learning.add_tutorial'

    # Change this to True if you want to raise 403 instead of redirecting
    raise_exception = False
    login_url = reverse_lazy('accounts:login')

    def handle_no_permission(self):

        # User not logged in -> redirect to login, if tried to access via URL
        if not self.request.user.is_authenticated:
            return redirect(self.get_login_url())
        
        # User logged in but lacking permission -> redirect to verification
        return redirect('accounts:verification_request')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.authors.add(self.request.user)
        return response
    
    def get_success_url(self):
        return self.object.get_absolute_url()


class TutorialEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tutorial
    form_class = TutorialForm
    template_name = 'learning/tutorial_form.html'

    def test_func(self):
        tutorial = self.get_object()
        user = self.request.user
        return (
            tutorial.authors.filter(pk=user.pk).exists() or
            user.has_perm('learning.can_edit_others_tutorials')
        )

    def get_success_url(self):
        return self.object.get_absolute_url()


class TutorialDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tutorial
    template_name = 'learning/tutorial_confirm_delete.html'
    success_url = reverse_lazy('learning:tutorial_list')

    def test_func(self):
        tutorial = self.get_object()
        user = self.request.user

        return (
            tutorial.authors.filter(pk=user.pk).exists() or
            user.has_perm('learning.can_edit_others_tutorials')
        )
    

class TutorialCompleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        tutorial = get_object_or_404(Tutorial, slug=kwargs.get('slug'))

        progress, created = TutorialProgress.objects.get_or_create(
            user=request.user,
            tutorial=tutorial,
            defaults={'status': TutorialProgress.StatusChoices.COMPLETED}
        )

        if not created and progress.status != TutorialProgress.StatusChoices.COMPLETED:
            progress.status = TutorialProgress.StatusChoices.COMPLETED
            progress.save(update_fields=['status', 'updated_at'])

        return redirect(tutorial.get_absolute_url())
    

class TutorialTogglePublishView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        tutorial = get_object_or_404(Tutorial, slug=self.kwargs['slug'])
        user = self.request.user
        return (
            user.is_staff or
            user.is_superuser or
            tutorial.authors.filter(pk=user.pk).exists()
        )

    def post(self, request, *args, **kwargs):
        tutorial = get_object_or_404(Tutorial, slug=kwargs['slug'])

        tutorial.is_published = not tutorial.is_published
        tutorial.save(update_fields=['is_published'])

        return redirect(tutorial.get_absolute_url())


class TutorialProgressUpdateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        tutorial = get_object_or_404(Tutorial, slug=kwargs.get('slug'))
        status = request.POST.get('status')
        toggle_bookmark = request.POST.get('toggle_bookmark')

        progress, _ = TutorialProgress.objects.get_or_create(
            user=request.user,
            tutorial=tutorial
        )

        if status in TutorialProgress.StatusChoices.values:
            progress.status = status

        if toggle_bookmark:
            progress.bookmarked = not progress.bookmarked

        progress.save(update_fields=['status', 'bookmarked', 'updated_at'])
        return redirect(tutorial.get_absolute_url())
    

class WaitingApprovalRedirectView(PermissionRequiredMixin, View):
    permission_required = 'learning.can_publish_tutorials'

    def get(self, request, *args, **kwargs):
        return redirect(f"{reverse('learning:tutorial_list')}?filter=waiting")
    

##### Article Views #####

class ArticleListView(ListView):
    model = Article
    template_name = 'learning/article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(is_published=True)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'learning/article_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        return Article.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object

        context['comments'] = article.comments.all()
        context['stars_count'] = article.stars.count()
        context['tags'] = article.tags.all()
        context['related_articles'] = Article.objects.filter(
            is_published=True,
            difficulty=article.difficulty,
        ).exclude(pk=article.pk)[:5]

        return context


class ArticleCreateView(PermissionRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'learning/article_form.html'
    permission_required = 'learning.add_article'
    raise_exception = False
    login_url = reverse_lazy('accounts:login')

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(self.get_login_url())
        return redirect('accounts:verification_request')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.authors.add(self.request.user)
        return response
    
    def get_success_url(self):
        return self.object.get_absolute_url()


class ArticleEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'learning/article_form.html'

    def test_func(self):
        article = self.get_object()
        user = self.request.user
        return (
            article.authors.filter(pk=user.pk).exists() or
            user.has_perm('learning.can_edit_others_articles')
        )

    def get_success_url(self):
        return self.object.get_absolute_url()


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'learning/article_confirm_delete.html'
    success_url = reverse_lazy('learning:article_list')

    def test_func(self):
        article = self.get_object()
        user = self.request.user
        return (
            article.authors.filter(pk=user.pk).exists() or
            user.has_perm('learning.can_edit_others_articles')
        )


class ArticleTogglePublishView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        article = get_object_or_404(Article, slug=self.kwargs['slug'])
        user = self.request.user
        return (
            user.is_staff or
            user.is_superuser or
            article.authors.filter(pk=user.pk).exists()
        )

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, slug=kwargs['slug'])

        article.is_published = not article.is_published
        article.save(update_fields=['is_published'])

        return redirect(article.get_absolute_url())
    

##### Author Content #####

class AuthorContentListView(ListView):
    pass
