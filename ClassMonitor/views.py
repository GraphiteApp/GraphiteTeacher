from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from . import utils
from . import models
import random


def index(request):
    if not utils.check_login(request):
        return redirect('login')

    if request.method == 'POST':
        models.Profile.objects.filter(user=request.user).update(examStarted=True)
        # redirect to exam
        return redirect('/exam')

    return render(request, './ClassMonitor/index.html', {
        'class_code': models.Profile.objects.get(user=request.user).classCode if models.Profile.objects.filter(user=request.user).exists() else "no class code",
        'user': request.user,
        'exam_started': models.Profile.objects.get(user=request.user).examStarted if models.Profile.objects.filter(user=request.user).exists() else False,
    })


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

        # generate unique class code
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        while True:
            class_code = ''
            for i in range(10):
                class_code += alphabet[random.randrange(0, 26)]
            # check if class code is unique
            if not models.Profile.objects.filter(classCode=class_code).exists():
                break

        models.Profile(
            user=User.objects.get(username=request.POST['username']),
            classCode=class_code
        ).save()

        return redirect('login')

    return render(request, './ClassMonitor/register.html')


def logout_page(request):
    logout(request)
    return redirect('login')


def exam(request):
    if request.method == 'POST':
        request_type = request.POST['type']
        if request_type == 'end_exam':
            models.Profile.objects.filter(user=request.user).update(examStarted=False)
            return redirect('/')

    return render(request, './ClassMonitor/exam.html', {
        'students': models.Student.objects.filter(teacher=request.user),
        'students_length': len(models.Student.objects.filter(teacher=request.user)),
        'class_code': models.Profile.objects.get(user=request.user).classCode if models.Profile.objects.filter(user=request.user).exists() else "no class code",
    })
