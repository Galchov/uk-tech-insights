from django.urls import path
from . import views


urlpatterns = [
    path('signin/', views.sign_in_view, name="signin"),
]