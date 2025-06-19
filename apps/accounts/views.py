from django.shortcuts import render
from django.http import HttpResponse
from urllib.request import Request
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def login_view(request: Request) -> HttpResponse:
    return render(request, 'accounts/login.html', {'hide_navbar': True})


def logout_view(request: Request) -> HttpResponse:
    logout(request)
    return redirect('login')


def register_view(request: Request) -> HttpResponse:
    return render(request, 'accounts/register.html', {'hide_navbar': True})


password_reset_view = auth_views.PasswordResetView.as_view(
    template_name='accounts/password_reset_request.html',
    email_template_name='accounts/password_reset_email.html',   # For testing
)


password_reset_done_view = auth_views.PasswordResetDoneView.as_view(
    template_name='accounts/password_reset_done.html',
)


password_reset_confirm_view = auth_views.PasswordResetConfirmView.as_view(
    template_name='accounts/password_reset_confirm.html',
)


password_reset_complete_view = auth_views.PasswordResetCompleteView.as_view(
    template_name='accounts/password_reset_complete.html',
)


def change_password_view(request: Request, pk: int) -> HttpResponse:
    return render(request, 'accounts/change_password.html')


def delete_account_view(request: Request, pk: int) -> HttpResponse:
    return render(request, 'accounts/delete_account.html')


# TODO: To be implemented
# @login_required   
def dashboard_view(request: Request) -> HttpResponse:
    return render(request, 'accounts/dashboard.html')


def profile_details_view(request: Request, pk: int) -> HttpResponse:
    return render(request, 'accounts/profile_details.html')


def profile_edit_view(request: Request, pk: int) -> HttpResponse:
    return render(request, 'accounts/profile_edit.html')
