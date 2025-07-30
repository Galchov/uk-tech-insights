from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from .models import JobPost, JobApplication, JobPostUpdateHistory
from .forms import JobPostForm, JobApplicationForm


class JobsPostListView(ListView):
    model = JobPost
    template_name = 'job_listings/jobs_home_page.html'
    context_object_name = 'jobs'
    queryset = JobPost.objects.active()


class JobPostDetailView(DetailView):
    model = JobPost
    template_name = 'job_listings/job_post_detail.html'
    context_object_name = 'job'


class JobPostAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = JobPost
    form_class = JobPostForm
    template_name = 'job_listings/job_post_form.html'

    def test_func(self):
        return self.request.user.groups.filter(name__in=['Verified User', 'Moderator', 'Admin']).exists()

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


class JobPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = JobPost
    form_class = JobPostForm
    template_name = 'job_listings/job_post_form.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = False
        return context

    def test_func(self):
        job = self.get_object()
        user = self.request.user
        is_verified = user.groups.filter(name='Verified User').exists()
        is_moderator_or_admin = user.groups.filter(name__in=['Moderator', 'Admin']).exists()

        return (
            (is_verified and job.created_by == user)
            or is_moderator_or_admin
        )

    def form_valid(self, form):
        messages.success(self.request, "Job post successfully updated.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Update failed. Please correct the form.")
        return super().form_invalid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class JobApplicationCreateView(LoginRequiredMixin, CreateView):
    model = JobApplication
    form_class = JobApplicationForm
    template_name = 'job_listings/job_application_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.job = get_object_or_404(JobPost, slug=self.kwargs['slug'], is_active=True)
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        form.instance.job = self.job
        form.instance.user = self.request.user
        messages.success(self.request, "Your application was successfully submitted.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your application.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = self.job
        return context

    def get_success_url(self):
        return self.job.get_absolute_url()


class JobPostToggleStatusView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, slug, *args, **kwargs):
        job = get_object_or_404(JobPost, slug=slug)
        job.is_active = not job.is_active
        job.save()

        if job.is_active:
            messages.success(request, f"The job '{job.title}' has been reopened.")
        else:
            messages.success(request, f"The job '{job.title}' has been closed.")

        return redirect('job_listings:job_detail', slug=slug)

    def test_func(self):
        job = get_object_or_404(JobPost, slug=self.kwargs['slug'])
        user = self.request.user
        is_verified = user.groups.filter(name='Verified User').exists()
        is_moderator_or_admin = user.groups.filter(name__in=['Moderator', 'Admin']).exists()

        return (
            (is_verified and job.created_by == user)
            or is_moderator_or_admin
        )
