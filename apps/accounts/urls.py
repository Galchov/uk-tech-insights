from django.urls import include, path
from . import views


urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name="login"),
    path('logout/', views.CustomLogoutView.as_view(), name="logout"),
    path('register/', views.register_view, name="register"),

    path('password-reset/', views.CustomPasswordResetView.as_view(), name="password_reset"),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset/confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password-reset/complete/', views.CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path('profile/<int:pk>/', views.dashboard_view, name="dashboard"),
    path('profile/<int:pk>/edit/', views.profile_edit_view, name="profile_edit"),
    path('profile/<int:pk>/password-change/', views.CustomPasswordChangeView.as_view(), name="password_change"),
    path('profile/<int:pk>/password-change-done/', views.CustomPasswordChangeDoneView.as_view(), name="password_change_done"),
    path('profile/<int:pk>/delete-account/', views.delete_account_view, name="delete_account"),
]
