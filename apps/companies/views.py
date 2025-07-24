from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Company


class CompanyListView(ListView):
    model = Company
    template_name = 'companies/company_list.html'
    context_object_name = 'companies'
    paginate_by = 10
    queryset = Company.objects.all()


class CompanyDetailView(DetailView):
    model = Company
    template_name = 'companies/company_detail.html'
    context_object_name = 'company'
