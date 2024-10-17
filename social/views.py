from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from taggit.models import Tag

from social.forms import UserRegistrationForm, UserEditForm, TicketForm, CreatePostForm
from social.models import Post


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

@login_required
def edit_user(request):
    if request.method == "POST":
        user_form = UserEditForm(data=request.POST, instance=request.user, files=request.FILES)
        if user_form.is_valid():
            user_form.save()
            return redirect('social:index')
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, 'registration/edit_user.html', {'user_form': user_form})

def ticket(request):
    # view for send ticket to mail
    sent = False
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            message = f"{cd['name']}\n{cd['email']}\n{cd['phone']}\n\n{cd['message']}"
            send_mail(
                cd['subject'],
                message, settings.EMAIL_HOST_USER,
                ['djangotestmenow@gmail.com'],
                fail_silently=False
            )
            sent = True
    else:
        form = TicketForm()
    return render(request, 'forms/ticket.html', {"form": form, "sent": sent})

def post_list(request, tag_slug=None):
    # view for show list posts
    posts = Post.objects.all()
    tag = None
    if tag_slug:
        tag = Tag.objects.get(slug=tag_slug)
        posts = Post.objects.filter(tags__in=[tag])
    context = {
        'posts': posts,
        'tag': tag,
    }
    return render(request, 'social/list.html', context)

def create_post(request):
    # view for create post form
    if request.method == "POST":
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('social:post_list')
    else:
        form = CreatePostForm()
    return render(request, 'forms/create_post.html', {"form": form})
