from django import forms

from .models import InternalArticle


class InternalArticleForm(forms.ModelForm):
    class Meta:
        model = InternalArticle
        fields = ['title', 'summary', 'content', 'cover_image', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 12}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select w-auto'}),
        }
