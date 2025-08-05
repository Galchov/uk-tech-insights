from django.shortcuts import render
from django.views.generic import TemplateView


class PublicAPIPageView(TemplateView):
    template_name = 'api/index.html'
    

class NewsAPIPageView(TemplateView):
    template_name = "api/news/endpoints.html"


class CompaniesAPIPageView(TemplateView):
    template_name = "api/companies/endpoints.html"
    