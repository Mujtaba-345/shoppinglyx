from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm)
from django.contrib.auth.models import User
from .models import Customer
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError


class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                    'placeholder': 'Enter Your Password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Your Confirm Password'}))
    email = forms.CharField(required=True,
                            widget=forms.EmailInput(
                                attrs={'class': 'form-control', 'placeholder': 'Enter Your Email Address'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {'email': 'Email', 'first_name': 'First Name', 'last_name': 'Last Name'}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Username'}),
                   'first_name': forms.TextInput(
                       attrs={'class': 'form-control', 'placeholder': 'Enter Your First Name (optional)'}),
                   'last_name': forms.TextInput(
                       attrs={'class': 'form-control', 'placeholder': 'Enter Your Last Name (optional)'})}

    # check the user email is already exist or not
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("User with this email is already exists")
        return email


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'autofocus': True, 'placeholder': 'Enter Your Username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'autocomplete': 'current-password', 'placeholder': 'Enter Your Password'}),
        label=_("Password"), strip=False)


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', 'autofocus': True, 'class': 'form-control',
                   'placeholder': 'Enter Your Old Password'})
    )
    new_password1 = forms.CharField(
        label=_("New Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'Enter Your New Password'}),
        help_text=password_validation.password_validators_help_text_html()
    )

    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control',
                   'placeholder': 'Enter Your Confirm New Password'}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control',
                                       'placeholder': 'Enter Your Email Address'})
    )


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'Enter Your New Password'}),
        help_text=password_validation.password_validators_help_text_html()
    )

    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control',
                   'placeholder': 'Enter Your Confirm New Password'}))


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'state', 'city', 'zipcode']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Name'}),
                   'locality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Locality'}),
                   'state': forms.Select(attrs={'class': 'form-control form-select'}),
                   'city': forms.Select(attrs={'class': 'form-control form-select'}),
                   'zipcode': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Zipcode'})}