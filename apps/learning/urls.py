from django.urls import path
from . import views


app_name = 'learning'

urlpatterns = [
    path('', views.LearningHomeView.as_view(), name="home_page"),
]