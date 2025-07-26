from django import forms

from .models import Company, Industry


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'name',
            'logo',
            'description',
            'website',
            'foundation_date',
            'operating_countries',
            'industries',
            'tech_stack',
        ]


class IndustryForm(forms.ModelForm):
    class Meta:
        model = Industry
        fields = "__all__"
