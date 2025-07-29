from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import JobPost, JobApplication, JobPostUpdateHistory
from .forms import JobPostForm


class JobsPostListView(ListView):
    model = JobPost
    template_name = 'job_listings/jobs_home_page.html'
    context_object_name = 'jobs'
    queryset = JobPost.objects.active()


class JobPostDetailView(DetailView):
    model = JobPost
    template_name = 'job_listings/job_detail.html'
    context_object_name = 'job'


class JobPostAddView(LoginRequiredMixin, CreateView):
    model = JobPost
    form_class = JobPostForm
    template_name = 'job_listings/job_post_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = True
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Job post successfully created.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your submission. Please check the form.")
        return super().form_invalid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class JobPostUpdateView(UpdateView):
    pass


class JobPostDeleteView(DeleteView):
    pass

