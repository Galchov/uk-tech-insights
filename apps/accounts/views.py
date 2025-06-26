from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse

from .forms import CustomRegistrationForm, CustomEmailAuthenticationForm


class CustomLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomEmailAuthenticationForm
    redirect_authenticated_user = True
    extra_context = {'hide_navbar': True}

    def get_success_url(self):
        return reverse('dashboard', kwargs={'pk': self.request.user.pk}) or self.get_redirect_url()
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid Email or Passowrd. Please try again.")
        return super().form_invalid(form)


class CustomLogoutView(auth_views.LogoutView):
    next_page = 'login'

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, "You have been logged out.")
        return super().dispatch(request, *args, **kwargs)


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


class CustomPasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'accounts/password_change.html'
    
    def get_success_url(self):
        return reverse('password_change_done', kwargs={'pk': self.request.user.pk})


class CustomPasswordChangeDoneView(LoginRequiredMixin, auth_views.PasswordChangeDoneView):
    template_name='accounts/password_change_done.html'


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name='accounts/password_reset_request.html'
    email_template_name='accounts/password_reset_email.html'


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name='accounts/password_reset_done.html'
    

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name='accounts/password_reset_confirm.html'


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name='accounts/password_reset_complete.html'


# @login_required   
def dashboard_view(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'accounts/dashboard.html')


# @login_required
def profile_edit_view(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'accounts/profile_edit.html')


# @login_required
def delete_account_view(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'accounts/delete_account.html')
