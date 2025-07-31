from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.apps import apps

from .models import Comment
from .forms import CommentForm


class HomePageView(TemplateView):
    template_name = 'common/home-page.html'


class PublicAPIPageView(TemplateView):
    template_name = 'common/public_api.html'


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.model_name = self.kwargs.get('model')
        self.slug = self.kwargs.get('slug')
        return super().dispatch(request, *args, **kwargs)

    def get_content_object(self):
        model = apps.get_model(app_label='forum', model_name=self.model_name)
        return get_object_or_404(model, slug=self.slug)

    def form_valid(self, form):
        content_object = self.get_content_object()
        form.instance.user = self.request.user
        form.instance.content_object = content_object
        return super().form_valid(form)

    def get_success_url(self):
        content_object = self.get_content_object()
        return content_object.get_absolute_url()
