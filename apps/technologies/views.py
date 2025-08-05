from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Technology


class ModeratorOrAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_staff or user.groups.filter(name='Moderators').exists())


class TechnologyListView(LoginRequiredMixin, ModeratorOrAdminRequiredMixin, ListView):
    model = Technology
    template_name = 'technologies/technology_list.html'
    context_object_name = 'technologies'


class TechnologyDetailView(LoginRequiredMixin, ModeratorOrAdminRequiredMixin, DetailView):
    model = Technology
    template_name = 'technologies/technology_detail.html'
    context_object_name = 'technology'


class TechnologyCreateView(LoginRequiredMixin, ModeratorOrAdminRequiredMixin, CreateView):
    model = Technology
    fields = ['name', 'description', 'website', 'logo']
    template_name = 'technologies/technology_form.html'
    success_url = reverse_lazy('technologies:technology_list')


class TechnologyUpdateView(LoginRequiredMixin, ModeratorOrAdminRequiredMixin, UpdateView):
    model = Technology
    fields = ['name', 'description', 'website', 'logo']
    template_name = 'technologies/technology_form.html'
    success_url = reverse_lazy('technologies:technology_list')


class TechnologyDeleteView(LoginRequiredMixin, ModeratorOrAdminRequiredMixin, DeleteView):
    model = Technology
    template_name = 'technologies/technology_confirm_delete.html'
    success_url = reverse_lazy('technologies:technology_list')
