from django import forms
from django.core.exceptions import ValidationError

from .models import JobPost


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        exclude = ['id', 'slug', 'created_by', 'published_at', 'updated_at']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'responsibilities': forms.Textarea(attrs={'rows': 3}),
            'requirements': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()

        source = cleaned_data.get('source', '').strip()
        reference = cleaned_data.get('external_reference', '').strip()

        cleaned_data['source'] = source
        cleaned_data['external_reference'] = reference
    
        if source and reference:
            if JobPost.objects.filter(source=source, external_reference=reference).exists():
                raise forms.ValidationError("This job has already been imported.")

        return cleaned_data