from django import forms

from . models import Tutorial, Article


class BaseLearningContentForm(forms.ModelForm):
    class Meta:
        fields = [
            'title',
            'cover_image',
            'summary',
            'content',
            'difficulty',
            'estimated_hours',
            'tags',
            'is_published',
        ]


class TutorialForm(BaseLearningContentForm):
    class Meta:
        model = Tutorial


class ArticleForm(BaseLearningContentForm):
    class Meta:
        model = Article
        