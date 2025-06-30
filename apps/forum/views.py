from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import ForumPost, ForumCategory


class PostListView(ListView):
    model = ForumPost
    template_name = 'forum/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return ForumPost.objects.filter(is_published=True)


class PostDetailView(DetailView):
    model = ForumPost
    template_name = 'forum/post_details.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.increment_views()
        return obj
    

class PostCreateView(LoginRequiredMixin, CreateView):
    model = ForumPost
    template_name = 'forum/post_form.html'
    fields = ['title', 'content', 'category', 'is_pinned', 'is_closed', 'is_published']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ForumPost
    template_name = 'forum/post_form.html'
    fields = ['title', 'content', 'category', 'is_pinned', 'is_closed', 'is_published']

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff
    

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ForumPost
    template_name = 'forum/post_confirm_delete.html'
    success_url = '/forum/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff
    

class CategoryListView(ListView):
    model = ForumCategory
    template_name = 'forum/category_list.html'
    context_object_name = 'categories'
