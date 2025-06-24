from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CustomRegistrationForm, CustomEmailAuthenticationForm


login_view = auth_views.LoginView.as_view(
    template_name='accounts/login.html',
    authentication_form=CustomEmailAuthenticationForm,
    extra_context={'hide_navbar': True},
)


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('login')


def register_view(request: HttpRequest) -> HttpResponse:
    form = CustomRegistrationForm()

    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"{username}, your account has successfully been created.")

            return redirect('login')

    context = {
        'form': form,
        'hide_navbar': True,
    }
    return render(request, 'accounts/register.html', context)


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


# @login_required
# def profile_details_view(request: HttpRequest, pk: int) -> HttpResponse:
#     return render(request, 'accounts/profile_details.html')


# @login_required   
def dashboard_view(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'accounts/dashboard.html')


# @login_required
def profile_edit_view(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'accounts/profile_edit.html')


# @login_required
password_change_view = auth_views.PasswordChangeView.as_view(
    template_name='accounts/password_change.html',
)


# @login_required
password_change_done_view = auth_views.PasswordChangeDoneView.as_view(
    template_name='accounts/password_change_done.html',
)


# @login_required
def delete_account_view(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'accounts/delete_account.html')
