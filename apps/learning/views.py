from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.urls import reverse_lazy

from .models import Article, Tutorial
from .forms import TutorialForm


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
        return Tutorial.objects.filter(is_published=True)
    

class TutorialDetailView(DetailView):
    model = Tutorial
    template_name = 'learning/tutorial_detail.html'
    context_object_name = 'tutorial'

    def get_queryset(self):
        return Tutorial.objects.filter(is_published=True)
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
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

        return context


class TutorialCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Tutorial
    form_class = TutorialForm
    template_name = 'learning/tutorial_form.html'
    success_url = reverse_lazy('learning:tutorial_list')
    permission_required = 'learning.add_tutorial'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TutorialEditView(UpdateView):
    template_name = 'learning/tutorial_form.html'


class TutorialDeleteView(DeleteView):
    template_name = 'learning/tutorial_confirm_delete.html'


class TutorialCompleteView(View):
    pass


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


class ArticleCreateView(CreateView):
    template_name = 'learning/article_form.html'


class ArticleEditView(UpdateView):
    template_name = 'learning/article_form.html'


class ArticleDeleteView(DeleteView):
    template_name = 'learning/article_confirm_delete.html'


##### Author Content #####

class AuthorContentListView(ListView):
    pass
