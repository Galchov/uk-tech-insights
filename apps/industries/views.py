from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Industry


class IndustryAccessMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_staff or user.groups.filter(name='Moderators').exists())


class IndustryListView(IndustryAccessMixin, ListView):
    model = Industry
    template_name = 'industries/industry_list.html'
    context_object_name = 'industries'


class IndustryCreateView(IndustryAccessMixin, CreateView):
    model = Industry
    fields = ['name', 'description']
    template_name = 'industries/industry_form.html'
    success_url = reverse_lazy('industries:industry_list')


class IndustryUpdateView(IndustryAccessMixin, UpdateView):
    model = Industry
    fields = ['name', 'description']
    template_name = 'industries/industry_form.html'
    success_url = reverse_lazy('industries:industry_list')


class IndustryDeleteView(IndustryAccessMixin, DeleteView):
    model = Industry
    template_name = 'industries/industry_confirm_delete.html'
    success_url = reverse_lazy('industries:industry_list')
