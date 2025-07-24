from django.urls import path

from . import views


app_name = 'jobs'

urlpatterns = [
    path('', views.JobsMainView.as_view(), name="home_page"),
]
