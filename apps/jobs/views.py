from django.shortcuts import render
from django.views.generic import TemplateView


class JobsMainView(TemplateView):
    template_name = 'jobs/jobs_home_page.html'
