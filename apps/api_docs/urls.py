from django import urls
from django.urls import path

from . import views


app_name = 'api_docs'

urlpatterns = [
    path('', views.PublicAPIPageView.as_view(), name="public_api"),
    path("news/", views.NewsAPIPageView.as_view(), name="news"),
    path("companies/", views.CompaniesAPIPageView.as_view(), name="companies"),
]
