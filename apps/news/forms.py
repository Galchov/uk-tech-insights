from django import forms
from .models import NewsArticle


class NewsArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = ['title', 'summary', 'content', 'cover_image', 'category', 'source', 'authors']
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'rows': 10, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'source': forms.Select(attrs={'class': 'form-select'}),
            'authors': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'summary': 'Short teaser that appears in article lists.',
            'cover_image': 'Optional. Used as a thumbnail or featured image.',
            'source': 'Leave empty if the article is original.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['authors'].required = False  # In case of scraping
