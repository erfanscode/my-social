from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from taggit.models import Tag
from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from social.forms import (
    UserRegistrationForm,
    UserEditForm,
    TicketForm,
    CreatePostForm,
    SearchForm
)
from social.models import Post, User, Contact


def index(request):
    return HttpResponse("شما با موفقیت وارد شدید")

def profile(request):
    user = User.objects.prefetch_related('followers', 'following').get(id=request.user.id)
    saved_posts = user.saved_posts.all()
    return render(request, 'social/profile.html', {'saved_posts': saved_posts, 'user': user})

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
    posts = Post.objects.select_related('author').order_by('-total_likes')
    tag = None
    if tag_slug:
        tag = Tag.objects.get(slug=tag_slug)
        posts = Post.objects.filter(tags__in=[tag])
    page = request.GET.get('page')
    paginator = Paginator(posts, 2)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = []
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'social/list_ajax.html', {"posts": posts})
    context = {
        'posts': posts,
        'tag': tag,
    }
    return render(request, 'social/list.html', context)

@login_required
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

def post_detail(request, pk):
    # show detail post and similar posts
    post = get_object_or_404(Post, id=pk)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_post = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_post = similar_post.annotate(same_tags=Count('tags')).order_by('-same_tags')[:2]
    context = {
        'post': post,
        'similar_post': similar_post,
    }
    return render(request, 'social/detail.html', context)

def post_search(request):
    # view for search posts
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.filter(Q(tags__name__icontains=query) | Q(description__icontains=query))
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'social/search.html', context)

@login_required
@require_POST
def like_post(request):
    # view for like and unlike posts
    post_id = request.POST.get('post_id')
    if post_id is not None:
        post = get_object_or_404(Post, pk=post_id)
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True

        post_likes_count = post.likes.count()
        response_data = {
            'liked': liked,
            'post_likes_count': post_likes_count
        }
    else:
        response_data = {'error': 'Invalid post_id'}
    return JsonResponse(response_data)

@login_required
@require_POST
def save_post(request):
    # view for save and unsave posts
    post_id = request.POST.get('post_id')
    if post_id is not None:
        post = get_object_or_404(Post, pk=post_id)
        user = request.user
        if user in post.saved_by.all():
            post.saved_by.remove(user)
            saved = False
        else:
            post.saved_by.add(user)
            saved = True
        return JsonResponse({'saved': saved})
    return JsonResponse({'error': 'Invalid Request'})

@login_required
def user_list(request):
    # view for show users list
    users = User.objects.filter(is_active=True)
    return render(request, "user/user_list.html", {"users": users})

@login_required
def user_detail(request, username):
    # view for show user detail
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, "user/user_detail.html", {"user": user})

@login_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            if request.user in user.followers.all():
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
                follow = False
            else:
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                follow = True
            followers_count = user.followers.count()
            following_count = user.following.count()

            return JsonResponse({
                'follow': follow,
                'followers_count': followers_count,
                'following_count': following_count
            })

        except User.DoesNotExist:
            return JsonResponse({'error': 'کاربر یافت نشد.'})

    return JsonResponse({'error': 'درخواست نامعتبر است.'})
