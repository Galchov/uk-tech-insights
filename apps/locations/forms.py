from django import forms


class LocationForm(forms.Form):
    city_name = forms.CharField(label="City", max_length=100)
    country_name = forms.CharField(label="Country", max_length=100)
    