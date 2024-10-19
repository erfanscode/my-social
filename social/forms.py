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


class TicketForm(forms.Form):
    # form for send ticket
    CHOICES_SUBJECT = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش')
    )
    message = forms.CharField(widget=forms.Textarea, required=True)
    name = forms.CharField(max_length=120, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=11, required=True)
    subject = forms.ChoiceField(choices=CHOICES_SUBJECT, required=True)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError('شماره تلفن باید عدد باشد')
            else:
                return phone


class CreatePostForm(forms.ModelForm):
    # form for create post
    class Meta:
        model = Post
        fields = ['description', 'tags']


class SearchForm(forms.Form):
    query = forms.CharField()
