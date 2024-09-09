from dataclasses import fields
from pyexpat import model
from urllib import request
from django import forms
from django.forms import ModelForm
from . models import *
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .auth_backend import PasswordlessAuthBackend
from django.contrib.auth.forms import UsernameField
from django.contrib.auth import login
from django.shortcuts import redirect
import urllib.request


usertype_choice = (
    (None,'-------'),
    ('is_admin','is_admin'),
    ('is_staff','is_staff'),
    ('is_student','is_student'),
)

class PickyAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.user_type == 'is_staff':
            raise ValidationError(
        ("This account is inactive."),
                code='inactive',
            )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class Signup_form(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class signup_form(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"}))
    register_number = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Register Number"}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"class": "form-control", "placeholder": "Date of Birth"}))
    user_type = forms.ChoiceField(choices=usertype_choice)
    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Fullname"}))
    address = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Address"}))
    standard = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Standard"}))
    section = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Section"}))
    data_entry_user = forms.BooleanField(required=False)


class login_form(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
    attrs={"class": "form-control", "placeholder": "Email", "autocomplete": "off"}))
    phone = forms.CharField(widget=forms.TextInput(
    attrs={"class": "form-control", "placeholder": "Phone", "autocomplete": "off"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['phone'].required = True


def get_user(self):
    return self.user_cache


def get_invalid_login_error(self):
    return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
        )