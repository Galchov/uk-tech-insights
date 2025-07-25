from django import forms

from .models import Company, Industry, Location


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'name',
            'logo',
            'description',
            'website',
            'foundation_date',
            'headquarters',
            'operating_countries',
            'industries',
            'tech_stack',
        ]


class IndustryForm(forms.ModelForm):
    class Meta:
        model = Industry
        fields = "__all__"


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = "__all__"
