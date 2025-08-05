from django import forms

from .models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'name',
            'logo',
            'description',
            'website',
            'foundation_date',
            'location',
            'address',
            'operating_countries',
            'industries',
            'tech_stack',
        ]
