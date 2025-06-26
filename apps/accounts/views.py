from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from django.views.generic import TemplateView

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


class CustomRegisterView(SuccessMessageMixin, FormView):
    template_name = 'accounts/register.html'
    form_class = CustomRegistrationForm
    success_url = reverse_lazy('login')
    success_message = "%(username)s, your account has successfully been created."
    extra_context = {'hide_navbar': True}

    def form_valid(self, form):
        form.save()
        self.object = form.instance
        return super().form_valid(form)


class CustomPasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'accounts/password_change.html'
    
    def get_success_url(self):
        return reverse('password_change_done', kwargs={'pk': self.request.user.pk})


class CustomPasswordChangeDoneView(LoginRequiredMixin, auth_views.PasswordChangeDoneView):
    template_name='accounts/password_change_done.html'


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name='accounts/password_reset_request.html'
    email_template_name='accounts/password_reset_email.html'
    extra_context = {'hide_navbar': True}


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name='accounts/password_reset_done.html'
    extra_context = {'hide_navbar': True}
    

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name='accounts/password_reset_confirm.html'
    extra_context = {'hide_navbar': True}


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name='accounts/password_reset_complete.html'
    extra_context = {'hide_navbar': True}


class CustomDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context.update({
            'profile': user.profile,
            'show_navbar': True,

            # TODO: Uncomment when models are in place
            # "post_count": getattr(user, 'posts', []).count(),
            # "tutorial_count": getattr(user, 'tutorials', []).count(),
            # "followers_count": getattr(user, 'followers', []).count(),
            # "following_count": getattr(user, 'following', []).count(),
        })

        return context


# @login_required
def profile_edit_view(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'accounts/profile_edit.html')


# @login_required
def delete_account_view(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'accounts/delete_account.html')
