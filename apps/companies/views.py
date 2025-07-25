from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Company
from .forms import CompanyForm


##### Public Views #####

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


##### Admins and Moderators Only Views #####

class CompanyAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'companies/company_form.html'
    permission_required = 'companies.add_company'
    context_object_name = 'company'

    raise_exception = False
    login_url = reverse_lazy('accounts:login')

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(self.get_login_url())
        return redirect('companies:company_list')
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.object.get_absolute_url()
    

class CompanyEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'companies/company_form.html'
    permission_required = 'companies.change_company'
    context_object_name = 'company'

    raise_exception = False
    login_url = reverse_lazy('accounts:login')

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(self.get_login_url())
        return redirect('companies:company_list')

    def get_success_url(self):
        return self.object.get_absolute_url()


class CompanyDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Company
    template_name = 'companies/company_confirm_delete.html'
    context_object_name = 'company'
    permission_required = 'companies.delete_company'
    success_url = reverse_lazy('companies:company_list')
