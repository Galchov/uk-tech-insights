from django.urls import include, path
from . import views


urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),  # TODO: Test when User model is in DB
    path('register/', views.register_view, name="register"),

    path('password-reset/', include([
        path('', views.password_reset_view, name="password_reset"),
        path('done/', views.password_reset_done_view, name="password_reset_done"),
        path('confirm/<uidb64>/<token>/', views.password_reset_confirm_view, name="password_reset_confirm"),
        path('complete/', views.password_reset_complete_view, name="password_reset_complete"),
    ])),

    path('dashboard/', views.dashboard_view, name="dashboard"),

    path('profile/<int:pk>/', include([
        path('', views.profile_details_view, name="profile_details"),
        path('edit/', include([
            path('', views.profile_edit_view, name="profile_edit"),
            path('change-password/', views.change_password_view, name="change_password"),
            path('delete/', views.profile_delete_view, name="profile_delete"),
        ])),
    ])),
]
