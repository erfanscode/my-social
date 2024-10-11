from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from social.forms import UserRegistrationForm, UserEditForm


def index(request):
    return HttpResponse("شما با موفقیت وارد شدید")

def log_out(request):
    logout(request)
    return HttpResponse("شما خارج شدید")

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'registration/register_done.html', {'user': user})
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def edit_user(request):
    if request.method == "POST":
        user_form = UserEditForm(data=request.POST, instance=request.user, files=request.FILES)
        if user_form.is_valid():
            user_form.save()
            return redirect('social:index')
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, 'registration/edit_user.html', {'user_form': user_form})