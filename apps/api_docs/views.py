from django.shortcuts import render
from django.views.generic import TemplateView


class PublicAPIPageView(TemplateView):
    template_name = 'api/index.html'
    