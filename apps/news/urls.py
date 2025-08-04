from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('article/create/', views.InternalArticleCreateView.as_view(), name='article_create'),
    path('article/<slug:slug>/', views.NewsArticleDetailView.as_view(), name='article_detail'),

    path('internal/pending/', views.InternalArticleModerationListView.as_view(), name='internal_article_pending'),
    path('internal/<slug:slug>/publish/', views.InternalArticlePublishView.as_view(), name='internal_article_publish'),
    path('internal/<slug:slug>/edit/', views.InternalArticleUpdateView.as_view(), name='internal_article_edit'),
    path('internal/<slug:slug>/unpublish/', views.InternalArticleUnpublishView.as_view(), name='internal_article_unpublish'),

    path('article/<slug:slug>/delete/', views.NewsArticleDeleteView.as_view(), name='article_delete'),
    # path('article/<slug:slug>/edit/', views.NewsArticleUpdateView.as_view(), name='article_edit'),
    # path('article/<slug:slug>/delete/', views.NewsArticleDeleteView.as_view(), name='article_delete'),

    # path('category/<slug:slug>/', views.NewsByCategoryListView.as_view(), name='articles_by_category'),
    # path('source/<slug:slug>/', views.NewsBySourceListView.as_view(), name='articles_by_source'),

    # path('author/<str:username>/', views.NewsByAuthorListView.as_view(), name='articles_by_author'),
]
