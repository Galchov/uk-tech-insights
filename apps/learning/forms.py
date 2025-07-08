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
            'estimated_duration',
            'is_published',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter a clear, concise title'}),
            'summary': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Short summary (1-2 sentences)'}),
            'content': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Detailed tutorial content'}),
            'difficulty': forms.Select(),
            'estimated_hours': forms.NumberInput(attrs={'min': 1}),
        }
        help_texts = {
            'cover_image': 'Upload an image to visually represent your tutorial.',
            'estimated_duration': 'Estimated number of hours to complete.',
        }
        labels = {
            'is_published': 'Publish now?',
        }


class TutorialForm(BaseLearningContentForm):
    class Meta(BaseLearningContentForm.Meta):
        model = Tutorial
        fields = BaseLearningContentForm.Meta.fields


class ArticleForm(BaseLearningContentForm):
    class Meta(BaseLearningContentForm.Meta):
        model = Article
        fields = BaseLearningContentForm.Meta.fields
        