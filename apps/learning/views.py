from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Article, Tutorial, TutorialCompletion


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
    template_name = 'learning/tutorial_detail.html'


class TutorialCreateView(CreateView):
    template_name = 'learning/tutorial_form.html'


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
    template_name = 'learning/article_detail.html'


class ArticleCreateView(CreateView):
    template_name = 'learning/article_form.html'


class ArticleEditView(UpdateView):
    template_name = 'learning/article_form.html'


class ArticleDeleteView(DeleteView):
    template_name = 'learning/article_confirm_delete.html'


##### Author Content #####

class AuthorContentListView(ListView):
    pass
