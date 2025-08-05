from django import urls
from django.urls import path

from . import views


app_name = 'api_docs'

urlpatterns = [
    path('public-api/', views.PublicAPIPageView.as_view(), name="public_api"),
]