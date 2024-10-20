# Url for social app
from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

app_name = 'social'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_view.LoginView.as_view(), name='login'),
    path('logout/', views.log_out, name='logout'),
    path('register/', views.register, name='register'),
    path('user/edit', views.edit_user, name='edit_user'),
    path('ticket/', views.ticket, name='ticket'),
    path("password-change/", auth_view.PasswordChangeView.as_view(success_url='done'), name="password_change"),
    path("password-change/done", auth_view.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("password-reset/", auth_view.PasswordResetView.as_view(success_url="done"), name="password_reset"),
    path("password-reset/done", auth_view.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password-reset/<uidb64>/<token>/",
         auth_view.PasswordResetConfirmView.as_view(success_url="/password-reset/complete"),
         name="password_reset_confirm"
    ),
    path("password-reset/complete/", auth_view.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("posts/", views.post_list, name='post_list'),
    path("posts/<slug:tag_slug>", views.post_list, name='post_list_by_tag'),
    path("posts/detail/<pk>", views.post_detail, name='post_detail'),
    path("create_post/", views.create_post, name='create_post'),
    path("search/", views.post_search, name='post_search'),
    path("liked_post/", views.like_post, name='like_post'),
]