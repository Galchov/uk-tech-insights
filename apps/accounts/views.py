from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import views as auth_views, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, UpdateView, DeleteView
from django.template.loader import render_to_string
from django.shortcuts import redirect, render
from django.conf import settings

from datetime import datetime

from .forms import CustomRegistrationForm, CustomEmailAuthenticationForm, ProfileEditForm, AccountEditForm
from .models import CustomUser, Profile


User = get_user_model()

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
    success_message = "%(username)s, your account has successfully been created. Please confirm your email before logging in."
    extra_context = {'hide_navbar': True}

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        domain = current_site.domain
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = self.request.build_absolute_uri(
            reverse('accounts:activate', kwargs={'uidb64': uid, 'token': token})
        )

        subject = f"Activate your account at {domain}"
        from_email = settings.DEFAULT_FROM_EMAIL
        html_content = render_to_string('accounts/account_activation_email.html', {
            'user': user,
            'activation_link': activation_link,
            'current_year': datetime.now().year,
        })
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            [user.email],
        )
        email.attach_alternative(
            html_content,
            'text/html',
        )
        email.send()

        self.object = user

        return super().form_valid(form)
    

class ActivateUserView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
        
            regular_group, created = Group.objects.get_or_create(name='Regular User')
            user.groups.add(regular_group)

            messages.success(request, "Your account has been activated. You can now log in.")

            return redirect(reverse('accounts:login'))
        else:
            return redirect(reverse('accounts:activation_failed'))
        

class ActivationFailedView(TemplateView):
    template_name = 'accounts/activation_failed.html'
    extra_context = {'hide_navbar': True}


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


##### User Verification / User becomes a creator #####

class VerificationRequestView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/verification_request.html')
    
    def post(self, request):
        return redirect('accounts:verification_check.html')


class VerificationCheckView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        missing = []

        if not user.profile.linkedin:
            missing.append("LinkedIn profile link")
        if not user.profile.github:
            missing.append("GitHub profile link")
        
        if not missing:
            user.is_verified = True
            user.save()

            verified_group, create = Group.objects.get_or_create(name="Verified User")
            user.groups.add(verified_group)

            return redirect('accounts:verification_success')
        else:
            return redirect('accounts:verification_failed')


class VerificationSuccessView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/verification_success.html')


class VerificationFailedView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        missing = []

        if not user.profile.github:
            missing.append('GitHub profile link')
        if not user.profile.linkedin:
            missing.append('LinkedIn profile link')

        context = {'missing': missing}
        return render(request, 'accounts/verification_failed.html', context)
