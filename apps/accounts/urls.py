from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name="login"),
    path('logout/', views.CustomLogoutView.as_view(), name="logout"),
    path('register/', views.CustomRegisterView.as_view(), name="register"),

    path('activate/<uidb64>/<token>/', views.ActivateUserView.as_view(), name="activate"),
    path('activation-failed/', views.ActivationFailedView.as_view(), name='activation_failed'),

    path('verification/request/', views.VerificationRequestView.as_view(), name='verification_request'),
    path('verification/check/', views.VerificationCheckView.as_view(), name='verification_check'),
    path('verification/success/', views.VerificationSuccessView.as_view(), name='verification_success'),
    path('verification/failed/', views.VerificationFailedView.as_view(), name='verification_failed'),

    path('password-reset/', views.CustomPasswordResetView.as_view(), name="password_reset"),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset/confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password-reset/complete/', views.CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path('profile/<int:pk>/', views.CustomDashboardView.as_view(), name="dashboard"),
    path('profile/<int:pk>/profile-edit/', views.ProfileEditView.as_view(), name="profile_edit"),
    path('profile/<int:pk>/account-edit/', views.AccountEditView.as_view(), name="account_edit"),
    path('profile/<int:pk>/password-change/', views.CustomPasswordChangeView.as_view(), name="password_change"),
    path('profile/<int:pk>/password-change-done/', views.CustomPasswordChangeDoneView.as_view(), name="password_change_done"),
    path('profile/<int:pk>/delete-account/', views.AccountDeleteView.as_view(), name="delete_account"),
]
