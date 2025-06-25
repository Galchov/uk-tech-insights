from django.urls import include, path
from . import views


urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register_view, name="register"),

    path('password-reset/', views.password_reset_view, name="password_reset"),
    path('password-reset/done/', views.password_reset_done_view, name="password_reset_done"),
    path('password-reset/confirm/<uidb64>/<token>/', views.password_reset_confirm_view, name="password_reset_confirm"),
    path('password-reset/complete/', views.password_reset_complete_view, name="password_reset_complete"),

    path('profile/<int:pk>/', views.dashboard_view, name="dashboard"),
    path('profile/<int:pk>/edit/', views.profile_edit_view, name="profile_edit"),
    path('profile/<int:pk>/password-change/', views.password_change_view, name="password_change"),
    path('profile/<int:pk>/password-change-done/', views.password_change_done_view, name="password_change_done"),
    path('profile/<int:pk>/delete-account/', views.delete_account_view, name="delete_account"),
]
