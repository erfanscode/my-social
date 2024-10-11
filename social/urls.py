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
]