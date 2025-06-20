from django.urls import include, path
from . import views


urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register_view, name="register"),

    path('password-reset/', include([
        path('', views.password_reset_view, name="password_reset"),
        path('done/', views.password_reset_done_view, name="password_reset_done"),
        path('confirm/<uidb64>/<token>/', views.password_reset_confirm_view, name="password_reset_confirm"),
        path('complete/', views.password_reset_complete_view, name="password_reset_complete"),
    ])),

    path('profile/<int:pk>/', include([
        path('', views.dashboard_view, name="dashboard"),
        path('edit/', views.profile_edit_view, name="profile_edit"),
        path('password-change/', views.password_change_view, name="password_change"),
        path('password-change-done/', views.password_change_done_view, name="password_change_done"),
        path('delete-account/', views.delete_account_view, name="delete_account"),
    ]))
]
