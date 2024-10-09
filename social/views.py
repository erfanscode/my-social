from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth import logout


def index(request):
    return HttpResponse("شما با موفقیت وارد شدید")

def log_out(request):
    logout(request)
    return HttpResponse("شما خارج شدید")
