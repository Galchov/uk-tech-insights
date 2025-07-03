from django.urls import path
from . import views


app_name = 'forum'

urlpatterns = [
    path('', views.ForumPostListView.as_view(), name="post_list"),
    path('post/create/', views.ForumPostCreateView.as_view(), name="post_create"),
    path('user-posts/', views.UserPostsListView.as_view(), name="user_posts"),
    path('post/<slug:slug>/', views.ForumPostDetailView.as_view(), name="post_details"),
    path('post/<slug:slug>/edit/', views.ForumPostUpdateView.as_view(), name="post_edit"),
    path('post/<slug:slug>/delete/', views.ForumPostDeleteView.as_view(), name="post_delete"),
    path('post/<slug:slug>/publish/', views.PublishPostView.as_view(), name="publish_post"),
    path('post/<slug:slug>/pin/', views.PinPostView.as_view(), name="pin_post"),
    path('post/<slug:slug>/close/', views.ClosePostView.as_view(), name="close_post"),

    path('categories/', views.CategoryListView.as_view(), name="category_list"),
]
