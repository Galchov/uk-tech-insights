from django.urls import include, path
from . import views

urlpatterns  = [
    path('dashboard/', views.dashboard_view, name="dashboard"),

    path('profile/<int:pk>/', include([
        path('', views.profile_details_view, name="profile_details"),
        path('edit/', views.profile_edit_view, name="profile_edit"),
    ])),
]
