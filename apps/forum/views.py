from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied

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
        if self.raise_exception or self.request.user.is_authenticated:
            raise PermissionDenied("You do not have permission to create posts. Please verify your account.")
        return super().handle_no_permission()


class ForumPostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ForumPost
    template_name = 'forum/post_form.html'
    fields = ['title', 'content', 'category', 'is_pinned', 'is_closed', 'is_published']
    permission_required = 'forum.change_forumpost'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff
    
    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            raise PermissionDenied("You have no permission to update this post.")
        return super().handle_no_permission()
    

class ForumPostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ForumPost
    template_name = 'forum/post_confirm_delete.html'
    success_url = '/forum/'
    permission_required = 'forum.delete_forumpost'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff
    
    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            raise PermissionDenied("You do not have permission to delete this post.")
        return super().handle_no_permission()
