from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # path('', views.NewsArticleListView.as_view(), name='article_list'),
    # path('article/create/', views.NewsArticleCreateView.as_view(), name='article_create'),
    # path('article/<slug:slug>/', views.NewsArticleDetailView.as_view(), name='article_detail'),
    # path('article/<slug:slug>/edit/', views.NewsArticleUpdateView.as_view(), name='article_edit'),
    # path('article/<slug:slug>/delete/', views.NewsArticleDeleteView.as_view(), name='article_delete'),

    # path('category/<slug:slug>/', views.NewsByCategoryListView.as_view(), name='articles_by_category'),
    # path('source/<slug:slug>/', views.NewsBySourceListView.as_view(), name='articles_by_source'),

    # path('author/<str:username>/', views.NewsByAuthorListView.as_view(), name='articles_by_author'),
]