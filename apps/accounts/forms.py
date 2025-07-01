from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms

from .models import CustomUser, Profile


class CustomRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password1', 'password2']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name')


class CustomEmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'autofocus': True,
            'autocomplete': 'username',
            'required': True,
            'class': 'form-control',
        }),
        label='Email',
        max_length=254,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'required': True,
            'class': 'form-control',
        }),
        label='Password',
    )

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError("This account is inactive.", code='inactive')
    

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'headline', 'bio', 'date_of_birth', 'city', 'country', 'profile_picture',
            'personal_website', 'linkedin', 'twitter', 'github', 'gitlab',
            'tech_stack', 'contact_email', 'languages',
        ]


class AccountForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'first_name', 'last_name',
        ]
