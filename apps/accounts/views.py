from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, UpdateView, DeleteView

from .forms import CustomRegistrationForm, CustomEmailAuthenticationForm, ProfileEditForm, AccountEditForm
from .models import CustomUser, Profile


##### Authentication #####

class CustomLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomEmailAuthenticationForm
    redirect_authenticated_user = True
    extra_context = {'hide_navbar': True}

    def get_success_url(self):
        return reverse('accounts:dashboard', kwargs={'pk': self.request.user.pk}) or self.get_redirect_url()
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid Email or Passowrd. Please try again.")
        return super().form_invalid(form)


class CustomLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('accounts:login')

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, "You have been logged out.")
        return super().dispatch(request, *args, **kwargs)


class CustomRegisterView(SuccessMessageMixin, FormView):
    template_name = 'accounts/register.html'
    form_class = CustomRegistrationForm
    success_url = reverse_lazy('accounts:login')
    success_message = "%(username)s, your account has successfully been created."
    extra_context = {'hide_navbar': True}

    def form_valid(self, form):
        form.save()
        self.object = form.instance
        return super().form_valid(form)


class CustomPasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'accounts/password_change.html'
    
    def get_success_url(self):
        return reverse('accounts:password_change_done', kwargs={'pk': self.request.user.pk})


class CustomPasswordChangeDoneView(LoginRequiredMixin, auth_views.PasswordChangeDoneView):
    template_name='accounts/password_change_done.html'


##### Password Reset Cycle #####

class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name='accounts/password_reset_request.html'
    email_template_name='accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    extra_context = {'hide_navbar': True}


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name='accounts/password_reset_done.html'
    extra_context = {'hide_navbar': True}
    

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name='accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')
    extra_context = {'hide_navbar': True}


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name='accounts/password_reset_complete.html'
    extra_context = {'hide_navbar': True}


##### Account and Profile Details #####

class CustomDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'
    login_url = 'accounts:login'

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


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'accounts/profile_edit.html'
    form_class = ProfileEditForm

    def get_object(self, queryset=None):
        return self.request.user.profile
    
    def get_success_url(self):
        return reverse_lazy('accounts:dashboard', kwargs={'pk': self.request.user.pk})


class AccountEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'accounts/account_edit.html'
    form_class = AccountEditForm

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    
    def get_success_url(self):
        return reverse_lazy('accounts:dashboard', kwargs={'pk': self.request.user.pk})


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'accounts/delete_account.html'
    success_url = reverse_lazy('common:home')

    def get_object(self, queryset=None):
        return self.request.user
    
    def delete(self, request, *args, **kwargs):
        logout(request)
        return super().delete(request, *args, **kwargs)
