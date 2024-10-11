# Forms for social app
from django import forms
from django.core.exceptions import ValidationError

from .models import *


class UserRegistrationForm(forms.ModelForm):
    # Registration form
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone']

    def clean_password2(self):
        # Checked password and re-password is equal
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError("رمزعبور یکسان نمیباشد")
        return cd['password2']

    def clean_username(self):
        # Checked not exists username
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("نام کاربری از قبل وجود دارد")
        return username

    def clean_phone(self):
        # Checked not exists phone number
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone=phone).exists():
            raise ValidationError("شماره موبایل از قبل وجود دارد")
        return phone


class UserEditForm(forms.ModelForm):
    # Edit user information form
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'date_of_birth', 'photo', 'email', 'phone']

    def clean_username(self):
        # Checked not exists username
        username = self.cleaned_data['username']
        if User.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise ValidationError("نام کاربری از قبل وجود دارد")
        return username

    def clean_phone(self):
        # Checked not exists phone number
        phone = self.cleaned_data['phone']
        if User.objects.exclude(id=self.instance.id).filter(phone=phone).exists():
            raise ValidationError("شماره موبایل از قبل وجود دارد")
        return phone
