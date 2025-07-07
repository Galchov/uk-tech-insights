from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from .models import ForumPost, ForumCategory


##### Public Views #####

class ForumPostListView(ListView):
    model = ForumPost
    template_name = 'forum/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return ForumPost.objects.filter(is_published=True)


class ForumPostDetailView(DetailView):
    model = ForumPost
    template_name = 'forum/post_details.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.increment_views()
        return obj
    

class CategoryListView(ListView):
    model = ForumCategory
    template_name = 'forum/category_list.html'
    context_object_name = 'categories'


class CategoryPostListView(ListView):
    model = ForumPost
    template_name = 'forum/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return ForumPost.objects.filter(
            category__slug=self.kwargs['slug'],
            is_published=True,
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(ForumCategory, slug=self.kwargs['slug'])
        return context
    

##### Restricted Views (Verified Users) #####

class ForumPostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ForumPost
    template_name = 'forum/post_form.html'
    fields = ['title', 'content', 'category', 'is_pinned', 'is_closed', 'is_published']
    permission_required = 'forum.add_forumpost'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to create posts. Please verify your account.")
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        can_moderate = (
            self.request.user.has_perm('forum.can_pin_posts')
            or self.request.user.has_perm('forum.can_close_posts')
            or self.request.user.has_perm('forum.can_publish_posts')
        )

        if not can_moderate:
            form.fields['is_pinned'].widget.attrs['disabled'] = True
            form.fields['is_closed'].widget.attrs['disabled'] = True
            form.fields['is_published'].widget.attrs['disabled'] = True

            form.fields['is_pinned'].initial = False
            form.fields['is_closed'].initial = False
            form.fields['is_published'].initial = False

        return form
    
    def form_valid(self, form):
        can_moderate = (
            self.request.user.has_perm('forum.can_pin_posts')
            or self.request.user.has_perm('forum.can_close_posts')
            or self.request.user.has_perm('forum.can_publish_posts')
        )

        if not can_moderate:
            form.instance.is_pinned = False
            form.instance.is_closed = False
            form.instance.is_published = False

        form.instance.author = self.request.user

        return super().form_valid(form)


class ForumPostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ForumPost
    template_name = 'forum/post_form.html'
    fields = ['title', 'content', 'category', 'is_pinned', 'is_closed', 'is_published']
    permission_required = 'forum.change_forumpost'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        if self.request.user.has_perm('forum.can_edit_others_posts'):
            return True
        return False
    
    def handle_no_permission(self):
        raise PermissionDenied("You have no permission to update this post.")
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        can_moderate = (
            self.request.user.has_perm('forum.can_pin_posts')
            or self.request.user.has_perm('forum.can_close_posts')
            or self.request.user.has_perm('forum.can_publish_posts')
        )

        if not can_moderate:
            form.fields['is_pinned'].widget.attrs['disabled'] = True
            form.fields['is_closed'].widget.attrs['disabled'] = True
            form.fields['is_published'].widget.attrs['disabled'] = True

        return form
    
    def form_valid(self, form):
        can_moderate = (
            self.request.user.has_perm('forum.can_pin_posts')
            or self.request.user.has_perm('forum.can_close_posts')
            or self.request.user.has_perm('forum.can_publish_posts')
        )

        if not can_moderate:
            form.instance.is_pinned = False
            form.instance.is_closed = False
            form.instance.is_published = False

        form.instance.author = self.request.user

        return super().form_valid(form)
    

class ForumPostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ForumPost
    template_name = 'forum/post_confirm_delete.html'
    success_url = reverse_lazy('forum:post_list')
    permission_required = 'forum.delete_forumpost'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        if self.request.user.has_perm('forum.can_edit_others_posts'):
            return True
        return False
    
    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to delete this post.")


class PublishPostView(PermissionRequiredMixin, View):
    permission_required = 'forum.can_publish_posts'
    raise_exception = True

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(ForumPost, slug=slug)
        post.is_published = True
        post.save()
        return redirect(post.get_absolute_url())


class PinPostView(PermissionRequiredMixin, View):
    permission_required = 'forum.can_pin_posts'
    raise_exception = True

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(ForumPost, slug=slug)
        post.is_pinned = not post.is_pinned
        post.save()
        return redirect(post.get_absolute_url())


class ClosePostView(PermissionRequiredMixin, View):
    permission_required = 'forum.can_close_posts'
    raise_exception = True

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(ForumPost, slug=slug)
        post.is_closed = not post.is_closed
        post.save()
        return redirect(post.get_absolute_url())


class UserPostsListView(LoginRequiredMixin, ListView):
    model = ForumPost
    template_name = 'forum/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return ForumPost.objects.filter(author=self.request.user).order_by('-created_at')
