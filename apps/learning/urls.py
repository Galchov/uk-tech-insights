from django.urls import path
from . import views


app_name = 'learning'

urlpatterns = [
    path('', views.LearningHomeView.as_view(), name="home_page"),

    path('tutorials/', views.TutorialListView.as_view(), name="tutorial_list"),
    path('tutorials/create/', views.TutorialCreateView.as_view(), name="tutorial_create"),
    path('tutorials/<slug:slug>/', views.TutorialDetailView.as_view(), name="tutorial_detail"),
    path('tutorials/<slug:slug>/edit/', views.TutorialEditView.as_view(), name="tutorial_edit"),
    path('tutorials/<slug:slug>/delete/', views.TutorialDeleteView.as_view(), name="tutorial_delete"),
    path('tutorials/<slug:slug>/complete/', views.TutorialCompleteView.as_view(), name="tutorial_complete"),
    path('tutorials/<slug:slug>/toggle-publish/', views.TutorialTogglePublishView.as_view(), name='tutorial_toggle_publish'),

    path('articles/', views.ArticleListView.as_view(), name="article_list"),
    path('articles/create/', views.ArticleCreateView.as_view(), name="article_create"),
    path('articles/<slug:slug>/', views.ArticleDetailView.as_view(), name="article_detail"),
    path('articles/<slug:slug>/edit/', views.ArticleEditView.as_view(), name="article_edit"),
    path('articles/<slug:slug>/delete/', views.ArticleDeleteView.as_view(), name="article_delete"),

    path('author/<str:username>/', views.AuthorContentListView.as_view(), name="author_content"),
]
