from django.shortcuts import render
from django.views.generic import TemplateView

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
