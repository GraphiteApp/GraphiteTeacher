from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from . import utils


def index(request):
    if not utils.check_login(request):
        return redirect('login')

    return render(request, './ClassMonitor/index.html')


def login_page(request):
    if request.method == 'POST':
        print(request.POST['username'])
        print(request.POST['password'])
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password'],
        )
        if user is not None:
            login(request, user)
            return redirect('index')

        return HttpResponse('Invalid username or password')

    return render(request, './ClassMonitor/login.html')


def register(request):
    if request.method == 'POST':
        User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        ).save()
        return redirect('login')

    return render(request, './ClassMonitor/register.html')


def logout_page(request):
    logout(request)
    return redirect('login')
